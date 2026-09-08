# Provisional OCR/centre criteria audit

Source is the checklist transcribed in the user's supplied brief, not a separately received Full Mark Criteria document. No marks or full compliance are asserted. EVIDENCED means an artefact exists for that aspect; it does not mean a teacher has accepted its quality or authorship.

| Criterion | Current evidence | Evidence file | Status and outstanding review |
|---|---|---|---|
|3.1.1.a problem/justification|Strategy trade-offs and computational problem|docs/analysis/requirements.md|NEEDS REVIEW: candidate justification|
|3.1.1.b computational methods|Abstraction,decomposition,iteration,selection,visualisation|docs/analysis/requirements.md|NEEDS REVIEW: candidate explanation|
|3.1.2 stakeholders|Categories and questions; no responses|docs/testing/manual-usability.md|PLANNED: genuine stakeholder work required|
|3.1.3.a three systems|Three cited reviews with decisions and honest research timing|docs/analysis/research.md|NEEDS REVIEW: candidate depth and centre expectations|
|3.1.3.b essential features|FR01..FR12 table|docs/analysis/requirements.md|EVIDENCED: provisional brief source|
|3.1.3.c limitations|Initial and implemented limitations|docs/evaluation/review.md|EVIDENCED: review with stakeholders|
|3.1.4.a hardware/software|Runtime instructions,justifications,actual benchmark machine|README.md; evidence/benchmarks/BENCH-01-20260908T212651988284Z/timings.json|NEEDS REVIEW: target-user hardware untested|
|3.1.4.b success criteria|SC01..SC14 measurable conditions|docs/analysis/requirements.md; docs/analysis/advanced-success-criteria.md|NEEDS REVIEW: stakeholder approval|
|3.2.1 problem decomposition|Problem before solution components|docs/design/architecture.md|EVIDENCED|
|3.2.2.a solution structure|Planned and actual diagrams|docs/design/implemented-structure.md|EVIDENCED|
|3.2.2.b algorithms|A01..A14 distributed across dated iteration designs|docs/design/architecture.md; docs/design/I13-optimiser.md; report/master-evidence-pack.md|NEEDS REVIEW: candidate defence and diagram detail|
|3.2.2.c usability design|Labels,validation,stale-state clearing,worker model|docs/design/I07-gui.md; docs/design/I14-I16-interface.md|EVIDENCED design; human review pending|
|3.2.2.d variables/data/classes/validation|Typed models,units,class table,schema and validation|src/pitwall/models.py; docs/design/architecture.md|EVIDENCED|
|3.2.3.a iterative test data|Typical/boundary/erroneous plans before each stage|docs/design/; tests/|EVIDENCED; candidate rationale review|
|3.2.3.b post-development plan|Independent robustness/performance and separate usability protocol|docs/design/I17-verification.md; docs/testing/manual-usability.md|EVIDENCED plan|
|3.3 development: iterative coded stages|Chronological designs,code,tests and genuine Git commits|docs/iterations/; src/pitwall/|EVIDENCED; AI assistance declared|
|3.3 development: modularity/naming/annotations|Pure modules,typed immutable inputs,comments and diagrams|src/pitwall/; docs/design/implemented-structure.md|NEEDS REVIEW: candidate understanding|
|3.3 development: prototypes/validation|First deterministic milestone and later integration|evidence/screenshots/FIG-I07-20260908T210757444690Z/; docs/iterations/I07.md|EVIDENCED|
|3.3 testing to inform development|Actual iterative pytest runs|evidence/test-runs/|TESTED and EVIDENCED|
|3.3 failed tests/remedial action|Two real failed assertions,fixed and rerun|docs/testing/FAIL-I17-01.md|EVIDENCED; no manufactured failures|
|3.4.1 post-development testing|Independent robustness checks,full regression,benchmark|tests/test_final_robustness.py; docs/iterations/I17.md|NEEDS REVIEW: genuine usability tests missing|
|3.4.2 success of solution|Provisional criterion judgements with references|docs/evaluation/review.md|NEEDS REVIEW: candidate evaluation|
|3.4.3 usability features|Real captures and automated checks|evidence/screenshots/FIG-I16-20260908T213427339706Z/|NEEDS REVIEW: audience success not established|
|3.4.4 maintenance/limitations|Six maintenance issues,eight limitations with consequences|docs/evaluation/review.md|NEEDS REVIEW: candidate technical judgement|
|3.4.4.b improvements|Technical changes tied to actual architecture|docs/evaluation/review.md|NEEDS REVIEW: priorities from genuine feedback|

The brief gives15 development and10 testing marks but no full3.3 subcriterion numbering; do not invent exact codes. Update this audit against the actual centre document when received. The final assessed submission is not generated automatically from this audit.
