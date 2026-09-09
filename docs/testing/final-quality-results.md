# Final quality verification

SC05 focused run: evidence/test-runs/TEST-SC05-20260908T224145702053Z. One test passed. Absolute tolerance is 1e-9 seconds with no relative component. Every recorded lap and cumulative value had zero difference from its expected Python float value; this is not a claim of infinite decimal precision. The test also checks total time and deterministic replay.

Full regression: evidence/test-runs/TEST-QUALITY-FINAL-20260908T224148466396Z. All 87 collected cases passed. The old 86-case run and both I17 failing assertions remain preserved.

Comparison-only measurements: evidence/benchmarks/BENCH-COMPARE-20260908T224158666794Z/timings.json. Five repeats after one warm-up per size. Input construction and GUI drawing are excluded. No new speed threshold was invented. Raw output, environment, command and source hashes are retained.

| Strategies | Laps | Minimum s | Maximum s | Mean s | Median s |
|---|---|---|---|---|---|
| 2 | 50 | 0.000999200 | 0.001561200 | 0.001120600 | 0.001018200 |
| 20 | 50 | 0.010145800 | 0.014767600 | 0.011749560 | 0.011352200 |
| 20 | 500 | 0.153045700 | 0.179047800 | 0.161278460 | 0.157290200 |

SC05 and the missing SC13 computational evidence are now satisfied for the tested cases. SC04 and SC14 still need genuine human evidence. No application source was changed and no new feedback-driven iteration was fabricated.
