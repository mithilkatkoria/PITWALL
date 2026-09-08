# Iteration 3 design: A01 lap time and A03 fuel

Requirements FR05, FR06. Inputs: validated RaceConfig, lap index, current tyre, tyre age and pit loss. Output: lap time plus wear and fuel components. No random terms.

```text
REQUIRE lap in [1, race.laps]
IF race.laps = 1 THEN fuel = 0
ELSE fuel = initial_fuel_penalty * (race.laps - lap) / (race.laps - 1)
wear = A02(tyre, age)
time = base_lap_time + driver_penalty + tyre_pace_penalty + wear + fuel + pit_loss
REQUIRE time is finite and positive
RETURN time, wear, fuel
```

Fuel is an illustrative time penalty decreasing linearly from the configured first-lap amount to zero on the final lap. The one-lap boundary uses zero. This abstracts consumed fuel without mass or burn-rate calibration. O(1) time/space.

Planned tests TEST-I03: 5 laps, initial 2 gives fuel 2, 1.5, 1, .5, 0; 1 lap gives zero; invalid lap rejected. Base 90, driver 0, Soft pace 0, age 3 at .2, lap 2 fuel 1.5, pit 22.5 yields 114.6. Negative pit loss rejected. Alternative physical mass model is deferred.
