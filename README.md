# PITWALL

**Motorsport Race Strategy Simulation and Optimisation System**

OCR A Level Computer Science H446-03 project. Candidate Mithil Katkoria,0460. Centre12709.

PITWALL is a working Python/PySide6 desktop prototype with a deterministic race model, tyre/fuel/pit effects, multi-strategy comparison, event-driven weather and safety car, seeded variation, paired Monte Carlo, bounded strategy search, JSON scenarios and actual-output charts.

This is AI-assisted coursework development. See [assistance log](docs/assistance-log.md). Candidate review, explanation, genuine stakeholder work and centre requirements remain outstanding. No guaranteed mark is claimed.

## Run on this machine

Open PowerShell in this directory and run:

```powershell
.\launch.ps1
```

The working runtime is currently `%TEMP%\pitwall-0460-venv`. It avoids a Windows long-path installation failure in the deeply nested workspace. Temporary directories can be cleaned by Windows. The local `.venv` contains an incomplete GUI dependency installation; recreate a short runtime if the working one disappears.

## Recreate the environment

Use Python3.14 as tested, and a short environment location on Windows:

```powershell
python -m venv "$env:TEMP\pitwall-0460-venv"
& "$env:TEMP\pitwall-0460-venv\Scripts\python.exe" -m pip install -r requirements-lock.txt
& "$env:TEMP\pitwall-0460-venv\Scripts\python.exe" main.py
```

`requirements-lock.txt` records the actually installed versions. `requirements.txt` records the supported dependency ranges. Python3.10+ syntax is used, but other Python/OS combinations have not been verified.

## Use

1. Configure laps, base pace, pit loss, fuel and tyre penalties. Parameters are illustrative, not telemetry.
2. Edit strategy rows. Stop syntax `15:Medium, 35:Hard`; blank means no stop. Optional service override: `25:Hard:3.0`. Stops occur **after** their racing lap; new tyres run the next lap.
3. Select a row and simulate, or compare all rows. Inspect graph, summary and every-lap tabs. Editing inputs clears old results.
4. Conditions & experiments contains weather/events, seed/noise, Monte Carlo and search controls. Scroll this tab to reach experiment actions.
5. Event syntax: `10:Wet, 15:SC_START, 18:SC_END, 25:Dry`. Events occur **before** the lap. Same-lap commands use input order.
6. Monte Carlo uses the first two rows with common per-trial conditions. Search ignores noise, uses fixed events, and reports the best strategy in its bounded grid. Cancel long runs with CANCEL RUN.
7. SAVE/LOAD stores race scenarios. EXPORT RUN stores complete search scores or Monte Carlo trials and inputs. Example scenarios are in `scenarios/`.

Model and limits: linear wear; fuel penalty decreases to zero; single-car model; only dry compounds; weather penalties equal across compounds; SC changes lap penalty and relative pit loss without field bunching. No FIA compound rules or real-world calibration. Search maximum2 stops,10,000 candidates/two million lap evaluations; race1..500 laps; comparison2..20; Monte Carlo1..1000 trials (GUI100/500/1000). Oversized search fails explicitly. Generated SC commands can overlap fixed commands, which are simple state assignments.

GUI numeric inputs use three decimal places and finite ranges. Loading out-of-range or more precise parameters fails before altering inputs. Research findings and limitations are documented rather than hidden.

## Verification and evidence

```powershell
& "$env:TEMP\pitwall-0460-venv\Scripts\python.exe" scripts/run_tests.py TEST-LOCAL
& "$env:TEMP\pitwall-0460-venv\Scripts\python.exe" scripts/benchmark.py
```

The test runner preserves stdout/stderr,JUnit XML, command, environment and source hashes in a unique directory. Failed runs remain preserved. Benchmark output contains raw timings and machine details. GUI captures come from actual running Qt widgets and are labelled automated captures, not human usability evidence.

Final verified run: **86 tests passed**. Earlier genuine failures and retests are retained. Git attributes preserve exact bytes to keep source/evidence hashes meaningful across Windows checkouts. Rebuild indexes after new evidence with `scripts/build_index.py` using the same Python runtime.

Start with [master evidence pack](report/master-evidence-pack.md), [criteria audit](report/mark-audit.md), [missing evidence](report/missing-evidence.md) and [iteration records](docs/iterations/). Genuine commits are in this directory's independent Git repository. Existing workspace projects were not edited.
