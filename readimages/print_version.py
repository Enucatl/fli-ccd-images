"""Print version info from setuptools."""

from __future__ import division, print_function
import pkg_resources

def print_version(programme_name):
    """Print version info for the programme"""
    
    version = pkg_resources.require("readimages")[0].version
    print("\n", programme_name, version, end="\n\n")
