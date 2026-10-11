"""Resource model of the sixteen-channel hybrid TDM receiver on a Xilinx Zynq-7020."""
import math

XC7Z020 = {"LUT": 53200, "FF": 106400, "DSP": 220, "BRAM36": 140}
BRAM36_BITS = 36 * 1024
ACTIVITY = {"LUT": 0.15, "FF": 0.10, "DSP": 0.25, "BRAM": 0.05}


def dsp_parallel(L):
    """Multipliers of a fully parallel symmetric Type-I FIR: ceil(L/2)."""
    return math.ceil(L / 2)


def tdl_bram36(L, channels=16, width=24):
    """BRAM36 blocks for the tapped delay line of all channels (channels x L words)."""
    return math.ceil(channels * L * width / BRAM36_BITS)


def service_rate(f_out, channels=16):
    """Outputs per second the shared engine must produce."""
    return channels * f_out


def cycles_per_output(f_out, f_clk=200e6, channels=16):
    return f_clk / service_rate(f_out, channels)


def dsp_folded(L, f_out, f_clk=200e6, channels=16, iq=False):
    """Minimum physical multipliers if the shared engine is folded over time."""
    rate = service_rate(f_out, channels) * dsp_parallel(L) * (2 if iq else 1)
    return math.ceil(rate / f_clk)


def area_score(util_pct):
    """Weighted area score from utilisation percentages (LUT, FF, DSP, BRAM)."""
    return 0.30 * util_pct["LUT"] + 0.15 * util_pct["FF"] + 0.40 * util_pct["DSP"] + 0.15 * util_pct["BRAM"]


def power_proxy(items):
    """Relative dynamic-power proxy: sum of count x width x activity x clock (not watts).

    items: iterable of (resource, count, width_bits, clock_hz)."""
    return sum(n * w * ACTIVITY[r] * f for r, n, w, f in items)


def pareto(points, keys):
    """Non-dominated subset of a list of dicts, all objectives minimised."""
    out = []
    for p in points:
        dominated = any(all(q[k] <= p[k] for k in keys) and any(q[k] < p[k] for k in keys)
                        for q in points if q is not p)
        if not dominated:
            out.append(p)
    return out
