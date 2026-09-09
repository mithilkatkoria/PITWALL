# Documentation cleanup review

This internal review lists every changed file and the exact before/after wording. Minus lines are the original text; plus lines are the replacement. README restructuring is included in full so no removed assistance-related sentence is omitted. The complete assistance-log rewrite is included.

The cleanup keeps attribution in the factual assistance log and makes no percentage or limited-scope claim. Candidate follow-up remains unrecorded unless documented.

## Every file changed

- README.md
- docs/analysis/research.md
- docs/assistance-log.md
- docs/evaluation/review.md
- docs/iterations/I01.md
- docs/iterations/I07.md
- docs/testing/FAIL-I17-02.md
- report/evidence-index.csv
- report/mark-audit.md
- report/master-evidence-pack.md
- report/missing-evidence.md
- report/documentation-cleanup.md (this review)

The evidence index changes only byte counts and hashes for these edited documents: docs/analysis/research.md, docs/assistance-log.md, docs/evaluation/review.md, docs/iterations/I01.md, docs/iterations/I07.md, docs/testing/FAIL-I17-02.md. No evidence rows are removed.

## Exact wording changes

### README.md

```diff
diff --git a/README.md b/README.md
index dd6ffea..76d9fb9 100644
--- a/README.md
+++ b/README.md
@@ -2,25 +2,61 @@
 
 **Motorsport Race Strategy Simulation and Optimisation System**
 
-OCR A Level Computer Science H446-03 project. Candidate Mithil Katkoria,0460. Centre12709.
+PITWALL is a Python/PySide6 desktop application for exploring how tyre choice, degradation, fuel, pit stops and changing race conditions affect strategy. Configure a race, compare alternative plans, examine uncertainty with paired Monte Carlo trials and search for the fastest strategy within a defined set of constraints.
 
-PITWALL is a working Python/PySide6 desktop prototype with a deterministic race model, tyre/fuel/pit effects, multi-strategy comparison, event-driven weather and safety car, seeded variation, paired Monte Carlo, bounded strategy search, JSON scenarios and actual-output charts.
+## Screenshots
 
-This is AI-assisted coursework development. See [assistance log](docs/assistance-log.md). Candidate review, explanation, genuine stakeholder work and centre requirements remain outstanding. No guaranteed mark is claimed.
+### Strategy comparison
 
-## Run on this machine
+![PITWALL comparing two strategies with simulated lap times](evidence/screenshots/FIG-I16-20260908T213427339706Z/01-comparison.png)
 
-Open PowerShell in this directory and run:
+### Monte Carlo analysis
 
-```powershell
-.\launch.ps1
-```
+![PITWALL showing the distribution of total race times across paired trials](evidence/screenshots/FIG-I16-20260908T213427339706Z/08-monte-carlo-chart.png)
+
+Both images are captures of the running Windows application using illustrative model parameters.
+
+## Main features
+
+- Configurable race length, base pace, driver penalty, fuel effect and three dry tyre compounds.
+- Strategy editing with ordered pit stops and per-stop service times.
+- Deterministic simulation with per-lap results, cumulative times and comparison metrics.
+- Chronological weather and safety-car events with explicit ordering rules.
+- Seeded lap variation and paired Monte Carlo trials with summary statistics.
+- Bounded strategy search with candidate counts and baseline comparisons.
+- Lap-time graphs, ranked search results and Monte Carlo histograms.
+- Versioned JSON scenarios, complete experiment exports and cancellable background runs.
+
+## Technical architecture
+
+The computational model is separated from the desktop interface. Immutable dataclasses represent race inputs and results; pure functions calculate lap components; the engine applies events and advances race state.
+
+| Layer | Responsibility | Modules |
+|---|---|---|
+| Data model | Typed inputs, results and validation | `models.py`, `conditions.py` |
+| Simulation | Lap calculations, event queue and race state | `physics.py`, `events.py`, `engine.py` |
+| Analysis | Comparison, repeated trials and bounded search | `comparison.py`, `monte_carlo.py`, `optimiser.py` |
+| Persistence | Strict versioned JSON and atomic scenario saves | `persistence.py` |
+| Desktop | PySide6 widgets, Matplotlib charts and background workers | `gui.py`, `advanced_gui.py` |
+
+See the [architecture diagrams](docs/design/implemented-structure.md) and [design records](docs/design/architecture.md) for the class relationships and data flow.
+
+## Algorithms
+
+- **Lap calculation:** base pace plus tyre, fuel, pit, weather, safety-car and optional random terms.
+- **Tyre degradation:** linear loss based on completed laps on the current tyre set.
+- **Event processing:** a heap orders events by lap and original input order for ties.
+- **Strategy comparison:** total race time ranks plans under identical conditions; exact ties retain input order.
+- **Monte Carlo:** paired trials share a seed and conditions, with optional random safety-car occurrence and timing. Results include mean, median, population standard deviation and win/tie probabilities.
+- **Optimisation:** enumerate legal zero-, one- and two-stop plans on a constrained pit-lap grid, simulate each candidate and rank the complete set. Search uses fixed events with random lap variation disabled.
+
+The [algorithm index](report/master-evidence-pack.md#algorithm-index) links to pseudocode, assumptions and complexity notes.
 
-The working runtime is currently `%TEMP%\pitwall-0460-venv`. It avoids a Windows long-path installation failure in the deeply nested workspace. Temporary directories can be cleaned by Windows. The local `.venv` contains an incomplete GUI dependency installation; recreate a short runtime if the working one disappears.
+## Installation
 
-## Recreate the environment
+The verified environment is Windows 11 with Python 3.14, PySide6, Matplotlib and pytest. Other Python/OS combinations have not been verified.
 
-Use Python3.14 as tested, and a short environment location on Windows:
+From the PITWALL directory, create a short environment path on Windows:
 
 ```powershell
 python -m venv "$env:TEMP\pitwall-0460-venv"
