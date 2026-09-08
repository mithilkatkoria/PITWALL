# Iteration 10 design: A08 safety car

FR10. Conditions adds safety_car_penalty (default 25 seconds/lap) and safety_car_pit_factor (default .5 in [0,1]). Both are configurable illustrative values. SC starts inactive. Start/end events before a lap toggle its state. Simultaneous commands use input order.

```text
ON SC start: active = true
ON SC end: active = false
IF active:
    pit loss = (lane loss + stationary time) * pit factor
    lap safety penalty = configured penalty
ELSE lap safety penalty = 0
ADD safety penalty and record flag and penalty
```

This models relative pit opportunity, not field bunching, speed control or race neutralisation physics. Weather/fuel/wear continue normally. O(1) additional work per lap. Planned TEST-I10: SC starts 2 ends 4, adds 25 on laps 2 and 3; stop lap 2 costs 11.25 rather than 22.5. Net change vs dry stop oracle = 50 - 11.25 = 38.75. Reject factor outside [0,1].
