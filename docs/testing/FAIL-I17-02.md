# FAIL-I17-02: automated capture result-delivery timing

Actual `scripts/capture_advanced.py` execution raised `RuntimeError: Running. You can cancel; editing inputs discards this run's displayed result.` at line61. The script checked `worker.isRunning()` and assumed the queued result had already arrived. It had not. Initial four actual screenshots and capture metadata remain in the first FIG-I16 directory. Tool output remains in this task; this record transcribes the actual message rather than inventing a test result.

The failed component is the capture harness. A completed thread does not guarantee its queued GUI signal has been processed. The earlier automated integration test explicitly processed events after thread completion; this script lacked that synchronisation.

Remedy: wait for the actual experiment_data result before capturing; keep the existing bounded timeout. Add a guarded callback that exits with an error and cancels/joins a worker on exceptions, avoiding a stranded capture window. Do not change simulation output or render fabricated result text. Retest must produce actual complete captures and run JSON.

Executed retest: process exited0; eight actual views and complete search/Monte Carlo JSON were captured in `evidence/screenshots/FIG-I16-20260908T213008377764Z/`. Visual inspection covered the comparison, controls, Monte Carlo results and histogram. The first failed capture directory `FIG-I16-20260908T212913236182Z` is retained. The original stuck capture process was interrupted before rerun.
