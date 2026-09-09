# Post-prototype review and next decisions

The problem is to compare complete race plans, not merely select the fastest fresh tyre. A faster compound may lose its advantage through wear or an additional pit stop. PITWALL keeps a common race configuration, evaluates each racing lap and ranks accumulated times so a user can inspect that trade-off.

Computation is useful because the same arithmetic must be applied consistently across many lap and stop combinations. Decomposition separates input validation, lap components, state transitions and result comparison. A priority queue preserves chronological events and deterministic ties. Bounded enumeration gives a checkable best plan inside an explicit search space. Seeded trials help explore variation but cannot calibrate the model by repetition alone.

The three existing-system reviews were recorded after the prototype. Their value is in reviewing scope: TUM's richer simulator highlights PITWALL's single-car simplification; FastF1 highlights the need for provenance before using real data; F1 Manager suggests clearer presentation but is not evidence for physical parameters. These findings support review exercises and possible future changes, not a rewritten claim that they created the original design. Genuine participant priorities are still required before choosing a new feature.
