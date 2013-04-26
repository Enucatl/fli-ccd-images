## 
## $Log: rootstyle.py,v $
## Revision 1.7  2010/07/15 16:22:47  wangdy
## change the pad right margin to allow for COLZ;use palatte from R.Reece
##
## Revision 1.6  2010/05/18 17:20:12  wangdy
## small updates
##
## Revision 1.5  2009/06/30 08:59:19  wangdy
## add mitstyle and some style functions
##
## Revision 1.4  2009/06/26 10:13:31  wangdy
## first import ildstyle; add yastyle and ildstyle directly into root logon
##
## Revision 1.3  2008/01/18 15:51:18  wangdy
## adjust top margin of the pad w/(o) title
##
## Revision 1.2  2008/01/18 11:33:19  wangdy
## add setting for title color
##
## Revision 1.1  2008/01/18 10:58:00  wangdy
## first import several root style related scripts
##
##

"""  Dayong's rootlogon file, python version """

from ROOT import *
from array import array


atlasStyle=TStyle("atlasStyle","Atlas style")
tdrStyle = TStyle("tdrStyle","Style for P-TDR")
ildStyle = TStyle("ildStyle","ILD Style")
yaStyle = TStyle("yaStyle","Yet Another Style, for talks")
MITStyle = TStyle("mitStyle","The Perfect Style for Plots ;-)");


def atlasstyle():
    """ ATLAS stylebased on a style file from BaBar"""

    global atlasStyle
    ##.. style from RooLogon.C in workdir

    ## use plain black on white colors
    icol=0
    atlasStyle.SetFrameBorderMode(icol)
    atlasStyle.SetFrameFillColor(icol)
    atlasStyle.SetCanvasBorderMode(icol)
    atlasStyle.SetPadBorderMode(icol)
    atlasStyle.SetPadColor(icol)
    atlasStyle.SetCanvasColor(icol)
    atlasStyle.SetStatColor(icol)
    ##atlasStyle.SetFillColor(icol)

    ## set the paper & margin sizes
    atlasStyle.SetPaperSize(20,26)

    ## with title:0.07 ;no title:0.05    
    atlasStyle.SetPadTopMargin(0.07) 
    atlasStyle.SetPadRightMargin(0.10)

    ## with title:0.14 ;no title:0.16        
    atlasStyle.SetPadBottomMargin(0.14)
    atlasStyle.SetPadLeftMargin(0.12)

    ## use large fonts
    ##Int_t font=72
    font=42
    tsize=0.05
    atlasStyle.SetTextFont(font)


    atlasStyle.SetTextSize(tsize)
    atlasStyle.SetLabelFont(font,"x")
    atlasStyle.SetTitleFont(font,"x")
    atlasStyle.SetLabelFont(font,"y")
    atlasStyle.SetTitleFont(font,"y")
    atlasStyle.SetLabelFont(font,"z")
    atlasStyle.SetTitleFont(font,"z")

    atlasStyle.SetLabelSize(tsize,"x")
    atlasStyle.SetTitleSize(tsize,"x")
    atlasStyle.SetLabelSize(tsize,"y")
    atlasStyle.SetTitleSize(tsize,"y")
    atlasStyle.SetLabelSize(tsize,"z")
    atlasStyle.SetTitleSize(tsize,"z")

    ## dayong add some settings for title
    atlasStyle.SetTitleFillColor(0)

    ##use bold lines and markers
    atlasStyle.SetMarkerStyle(20)
    atlasStyle.SetMarkerSize(1.2)
    atlasStyle.SetHistLineWidth(2)
    atlasStyle.SetLineStyleString(2,"[12 12]") ## postscript dashes

    ##get rid of X error bars and y error bar caps
    ##atlasStyle.SetErrorX(0.001)

    ##do not display any of the standard histogram decorations
    atlasStyle.SetOptTitle(0)
    ##atlasStyle.SetOptStat(1111)
    atlasStyle.SetOptStat(0)
    ##atlasStyle.SetOptFit(1111)
    atlasStyle.SetOptFit(0)

    atlasStyle.SetPalette(1);
    ## put tick marks on top and RHS of plots
    atlasStyle.SetPadTickX(1)
    atlasStyle.SetPadTickY(1)
    gROOT.SetStyle("atlasStyle")
    gROOT.ForceStyle()

