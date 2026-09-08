# Iteration 2 design: A02 tyre degradation

Requirement FR02; SC02. Purpose: return wear loss in seconds from a tyre's degradation rate and completed racing laps on that set.

Inputs: TyreCompound, integer age >= 0. Output: non-negative finite seconds. Structure: scalar arithmetic, no stored state.

```text
REQUIRE age is a non-negative integer
loss = tyre.degradation_rate * age
REQUIRE loss is finite
RETURN loss
```

O(1) time and space. Linear model selected over quadratic/cliff alternatives because the current milestone has no empirical reason for complexity. Fresh tyre age is zero. Recommended life does not force a cliff.

Planned TEST-I02: rate .2 at ages 0, 1, 3 gives 0, .2, .6; zero-rate tyre remains zero; reject -1, fractional and boolean ages. Later engine tests must demonstrate resetting age after a stop.
