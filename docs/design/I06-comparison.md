# Iteration 6 design: A09 comparison

Requirements FR07/SC07. Input: one RaceConfig and 2..20 distinct-named strategies. Output: results ranked by ascending total time, stable input order for exact ties. Limit 20 is an interactive application bound, not a motorsport rule.

```text
REQUIRE 2..20 strategies and unique names ignoring case and surrounding spaces
FOR each strategy: simulate using the same config
STABLE SORT results by total time
FOR each result:
    average = total / lap count
    fastest = minimum lap time
    slowest = maximum lap time
    total pit loss = sum of recorded pit loss
    stint lengths = successive differences of [0, stop laps..., race length]
RETURN sorted results with summaries
```

O(K*N + K log K) time and O(K*N) result space. All lap summary metrics include pit laps; UI must say so. Alternative median racing-lap metric is deferred. Expected TEST-I06: manual Soft 457.0 beats manual pit strategy 480.85 by 23.85; average Soft 91.4; fastest 90.8; slowest 92; stint lengths [2,3]; equal strategies retain input order; duplicate names and too few/many strategies rejected.
