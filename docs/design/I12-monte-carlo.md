# Iteration 12 design: A12 Monte Carlo and A13 statistics

FR11. Input: two distinct strategies, config, conditions, run count 1..1000 (GUI 100/500/1000), safety-car occurrence probability [0,1], duration >=1. Work cap two million racing laps per request. Store per-trial seed, generated SC lap or None, and paired totals. Summary: mean, median, population standard deviation, min, max, A-win probability and tie probability. Ties use absolute 1e-9 second tolerance to avoid floating noise.

```text
validate inputs and both strategies before loop
scheduler = independent Random(master seed)
FOR trial:
    draw trial seed
    with configured probability, draw SC start uniformly in [1,N]
    append generated SC start/end to fixed events (generated ties come last)
    simulate A and B using identical trial conditions
    store both totals and seed and generated start
summarise samples; count wins and ties; return audit data
```

No generated rain initially: fixed weather schedule remains reproducible. Common lap disturbances alone cancel; random SC timing changes relative pit opportunity. Generated SC may overlap fixed SC events: all commands are assignments in documented order, not independently stacked safety-car periods. GUI/user documentation must state this limitation.

O(R*(N+E log E)), O(R+N+E) working space by discarding full lap results after each total. Cancellation callback checked each trial. Alternative independent noise would create ranking variability from unrelated draws; common conditions chosen for fair pairing.

Planned TEST-I12: stats [1,2,3] mean/median 2, population SD sqrt(2/3), min1/max3; zero-uncertainty repeated totals; seed exact replay including SC events; identical strategies tie probability1 even with noise; invalid counts/probability/work rejected; count100 actual smoke before larger benchmark counts.
