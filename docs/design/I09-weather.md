# Iteration 9 design: A07 weather integration

FR10. Add Conditions: initial weather, immutable events, damp penalty 4 s, wet penalty 15 s (configurable illustrative assumptions, not measured data). All currently supported tyres are dry compounds. Wet/intermediate compounds remain optional and unimplemented, so wet weather penalises all dry tyres equally. This limits wet-weather strategy differentiation and must be visible in evaluation.

Add EnvironmentalLapResult extending LapResult with weather and weather_effect. Existing deterministic callers retain defaults and the same totals.

```text
initial weather = configured state
BEFORE each lap: consume queue events; for weather change, assign new weather
penalty = 0 if Dry, configured damp penalty if Damp, configured wet penalty if Wet
ADD penalty to lap time before cumulative update
RECORD effective weather and penalty
```

O(N + E log E) time with constant-size weather lookup; O(N+E) space. Alternative compound-specific wet suitability deferred until additional tyre types are justified. Planned TEST-I09: rain on lap 2, dry on lap 4 adds [0,15,15,0,0] to dry baseline; initial damp adds 4 each lap; same-lap wet then dry gives dry; event after race rejected. Dry regression total must remain identical.
