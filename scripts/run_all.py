"""Run every script and save the console output to results/summary.txt."""
import glob, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
out = []
for f in sorted(glob.glob(os.path.join(here, "0*.py"))):
    r = subprocess.run([sys.executable, f], capture_output=True, text=True)
    block = f"=== {os.path.basename(f)} ===\n{r.stdout}{r.stderr}"
    print(block); out.append(block)
open(os.path.join(os.path.dirname(here), "results", "summary.txt"), "w").write("\n".join(out))
