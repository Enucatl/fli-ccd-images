#!/bin/bash

rm test.root; ./bin/make_root test; python python/convert_images.py test.root
rm test.root; ./bin/make_root test; python python/intensity_scan.py test.root --roi 520 570 520 525
rm test.root; ./bin/make_root test; python python/make_projection_stack.py test.root 520
