# Implemented structure at the integrated prototype

This diagram reflects real classes after Iteration16, not the earlier planned diagram. The design files remain as chronological records.

```mermaid
classDiagram
  class RaceConfig
  class Circuit
  class Driver
  class TyreCompound
  class Strategy
  class PitStopPlan
  class RaceState
  class LapResult
  class EnvironmentalLapResult
  class StrategyResult
  class Conditions
  class RaceEvent
  class EventQueue
  class Scenario
  class MainWindow
  class AdvancedWindow
  class ExperimentWorker
  class SearchSettings
  class CandidateScore
  class MonteCarloResult
  class Trial
  RaceConfig *-- Circuit
  RaceConfig *-- Driver
  RaceConfig *-- TyreCompound
  Strategy *-- PitStopPlan
  StrategyResult --> Strategy
  StrategyResult *-- LapResult
  LapResult <|-- EnvironmentalLapResult
  Conditions *-- RaceEvent
  EventQueue o-- RaceEvent
  Scenario *-- RaceConfig
  Scenario *-- Conditions
  Scenario *-- Strategy
  MainWindow <|-- AdvancedWindow
  AdvancedWindow --> ExperimentWorker
  AdvancedWindow --> Scenario
  CandidateScore --> Strategy
  MonteCarloResult *-- Trial
```

RaceState is a temporary immutable state in the engine loop. SearchSettings constrains generator enumeration; CandidateScore retains candidate and total. MonteCarloResult retains trials and derived statistics. Enum definitions live in models/events; no weather/SC state is invented in earlier-stage LapResult.

```mermaid
sequenceDiagram
  actor User
  participant UI as AdvancedWindow
  participant Worker as ExperimentWorker
  participant Search as optimise
  participant Engine as simulate
  User->>UI: Optimise
  UI->>UI: Validate immutable snapshot and remember revision
  UI->>Worker: Start task
  Worker->>Search: Config, conditions, settings, cancellation callback
  loop each legal candidate within caps
    Search->>Engine: Simulate with variation zero
    Engine-->>Search: Lap results and total
  end
  Search-->>Worker: Ranked complete scores
  Worker-->>UI: Queued completed signal
  UI->>UI: Check revision, populate output and graph
```

Validation responsibility: local numeric/enum checks in models/conditions; race-dependent stops/events in engine/scenario; JSON types and exact keys in persistence; widget representability before loaded data is applied; work limits in search/Monte Carlo. Computational routines import no GUI components.

Maintenance hotspots: adding enum members affects config completeness, defaults, GUI choices, persistence decoding and tests; changing a formula requires updating the independent oracle deliberately; schema changes need version migration, not silently accepting fields; additional event states need explicit ordering semantics.
