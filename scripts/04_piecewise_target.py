"""Chapter 9: error of a piecewise-linear target against the exact inverse droop (Path 1)."""
import _common  # noqa: F401
from ddc import cic, compensator as comp

fs_in, f_pass, chain = 200e6, 125e3, [400]
for N in (4, 3):
    print(f"N = {N}: droop at band edge {cic.droop_db(f_pass, chain, N, fs_in):.2f} dB")
    for K in (1, 2, 3, 5, 8, 10, 15, 20):
        print(f"  {K:2d} segments: max error {comp.target_error_db(f_pass, chain, N, fs_in, K):.4f} dB")
