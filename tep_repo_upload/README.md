# Fault Detection on the Tennessee Eastman Process
### Why error composition matters more than accuracy

A machine-learning study of fault detection on the Tennessee Eastman Process (TEP), comparing static and time-aware features under a strict leakage-safe evaluation.

**Author:** Mrinal Gala · [Avisha](https://avisha.ai) — Engineering Intelligence Atelier, Mumbai
**Full paper:** [`TEP_Fault_Detection_Case_Study.pdf`](./TEP_Fault_Detection_Case_Study.pdf)

---

## The finding

Adding temporal context raised overall accuracy by less than one percentage point — from **0.849 to 0.855**. On that number alone, the time-aware model is barely worth the trouble.

The number is misleading.

| | Static | Time-aware |
|---|---|---|
| Accuracy | 0.849 | 0.855 |
| **Missed faults** | **871** | **492** |
| False alarms | 358 | 690 |

The time-aware model misses **43% fewer faults** and raises roughly twice as many false alarms. Overall accuracy hides this entirely, because it treats both errors as equivalent. In a plant they are not: a missed fault is a hazard, a false alarm is a nuisance. The trade-off favours safety.

**In process fault detection, the composition of the error is more informative than the accuracy.**

---

## The evaluation protocol — the part worth attention

Every result here is from a **run-level split**: entire simulation runs are assigned wholly to train or test (80/20). Splitting at sample level lets adjacent, near-identical samples from the same run appear on both sides, and the resulting scores are optimistic.

This is not hypothetical. When the time-aware features were first evaluated with a sample-level split, the hardest faults appeared to reach detection rates near **0.80**. That improvement was an illusion — the rolling features were borrowing from neighbouring samples across the split, and the model was effectively reading part of its own answer key. Re-evaluating at run level returned the honest figures below, with the hardest faults closer to **0.50**.

The inflation affected the time-aware features far more than the static ones — precisely where the rolling window could borrow from adjacent samples. Whenever features carry temporal context, the unit of splitting must be the whole run, or reported performance can be substantially overstated.

---

## Per-fault results

| Fault | Static | Time-aware | |
|---|---|---|---|
| 1 | 1.00 | 1.00 | |
| 2 | 1.00 | 1.00 | |
| 3 | 0.14 | **0.51** | hardest in the literature |
| 4 | 1.00 | 1.00 | |
| 5 | 0.78 | 0.92 | |
| 6 | 1.00 | 1.00 | worked example in the paper |
| 7 | 1.00 | 1.00 | |
| 8 | 0.97 | 0.98 | |
| 9 | 0.15 | **0.50** | hardest in the literature |
| 10 | 0.86 | 0.95 | |
| 11 | 0.88 | 0.92 | |
| 12 | 0.98 | 0.98 | |
| 13 | 0.90 | 0.93 | |
| 14 | 0.99 | 1.00 | |
| 15 | 0.11 | **0.48** | hardest in the literature |
| 16 | 0.79 | 0.93 | |
| 17 | 0.96 | 0.97 | |
| 18 | 0.89 | 0.91 | |
| 19 | 0.70 | 0.82 | |
| 20 | 0.78 | 0.88 | |

Detection improves for nearly every fault when temporal context is added. The gains are largest where they matter most: **Faults 3, 9, and 15** — the ones the literature consistently finds hardest — improve three- to four-fold. They are still the weakest in the study: roughly half of those faults remain undetected. Temporal features narrow the gap; they do not close it.

---

## Method

- **Data:** Tennessee Eastman Process simulation data, Rieth et al. (2017), Harvard Dataverse
- **Model:** Random Forest, 300 trees, binary classification (normal vs. faulty)
- **Static features:** the 52 instantaneous sensor measurements
- **Time-aware features:** static features plus rolling mean, rolling standard deviation, and rate of change over a 15-sample window, computed strictly within each run
- **Evaluation:** run-level 80/20 split — entire simulation runs assigned wholly to train or test
- **Interpretation:** dataset variable codes mapped to physical meanings (e.g. `xmeas_16` → Stripper Pressure), so model behaviour can be reasoned about as process engineering rather than anonymous columns

---

## Repository

```
notebooks/te_exploration.ipynb    exploration, features, training, and the run-level evaluation
scripts/                          data exploration, figure generation, and dictionary verification
docs/                             TEP variable dictionary + its verification report (0 mismatches vs teprob.f)
figures/                          TEP flowsheet, Fault 6 stripper pressure traces
data/                             dataset location (not committed — see data/README.md)
PROJECT_LOG.md                    dated log of the analysis, including the leakage discovery
TEP_Fault_Detection_Case_Study.pdf   full manuscript
```

## Reproducing

The dataset is not redistributed here. Download it from the [Harvard Dataverse (Rieth et al., 2017)](https://doi.org/10.7910/DVN/6C3JR1) and place it in `data/`.

```bash
pip install -r requirements.txt
```

---

## Notes on verification

Two claims in this work were checked against primary sources rather than taken from secondary summaries:

- **Fault 6 is a loss of A feed** — confirmed against Downs & Vogel (1993) and four further sources.
- **`xmeas_16` is Stripper Pressure** — confirmed from the simulator source. The baseline in the Fault 6 figure sits at approximately 3100 kPa, against a published nominal of 3102.2 kPa gauge.
- The full variable dictionary (`docs/data_dictionary.md`) is verified entry-by-entry against `teprob.f` by `scripts/verify_data_dictionary.py` — currently **0 mismatches across all 53 variables**. An earlier draft mis-described the composition analyzers (`xmeas_23`–`xmeas_41`); the verification script caught it, and the correction is documented in the dictionary itself.

---

## Reference

Downs, J.J. and Vogel, E.F. (1993). *A plant-wide industrial process control problem.* Computers & Chemical Engineering, 17(3), 245–255.

Rieth, C.A., Amsel, B.D., Tran, R. and Cook, M.B. (2017). *Additional Tennessee Eastman Process Simulation Data for Anomaly Detection Evaluation.* Harvard Dataverse.

---

## Author

**Mrinal Gala** — process engineer. MS Chemical Engineering, University of Oklahoma. US Patent 2008/0200565 A1. Previously Jacobs Engineering, AkerKvaerner Powergas, SouthWest Nanotechnologies.

Built at [Avisha](https://avisha.ai) — an engineering intelligence atelier in Mumbai.
