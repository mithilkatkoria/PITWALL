# FAIL-I17-01: empty JSON objects accepted as arrays

Observed during actual final robustness execution on2026-09-08. Evidence saved BEFORE remedial changes: `evidence/test-runs/TEST-I17-ROBUSTNESS-20260908T212523289799Z/` (2 failed,3 passed; output,JUnit,source hashes).

Input: replace `conditions.events` or a strategy's `planned_stops` JSON array with `{}`. Expected: ValueError for incorrect collection type. Actual: loader iterated zero dictionary keys and accepted an empty tuple. This is a genuine decoder bug, not an intentionally introduced failure. It was identified by review and reproduced through new adversarial tests.

Root cause: exact dictionary field checks validated each element but did not validate the container type before iteration. An empty invalid container therefore never reached element checks.

Options: (1) explicit JSON-array guard at each collection boundary; (2) introduce a schema-validation dependency; (3) accept any iterable. Selected1 because the schema is small, keeps dependencies minimal and rejects data outside the documented contract. Option3 would preserve the bug's ambiguity.

Planned remedy: helper requiring list with explicit name, used for tyres,events,strategies,planned_stops. Planned retest: unchanged failing cases plus complete regression. Design impact: make collection validation explicit before element validation. Retest results will be added after execution.
