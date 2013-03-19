from __future__ import division, print_function
from base_rootfile_analyser import BaseRootfileAnalyser
import ROOT

class ImageCombination(BaseRootfileAnalyser):
    """Combine some consecutive images to form an interesting image for post-processing
    
    These objects should run with the following steps:

        - construction
        - initialization with open()
        - running with calculate()
        - closing with close()

    The open() and close() methods are automatically called if you use the
    with statement:

        with ImageCombination(args) as ic:
            pass

    calls open() from __enter__() and close() from __exit()

    """

    def __init__(self, root_file_name, first_index, last_index):
        """Open the input file and make an output folder if it doesn't
        exist.

        :root_file_name: name of the input root file
        :first_index: index of the first image in the tree to be
            analysed (starts a 0!)
        :last_index: index of the last image to be analysed (included!)

        """
        super(ImageCombination, self).__init__(root_file_name)
        self.first_index = first_index
        self.last_index = last_index
        self.n_images = last_index - first_index + 1

    def output_name(self):
        raise NotImplementedError

    def if_not_exists(self):
        super(ImageCombination, self).if_not_exists()
        self.tree.GetEntry(0)
        width = self.tree.rows
        height = self.tree.columns
        min_x = self.tree.min_x
        max_x = self.tree.max_x
        min_y = self.tree.min_y
        max_y = self.tree.max_y
        self.n_bins = (width + 2) * (height + 2)
        self.output_object = ROOT.TH2I(self.output_name(), self.output_name(),
                width, min_x, max_x,
                height, min_y, max_y)
        print()
        print("calculating", self.output_name())
        self.calculate_output()

    def calculate_output(self):
        raise NotImplementedError
