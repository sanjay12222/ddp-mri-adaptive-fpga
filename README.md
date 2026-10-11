# Hardware-Efficient Adaptive Filtering for Multi-Channel MRI Receivers on FPGA

**Dual Degree Project, Stage I: Multirate Digital Down-Conversion for On-Chip Signal Acquisition**

Sanjay Kumar Meena (22B3978) · Department of Electrical Engineering, IIT Bombay
Guide: Prof. Vikram M. Gadre · Mentors: Shri Rahul Chowdhary and Shri Dharmesh Verma, SAMEER

This repository contains the code behind the DDP Stage I report. The project designs the digital receiver of an MRI spectrometer on an FPGA: the hardware between the ADC and a clean, decimated baseband stream. Stage I makes this receiver hardware-efficient, using a CIC decimator, a piecewise least-squares (FIRLS) compensator, a shared decimation tree and a sixteen-channel time-division-multiplexed (TDM) filter. Stage II will use the freed FPGA resources for adaptive filtering.

## Repository layout

```
ddc/            Python package: the models used in the report
  cic.py          CIC response, multistage droop, register growth, image rejection
  compensator.py  piecewise FIRLS target, design, cascade check, length search, quantisation
  hardware.py     resource model: DSP slices, BRAM, folding, area score, power proxy, Pareto filter
  nlms.py         complex leaky NLMS canceller and fixed-point encoding
  signal_model.py Larmor frequency, gradient-echo and spin-echo contrast
scripts/        one script per result in the report (run_all.py runs them all)
notebooks/      original development notebooks (see notebooks/README.md)
results/        output of run_all.py
```

## How to run

```bash
pip install -r requirements.txt
python scripts/run_all.py        # prints every result and writes results/summary.txt
```

The full run takes about 15 seconds.

## Results reproduced by the scripts

| Report | Result | Script |
|---|---|---|
| Ch. 5 | Larmor frequency 63.87 MHz; Ernst angle 23.1° (debug) | `01_signal_model.py` |
| Ch. 7 | Single filter at 250 MSPS: 6,045 taps, 3,023 multipliers, 12.1 µs delay | `02_single_stage_bottleneck.py` |
| Ch. 8, App. B | CIC droop −0.143 dB; 31-tap cascade 0.0376 dB ripple, 69.4 dB attenuation | `03_cic_firls_single_path.py` |
| Ch. 9 | Target error: 1 segment 1.12 dB, 15 segments 0.008 dB | `04_piecewise_target.py` |
| Ch. 9 | Five paths, M = 400 … 10,000; Path 1 compensator 87 / 41 / 29 taps at 0.6 / 0.7 / 0.8 of Nyquist | `05_five_paths.py` |
| Ch. 10–11 | Register widths 42–56 bits (N = 3), 56 → 84 bits for Path 5 (N = 3 → 5) | `06_order_growth_tree.py` |
| Sec. 3.4.5 | Image rejection 31.4 / 41.8 / 52.3 dB for N = 3 / 4 / 5 | `07_image_rejection.py` |
| Ch. 12 | Service rates, 31.25 cycles per output, BRAM36 count, folded DSP count | `08_tdm_cost.py` |
| Ch. 6 | NLMS canceller and Q-format encoding of µ and ε | `09_nlms_demo.py` |

Notes:
- The scripts are a clean re-implementation. The design-space exploration (392 configurations) and the figures in the report were produced with the original notebooks in `notebooks/`.
- `05_five_paths.py` matches the report at 0.6, 0.7 and 0.8 of the Nyquist frequency. At 0.9 and above it finds slightly shorter filters (19 and 15 taps) than the report's 21, because the length search here is exhaustive over odd lengths.
- The sixteen-channel resource figures (25 DSP48E1, 8,918 LUTs, 10,800 flip-flops, one BRAM36) are model predictions. RTL and Vivado validation are ongoing.

## Data

The MRI phantom images were acquired on SAMEER's IMRI system and are not included in this repository. All signals used by the scripts are synthetic.

## Citation

S. K. Meena, *Hardware-Efficient Adaptive Filtering for Multi-Channel MRI Receivers on FPGA, Stage I: Multirate Digital Down-Conversion for On-Chip Signal Acquisition*, Dual Degree Project Stage I Report, Department of Electrical Engineering, IIT Bombay, October 2026.

## Acknowledgements

Prof. Vikram M. Gadre (guide); Shri Rajesh Harsh, Programme Director, SAMEER; Shri Rahul Chowdhary and Shri Dharmesh Verma, Scientists, SAMEER.