def tdrstyle_grayscale(ncolors=999):
    tdrstyle()
    return set_palette('gray_inverted', ncolors)

def tdrstyle():
    """
    Here is CMS ptdr style
    """
    global tdrStyle
    ## tdrStyle = TStyle("tdrStyle","Style for P-TDR")

    tdrStyle.SetStripDecimals(0)
    ## For the canvas:
    tdrStyle.SetCanvasBorderMode(0)
    tdrStyle.SetCanvasColor(kWhite)
    tdrStyle.SetCanvasDefH(900) ##Height of canvas
    tdrStyle.SetCanvasDefW(1456) ##Width of canvas
    tdrStyle.SetCanvasDefX(0)   ##POsition on screen
    tdrStyle.SetCanvasDefY(0)

    ## For the Pad:
    tdrStyle.SetPadBorderMode(0)
    ## tdrStyle.SetPadBorderSize(Width_t size = 1)
    tdrStyle.SetPadColor(kWhite)
    tdrStyle.SetPadGridX(false)
    tdrStyle.SetPadGridY(false)
    tdrStyle.SetGridColor(0)
    tdrStyle.SetGridStyle(3)
    tdrStyle.SetGridWidth(1)

    ## For the frame:
    tdrStyle.SetFrameBorderMode(0)
    tdrStyle.SetFrameBorderSize(1)
    tdrStyle.SetFrameFillColor(0)
    tdrStyle.SetFrameFillStyle(0)
    tdrStyle.SetFrameLineColor(1)
    tdrStyle.SetFrameLineStyle(1)
    tdrStyle.SetFrameLineWidth(1)

    ## For the histo:
    ## tdrStyle.SetHistFillColor(1)
    ## tdrStyle.SetHistFillStyle(0)
    tdrStyle.SetHistLineColor(1)
    tdrStyle.SetHistLineStyle(0)
    tdrStyle.SetHistLineWidth(2)
    ## tdrStyle.SetLegoInnerR(Float_t rad = 0.5)
    ## tdrStyle.SetNumberContours(Int_t number = 20)
    tdrStyle.SetEndErrorSize(2)
    tdrStyle.SetMarkerStyle(20)
    tdrStyle.SetErrorX(0.)
    tdrStyle.SetMarkerStyle(20)

    ##For the fit/function:
    tdrStyle.SetOptFit(1)
    tdrStyle.SetFitFormat("5.4g")
    tdrStyle.SetFuncColor(2)
    tdrStyle.SetFuncStyle(1)
    tdrStyle.SetFuncWidth(1)

    ##For the date:
    tdrStyle.SetOptDate(0)
    ## tdrStyle.SetDateX(Float_t x = 0.01)
    ## tdrStyle.SetDateY(Float_t y = 0.01)
    
    ## For the statistics box:
    tdrStyle.SetOptFile(0)
    tdrStyle.SetOptStat(0) ## To display the mean and RMS:   SetOptStat("mr")
    tdrStyle.SetStatColor(kWhite)
    tdrStyle.SetStatFont(42)
    tdrStyle.SetStatFontSize(0.025)
    tdrStyle.SetStatTextColor(1)
    tdrStyle.SetStatFormat("6.4g")
    tdrStyle.SetStatBorderSize(1)
    tdrStyle.SetStatH(0.1)
    tdrStyle.SetStatW(0.15)
    ## tdrStyle.SetStatStyle(Style_t style = 1001)
    ## tdrStyle.SetStatX(Float_t x = 0)
    ## tdrStyle.SetStatY(Float_t y = 0)

    ## Margins:
    tdrStyle.SetPadTopMargin(0.05)
    tdrStyle.SetPadBottomMargin(0.15)
    tdrStyle.SetPadLeftMargin(0.15)
    tdrStyle.SetPadRightMargin(0.12)
    
    ## For the Global title:
    tdrStyle.SetOptTitle(0)
    tdrStyle.SetTitleFont(42)
    tdrStyle.SetTitleColor(1)
    tdrStyle.SetTitleTextColor(1)
    tdrStyle.SetTitleFillColor(10)
    tdrStyle.SetTitleFontSize(0.05)
    ## tdrStyle.SetTitleH(0) ## Set the height of the title box
    ## tdrStyle.SetTitleW(0) ## Set the width of the title box
    ## tdrStyle.SetTitleX(0) ## Set the position of the title box
    ## tdrStyle.SetTitleY(0.985) ## Set the position of the title box
    ## tdrStyle.SetTitleStyle(Style_t style = 1001)
    ## tdrStyle.SetTitleBorderSize(2)
    
    ## For the axis titles:
    tdrStyle.SetTitleColor(1, "XYZ")
    tdrStyle.SetTitleFont(42, "XYZ")
    tdrStyle.SetTitleSize(0.06, "XYZ")
    ## tdrStyle.SetTitleXSize(Float_t size = 0.02) ## Another way to set the size?
    ## tdrStyle.SetTitleYSize(Float_t size = 0.02)
    tdrStyle.SetTitleXOffset(0.9)
    tdrStyle.SetTitleYOffset(1.25)
    ## tdrStyle.SetTitleOffset(1.1, "Y") ## Another way to set the Offset
    
    ## For the axis labels:
    tdrStyle.SetLabelColor(1, "XYZ")
    tdrStyle.SetLabelFont(42, "XYZ")
    tdrStyle.SetLabelOffset(0.007, "XYZ")
    tdrStyle.SetLabelSize(0.05, "XYZ")
    
    ## For the axis:
    tdrStyle.SetAxisColor(1, "XYZ")
    tdrStyle.SetStripDecimals(kFALSE)
    tdrStyle.SetTickLength(0.03, "XYZ")
    tdrStyle.SetNdivisions(510, "XYZ")
    tdrStyle.SetPadTickX(0)  ## To get tick marks on the opposite side of the frame
    tdrStyle.SetPadTickY(0)

    ## for the palette:
    tdrStyle.SetPalette(1);
    ## tdrStyle.SetNumberContours(8);    
    
    ## Change for log plots:
    tdrStyle.SetOptLogx(0)
    tdrStyle.SetOptLogy(0)
    tdrStyle.SetOptLogz(0)
    set_palette('white_to_black', 999)
    
    ## Postscript options:
    ## tdrStyle.SetPaperSize(20.,20.)
    ## tdrStyle.SetLineScalePS(Float_t scale = 3)
    ## tdrStyle.SetLineStyleString(Int_t i, const char* text)
    ## tdrStyle.SetHeaderPS(const char* header)
    ## tdrStyle.SetTitlePS(const char* pstitle)
    
    ## tdrStyle.SetBarOffset(Float_t baroff = 0.5)
    ## tdrStyle.SetBarWidth(Float_t barwidth = 0.5)
    ## tdrStyle.SetPaintTextFormat(const char* format = "g")
    ## tdrStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
    ## tdrStyle.SetTimeOffset(Double_t toffset)
    ## tdrStyle.SetHistMinimumZero(kTRUE)
    gROOT.SetStyle("tdrStyle")
    gROOT.ForceStyle()

