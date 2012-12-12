#!/usr/bin/env python
from __future__ import division, print_function
import numpy
from skimage import io, transform

def header(file_name):
    lines = []
    rows = 0
    columns = 0
    with open(file_name, "rb") as input_file:
        for line in input_file:
            lines.append(line)
            if "rows" in line:
                rows = int(line.split()[2])
            elif "columns" in line:
                columns = int(line.split()[2])
            if "EOH" in line:
                break
    return rows, columns, len("".join(lines)) + 1

def fromfile(file_name):
    "similar to numpy.fromfile, cuts the header and sets the image"
    rows, columns, header_len = header(file_name)
    with open(file_name) as input_file:
        input_file.read(header_len)
        array = numpy.fromfile(input_file, dtype=numpy.uint16) 
    array = numpy.resize(array, (rows, columns))
    return transform.rotate(io.Image(array), 90)

if __name__ == '__main__':
    import sys
    image = fromfile(sys.argv[1])
    from skimage import feature
    from matplotlib import pyplot as plt
    y, x = numpy.transpose(feature.harris(image, min_distance=100,
        threshold=0.3, gaussian_deviation=5))
    print(x, y)
    plt.plot(x, y, "b.")
    plt.imshow(image)
    plt.show()
