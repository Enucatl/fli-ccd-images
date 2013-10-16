"""Test the projection_stack.py script.

"""

from __future__ import division, print_function

import h5py
import os
import numpy as np

from readimages.projections.commandline_parser import commandline_parser
from readimages.projections.get_projection_stack import get_projection_stack

test_file = "data.hdf5"
golden_file = "data_golden_projection.hdf5"

class TestProjectionStack(object):
    """Tests:
        - test algorithm
        - golden log test
        - overwrite flag.
        
        """

    def test_algorithm(self):
        """Test that the algorithm works:
        should take the Nth pixel from all the images and stack them
        together.

        """
        args = commandline_parser.parse_args(
                ["--overwrite", test_file])
        stack = get_projection_stack(
                args.file, args)
        h5_file = h5py.File(test_file)
        images = h5_file["raw_images"].itervalues()
        first_pixel = h5_file[
                "raw_images/ccdimage_00045_00000_00"].attrs["min_y"]
        projection_pixel = args.pixel - first_pixel
        manual_stack = np.dstack(
                (image[:, args.roi[0]:args.roi[1]]
                    for image in images))
        manual_projection = np.transpose(manual_stack[
                            projection_pixel, :, :])
        h5_file.close()
        """Apply 3 sigma correction."""
        for line in manual_projection:
            mean = np.mean(line)
            std_dev = np.std(line)
            if (line > mean + 3 * std_dev).any():
                line[line > mean + 3 * std_dev] = mean
        print(manual_projection.shape)
        print(stack.shape)
        print(manual_projection.dtype)
        print(stack.dtype)
        print((manual_projection == stack).all())
        difference = manual_projection - stack
        print(difference.nonzero())
        assert (manual_projection == stack).all()


    def test_golden_log(self):
        """Open a known projection stack and check that
        the algorithm produces the same result.

        """
        args = commandline_parser.parse_args(
                [test_file, "--overwrite"])
        stack = get_projection_stack(
                args.file, args)
        golden = h5py.File(golden_file, "r")
        golden_stack = golden["postprocessing/stack_pixel_510"][
                :, args.roi[0]:args.roi[1]]
        assert (stack == golden_stack).all()

    def test_overwrite(self):
        """Test the overwrite flag.

        """
        args = commandline_parser.parse_args(
                ["--overwrite", test_file])
        get_projection_stack(args.file, args)
        date_modified = os.path.getmtime(test_file)
        args = commandline_parser.parse_args(
                [test_file])
        get_projection_stack(args.file, args)
        date_modified2 = os.path.getmtime(test_file)
        """Check that it was not overwritten."""
        assert date_modified == date_modified2
        """Check that it was overwritten."""
        args = commandline_parser.parse_args(
                ["--overwrite", test_file])
        get_projection_stack(args.file, args)
        date_modified3 = os.path.getmtime(test_file)
        assert date_modified3 >= date_modified
