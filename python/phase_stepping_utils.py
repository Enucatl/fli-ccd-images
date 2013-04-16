from __future__ import division, print_function

import math
import numpy as np

from base_rootfile_analyser import commandline_parser
commandline_parser.add_argument('--periods', metavar='PERIODS',
        type=int, default=1,
        help='number of phase stepping periods (default 1)')

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
