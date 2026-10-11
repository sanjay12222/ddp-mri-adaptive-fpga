"""Chapter 7: length of a single low-pass filter at the ADC rate (Kaiser estimate)."""
import math
import _common  # noqa: F401
from scipy import signal

fs, f_pass, f_stop, atten = 250e6, 50e3, 200e3, 60.0
width = (f_stop - f_pass) / (fs / 2)
L, beta = signal.kaiserord(atten, width)
L = L + 1 if L % 2 == 0 else L
print(f"Transition width: {width:.2e} of Nyquist")
print(f"Kaiser estimate: {L} taps (odd), {math.ceil(L/2)} multipliers with symmetry, group delay {(L-1)//2} samples = {(L-1)/2/fs*1e6:.1f} us")
print("Zynq-7020 DSP48E1 slices: 220")
