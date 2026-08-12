# Project Log

## 2026-06-19 — First-pass binary fault detector
- Loaded the fault-free and faulty training datasets from the `.RData` files.
- Assigned labels so that `healthy = 0` for fault-free rows and for faulty rows with `sample <= 20`, and `faulty = 1` for faulty rows with `sample > 20`.
- Used only the sensor and valve feature columns (`xmeas_*` and `xmv_*`), excluding bookkeeping fields.
- Trained a `RandomForestClassifier` on a balanced sampled subset for a quick first-pass baseline.
- Result on the held-out test split: accuracy = 0.8578, false alarms = 268, and missed faults = 870.

## 2026-06-19 — Per-fault detection diagnosis
- Evaluated the trained model on the held-out test split and computed the fraction of true faulty rows correctly flagged for each fault type.
- The model performed very well for faults 1, 2, 4, 6, 7, 8, 12, 14, and 17 (detection rates above roughly 0.90).
- Faults 3, 9, and 15 were the weakest, with detection rates of about 0.11, 0.15, and 0.13 respectively, suggesting these fault patterns are harder for the current feature set and model to separate from normal behavior.
- This suggests the next improvement should focus on fault-specific feature engineering or class-specific modeling for the hardest fault types.

## 2026-06-19 — Leakage-safe evaluation (run-level split)
- Re-ran the evaluation with a strict split by full `(faultNumber, simulationRun)` so that rolling features could not leak between train and test.
- Compared two models on the same clean split:
  - Static features only: accuracy = 0.849, false alarms = 358, missed faults = 871.
  - Time-aware features (rolling mean/std/delta): accuracy = 0.8548, false alarms = 690, missed faults = 492.
- Under this leakage-safe setup, the time-aware model improved the overall accuracy slightly and substantially reduced missed faults, but it increased false alarms.
- Full per-fault detection rates on the clean run-level test split (computed as correctly detected faulty rows divided by true faulty rows) are:

| Fault | Static detection rate | Time-aware detection rate |
|---|---:|---:|
| 1 | 0.9952 | 1.0000 |
| 2 | 1.0000 | 1.0000 |
| 3 | 0.1359 | 0.5146 |
| 4 | 1.0000 | 1.0000 |
| 5 | 0.7778 | 0.9167 |
| 6 | 0.9951 | 0.9951 |
| 7 | 1.0000 | 1.0000 |
| 8 | 0.9712 | 0.9808 |
| 9 | 0.1467 | 0.4978 |
| 10 | 0.8614 | 0.9505 |
| 11 | 0.8774 | 0.9245 |
| 12 | 0.9849 | 0.9849 |
| 13 | 0.8959 | 0.9321 |
| 14 | 0.9912 | 0.9956 |
| 15 | 0.1100 | 0.4785 |
| 16 | 0.7943 | 0.9282 |
| 17 | 0.9607 | 0.9663 |
| 18 | 0.8938 | 0.9115 |
| 19 | 0.7009 | 0.8214 |
| 20 | 0.7800 | 0.8800 |

- For the hardest fault types, the leakage-safe time-aware detection rates were:
  - Fault 3: 0.5146
  - Fault 9: 0.4978
  - Fault 15: 0.4785
- These results are lower than the earlier row-level time-aware numbers (which were optimistic because of leakage), so the new run-level evaluation is the more trustworthy estimate of real performance.