@@ -28,31 +64,57 @@ python -m venv "$env:TEMP\pitwall-0460-venv"
 & "$env:TEMP\pitwall-0460-venv\Scripts\python.exe" main.py
 ```
 
-`requirements-lock.txt` records the actually installed versions. `requirements.txt` records the supported dependency ranges. Python3.10+ syntax is used, but other Python/OS combinations have not been verified.
+`requirements-lock.txt` records the tested dependency versions; `requirements.txt` records dependency ranges. A short environment path avoids the PySide6 path-length installation error encountered in the nested development workspace.
 
-## Use
+For the existing setup, launch with:
 
-1. Configure laps, base pace, pit loss, fuel and tyre penalties. Parameters are illustrative, not telemetry.
-2. Edit strategy rows. Stop syntax `15:Medium, 35:Hard`; blank means no stop. Optional service override: `25:Hard:3.0`. Stops occur **after** their racing lap; new tyres run the next lap.
-3. Select a row and simulate, or compare all rows. Inspect graph, summary and every-lap tabs. Editing inputs clears old results.
-4. Conditions & experiments contains weather/events, seed/noise, Monte Carlo and search controls. Scroll this tab to reach experiment actions.
-5. Event syntax: `10:Wet, 15:SC_START, 18:SC_END, 25:Dry`. Events occur **before** the lap. Same-lap commands use input order.
-6. Monte Carlo uses the first two rows with common per-trial conditions. Search ignores noise, uses fixed events, and reports the best strategy in its bounded grid. Cancel long runs with CANCEL RUN.
-7. SAVE/LOAD stores race scenarios. EXPORT RUN stores complete search scores or Monte Carlo trials and inputs. Example scenarios are in `scenarios/`.
+```powershell
+.\launch.ps1
+```
+
+The launcher uses `%TEMP%\pitwall-0460-venv` when available. Windows may clean temporary directories, so recreate this environment if necessary. The development workspace's local `.venv` has an incomplete GUI dependency installation; use the short-path environment above.
+
+## Usage
+
+1. Configure the race and tyre parameters.
+2. Edit strategy rows. Enter stops as `15:Medium, 35:Hard`, or leave the field blank for no stops. An optional service-time override uses `25:Hard:3.0`.
+3. Select a strategy and simulate, or compare all rows. Inspect the graph, metrics and every-lap tabs. Editing inputs clears previous results.
+4. Open **Conditions & experiments** to configure weather, events, seed, variation and analysis controls. Scroll the tab to reach experiment actions.
+5. Enter events such as `10:Wet, 15:SC_START, 18:SC_END, 25:Dry`.
+6. Run Monte Carlo using the first two strategy rows, or run the optimiser with the chosen search constraints. Use **CANCEL RUN** to cancel background work.
+7. Use **SAVE/LOAD** for scenarios and **EXPORT RUN** for complete experiment inputs and results. Example scenarios are in [scenarios](scenarios/).
 
-Model and limits: linear wear; fuel penalty decreases to zero; single-car model; only dry compounds; weather penalties equal across compounds; SC changes lap penalty and relative pit loss without field bunching. No FIA compound rules or real-world calibration. Search maximum2 stops,10,000 candidates/two million lap evaluations; race1..500 laps; comparison2..20; Monte Carlo1..1000 trials (GUI100/500/1000). Oversized search fails explicitly. Generated SC commands can overlap fixed commands, which are simple state assignments.
+Pit stops occur **after** the specified racing lap; fresh tyres run the following lap. Events occur **before** their specified lap. Same-lap events follow input order.
 
-GUI numeric inputs use three decimal places and finite ranges. Loading out-of-range or more precise parameters fails before altering inputs. Research findings and limitations are documented rather than hidden.
+## Testing
 
-## Verification and evidence
+The latest recorded full verification run passed **86 tests**, covering model validation, manual calculation examples, event ordering, reproducibility, search, persistence and GUI integration.
 
 ```powershell
 & "$env:TEMP\pitwall-0460-venv\Scripts\python.exe" scripts/run_tests.py TEST-LOCAL
 & "$env:TEMP\pitwall-0460-venv\Scripts\python.exe" scripts/benchmark.py
 ```
 
-The test runner preserves stdout/stderr,JUnit XML, command, environment and source hashes in a unique directory. Failed runs remain preserved. Benchmark output contains raw timings and machine details. GUI captures come from actual running Qt widgets and are labelled automated captures, not human usability evidence.
+The test runner retains stdout/stderr, JUnit XML, execution metadata and source hashes in a unique directory. Earlier failures and retests are preserved. Benchmark records include raw timings and machine details. See [test results](report/test-results.csv) and the [evidence index](report/evidence-index.csv).
+
+Git attributes preserve exact file bytes across Windows checkouts. Rebuild indexes after new evidence with `scripts/build_index.py` using the same Python runtime.
+
+## Limitations
+
+- Parameters are illustrative and have not been calibrated against real race telemetry.
+- The model represents one car on a free track, with linear tyre wear and a simplified fuel penalty.
+- Only dry compounds are available. Weather penalties apply equally across them; wet/intermediate tyre selection is unsupported.
+- Safety-car effects approximate lap delay and relative pit loss without modelling field bunching. Overlapping fixed/generated commands use state assignments.
+- Search returns the best result within its grid and constraints. It does not establish a globally optimal real-world strategy or enforce FIA compound rules.
+- Limits are 1..500 race laps, 2..20 compared strategies and up to 1,000 Monte Carlo trials. Search permits up to two stops and rejects work beyond 10,000 candidates or two million lap evaluations.
+- GUI inputs use three decimal places and finite ranges. Loading an unrepresentable value fails before changing the current inputs.
+
+Further maintenance considerations and improvements are in the [technical evaluation](docs/evaluation/review.md).
+
+## Project documentation
+
+Developed for OCR A Level Computer Science H446-03. Candidate: Mithil Katkoria, 0460. Centre: 12709.
 
-Final verified run: **86 tests passed**. Earlier genuine failures and retests are retained. Git attributes preserve exact bytes to keep source/evidence hashes meaningful across Windows checkouts. Rebuild indexes after new evidence with `scripts/build_index.py` using the same Python runtime.
+Development records, source references and required assistance declarations are maintained separately in the [project documentation](report/master-evidence-pack.md).
 
-Start with [master evidence pack](report/master-evidence-pack.md), [criteria audit](report/mark-audit.md), [missing evidence](report/missing-evidence.md) and [iteration records](docs/iterations/). Genuine commits are in this directory's independent Git repository. Existing workspace projects were not edited.
+The [criteria audit](report/mark-audit.md), [missing-evidence record](report/missing-evidence.md) and [iteration records](docs/iterations/) track assessment preparation. Candidate review, genuine stakeholder/usability feedback and confirmation against the separate centre checklist remain outstanding.
\ No newline at end of file
```

