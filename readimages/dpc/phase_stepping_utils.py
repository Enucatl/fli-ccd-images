"""Utility functions for dpc analysis.

"""

from __future__ import division, print_function

import math
import numpy as np

def get_signals(phase_stepping_curves, flat=None, n_periods=1):
    """Get the three images from the phase stepping curves.
    flat contains a0, phi and a1 from the flat image
    These are the columns of the phase_stepping_curve
    input, while the row is the pixel number."""
    n_phase_steps = phase_stepping_curves.shape[0]
    transformed = np.fft.rfft(
            phase_stepping_curves,
            n_phase_steps,
            axis=0)
    a0 = np.abs(transformed[0, :, :]) 
    a1 = np.abs(transformed[n_periods, :, :]) 
    phi1 = np.angle(transformed[n_periods, :, :])
    if flat:
        a0_flat, phi_flat, a1_flat = flat
        a0 /= a0_flat
        a1 /= a1_flat / a0
        phi1 -= phi_flat
        phi1 = np.mod(phi1 + math.pi, 2 * math.pi) - math.pi
    return a0, phi1, a1

def subtract_drift(image):
    """Force the phase to have zero mean in all lines.

    """
    correction = np.tile(np.mean(image, axis=1),
            (image.shape[1], 1)).transpose()
    corrected_image = image - correction
    return corrected_image
 
