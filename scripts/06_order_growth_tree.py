"""Chapters 10-11: register growth per chain, order comparison, shared-tree saving."""
import _common  # noqa: F401
from ddc import cic

chains = {1: [10, 10, 4], 2: [10, 10, 5], 3: [10, 10, 10], 4: [10, 10, 10, 5], 5: [10, 10, 10, 10]}
print("Path  chain            raw width (N=3)  pruned to 24")
for p, c in chains.items():
    w = cic.register_widths(c, 3)[-1]
    print(f"{p:4d}  {str(c):15s}  {w:15d}  {w-24:12d}")
print("\nFinal bus width for N = 3, 4, 5:")
for p, c in chains.items():
    print(f"  Path {p}: " + ", ".join(str(cic.register_widths(c, N)[-1]) for N in (3, 4, 5)))
print("\nPath 5 register widths, chain [10,10,10,10], N = 3:", cic.register_widths(chains[5], 3))
print("Shared [10,10] trunk: CIC logic 5,049 -> 1,887 LUTs (report, Table 11.1): "
      f"{100*(1-1887/5049):.1f} % saving")
