# Iteration 13 design: A10 generation and A11 optimisation

FR12. Inputs: max stops 0..2, minimum stint >=1, pit-grid step >=1, stationary time, config and conditions. Generate compound products over Soft/Medium/Hard for each stint; combinations of eligible pit laps enforce increasing stops. Include 0-stop strategies. Grid begins at minimum stint and ends N-minimum stint. All consecutive stint lengths must satisfy the minimum, including final stint. Reject minimum stint > N.

```text
FOR stops from 0 to maximum:
    FOR increasing stop-lap combination from grid:
        IF every stint has minimum length:
            FOR every compound tuple of length stops+1:
                YIELD legal Strategy
FOR candidate:
    check candidate/work caps BEFORE simulating
    simulate and STORE candidate plus total
STABLE SORT scores by total; return scores and count
```

Caps: 10,000 candidate scores and two million lap evaluations. Abort descriptively if exceeded; never silently present a partial search as complete. Bounds stop generation before large allocation. Cancellation callback each candidate. Conditions noise is set to zero for search: result is deterministic under fixed events, not a stochastic optimum.

Time O(C*N + C log C), memory O(C*S + N); compounds contribute 3^(S+1). Candidate generation uses itertools combinations/product (explainable nested iteration). Baselines: Hard no-stop, Medium->Hard halfway when legal, Medium renewed at its recommended life up to two stops. Baselines may fall outside search grid and must be identified as separately evaluated reference rules.

Planned TEST-I13: N=3, min1, max1, grid1 yields 3+2*9=21 unique candidates; stop bounds and minimum stints; N=2 under manual config has best Soft no-stop at182.2 s; independent exhaustive candidate totals must match ranking; cap failure rather than partial answer; cancellation; zero-noise search matches input conditions replaced with amplitude0. Alternative heuristic faster but lacks complete bounded enumeration.
