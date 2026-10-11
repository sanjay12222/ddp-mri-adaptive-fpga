"""Chapter 8 and Appendix B: CIC (N=4, M=250) + 31-tap FIRLS compensator at 250 MSPS."""
import numpy as np
import _common  # noqa: F401
from ddc import cic, compensator as comp

half = [-0.00041774, -0.00147870, -0.00258726, -0.00196545, 0.00211328, 0.00872297, 0.01261689,
        0.00648737, -0.01242889, -0.03564306, -0.04337501, -0.01465257, 0.05703228, 0.15361043,
        0.23740143, 0.27060299]
h = np.array(half + half[-2::-1])
fs_in, fs_out, f_pass, f_stop, chain, N = 250e6, 1e6, 50e3, 200e3, [250], 4
print(f"CIC droop at 50 kHz: {cic.droop_db(f_pass, chain, N, fs_in):.3f} dB")
r, a = comp.cascade_metrics(h, f_pass, f_stop, fs_out, chain, N, fs_in)
print(f"31-tap cascade: ripple {r:.4f} dB, attenuation {a:.1f} dB from {f_stop/1e3:.0f} kHz")
print(f"Multipliers: 3023 at 250 MHz -> {int(np.ceil(43/2))} at 1 MHz for the 43-tap design "
      f"(multiply rate ratio {3023*250e6/(22*1e6):,.0f}x)")
