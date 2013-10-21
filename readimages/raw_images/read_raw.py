"""read a single CCDFLI RAW image."""

from itertools import islice
import numpy as np

#number of lines in a CCD FLI header
HEADER_LINES = 16

def analyse_header(input_file_name):
    """Analyse a CCD FLI header in a RAW file saved as file_name.

    Return the bytes in the header, exposure, min_x, max_x, min_y, max_y.

    """
    input_file = open(input_file_name, 'rb')
    header = list(islice(input_file, HEADER_LINES))
    header_len = len("".join(header))
    exposure_time = float(header[4].split()[-1])
    min_y, min_x, max_y, max_x = [
            int(x) for x in header[-2].split()[2:]]
    input_file.close()
    return header_len, exposure_time, min_x, max_x, min_y, max_y

def read_data(input_file_name):
    """Read the data into a numpy array,
    shaped according to the header."""
    (header_len, _,
                    min_x, max_x, 
                    min_y, max_y) = analyse_header(input_file_name)
    input_file = open(input_file_name, 'rb')
    input_file.read(header_len + 1)
    image = np.reshape(
            np.fromfile(input_file, dtype=np.uint16),
            (max_y - min_y, max_x - min_x),
            order='FORTRAN')
    input_file.close()
    return image