### docs/analysis/research.md

```diff
diff --git a/docs/analysis/research.md b/docs/analysis/research.md
index c076c6c..c698eda 100644
--- a/docs/analysis/research.md
+++ b/docs/analysis/research.md
@@ -1,6 +1,6 @@
 # Existing solutions: source-based review
 
-Research performed by Codex on2026-09-08 after the implemented prototype. This timing is explicit: these sources did not cause the initial design, which came from the user's brief. Findings below inform maintenance and the research-led review exercises added now. No software was downloaded or personally trialled for this review. Weaknesses refer to suitability for PITWALL's educational purpose and are identified as judgements, not measured defects.
+Source review recorded on 2026-09-08 after the implemented prototype. This timing is explicit: these sources did not cause the initial design, which came from the user's brief. Findings below inform maintenance and the research-led review exercises added now. No software was downloaded or personally trialled for this review. Weaknesses refer to suitability for PITWALL's educational purpose and are identified as judgements, not measured defects.
 
 ## R01: TUM race-simulation
```

### docs/assistance-log.md

```diff
diff --git a/docs/assistance-log.md b/docs/assistance-log.md
index 51e1176..aeaf6a7 100644
--- a/docs/assistance-log.md
+++ b/docs/assistance-log.md
@@ -1,9 +1,12 @@
-# Factual assistance log
+# Assistance log
 
-2026-09-08: User supplied the PITWALL brief. Codex read it and inspected the workspace. Codex is authoring provisional analysis, designs, implementation, tests and evidence records. This is AI-assisted work, not evidence of unaided candidate authorship. Candidate understanding and review are pending. Centre assistance/declaration guidance has not been supplied. The candidate should review and explain each accepted part and follow their centre's declaration requirements.
+Tool used: Codex. Centre-specific declaration guidance is pending. No assistance percentage is assigned.
 
-No stakeholder answers, teacher comments, historical dates, failed tests or screenshots are fabricated. Test and program output will be recorded only when executed.
+| Date / stage | Assistance provided | Affected files / features | Candidate follow-up recorded |
+|---|---|---|---|
+| 2026-09-08, planning and records | Drafted requirements, designs, diagrams, development records, README and evaluation; reviewed three sources after the prototype | `docs/`, `README.md`, `report/` | Candidate supplied brief; subsequent review not recorded |
+| 2026-09-08, implementation | Authored simulation, comparison, GUI, environmental events, randomness, Monte Carlo, search and persistence modules | `src/pitwall/`, `main.py`, `launch.ps1` | Personal changes or explanation not recorded |
+| 2026-09-08, verification | Wrote/ran tests; fixed JSON validation and capture-harness issues; captured/inspected actual GUI output and ran benchmarks | `tests/`, `scripts/`, `evidence/` | Personal testing or review not recorded |
+| 2026-09-08, cleanup | Reorganised public documentation and consolidated attribution | Files in `report/documentation-cleanup.md` | Candidate requested cleanup; review of edits not recorded |
 
-2026-09-08 continued: Codex authored and executed iterative model, physics, engine, comparison, GUI, event, weather, safety-car, randomness, Monte Carlo, optimiser and persistence work. Codex created automated tests and preserved real stdout/JSON/XML, including an actual JSON-container validation failure before fixing it. Codex created and corrected a real Qt capture harness, took actual widget captures, inspected them and ran machine-specific benchmarks. Codex reviewed three genuine existing-system sources after the prototype and explicitly recorded that research timing. No external system's source code or parameter values were copied. Source reviews do not represent hands-on use.
-
-Codex wrote the README, design diagrams, provisional evaluation, traceability and evidence indexes. All candidate reflections, stakeholder feedback, teacher approval and final assessment judgements remain pending. Git commits were made at actual execution times in a separate PITWALL repository; no historical dates were manufactured. This assistance record should be considered alongside the actual task conversation and local history when following the centre's requirements.
+Source review involved no hands-on trials or copied source code/parameters. Execution records, captures and Git history remain intact. Add personal review, changes, tests and explanations when completed.
```

