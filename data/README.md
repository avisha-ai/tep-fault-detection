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

## Where the founders' local copies live

Recorded during Brick 1 estate alignment, 12 August 2026. On Mrinal's machine the raw data
sits outside this repo, deliberately:

```
~/Documents/Avisha/_local/tep-data/
├── TEP_FaultFree_Training.RData          24 MB
├── TEP_Faulty_Training.RData            471 MB
├── fault_free_training_first_1000.csv   372 KB   1,000-row extract
└── faulty_training_first_1000.csv       368 KB   1,000-row extract
```

The two CSV extracts are **not committed** for the same reason as the source data: a 1,000-row
sample is still a partial redistribution of a dataset this repo declines to redistribute.
Nothing in the repo references them. If the source terms turn out to permit small excerpts,
they would be genuinely useful here — they would let anyone run the notebook without the
495 MB download. That is a founder call, not an assumption to make silently.
