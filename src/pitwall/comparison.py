"""Comparison under identical conditions. Summary metrics include pit laps."""
from .engine import simulate
from .models import RaceConfig, Strategy, StrategyResult

MAX_STRATEGIES = 20


def compare(config: RaceConfig, strategies: tuple[Strategy, ...]) -> tuple[StrategyResult, ...]:
    if not 2 <= len(strategies) <= MAX_STRATEGIES:
        raise ValueError(f"Compare between 2 and {MAX_STRATEGIES} strategies")
    names = [s.name.strip().casefold() for s in strategies]
    if len(set(names)) != len(names):
        raise ValueError("Strategy names must be unique")
    return tuple(sorted((simulate(config, s) for s in strategies), key=lambda r: r.total_time))


def summary(result: StrategyResult) -> dict:
    times = [lap.lap_time for lap in result.laps]
    boundaries = [0, *(s.lap for s in result.strategy.planned_stops), len(times)]
    return {
        "name": result.strategy.name,
        "total": result.total_time,
        "stops": len(result.strategy.planned_stops),
        "average": result.total_time / len(times),
        "fastest": min(times),
        "slowest": max(times),
        "pit_loss": sum(lap.pit_loss for lap in result.laps),
        "stints": tuple(b - a for a, b in zip(boundaries, boundaries[1:])),
    }
