"""Chapter 6: reference-channel NLMS canceller (illustrative synthetic demo)."""
import numpy as np
import _common  # noqa: F401
from ddc import nlms

rng = np.random.default_rng(0)
n = 4000
t = np.arange(n)
s = 0.1 * np.sinc((t - n / 2) / 60) * np.exp(1j * np.pi / 4)
v = (rng.standard_normal(n) + 1j * rng.standard_normal(n)) * np.sqrt(np.mean(np.abs(s) ** 2) / 10 / 2)
ref = 0.85 * v + 0.15 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)) * np.std(v) / np.sqrt(2)
e = nlms.nlms(s + v, ref, order=32, mu=0.1, eps=0.05, lam=0.0)
before = np.mean(np.abs(v) ** 2)
after = np.mean(np.abs(e[n // 4:] - s[n // 4:]) ** 2)
print(f"Noise power before {before:.2e}, after {after:.2e} (illustrative; differs from the report's line-by-line setup)")
print(f"mu = 0.1 in Q1.15: 0x{nlms.to_fixed(0.1, 15, mode='trunc'):04X} truncated, 0x{nlms.to_fixed(0.1, 15):04X} rounded")
print(f"eps = 0.05 in Q4.12: 0x{nlms.to_fixed(0.05, 12):04X} rounded")