def ildstyle():
    """
    Here is ILD style
    """
    global ildStyle


    #set the background color to white
    ildStyle.SetFillColor(10)
    ildStyle.SetFrameFillColor(10)
    ildStyle.SetCanvasColor(10)
    ildStyle.SetPadColor(10)
    ildStyle.SetTitleFillColor(0)
    ildStyle.SetStatColor(10)

    #dont put a colored frame around the plots
    ildStyle.SetFrameBorderMode(0)
    ildStyle.SetCanvasBorderMode(0)
    ildStyle.SetPadBorderMode(0)
    ildStyle.SetLegendBorderSize(0)

    #use the primary color palette
    ildStyle.SetPalette(1)

    #set the default line color for a histogram to be black
    ildStyle.SetHistLineColor(kBlack)

    #set the default line color for a fit function to be red
    ildStyle.SetFuncColor(kRed)

    #make the axis labels black
    ildStyle.SetLabelColor(kBlack,"xyz")

    #set the default title color to be black
    ildStyle.SetTitleColor(kBlack)

    #set the margins
    ildStyle.SetPadBottomMargin(0.18)
    ildStyle.SetPadTopMargin(0.08)
    ildStyle.SetPadRightMargin(0.08)
    ildStyle.SetPadLeftMargin(0.17)

    #set axis label and title text sizes
    ildStyle.SetLabelFont(42,"xyz")
    ildStyle.SetLabelSize(0.06,"xyz")
    ildStyle.SetLabelOffset(0.015,"xyz")
    ildStyle.SetTitleFont(42,"xyz")
    ildStyle.SetTitleSize(0.07,"xyz")
    ildStyle.SetTitleOffset(1.1,"yz")
    ildStyle.SetTitleOffset(1.0,"x")
    ildStyle.SetStatFont(42)
    ildStyle.SetStatFontSize(0.07)
    ildStyle.SetTitleBorderSize(0)
    ildStyle.SetStatBorderSize(0)
    ildStyle.SetTextFont(42)

    #set line widths
    ildStyle.SetFrameLineWidth(2)
    ildStyle.SetFuncWidth(2)
    ildStyle.SetHistLineWidth(2)

    #set the number of divisions to show
    ildStyle.SetNdivisions(506, "xy")

    #turn off xy grids
    ildStyle.SetPadGridX(0)
    ildStyle.SetPadGridY(0)

    #set the tick mark style
    ildStyle.SetPadTickX(1)
    ildStyle.SetPadTickY(1)

    #turn off stats
    ildStyle.SetOptStat(0)
    ildStyle.SetOptFit(0)

    #marker settings
    ildStyle.SetMarkerStyle(20)
    ildStyle.SetMarkerSize(0.7)
    ildStyle.SetLineWidth(2) 

    gROOT.SetStyle("ildStyle")
    gROOT.ForceStyle()