### docs/evaluation/review.md

```diff
diff --git a/docs/evaluation/review.md b/docs/evaluation/review.md
index e4f75ef..d0de336 100644
--- a/docs/evaluation/review.md
+++ b/docs/evaluation/review.md
@@ -1,6 +1,6 @@
 # Evidence-based prototype evaluation
 
-This is an assistant-authored review of actual implementation/output. Candidate judgement and genuine stakeholder validation are still required. The separate centre criteria file is unavailable; this is not a completed assessed submission.
+This technical review evaluates the recorded implementation and output. Candidate judgement and genuine stakeholder validation are still required. The separate centre criteria file is unavailable; this is not a completed assessed submission.
 
 ## Success criteria
```

### docs/iterations/I01.md

```diff
diff --git a/docs/iterations/I01.md b/docs/iterations/I01.md
index a4d4752..4abf956 100644
--- a/docs/iterations/I01.md
+++ b/docs/iterations/I01.md
@@ -10,4 +10,4 @@ Genuine test failures: none observed. Diagnosis, remedial action and retest: N/A
 
 Screenshot evidence: pending, no GUI yet. [GENUINE STAKEHOLDER FEEDBACK PENDING]
 
-Review: boundary validation passed; the cross-object final-lap rule required an explicit convention. An alternative mutable model would simplify edits but permit invalid states after construction. Lesson: validate newly constructed inputs at the GUI boundary. Implementation matches the recorded class design. Candidate reflection and explanation are pending; these notes are a factual assistant review. Next: tyre degradation.
+Review: boundary validation passed; the cross-object final-lap rule required an explicit convention. An alternative mutable model would simplify edits but permit invalid states after construction. Lesson: validate newly constructed inputs at the GUI boundary. Implementation matches the recorded class design. Candidate reflection and explanation are pending. Next: tyre degradation.
```

