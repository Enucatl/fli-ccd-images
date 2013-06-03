from __future__ import division, print_function

import h5py
import matplotlib.pyplot as plt

input_file = h5py.File('S00140.hdf5')

array = input_file['reconstruction']

plt.figure()
plt.imshow(array)
plt.ion()
plt.show()
raw_input("press ENTER to quit.")