def yastyle():
    """
    Here is Yet Another style
    """
    global yaStyle

    yaStyle.SetFillColor(0)
    yaStyle.SetOptDate()
    yaStyle.SetOptStat(111110)
    yaStyle.SetOptFit(1111)
    yaStyle.SetPadTickX(1)
    yaStyle.SetPadTickY(1)
    yaStyle.SetMarkerSize(0.5)
    yaStyle.SetMarkerStyle(8)
    yaStyle.SetGridStyle(3)
    yaStyle.SetPaperSize(kA4)
    yaStyle.SetStatW(0.35) # width of statistics box; default is 0.19
    yaStyle.SetStatH(0.20) # height of statistics box; default is 0.1
    yaStyle.SetStatFormat("6.4g")  # leave default format for now
    yaStyle.SetTitleSize(0.055, "")   # size for pad title; default is 0.02
    # Really big; useful for talks.
    yaStyle.SetTitleSize(0.1, "")   # size for pad title; default is 0.02
    yaStyle.SetLabelSize(0.05, "XYZ") # size for axis labels; default is 0.04
    yaStyle.SetStatFontSize(0.06)     # size for stat. box
    yaStyle.SetTitleFont(32, "XYZ") # times-bold-italic font (p. 153) for axes
    yaStyle.SetTitleFont(32, "")    # same for pad title
    yaStyle.SetLabelFont(32, "XYZ") # same for axis labels
    yaStyle.SetStatFont(32)         # same for stat. box
    yaStyle.SetLabelOffset(0.006, "Y") # default is 0.005
    
    gROOT.SetStyle("yaStyle")
    gROOT.ForceStyle()

