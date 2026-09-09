# Evidence-based prototype evaluation

This technical review evaluates the recorded implementation and output. Candidate judgement and genuine stakeholder validation are still required. The separate centre criteria file is unavailable; this is not a completed assessed submission.

## Success criteria

| Criterion | Judgement within stated scope | Evidence and reason |
|---|---|---|
| SC01 | FULLY MET computationally | Race boundaries/invalid types in test_models and maximum comparison in test_final_robustness |
| SC02 | FULLY MET computationally | Linear wear manual examples and editable three-compound inputs |
| SC03 | FULLY MET computationally | Pit indexing, duplicate/final stops, consecutive same-compound resets tested |
| SC04 | PARTIALLY MET | Model/parser errors and GUI recovery tested; genuine users have not judged explanations |
| SC05 | FULLY MET | Explicit absolute 1e-9-second oracle passes for every lap, cumulative time and total; exact replay passes. See docs/testing/final-quality-results.md |
| SC06 | FULLY MET computationally/visually | Lap count/sum checks and actual Qt table capture |
| SC07 | FULLY MET in model | Rankings, ties, metrics and stints tested; real-world strategy validity not claimed |
| SC08 | FULLY MET for rendering | Actual Windows captures and graph-point tests; audience usability pending |
| SC09 | FULLY MET for tested schema | Exact round-trip and robust JSON checks; genuine discovered collection bug fixed/retested |
| SC10 | FULLY MET for simplified events | Queue tie tests and weather/SC arithmetic; wet tyre selection remains unsupported |
| SC11 | FULLY MET for selected uncertainties | Seed replay, fixed statistics oracle, actual trial output and1000-trial benchmark |
| SC12 | FULLY MET in constrained grid | Independent tiny exhaustive arithmetic, candidate counts and exported complete score list |
| SC13 | FULLY MET | Original search/Monte Carlo targets passed; separate five-repeat comparison timings now recorded. GUI latency and other machines remain outside these measurements. See docs/testing/final-quality-results.md |
| SC14 | PARTIALLY MET | Worker tests/cancellation and stale-input checks; genuine manual responsiveness observations pending |

Latest executed results and their evidence paths are indexed in `report/test-results.csv`. Earlier failures remain visible. Automated passing tests demonstrate their assertions, not absence of every possible bug.

## Actual performance

BENCH-01 used Windows11, Python3.14 AMD64 process on Snapdragon X10-core X1P64100, RAM16,756,006,912 bytes. Reported process architecture matters: results are specific to this environment and are not native-ARM claims.

Three-repeat means: one50-lap race0.000522s;1000 sequential races0.796304s; complete1056-candidate search1.161633s;1000 paired Monte Carlo trials2.099058s. Raw repetitions/min/max/median are preserved in `evidence/benchmarks/BENCH-01-20260908T212651988284Z/timings.json`. These measure computational work, not UI latency or memory peaks. Background machine load is uncontrolled.

## Usability judgement

Labels include units and stop/event boundaries; inputs invalidate old output; background work can be cancelled; graph and tables use real results. Actual captures confirm layout at the captured1440x960 window. Source review and automated checks do not demonstrate comprehension by intended users. The text syntax and scrollable experiment controls require genuine usability review. Human tasks remain unexecuted in `docs/testing/manual-usability.md`.

## Maintenance issues

| Issue | Actual affected architecture | Technical maintenance approach | Risk/test needed |
|---|---|---|---|
| New tyre compounds | Compound enum, RaceConfig completeness, defaults, GUI, persistence | Add explicit compound data and suitability, migrate schema if needed | Test completeness, serialization and mixed-weather behaviour |
| Changed formulas | physics.py, Conditions terms and engine | Isolate revised formula and retain versioned assumption notes | Recompute independent oracle without simply copying program output |
| New event types | RaceEvent payload validation, EventQueue, engine branches, parser/schema | Define new payload and deterministic same-lap semantics before implementation | Contradictory/same-lap and boundary-event tests |
| Schema evolution | persistence.py exact keys and version1 | Introduce explicit version2 decoder and migration from1 | Golden legacy fixtures, malformed/new field tests, no silent coercion |
| GUI growth | MainWindow/AdvancedWindow inheritance and snapshot conversion | Extract dedicated configuration/strategy panels while keeping pure model boundary | Round-trip, stale-output and keyboard/usability regressions |
| Search changes | candidates, SearchSettings, caps and baseline definitions | Compare a new heuristic against tiny exact oracle and measured exhaustive reference | Report search coverage, timing and any missed best candidate |

## Limitations and technically grounded improvements

| Limitation | Consequence | Possible implementation |
|---|---|---|
| Linear, uncalibrated degradation | Cannot predict thermal/cliff behaviour | Add optional quadratic/cliff coefficients only after empirical justification, explicit units and oracle tests |
| No wet/intermediate tyres | All dry compounds get same rain penalty | Extend Compound and per-weather suitability matrix with separate documented defaults and schema migration |
| Single-car/free-track abstraction | No traffic, overtaking or undercut interaction | Add field state and gap model as a separately evaluated extension; avoid claiming present ranking works in traffic |
| Lap-boundary events | Cannot resolve a mid-lap shower or SC deployment | Optional fractional-lap segments with explicit timing semantics and increased complexity tests |
| SC assignment model | Overlapping fixed/generated periods can override each other | Represent SC intervals with union semantics, compare against existing model and update event design |
| Shared additive noise and arbitrary SC probability | Noise alone cannot change relative pace ranking; probability is not a forecast | Introduce justified strategy-dependent uncertainties only with assumptions, paired draws and sensitivity studies |
| Grid-limited two-stop search | Better off-grid or three-stop plans may exist | Coarse-to-fine search, explicit evaluated regions and full tiny-space reference tests |
| GUI range/precision bounds and temporary runtime | Some valid API scenarios cannot load into widgets; runtime can be cleaned | Dedicated packaging, adjustable numeric precision and verified installer on target OS |

No final mark or real-world accuracy claim follows from these results. Candidate explanation, centre review and stakeholder evidence determine whether this prototype fits the assessed project.
