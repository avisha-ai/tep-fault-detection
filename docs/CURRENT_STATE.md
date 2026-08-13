# CURRENT_STATE — TEP Fault Detection
## The honest state of this project.
## Updated after every completed build. Never optimistic.

**Last updated:** 2026-08-13
**District:** Vault · **Stage:** Operate · **Status:** active
**Live:** not deployed

---

## What exists and works

- verify_data_dictionary.py reproduces 0 mismatches across 53/53 entries
- Figures and two 1,000-row sample extracts committed
- Nesting flattened

## What does not exist yet

- 495MB of raw .RData and a 428MB virtualenv are excluded from git on source-terms and size grounds — recorded in the repo's data/README.md

---

## Contract

This repo carries the five-file contract:
`avisha.yaml` · `CLAUDE.md` · `docs/CURRENT_STATE.md` · `NEXT_BUILD.md` · `events/`

The passport (`avisha.yaml`) is the machine-readable identity. This file is
the human-readable truth. If they disagree, the passport is wrong and gets
corrected — never the other way round.
