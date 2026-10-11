"""Cascaded integrator-comb (CIC) decimator: response, droop, word growth, image rejection."""
import math
import numpy as np


def response(f, M, N, fs):
    """Normalised magnitude |H(f)| of an N-th order CIC decimating by M at input rate fs."""
    x = np.pi * np.asarray(f, dtype=float) / fs
    with np.errstate(divide="ignore", invalid="ignore"):
        h = np.where(np.abs(np.sin(x)) < 1e-15, 1.0, np.sin(M * x) / (M * np.sin(x)))
    return np.abs(h) ** N


def chain_response(f, factors, N, fs):
    """Magnitude of a multistage CIC chain; each stage runs at its own input rate."""
    out = np.ones_like(np.asarray(f, dtype=float))
    for M in factors:
        out = out * response(f, M, N, fs)
        fs = fs / M
    return out


def droop_db(f, factors, N, fs):
    """Passband droop of the chain at frequency f, in dB (negative)."""
    return 20 * np.log10(chain_response(f, factors, N, fs))


def stage_growth(M, N):
    """Worst-case register growth of one stage: ceil(N log2 M) bits."""
    return math.ceil(N * math.log2(M))


def register_widths(factors, N, b_in=16):
    """Register width after each stage of a chain, with worst-case growth."""
    widths, b = [], b_in
    for M in factors:
        b += stage_growth(M, N)
        widths.append(b)
    return widths


def image_rejection_db(factors, N, fs, f_band):
    """Rejection of the image band nearest the passband, at f = f_out - f_band (dB, positive)."""
    f_out = fs / np.prod(factors)
    return -20 * np.log10(chain_response(f_out - f_band, factors, N, fs))
