# Iteration 8 design: A06 event queue

FR10. Implement the event data/queue separately before integration. Event types WEATHER_CHANGE, SAFETY_CAR_START, SAFETY_CAR_END. Weather states DRY, DAMP, WET. Input event: lap, type, optional weather value only for weather change. Queue key `(lap, input_sequence)` ensures chronological processing and deterministic same-lap ordering. Events apply before racing their lap, unlike pit stops which occur at the end.

```text
FOR each event with input index:
    REQUIRE lap between 1 and race length
    REQUIRE correctly typed event payload
    PUSH (lap, input index, event) into heap
WHILE heap not empty:
    POP smallest key and yield event
```

O(E log E) time, O(E) space. A sorted list would be simpler for static events; heap is chosen to support later dynamically scheduled events. Same-lap contradictory commands are applied in supplied order (last command determines state), documented rather than silently prioritised. Redundant SC starts/ends are idempotent state assignments.

Planned TEST-I08: unordered laps yield chronological order; ties preserve input sequence; lap 0/after race, invalid event type, wrong or missing weather payload rejected. Empty queue yields no events.
