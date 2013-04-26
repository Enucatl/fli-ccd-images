#!/usr/bin/env python
from __future__ import division, print_function

def progress_bar(fraction):
    return '\r[{0:50s}] {1:.1%}'.format('#'*int((fraction * 50)), fraction)
