"""Chapter 12: sixteen-channel hybrid TDM: service rates, memory, DSP and folding."""
import _common  # noqa: F401
from ddc import hardware as hw

configs = [("1 / 140 kHz", 143, 500e3), ("1 / 165 kHz", 53, 500e3), ("2 / 135 kHz", 49, 400e3),
           ("3 / 58 kHz", 107, 200e3), ("4 / 13 kHz", 57, 40e3), ("5 / 6.7 kHz", 49, 20e3)]
print("config        taps  f_TDM(MHz)  cycles/out  DSP(par)  BRAM36  DSP fold real / IQ")
for name, L, f_out in configs:
    print(f"{name:12s}  {L:4d}  {hw.service_rate(f_out)/1e6:10.2f}  {hw.cycles_per_output(f_out):10.2f}  "
          f"{hw.dsp_parallel(L):8d}  {hw.tdl_bram36(L):6d}  {hw.dsp_folded(L, f_out):4d} / {hw.dsp_folded(L, f_out, iq=True)}")
lead = {"LUT": 8918, "FF": 10800, "DSP": 25, "BRAM36": 1}
pct = {k: 100 * v / hw.XC7Z020[k] for k, v in lead.items()}
print("\nLead candidate utilisation on XC7Z020 (report model):",
      ", ".join(f"{k} {v:.2f} %" for k, v in pct.items()))
print(f"Replicated chains would need {16*22} multipliers; TDL for L=49: {16*49*24} bits")