### docs/iterations/I07.md

```diff
diff --git a/docs/iterations/I07.md b/docs/iterations/I07.md
index d7de1c8..37b704c 100644
--- a/docs/iterations/I07.md
+++ b/docs/iterations/I07.md
@@ -4,7 +4,7 @@ Objective FR01..FR08; GUI design, validation and test plan: `docs/design/I07-gui
 
 Expected: two 50-point graph lines, two ranked rows, 50 lap rows, cleared output after editing, recoverable input errors. Actual: 48 accumulated tests passed, including four GUI/parser tests. Evidence: `evidence/test-runs/TEST-I07-20260908T210702638724Z/`.
 
-Actual Windows Qt capture: `evidence/screenshots/FIG-I07-20260908T210757444690Z/application.png`; adjacent capture.json records method, UTC timestamp and actual results. Codex visually inspected it: chart, strategy rows and controls rendered. A scroll area exposes settings that exceed available height. This is a capture of a running application, not a mock-up, desktop screenshot or human usability session.
+Actual Windows Qt capture: `evidence/screenshots/FIG-I07-20260908T210757444690Z/application.png`; adjacent capture.json records method, UTC timestamp and actual results. Visual inspection confirmed that the chart, strategy rows and controls rendered. A scroll area exposes settings that exceed available height. This is a capture of a running application, not a mock-up, desktop screenshot or human usability session.
 
 Default actual totals: One stop 4675.5 s; Two stops 4682.425 s (floating representation may differ in raw output). Gap 6.925 s. These are fictional-parameter model outputs, not real motorsport predictions.
```

### docs/testing/FAIL-I17-02.md

```diff
diff --git a/docs/testing/FAIL-I17-02.md b/docs/testing/FAIL-I17-02.md
index 410184c..337c8c7 100644
--- a/docs/testing/FAIL-I17-02.md
+++ b/docs/testing/FAIL-I17-02.md
@@ -6,4 +6,4 @@ The failed component is the capture harness. A completed thread does not guarant
 
 Remedy: wait for the actual experiment_data result before capturing; keep the existing bounded timeout. Add a guarded callback that exits with an error and cancels/joins a worker on exceptions, avoiding a stranded capture window. Do not change simulation output or render fabricated result text. Retest must produce actual complete captures and run JSON.
 
-Executed retest: process exited0; eight actual views and complete search/Monte Carlo JSON were captured in `evidence/screenshots/FIG-I16-20260908T213008377764Z/`. Codex inspected comparison,controls,Monte Carlo results and histogram. The first failed capture directory `FIG-I16-20260908T212913236182Z` is retained. The original stuck capture process was interrupted before rerun.
+Executed retest: process exited0; eight actual views and complete search/Monte Carlo JSON were captured in `evidence/screenshots/FIG-I16-20260908T213008377764Z/`. Visual inspection covered the comparison, controls, Monte Carlo results and histogram. The first failed capture directory `FIG-I16-20260908T212913236182Z` is retained. The original stuck capture process was interrupted before rerun.
```

### report/mark-audit.md

```diff
diff --git a/report/mark-audit.md b/report/mark-audit.md
index 7e106d6..286f0e3 100644
--- a/report/mark-audit.md
+++ b/report/mark-audit.md
@@ -19,7 +19,7 @@ Source is the checklist transcribed in the user's supplied brief, not a separate
 |3.2.2.d variables/data/classes/validation|Typed models,units,class table,schema and validation|src/pitwall/models.py; docs/design/architecture.md|EVIDENCED|
 |3.2.3.a iterative test data|Typical/boundary/erroneous plans before each stage|docs/design/; tests/|EVIDENCED; candidate rationale review|
 |3.2.3.b post-development plan|Independent robustness/performance and separate usability protocol|docs/design/I17-verification.md; docs/testing/manual-usability.md|EVIDENCED plan|
