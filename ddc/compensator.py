"""Piecewise least-squares (FIRLS) compensator design and cascade verification."""
import numpy as np
from scipy import signal

from . import cic


def piecewise_target(f_pass, factors, N, fs_in, segments=15):
    """Band edges and desired gains of a piecewise-linear inverse-droop target."""
    edges = np.linspace(0, f_pass, segments + 1)
    gains = 1.0 / cic.chain_response(edges, factors, N, fs_in)
    return edges, gains


def target_error_db(f_pass, factors, N, fs_in, segments, n=20001):
    """Largest distance (dB) between the piecewise target and the exact inverse droop."""
    f = np.linspace(0, f_pass, n)
    exact = -20 * np.log10(cic.chain_response(f, factors, N, fs_in))
    e, g = piecewise_target(f_pass, factors, N, fs_in, segments)
    approx = 20 * np.log10(np.interp(f, e, g))
    return float(np.max(np.abs(approx - exact)))


def design(numtaps, f_pass, f_stop, fs_out, factors, N, fs_in, segments=15, stop_weight=500.0):
    """Design an odd-length compensator with scipy.signal.firls."""
    e, g = piecewise_target(f_pass, factors, N, fs_in, segments)
    bands, desired, weight = [], [], []
    for i in range(segments):
        bands += [e[i], e[i + 1]]
        desired += [g[i], g[i + 1]]
        weight.append(1.0)
    bands += [f_stop, fs_out / 2]
    desired += [0.0, 0.0]
    weight.append(stop_weight)
    return signal.firls(numtaps, bands, desired, weight=weight, fs=fs_out)


def cascade_metrics(h, f_pass, f_stop, fs_out, factors, N, fs_in, n=8192):
    """Peak-to-peak passband ripple and minimum stopband attenuation (dB) of CIC x FIR."""
    fp = np.linspace(0, f_pass, n)
    fsb = np.linspace(f_stop, fs_out / 2, n)
    _, hp = signal.freqz(h, worN=fp, fs=fs_out)
    _, hs = signal.freqz(h, worN=fsb, fs=fs_out)
    cp = 20 * np.log10(np.abs(hp) * cic.chain_response(fp, factors, N, fs_in))
    cs = 20 * np.log10(np.maximum(np.abs(hs) * cic.chain_response(fsb, factors, N, fs_in), 1e-15))
    return float(cp.max() - cp.min()), float(-cs.max())


def quantise(h, bits):
    """Round coefficients to `bits` bits with bits-1 fractional bits."""
    s = 2 ** (bits - 1)
    return np.round(np.asarray(h) * s) / s


def shortest(f_pass, f_stop, fs_out, factors, N, fs_in, ripple=0.05, atten=60.0,
             max_taps=301, bits=None, segments=15):
    """Smallest odd length (and its metrics) that meets the cascade specification."""
    for L in range(5, max_taps + 1, 2):
        h = design(L, f_pass, f_stop, fs_out, factors, N, fs_in, segments)
        if bits:
            h = quantise(h, bits)
        r, a = cascade_metrics(h, f_pass, f_stop, fs_out, factors, N, fs_in)
        if r <= ripple and a >= atten:
            return L, r, a, h
    return None
