"""Complex leaky NLMS noise canceller, in floating point and in integer (fixed-point) form."""
import numpy as np


def nlms(d, x, order=32, mu=0.1, eps=0.05, lam=0.0):
    """Returns the error signal e = d - w^H x (the cleaned output)."""
    w = np.zeros(order, dtype=complex)
    buf = np.zeros(order, dtype=complex)
    e = np.zeros_like(d, dtype=complex)
    for n in range(len(d)):
        buf = np.roll(buf, 1)
        buf[0] = x[n]
        y = np.vdot(w, buf)
        e[n] = d[n] - y
        w = (1 - lam) * w + mu * np.conj(e[n]) * buf / (eps + np.vdot(buf, buf).real)
    return e


def to_fixed(value, frac_bits, total_bits=16, mode="round"):
    """Integer code of a value in Q(total-frac-1).frac format, with saturation.

    mode: "round" (nearest) or "trunc" (toward zero)."""
    x = value * (1 << frac_bits)
    q = int(round(x)) if mode == "round" else int(x)
    lo, hi = -(1 << (total_bits - 1)), (1 << (total_bits - 1)) - 1
    return max(lo, min(hi, q))
