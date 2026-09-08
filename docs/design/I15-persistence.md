# Iteration 15 design: JSON persistence and A14 scenario validation

FR09. Order change: persistence before final GUI/charts so save/load integrates once. Scenario schema version1 stores config, all tyre inputs, driver/circuit names, conditions including seed and events, and1..20 strategies including each stop's stationary time. Search/Monte Carlo run controls are not part of the racing scenario; their result audit records will retain them separately.

Use dataclass-to-dict and explicit Enum values. Decode only exact expected fields, then construct validated dataclasses and validate all strategies/events against race length. Reject bool schema versions, unsupported versions, duplicate JSON keys, missing/extra fields, nonfinite JSON constants, files over1MiB and too many strategies/events. Max500 events. No pickle or executable objects.

```text
SAVE: validate scenario; encode JSON with nonfinite values disabled
write sibling temporary file; atomically replace requested destination
LOAD: check byte size; parse JSON rejecting duplicates/nonfinite
check schema version and exact keys recursively
construct and validate typed objects
return complete Scenario only after all checks pass
```

Atomic write reduces partial-save risk. Destination replacement is only through user-selected save or explicit scripting. O(file bytes + event count + stop count). Alternative database unnecessary for small portable scenarios.

Planned TEST-I15: exact round-trip includes events, seed, compounds and stop service time; malformed JSON, missing keys, duplicate keys, bad version, NaN, negative length, unsupported compound, duplicate stops, event after race, oversized file rejected; failed load cannot modify live GUI state.