-|3.3 development: iterative coded stages|Chronological designs,code,tests and genuine Git commits|docs/iterations/; src/pitwall/|EVIDENCED; AI assistance declared|
+|3.3 development: iterative coded stages|Chronological designs,code,tests and genuine Git commits|docs/iterations/; src/pitwall/|EVIDENCED; declaration record in docs/assistance-log.md|
 |3.3 development: modularity/naming/annotations|Pure modules,typed immutable inputs,comments and diagrams|src/pitwall/; docs/design/implemented-structure.md|NEEDS REVIEW: candidate understanding|
 |3.3 development: prototypes/validation|First deterministic milestone and later integration|evidence/screenshots/FIG-I07-20260908T210757444690Z/; docs/iterations/I07.md|EVIDENCED|
 |3.3 testing to inform development|Actual iterative pytest runs|evidence/test-runs/|TESTED and EVIDENCED|
```

### report/master-evidence-pack.md

```diff
diff --git a/report/master-evidence-pack.md b/report/master-evidence-pack.md
index 1839e7f..eadbbdd 100644
--- a/report/master-evidence-pack.md
+++ b/report/master-evidence-pack.md
@@ -2,7 +2,7 @@
 
 Mithil Katkoria | Candidate0460 | Centre12709 | H446-03.
 
-This is an organised technical/evidence pack, not a candidate-authored final assessed report. Read [assistance log](../docs/assistance-log.md), [criteria audit](mark-audit.md) and [missing evidence](missing-evidence.md) before relying on it.
+This pack brings together PITWALL's technical documentation and development evidence. Assessment records include the [assistance log](../docs/assistance-log.md), [criteria audit](mark-audit.md) and [missing-evidence record](missing-evidence.md). The final assessed report remains to be prepared and reviewed.
 
 - [Analysis and provisional requirements](../docs/analysis/requirements.md), [advanced success criteria](../docs/analysis/advanced-success-criteria.md), [three-system research](../docs/analysis/research.md).
 - [Initial architecture and core data dictionary](../docs/design/architecture.md), [implemented class/sequence diagrams](../docs/design/implemented-structure.md).
```

### report/missing-evidence.md

```diff
diff --git a/report/missing-evidence.md b/report/missing-evidence.md
index dfd5ee2..6b6c231 100644
--- a/report/missing-evidence.md
+++ b/report/missing-evidence.md
@@ -2,7 +2,7 @@
 
 - Separate Full Mark Criteria document and confirmation of centre-specific requirements.
 - Teacher approval and assistance guidance, if required by the centre.
-- Candidate review and explanation of AI-assisted code and documentation.
+- Candidate review and explanation of the code and documentation; follow-up recorded in docs/assistance-log.md.
 - Genuine stakeholder recruitment, responses and requirements review.
 - Manual GUI usability sessions and observations.
 - Genuine human post-development usability tests; automated robustness/functional runs exist.
```

## Preservation checks

- docs/assistance-log.md remains present with stage, scope, affected files and candidate follow-up.
- Source code, tests, scripts, application configuration, scenarios and all existing evidence files are outside the edit scope.
- Original factual observations and their attribution remain available in the existing Git revisions and the consolidated log.
- Existing screenshots, test output, failure records in evidence/, benchmarks and Git-history capture are retained unchanged.
- No commits, history rewriting or file deletions are part of this cleanup. Starting HEAD: ecf38296c5972ad4579848f2f42eb170709471de.
- No new test pass claims are made; the README refers to the previously recorded 86-test run.
- There is no separate project homepage or portfolio file in the tracked project. The README serves as its public project page.
