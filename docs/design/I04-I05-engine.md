# Iterations 4 and 5 design: pit integration and A05 race engine

Requirements FR03..FR06. These iterations are combined because applying a stop and verifying its following-lap effect requires a lap loop. The planned order is otherwise retained. Data: validated config and strategy, stop lookup by lap, RaceState and list of LapResult.

```text
VALIDATE strategy against race
INDEX stops by lap
state = completed 0, starting compound, age 0, time 0
FOR lap = 1 TO race length
    stop = lookup stop for lap, if any
    pit_loss = lane loss + stationary time IF stop ELSE 0
    time, wear, fuel = A01(config, current tyre, age, lap, pit_loss)
    cumulative = state time + time
    APPEND LapResult using the tyre and age that ran this lap
    IF stop THEN next compound = stop compound AND next age = 0
    ELSE next compound = current compound AND next age = age + 1
    state = lap, next compound, next age, cumulative
RETURN StrategyResult
```

Time O(N+S), space O(N+S). Immutable state chosen for clear transitions, mutable state is a possible allocation optimisation only if measured. No events exist at this stage.

## Independent manual oracle TEST-I05

Five laps, base 90, initial fuel penalty 2, lane loss 20, stationary 2.5. Soft pace 0/wear .2; Hard pace 1/wear .05. Stop after lap 2.

| Lap | Racing compound | Age | Wear | Fuel | Pit | Lap time | Cumulative |
|---|---|---|---|---|---|---|---|
| 1 | Soft | 0 | 0 | 2 | 0 | 92 | 92 |
| 2 | Soft | 1 | .2 | 1.5 | 22.5 | 114.2 | 206.2 |
| 3 | Hard | 0 | 0 | 1 | 0 | 92 | 298.2 |
| 4 | Hard | 1 | .05 | .5 | 0 | 91.55 | 389.75 |
| 5 | Hard | 2 | .1 | 0 | 0 | 91.1 | 480.85 |

These are hand-derived expected values, not executed output. No-stop Soft expected 92, 91.7, 91.4, 91.1, 90.8 = 457.0 seconds.

Planned tests: manual oracle; repeated identical runs; immutable config; zero-stop one-lap race; first and penultimate lap stops; consecutive stops with same compound; invalid final stop; zero pit loss; 500-lap output count; total equals sum. Extreme finite inputs that overflow must fail descriptively rather than return infinity.
