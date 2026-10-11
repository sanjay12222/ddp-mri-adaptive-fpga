"""MRI signal model: spoiled gradient echo (Ernst) and spin echo contrast."""
import numpy as np

GAMMA_BAR = 42.58e6  # Hz/T for protons


def larmor(b0):
    return GAMMA_BAR * b0


def gre(rho, alpha_deg, tr, te, t1, t2s):
    a = np.radians(alpha_deg)
    e1 = np.exp(-tr / t1)
    return rho * np.sin(a) * (1 - e1) / (1 - np.cos(a) * e1) * np.exp(-te / t2s)


def ernst_angle_deg(tr, t1):
    return np.degrees(np.arccos(np.exp(-tr / t1)))


def se(rho, tr, te, t1, t2):
    return rho * (1 - np.exp(-tr / t1)) * np.exp(-te / t2)
