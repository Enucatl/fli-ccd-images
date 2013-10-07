"""Test the make_hdf5.py script.

"""

import h5py
import os
import numpy as np
from glob import glob

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../bin")))

import make_hdf5

class TestMakeHdf5(object):
    """Tests:
        - header analysis
        - file creation
        - file content
        - overwrite flag.
        
        """

    def test_header(self):
        """Test the header analysis of a known file.

        """
        (header_len, exposure_time,
                min_x, max_x, 
                min_y, max_y) = make_hdf5.analyse_header(
                        "data/ccdimage_00045_00000_00.raw")
        assert header_len == 340
        assert exposure_time == 5
        assert min_x == 4
        assert max_x == 1028
        assert min_y == 500
        assert max_y == 560

    def test_main(self):
        """Test that the file is written,
        and that it contains the same number of images as
        the input folder.

        """
        args = make_hdf5.commandline_parser.parse_args(
                ["--overwrite", "--keep", "data"])
        output_files = make_hdf5.main(args)
        for output_file in output_files:
            assert os.path.exists(output_file)
            h5_file = h5py.File(output_file, "r")
            assert "raw_images" in h5_file
            folder_name = output_file.replace(".hdf5", "")
            n_original_files = len(glob(os.path.join(folder_name, "*.raw"))) 
            n_hdf5_images = len(h5_file["raw_images"])
            assert n_original_files == n_hdf5_images
            h5_file.close()

    def test_file_content(self):
        """Test that the file contains the same data as the original raw
        file.

        """
        input_file_name = "data/ccdimage_00045_00000_00.raw"
        (header_len, _,
                min_x, max_x, 
                min_y, max_y) = make_hdf5.analyse_header(input_file_name)
        input_file = open(input_file_name, 'rb')
        input_file.read(header_len + 1)
        image = np.reshape(
                np.fromfile(input_file, dtype=np.uint16),
                (max_y - min_y, max_x - min_x),
                order='FORTRAN')
        args = make_hdf5.commandline_parser.parse_args(
                ["--keep", "data"])
        output_files = make_hdf5.main(args)
        h5_file = h5py.File(output_files[0], "r")
        hdf5_data = h5_file["raw_images/ccdimage_00045_00000_00"][...]
        assert (hdf5_data == image).all()
        h5_file.close()
    
    def test_overwrite(self):
        """Test the overwrite flag.

        """
        args = make_hdf5.commandline_parser.parse_args(
                ["--overwrite", "--keep", "data"])
        output_files = make_hdf5.main(args)
        date_created = os.path.getctime(output_files[0])
        args = make_hdf5.commandline_parser.parse_args(
                ["--keep", "data"])
        output_files = make_hdf5.main(args)
        date_created2 = os.path.getctime(output_files[0])
        """Check that it was not overwritten."""
        assert date_created == date_created2
        """Check that it was overwritten."""
        args = make_hdf5.commandline_parser.parse_args(
                ["--overwrite", "--keep", "data"])
        output_files = make_hdf5.main(args)
        date_created3 = os.path.getctime(output_files[0])
        assert date_created3 >= date_created
