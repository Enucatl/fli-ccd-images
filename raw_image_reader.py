#!/usr/bin/env python
from __future__ import division, print_function
from rootstyle import tdrstyle_grayscale
from skimage_reader import fromfile
from matplotlib import pyplot, cm
import ROOT

class RawImageReader(object):
    """read raw image as saved by the Proline CCD camera in the PSI east
    lab.
    Store it as a ROOT 2d histogram.
    Uses c++ function defined in read_raw_image.C"""
    def __init__(self, file_name):
        super(RawImageReader, self).__init__()
        self.file_name = file_name
        input_file = open(file_name, "rb")
        text = input_file.read()
        input_file.close()
        text = text.split("\n")
        header_bytes = self.process_header(text)
        self.init_image(header_bytes)
        
    def process_header(self, text):
        self.rows = 0
        self.columns = 0
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        total_header_lines = 0
        for i, line in enumerate(text):
            total_header_lines += 1
            if "rows" in line:
                self.rows = int(line.split()[2])
            elif "columns" in line:
                self.columns = int(line.split()[2])
            elif "ROI" in line:
                #print(line, self.rows, self.columns)
                self.min_y, self.min_x, self.max_y, self.max_x = (int(x)
                        for x in line.split()[2:])
            elif "EOH" in line:
                break
        header_bytes = len("".join(text[:total_header_lines])) + 1
        return header_bytes

    def init_image(self, header_bytes):
        ROOT.gROOT.ProcessLine(".L read_raw_image.cpp+")
        ROOT.gROOT.ProcessLine(".L exec_draw_slice.cpp+")
        tdrstyle_grayscale()
        self.image = ROOT.TH2I(self.file_name, self.file_name,
                self.rows,
                self.min_x,
                self.max_x,
                self.columns,
                self.min_y,
                self.max_y)
        ROOT.read_raw_image(self.file_name, header_bytes, self.image)

    def draw(self, options="col"):
        canvas_name = self.file_name + "_canvas"
        ROOT.gROOT.ProcessLine("TCanvas canvas2;")
        self.canvas = ROOT.TCanvas(
                canvas_name,
                canvas_name)
        self.image.Draw(options)
        canvas_name2 = self.file_name + "_canvas2"
        self.canvas.AddExec("exec_draw_slice", "exec_draw_slice(canvas2)")

    def save(self, name):
        self.canvas.SaveAs(name)

    def update(self, new_name):
        self.file_name = new_name
        input_file = open(new_name, "rb")
        text = input_file.read()
        input_file.close()
        text = text.split("\n")
        header_bytes = self.process_header(text)
        ROOT.read_raw_image(new_name, header_bytes, self.image)
        self.canvas.Update()

class RawImageReaderScikit(object):
    """read raw image as saved by the Proline CCD camera in the PSI east
    lab.
    Store it as a skimage.io.Image
    """
    def __init__(self, file_name):
        super(RawImageReaderScikit, self).__init__()
        self.file_name = file_name
        self.image = fromfile(file_name)
        
    def draw(self, **kwargs):
        pyplot.imshow(self.image, **kwargs)
        pyplot.show()

    def save(self, fname, **kwargs):
        pyplot.imsave(fname, self.image, **kwargs)

if __name__ == '__main__':
    import sys
    file_name = sys.argv[1]
    image = RawImageReader(file_name)
    image.draw()
    image.save(sys.argv[1].replace(".raw", ".png"))
    #raw_input()

    #image2 = RawImageReaderScikit(file_name)
    #image2.draw(cmap=cm.gray)
    #image2.save("immagine.png")
    #raw_input()

