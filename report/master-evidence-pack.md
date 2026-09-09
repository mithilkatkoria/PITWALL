# PITWALL internal master evidence pack

Mithil Katkoria | Candidate0460 | Centre12709 | H446-03.

This pack brings together PITWALL's technical documentation and development evidence. Assessment records include the [assistance log](../docs/assistance-log.md), [criteria audit](mark-audit.md) and [missing-evidence record](missing-evidence.md). The final assessed report remains to be prepared and reviewed.

- [Analysis and provisional requirements](../docs/analysis/requirements.md), [advanced success criteria](../docs/analysis/advanced-success-criteria.md), [three-system research](../docs/analysis/research.md).
- [Initial architecture and core data dictionary](../docs/design/architecture.md), [implemented class/sequence diagrams](../docs/design/implemented-structure.md).
- [Iteration records](../docs/iterations/) preserve actual order:1,2,3,combined4/5,6,7,8,9,10,11,12,13,15,combined14/16,17.
- [Independent final checks](../tests/test_final_robustness.py), [JSON failure/fix/retest](../docs/testing/FAIL-I17-01.md), [capture harness failure/fix](../docs/testing/FAIL-I17-02.md), [planned genuine usability](../docs/testing/manual-usability.md).
- [Provisional evaluation and maintenance](../docs/evaluation/review.md), [candidate review exercises](../docs/testing/research-review-exercises.md).
- [Evidence index](evidence-index.csv) lists existing files with hashes. [Test results](test-results.csv) indexes the latest full run. [Traceability](traceability.csv) maps requirements to designs,classes,tests,evidence and evaluation.
- Source appendix: [models](../src/pitwall/models.py), [physics](../src/pitwall/physics.py), [engine](../src/pitwall/engine.py), [comparison](../src/pitwall/comparison.py), [events](../src/pitwall/events.py), [conditions](../src/pitwall/conditions.py), [Monte Carlo](../src/pitwall/monte_carlo.py), [optimiser](../src/pitwall/optimiser.py), [persistence](../src/pitwall/persistence.py), [base GUI](../src/pitwall/gui.py), [advanced GUI](../src/pitwall/advanced_gui.py).

## Algorithm index

| Algorithm | Design |
|---|---|
|A01 lap time,A03 fuel|docs/design/I03-lap.md|
|A02 degradation|docs/design/I02-tyres.md|
|A04 strategy validation|docs/design/architecture.md|
|A05 simulation|docs/design/I04-I05-engine.md|
|A06 event processing|docs/design/I08-events.md|
|A07 weather|docs/design/I09-weather.md|
|A08 safety car|docs/design/I10-safety-car.md|
|A09 comparison|docs/design/I06-comparison.md|
|A10 generation,A11 optimiser|docs/design/I13-optimiser.md|
|A12 Monte Carlo,A13 statistics|docs/design/I12-monte-carlo.md|
|A14 scenario validation|docs/design/architecture.md; docs/design/I15-persistence.md|

## Evidence interpretation

PLANNED = proposed material. IMPLEMENTED = code exists. TESTED = actual execution captured. EVIDENCED = corresponding file exists. Neither a screenshot nor a passing assertion establishes stakeholder approval, candidate understanding or real-world prediction accuracy.

Final software run:86 passing tests, with genuine earlier failures retained. Final screenshot set contains actual Windows widget captures, actual1056-candidate search and100 paired-trial output. Benchmark contains three repetitions at each documented scale. The repository has genuine current-date commits, never manufactured historical milestones. The evidence-index hashes detect later file changes; test metadata separately binds runs to source hashes.
