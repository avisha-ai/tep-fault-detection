# tep-fault-detection
Machine-learning fault detection on the Tennessee Eastman Process — why error composition matters more than accuracy
# Fault Detection on the Tennessee Eastman Process
### Why error composition matters more than accuracy

A machine-learning study of fault detection on the Tennessee Eastman Process (TEP), comparing static and time-aware features under a strict leakage-safe evaluation.

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

## Method

- **Data:** Tennessee Eastman Process simulation data, Rieth et al. (2017), Harvard Dataverse
- **Model:** Random Forest, 300 trees, binary classification (normal vs. faulty)
- **Static features:** instantaneous sensor measurements
- **Time-aware features:** static features plus rolling mean, rolling standard deviation, and rate of change over a 15-sample window, computed within each run
- **Evaluation:** run-level 80/20 split — entire simulation runs assigned wholly to train or test

The split is the part worth attention. Splitting at sample level lets adjacent, near-identical samples from the same run appear on both sides, and the resulting scores are optimistic. Every result here is from a run-level split.

---

## Per-fault results

Detection improves for nearly every fault when temporal context is added. The gains are largest where they matter most: **Faults 3, 9, and 15** — the ones the literature consistently finds hardest — improve three- to four-fold.

They are still the weakest in the study. Roughly half of those faults remain undetected. Temporal features narrow the gap; they do not close it.

---

## Repository

```
data/           loading and preparation (pyreadr)
notebooks/      exploration, feature construction, training, evaluation
figures/        TEP flowsheet, Fault 6 stripper pressure trace
paper/          full manuscript
```

---

## Reproducing

The dataset is not redistributed here. Download it from the Harvard Dataverse (Rieth et al., 2017) and place it in `data/`.

```bash
pip install -r requirements.txt
```

---

## Notes on verification

Two claims in this work were checked against primary sources rather than taken from secondary summaries:

- **Fault 6 is a loss of A feed** — confirmed against Downs & Vogel (1993) and four further sources.
- **`xmeas_16` is Stripper Pressure** — confirmed from the simulator source. The baseline in the Fault 6 figure sits at approximately 3100 kPa, against a published nominal of 3102.2 kPa gauge.

---

## Reference

Downs, J.J. and Vogel, E.F. (1993). *A plant-wide industrial process control problem.* Computers & Chemical Engineering, 17(3), 245–255.

Rieth, C.A., Amsel, B.D., Tran, R. and Cook, M.B. (2017). *Additional Tennessee Eastman Process Simulation Data for Anomaly Detection Evaluation.* Harvard Dataverse.

---

## Author

**Mrinal Gala** — process engineer. MS Chemical Engineering, University of Oklahoma. US Patent 2008/0200565 A1. Previously Jacobs Engineering, AkerKvaerner Powergas, SouthWest Nanotechnologies.

Built at [Avisha](https://avisha.ai) — a systems engineering atelier in Mumbai.
