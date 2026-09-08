"""Deterministic race loop. Stops occur after racing the specified lap."""
from .models import LapResult, RaceConfig, RaceState, Strategy, StrategyResult
from .physics import lap_time


def simulate(config: RaceConfig, strategy: Strategy) -> StrategyResult:
    strategy.validate_for(config)
    stops = {stop.lap: stop for stop in strategy.planned_stops}
    state = RaceState(0, strategy.starting_compound, 0, 0.0)
    results = []
    for lap in range(1, config.laps + 1):
        stop = stops.get(lap)
        pit_loss = config.circuit.pit_lane_loss + stop.stationary_time if stop else 0.0
        time, wear, fuel = lap_time(config, config.tyre(state.compound), state.tyre_age, lap, pit_loss)
        cumulative = state.cumulative_time + time
        results.append(LapResult(lap, time, cumulative, state.compound,
                                 state.tyre_age, wear, fuel, stop is not None, pit_loss))
        state = RaceState(lap, stop.compound if stop else state.compound,
                          0 if stop else state.tyre_age + 1, cumulative)
    return StrategyResult(strategy, tuple(results))
