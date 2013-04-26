from __future__ import division, print_function

import ROOT

class ImageCombination(object):
    """Descriptor. Combine a list of images to form an interesting image for
    post-processing.
    
    These objects should run with the following steps:

        - construction (no arguments)
        - calculate the image with __set__(self, obj, list_of_images)
        - get the image with __get__

    """

    def __init__(self):
        super(ImageCombination, self).__init__()
        self.image = None

    def __set__(self, obj, list_of_images):
        raise NotImplementedError

    def __get__(self, obj, klass):
        return self.image
