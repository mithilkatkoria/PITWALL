# Existing solutions: source-based review

Research performed by Codex on2026-09-08 after the implemented prototype. This timing is explicit: these sources did not cause the initial design, which came from the user's brief. Findings below inform maintenance and the research-led review exercises added now. No software was downloaded or personally trialled for this review. Weaknesses refer to suitability for PITWALL's educational purpose and are identified as judgements, not measured defects.

## R01: TUM race-simulation

The authors describe a lap-based simulator with fuel-mass reduction, degradation, participant interactions and Monte Carlo. Their separate basic simulator assumes a free track and finds minimum race time; the broader system includes neural-network strategy approaches. [TUM repository and documentation](https://github.com/TUMFTM/race-simulation).

| Feature | Strength | Weakness for this project (judgement) | Decision | PITWALL impact |
|---|---|---|---|---|
| Basic/full separation | Makes assumptions distinguishable | Full interaction model exceeds initial scope | ADAPT | Keep single-car limitation visible; compare baseline and search under identical assumptions |
| Lap discretisation | Supports repeated scenario evaluation | Cannot resolve within-lap changes | LEARN | Add review exercise identifying a mid-lap event that PITWALL cannot represent |
| Monte Carlo | Studies probabilistic effects | Results depend on distributions | ADAPT | Retain seeds and test probability sensitivity rather than claim calibrated confidence |
| Neural strategy engineer | Automates richer decisions | Harder to defend at A-level | REJECT | Retain bounded enumeration and explain candidate count |

No source code or parameter set was copied. The authors' warning about exact race reproduction reinforces the need for PITWALL's conditional claims.

## R02: FastF1

The maintainer describes timing/telemetry/session access, extended Pandas structures, Matplotlib integration and request caching. This is a data-analysis library rather than PITWALL's counterfactual strategy simulator. [FastF1 maintainer README](https://github.com/theOehrly/Fast-F1).

| Feature | Strength | Weakness for this project (judgement) | Decision | PITWALL impact |
|---|---|---|---|---|
| Structured timing data | Supports inspecting individual laps | Observed laps contain confounding race effects | LEARN | Add calibration exercise separating observations from model inputs |
| Matplotlib integration | Connects numeric data and plots | Plot alone cannot establish model correctness | ADOPT principle | Keep independent arithmetic tests alongside graphs |
| API caching | Reduces repeated retrieval | Introduces external data/cache concerns | REJECT dependency now | Keep scenarios offline and portable |
| Pandas extensions | Rich analysis tools | Extra abstraction for a small typed model | ADAPT idea | Retain explicit LapResult records instead of adding DataFrames |

Future calibration would need source/date/provenance and rules for excluding pit, traffic and weather laps. FastF1 is not evidence that current fictional parameters are accurate. No live feed is required or integrated.

## R03: F1 Manager series

Frontier's 2023 Belgian circuit guide discusses mistimed dry/intermediate changes and a one-stop versus extra-stop decision involving traffic. This illustrates a strategy-learning scenario; game guidance is not validated engineering telemetry. [Publisher circuit guide](https://www.f1manager.com/nl-NL/2023/grand-prixs/belgian-grand-prix).

The 2024 feature article describes mechanical failures, more aggressive battles and multiple viewing angles. These are publisher descriptions, not independent realism findings. [Publisher feature article](https://www.f1manager.com/features/new/levensechte-f1-races).

| Feature | Strength | Weakness for this project (judgement) | Decision | PITWALL impact |
|---|---|---|---|---|
| Scenario-based decisions | Gives users a concrete trade-off | Outcome mixes traffic and tyre effects | ADAPT | Add controlled comparison tasks in review materials |
| Wet tyre timing | Demonstrates transition risk | PITWALL lacks wet compounds | LEARN | Mark wet-tyre choice explicitly unimplemented; propose suitability matrix |
| Failures and battles | Rich race context | Too broad for explainable first model | REJECT | Maintain single-car abstraction |
| Race presentation | Helps users follow events | Cinematic view does not reveal formulas | ADAPT | Prioritise component tables and actual graphs |

## Research-led changes made at this review

Added `docs/testing/research-review-exercises.md`: inspect a mid-lap event limitation; compare one/two-stop cases; examine probability sensitivity; distinguish telemetry calibration from illustrative input; explicitly identify missing wet tyres. These are new review tasks, not retrospective claims of stakeholder requests or test results.

The initial guessed TUM URL returned404 and the FastF1 docs endpoint returned403. The canonical repositories above were then read successfully. Some publisher pages required search retrieval. The accessible source contents support this review; no unavailable page is cited as read.
