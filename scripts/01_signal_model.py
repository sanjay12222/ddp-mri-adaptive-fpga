"""Chapter 5: Larmor frequency and gradient-echo contrast at 1.5 T."""
import _common  # noqa: F401
from ddc import signal_model as sm

print(f"Larmor frequency at 1.5 T: {sm.larmor(1.5)/1e6:.2f} MHz")
for name, t1, t2s in [("debug", 0.600, 0.040), ("realistic", 0.800, 0.050)]:
    ea = sm.ernst_angle_deg(0.050, t1)
    m30 = sm.gre(1, 30, 0.050, 0.015, t1, t2s)
    mE = sm.gre(1, ea, 0.050, 0.015, t1, t2s)
    print(f"{name}: Ernst angle {ea:.1f} deg; 30 deg gives {100*m30/mE:.0f} % of the maximum; M_GRE(30 deg) = {m30:.4f}")
