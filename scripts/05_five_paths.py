"""Chapter 9: five acquisition paths, and compensator length against the stopband edge.

Path 1 with a single CIC stage (N=4, M=400) is designed here with the 15-segment
piecewise FIRLS method. The report's tables come from the original notebooks and
may differ slightly from this clean re-implementation."""
import _common  # noqa: F401
from ddc import compensator as comp

fs_in = 200e6
print("Path  dwell(us)  f_pass(kHz)  f_out(kHz)  M")
for i, dt in enumerate([4e-6, 5e-6, 10e-6, 50e-6, 100e-6], 1):
    f_out = 2 / dt
    print(f"{i:4d}  {dt*1e6:9.0f}  {1/(2*dt)/1e3:11.0f}  {f_out/1e3:10.0f}  {fs_in*dt/2:6.0f}")
f_pass, f_out = 125e3, 500e3
print("\nPath 1, N = 4, single stage M = 400: shortest compensator meeting 0.05 dB / 60 dB")
for frac in (0.6, 0.7, 0.8, 0.9, 0.95):
    res = comp.shortest(f_pass, frac * f_out / 2, f_out, [400], 4, fs_in)
    if res:
        L, r, a, _ = res
        print(f"  stopband edge {frac:.2f} x Nyquist: {L:3d} taps, ripple {r:.4f} dB, attenuation {a:.1f} dB")
    else:
        print(f"  stopband edge {frac:.2f} x Nyquist: no design up to 301 taps")
