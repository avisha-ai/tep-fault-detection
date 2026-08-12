# Data

The Tennessee Eastman simulation dataset is **not redistributed** here, per source terms.
Download from Harvard Dataverse (Rieth et al., 2017): https://doi.org/10.7910/DVN/6C3JR1

Place in this folder:

- `TEP_FaultFree_Training.RData` — 24 MB
- `TEP_Faulty_Training.RData` — 471 MB

Both are gitignored. `TEP_Faulty_Training.RData` alone is well past GitHub's 100 MB hard
limit, so this exclusion is a licensing decision **and** a mechanical one.

`scripts/verify_data_dictionary.py` caches the original simulator source (`teprob.f`) here
when run — it downloads it from the [Braatz group mirror][1] if absent. Also gitignored:
it is third-party Fortran, not ours to redistribute.

[1]: https://github.com/camaramm/tennessee-eastman-profBraatz

## Sample extracts — committed

Two 1,000-row extracts **are** committed, so the repo is useful without the 495 MB download:

| File | Rows | From |
|---|---|---|
| `fault_free_training_first_1000.csv` | 1,000 | `TEP_FaultFree_Training.RData` |
| `faulty_training_first_1000.csv` | 1,000 | `TEP_Faulty_Training.RData` |

TEP is an open research benchmark and small samples are standard practice in ML repositories,
so these excerpts sit comfortably within the source terms. They let anyone clone, inspect the
schema, and sanity-check the pipeline before committing to the full download.

## Where the founders' local copies live

Recorded during Brick 1 estate alignment, 12 August 2026. The full raw data sits outside this
repo, deliberately:

```
~/Documents/Avisha/_local/tep-data/
├── TEP_FaultFree_Training.RData          24 MB
└── TEP_Faulty_Training.RData            471 MB
```
