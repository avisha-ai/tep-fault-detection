# TEP variable dictionary

Variable mappings for the Tennessee Eastman Process simulation data (Rieth et al., 2017),
verified against the authoritative variable list in the original simulator source
(`teprob.f`, Downs & Vogel). Composition analyzers report in mole %; their stream
and sampling context is given in the last column.

Bookkeeping columns:

| Column | Meaning | Units |
|---|---|---|
| `faultNumber` | Fault identifier for the simulated disturbance (0 = fault-free) | - |
| `simulationRun` | Simulation run index | - |
| `sample` | Time sample index within a run (3-minute intervals) | - |

Process measurements:

| Column | Meaning | Units | Context |
|---|---|---|---|
| `xmeas_1` | A Feed (stream 1) | kscmh | |
| `xmeas_2` | D Feed (stream 2) | kg/hr | |
| `xmeas_3` | E Feed (stream 3) | kg/hr | |
| `xmeas_4` | A and C Feed (stream 4) | kscmh | |
| `xmeas_5` | Recycle Flow (stream 8) | kscmh | |
| `xmeas_6` | Reactor Feed Rate (stream 6) | kscmh | |
| `xmeas_7` | Reactor Pressure | kPa gauge | |
| `xmeas_8` | Reactor Level | % | |
| `xmeas_9` | Reactor Temperature | Deg C | |
| `xmeas_10` | Purge Rate (stream 9) | kscmh | |
| `xmeas_11` | Product Sep Temp | Deg C | |
| `xmeas_12` | Product Sep Level | % | |
| `xmeas_13` | Prod Sep Pressure | kPa gauge | |
| `xmeas_14` | Prod Sep Underflow (stream 10) | m3/hr | |
| `xmeas_15` | Stripper Level | % | |
| `xmeas_16` | Stripper Pressure | kPa gauge | |
| `xmeas_17` | Stripper Underflow (stream 11) | m3/hr | |
| `xmeas_18` | Stripper Temperature | Deg C | |
| `xmeas_19` | Stripper Steam Flow | kg/hr | |
| `xmeas_20` | Compressor Work | kW | |
| `xmeas_21` | Reactor Cooling Water Outlet Temp | Deg C | |
| `xmeas_22` | Separator Cooling Water Outlet Temp | Deg C | |
| `xmeas_23` | Component A | mol % | Reactor Feed Analysis (stream 6), sampling 0.1 hr |
| `xmeas_24` | Component B | mol % | Reactor Feed Analysis (stream 6), sampling 0.1 hr |
| `xmeas_25` | Component C | mol % | Reactor Feed Analysis (stream 6), sampling 0.1 hr |
| `xmeas_26` | Component D | mol % | Reactor Feed Analysis (stream 6), sampling 0.1 hr |
| `xmeas_27` | Component E | mol % | Reactor Feed Analysis (stream 6), sampling 0.1 hr |
| `xmeas_28` | Component F | mol % | Reactor Feed Analysis (stream 6), sampling 0.1 hr |
| `xmeas_29` | Component A | mol % | Purge Gas Analysis (stream 9), sampling 0.1 hr |
| `xmeas_30` | Component B | mol % | Purge Gas Analysis (stream 9), sampling 0.1 hr |
| `xmeas_31` | Component C | mol % | Purge Gas Analysis (stream 9), sampling 0.1 hr |
| `xmeas_32` | Component D | mol % | Purge Gas Analysis (stream 9), sampling 0.1 hr |
| `xmeas_33` | Component E | mol % | Purge Gas Analysis (stream 9), sampling 0.1 hr |
| `xmeas_34` | Component F | mol % | Purge Gas Analysis (stream 9), sampling 0.1 hr |
| `xmeas_35` | Component G | mol % | Purge Gas Analysis (stream 9), sampling 0.1 hr |
| `xmeas_36` | Component H | mol % | Purge Gas Analysis (stream 9), sampling 0.1 hr |
| `xmeas_37` | Component D | mol % | Product Analysis (stream 11), sampling 0.25 hr |
| `xmeas_38` | Component E | mol % | Product Analysis (stream 11), sampling 0.25 hr |
| `xmeas_39` | Component F | mol % | Product Analysis (stream 11), sampling 0.25 hr |
| `xmeas_40` | Component G | mol % | Product Analysis (stream 11), sampling 0.25 hr |
| `xmeas_41` | Component H | mol % | Product Analysis (stream 11), sampling 0.25 hr |

Manipulated variables:

| Column | Meaning | Units |
|---|---|---|
| `xmv_1` | D Feed Flow (stream 2) | % |
| `xmv_2` | E Feed Flow (stream 3) | % |
| `xmv_3` | A Feed Flow (stream 1) | % |
| `xmv_4` | A and C Feed Flow (stream 4) | % |
| `xmv_5` | Compressor Recycle Valve | % |
| `xmv_6` | Purge Valve (stream 9) | % |
| `xmv_7` | Separator Pot Liquid Flow (stream 10) | % |
| `xmv_8` | Stripper Liquid Product Flow (stream 11) | % |
| `xmv_9` | Stripper Steam Valve | % |
| `xmv_10` | Reactor Cooling Water Flow | % |
| `xmv_11` | Condenser Cooling Water Flow | % |
| `xmv_12` | Agitator Speed | rpm |

## Correction note

An earlier version of this dictionary mis-described `xmeas_23`–`xmeas_41`
(the composition analyzer outputs) as additional flow/temperature measurements.
The error was caught by `scripts/verify_data_dictionary.py`, which compares this
dictionary entry-by-entry against the simulator source. This version is rebuilt
from that authoritative list. The analysis in the accompanying paper is unaffected:
it interprets only `xmeas_16` (Stripper Pressure), which was verified correct.