def mitstyle():
    global MITStyle
    # Canvas
    MITStyle.SetCanvasColor     (0)
    MITStyle.SetCanvasBorderSize(10)
    MITStyle.SetCanvasBorderMode(0)
    MITStyle.SetCanvasDefH      (700)
    MITStyle.SetCanvasDefW      (700)
    MITStyle.SetCanvasDefX      (100)
    MITStyle.SetCanvasDefY      (100)

    # Pads
    MITStyle.SetPadColor       (0)
    MITStyle.SetPadBorderSize  (10)
    MITStyle.SetPadBorderMode  (0)
    MITStyle.SetPadBottomMargin(0.13)
    MITStyle.SetPadTopMargin   (0.08)
    MITStyle.SetPadLeftMargin  (0.15)
    MITStyle.SetPadRightMargin (0.05)
    MITStyle.SetPadGridX       (0)
    MITStyle.SetPadGridY       (0)
    MITStyle.SetPadTickX       (0)
    MITStyle.SetPadTickY       (0)

    # Frames
    MITStyle.SetFrameFillStyle ( 0)
    MITStyle.SetFrameFillColor ( 0)
    MITStyle.SetFrameLineColor ( 1)
    MITStyle.SetFrameLineStyle ( 0)
    MITStyle.SetFrameLineWidth ( 1)
    MITStyle.SetFrameBorderSize(10)
    MITStyle.SetFrameBorderMode( 0)

    # Histograms
    MITStyle.SetHistFillColor(2)
    MITStyle.SetHistFillStyle(0)
    MITStyle.SetHistLineColor(1)
    MITStyle.SetHistLineStyle(0)
    MITStyle.SetHistLineWidth(2)
    MITStyle.SetNdivisions(505)

    # Functions
    MITStyle.SetFuncColor(1)
    MITStyle.SetFuncStyle(0)
    MITStyle.SetFuncWidth(2)

    # Various
    MITStyle.SetMarkerStyle(20)
    MITStyle.SetMarkerColor(kBlack)
    MITStyle.SetMarkerSize (1.2)

    MITStyle.SetTitleSize  (0.055,"X")
    MITStyle.SetTitleOffset(0.900,"X")
    MITStyle.SetLabelOffset(0.005,"X")
    MITStyle.SetLabelSize  (0.050,"X")
    MITStyle.SetLabelFont  (42   ,"X")

    MITStyle.SetStripDecimals(kFALSE)

    MITStyle.SetTitleSize  (0.055,"Y")
    MITStyle.SetTitleOffset(1.300,"Y")
    MITStyle.SetLabelOffset(0.010,"Y")
    MITStyle.SetLabelSize  (0.050,"Y")
    MITStyle.SetLabelFont  (42   ,"Y")

    MITStyle.SetTextSize   (0.055)
    MITStyle.SetTextFont   (42)

    MITStyle.SetStatFont   (42)
    MITStyle.SetTitleFont  (42)
    MITStyle.SetTitleFont  (42,"X")
    MITStyle.SetTitleFont  (42,"Y")

    MITStyle.SetPalette    (1)

    MITStyle.SetOptStat    (0)
    #MITStyle.SetOptStat    (111111)
    gROOT.SetStyle("mitStyle")
    gROOT.ForceStyle()

def set_palette(name='default', ncontours=200):
    """Set a color palette from a given RGB list
    stops, red, green and blue should all be lists of the same length
    see set_decent_colors for an example"""

    if name == 'gray' or name == 'grayscale':
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [1.00, 0.84, 0.61, 0.34, 0.00]
        green = [1.00, 0.84, 0.61, 0.34, 0.00]
        blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
    if name == 'gray_inverted':
        black = 0.02
        white = 0.98
        stops = [0.00, black, white, 1.00]
        red   = [0.00, 0.0, 1.0, 1.00]
        green = [0.00, 0.0, 1.0, 1.00]
        blue  = [0.00, 0.0, 1.0, 1.00]
    elif name == 'white_to_black':
        stops = [0.00, 0.10, 0.25, 0.45, 0.60, 0.75, 1.00]
        red   = [1.00, 0.00, 0.00, 0.00, 0.97, 0.97, 0.10]
        green = [1.00, 0.97, 0.30, 0.40, 0.97, 0.00, 0.00]
        blue  = [1.00, 0.97, 0.97, 0.00, 0.00, 0.00, 0.00]
    else:
        # default palette, looks cool
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [0.00, 0.00, 0.87, 1.00, 0.51]
        green = [0.00, 0.81, 1.00, 0.20, 0.00]
        blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

    colors = [0] * ncontours
    s = array('d', stops)
    r = array('d', red)
    g = array('d', green)
    b = array('d', blue)

    npoints = len(s)
    color = TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    gStyle.SetNumberContours(ncontours)
    for i in xrange(ncontours):
        colors[i] = color + i
    return array('i', colors)

tdrstyle()
set_palette()

if __name__ == '__main__':
    ## default style
    gROOT.SetStyle("Plain")
    gStyle.SetOptStat(1111111)
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)

## activate these two style following way: better way
#     atlasstyle()
#     tdrstyle()
#     ildstyle()
#     yastyle()
#     mitstyle()
## activate these two style following way
## gROOT.SetStyle("atlasStyle")
## gROOT.SetStyle("tdrStyle")
## gROOT.SetStyle("ildStyle")
## gROOT.SetStyle("yaStyle")
## gROOT.SetStyle("mitStyle")    
## gROOT.ForceStyle()



