"""Section 3.4.5: rejection of the image bands that fold onto the passband."""
import _common  # noqa: F401
from ddc import cic

fs = 200e6
for N in (3, 4, 5):
    print(f"Path 1 chain [10,10,4], N = {N}: {cic.image_rejection_db([10, 10, 4], N, fs, 125e3):.1f} dB at 375 kHz")
print(f"Stage 1 alone (/10): {-20*__import__('numpy').log10(cic.response(20e6-125e3, 10, 3, fs)):.1f} dB")
print(f"Stage 2 alone (/10 at 20 MHz): {-20*__import__('numpy').log10(cic.response(2e6-125e3, 10, 3, 20e6)):.1f} dB")
print(f"Single-path design (N=4, M=250, 250 MSPS): {cic.image_rejection_db([250], 4, 250e6, 50e3):.1f} dB")
