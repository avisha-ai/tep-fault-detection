# Figures

Analysis output, committed because these are the study's own figures.

| File | What it shows |
|---|---|
| `fault6_xmeas_16.png` | Stripper Pressure (`xmeas_16`), healthy vs Fault 6 — produced by `scripts/visualize_fault_comparison.py` |
| `fault6_xmeas_16_comparison.png` | The same trace with the healthy/faulty comparison overlaid |
| `fault6_sensor_comparison.png` | Fault 6 across several sensors |

Regenerate with:

```bash
python3 scripts/visualize_fault_comparison.py
```

This requires the raw `.RData` files in `data/` — see `data/README.md`.

*A fourth file, `Fault 6.png`, was listed here previously. It was a byte-identical duplicate of
`fault6_xmeas_16.png` and has not been committed; the copy is parked in
`~/Documents/Avisha/_local/tep-superseded/`.*
