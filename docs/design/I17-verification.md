# Iteration17 plan: robustness, performance and independent final checks

Do not invent failures. The runner preserves every executed result with timestamp and source hashes before a fix.

Separate post-development tests will use different inputs from iterative tests: malformed collection types in JSON; bool and nonfinite settings; 500-lap completed comparison; 20-strategy limit; independent small exhaustive search oracle; random SC replay by reconstructing one trial; stale worker output rejection; complete advanced GUI capture with actual results. These are automated final checks, not human usability tests.

Performance: record Python/OS/CPU/RAM and raw perf_counter trials for one race,100/500/1000 sequential races,10/100/1000 candidate-scoring prefixes and full default search,100/500/1000 paired Monte Carlo trials. Three measured repeats each after one single-race warm-up. Include minimum,maximum,mean,median. Prefix scoring benchmarks measure throughput, not completed optimisation. Timings include Python result construction and omit GUI rendering. Machine workload/power may vary; no cross-machine guarantee.

Prospective target for this development machine: default comparison <1s, default bounded search <10s and1000 paired50-lap trials <30s; evaluate only after measurement. Cancellation should return promptly between laps/candidates/trials; no hard real-time guarantee. No5000-trial option until tested and justified.
