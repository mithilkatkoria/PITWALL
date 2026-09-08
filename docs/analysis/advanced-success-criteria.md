# Advanced acceptance criteria

These criteria consolidate the measurable conditions recorded before implementation in I08..I17 designs. Stakeholder approval is pending. They do not replace the earlier first-milestone criteria.

| ID | Requirement | Measurable criterion | Justification | Planned evidence |
|---|---|---|---|---|
| SC09 | FR09 | Exact scenario round-trip with seed/events/stop service; reject wrong schema, malformed data and collection types | Repeatable portable inputs | Persistence and final robustness tests |
| SC10 | FR10 | Events chronological; ties input-ordered; wet increments30s and SC manual result519.6s in documented five-lap examples | Verify state effects independently | Event and condition tests |
| SC11 | FR11 | Same seed reproduces full trials; summary oracle [1,2,3] correct;100 actual paired trials; count0/1001 rejected | Reproducible bounded uncertainty | Monte Carlo tests and benchmark |
| SC12 | FR12 | N3/max1 space contains21 unique plans; tiny winner182.2s; independent4-lap score distribution matches; report complete candidate count | Verify search coverage and scoring | Optimiser/final tests and exported search |
| SC13 | FR11/FR12 | Recorded machine default search <10s and1000 paired50-lap trials <30s (three repeats) | Usable bounded interactive workloads | Real BENCH-01 |
| SC14 | FR09..FR12 | Background task returns results; old-input results discarded; cancellation callback honoured; GUI data round-trip exact | Protect responsiveness and result provenance | GUI integration and cancellation tests |

The first13 criteria are computational/visual checks. SC14 needs additional genuine manual responsiveness and cancellation observations before usability is judged fully met. Working widgets are not automatically usable for the intended audience.
