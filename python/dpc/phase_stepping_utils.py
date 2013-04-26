from __future__ import division, print_function

import math
import numpy as np
import ROOT

from utils.th2_to_numpy import th2_to_numpy

def average_curve(curves, phase_stepping_points):
    """Split the curves input into phase stepping curves with the given
    number of points and return the average."""
    list_of_curves = np.split(curves,
            curves.shape[1] // phase_stepping_points,
            axis=0)
    stacked = np.dstack(list_of_curves)
    mean = np.mean(stacked, axis=-1)
    return mean

def get_signals(phase_stepping_curve, flat=None, n_periods=1):
    """Get the three images from the phase stepping curves.
    flat contains a0, phi and a1 from the flat image
    These are the columns of the phase_stepping_curve
    input, while the row is the pixel number."""
    n_phase_steps = phase_stepping_curve.shape[0]
    transformed = np.fft.rfft(phase_stepping_curve,
            n_phase_steps - 1, axis=0)
    a0 = np.abs(transformed[0, :]) 
    a1 = np.abs(transformed[n_periods, :]) 
    phi1 = np.angle(transformed[n_periods, :])
    if flat:
        a0_flat, phi_flat, a1_flat = flat
        a0 /= a0_flat
        a1 /= a1_flat / a0
        phi1 -= phi_flat
        phi1 = np.mod(phi1 + math.pi, 2 * math.pi) - math.pi
    return a0, phi1, a1

def goodness_of_fit(args, draw=False):
    """Return a histogram with the normalized chi2 calculated for the phase
    stepping fitted curve in each pixel."""
    roi = args.roi
    chi2_histogram = ROOT.TH1D("chi2",
            "normalized chi2; pixel; #chi^{2}/ndf",
            roi[1] - roi[0], roi[0], roi[1])
    root_file, histogram = get_projection_stack(args)
    image = th2_to_numpy(histogram)[:, roi[0]:roi[1]]
    n_periods = args.periods
    absorption, phase, dark = get_signals(image, n_periods=n_periods)
    normalization = 1 / (image.shape[0] - 1)
    n_phase_steps = image.shape[0] // n_periods
    function = ROOT.TF1("cosine", "[0] + [1] * cos(2 * pi * x / [2] - [3])",
            0, image.shape[0])
    degrees_of_freedom = image.shape[0] - 4
    for i in range(roi[1] - roi[0]):
        curve = histogram.ProjectionY("_py",
                roi[0] + i + 1, roi[0] + i + 1)
        function.SetParameters(
                absorption[i] * normalization,
                2 * dark[i] * normalization,
                n_phase_steps,
                phase[i])
        if draw:
            canvas = ROOT.TCanvas("dcanvas", "canvas")
            curve.Draw()
            function.SetLineColor(2)
            function.Draw("same")
            raw_input()
        chi_square = 0
        for j in range(curve.GetNbinsX()):
            observed = curve.GetBinContent(j + 1)
            expected = function.Eval(j + 0.5)
            chi_square += (observed - expected)**2 / observed
        normalized_chi_square = chi_square / degrees_of_freedom
        chi2_histogram.SetBinContent(i + 1, normalized_chi_square)
        #print("chi2 {0:.3f} with {1:.0f} degrees of freedom".format(chi_square, degrees_of_freedom))
        #print("chi2/ndf {0:.3f}".format(chi_square / degrees_of_freedom))
    return chi2_histogram


if __name__ == '__main__':
    """Test the phase stepping fit."""

    from handle_projection_stack import get_projection_stack
    args = commandline_parser.parse_args()
    histogram = goodness_of_fit(args, draw=False)
    canvas = ROOT.TCanvas("canvas", "canvas")
    histogram.Draw()
    raw_input()
