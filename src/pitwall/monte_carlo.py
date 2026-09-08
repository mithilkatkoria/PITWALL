"""Paired Monte Carlo with replayable seeds and optional safety-car occurrence."""
from dataclasses import dataclass, replace
import math
import random
import statistics
from .conditions import Conditions
from .engine import simulate
from .events import RaceEvent, EventType
from .models import RaceConfig, Strategy, integer, number

MAX_TRIALS = 1000
MAX_LAP_EVALUATIONS = 2_000_000


def describe(values: tuple[float, ...]) -> dict[str, float]:
    if not values:
        raise ValueError("Statistics require at least one sample")
    for value in values:
        number(value, "Sample")
    return {"mean": statistics.mean(values), "median": statistics.median(values),
            "stdev": statistics.pstdev(values), "minimum": min(values), "maximum": max(values)}


@dataclass(frozen=True)
class Trial:
    seed: int
    safety_car_start: int | None
    a_total: float
    b_total: float


@dataclass(frozen=True)
class MonteCarloResult:
    trials: tuple[Trial, ...]
    a_statistics: dict[str, float]
    b_statistics: dict[str, float]
    a_win_probability: float
    tie_probability: float


def monte_carlo(config: RaceConfig, a: Strategy, b: Strategy, conditions: Conditions,
                runs: int = 100, sc_probability: float = 0.0, sc_duration: int = 3,
                cancelled=lambda: False) -> MonteCarloResult:
    integer(runs, "Monte Carlo count", 1, MAX_TRIALS)
    integer(sc_duration, "Safety-car duration", 1, 500)
    number(sc_probability, "Safety-car probability")
    if sc_probability > 1:
        raise ValueError("Safety-car probability must be between 0 and 1")
    if runs * config.laps * 2 > MAX_LAP_EVALUATIONS:
        raise ValueError("Monte Carlo work limit exceeded")
    if a.name.strip().casefold() == b.name.strip().casefold():
        raise ValueError("Monte Carlo strategy names must be unique")
    a.validate_for(config)
    b.validate_for(config)
    scheduler = random.Random(conditions.seed)
    trials = []
    for _ in range(runs):
        if cancelled():
            raise InterruptedError("Monte Carlo cancelled")
        seed = scheduler.randrange(2**32)
        start = scheduler.randint(1, config.laps) if scheduler.random() < sc_probability else None
        events = list(conditions.events)
        if start is not None:
            events.append(RaceEvent(start, EventType.SAFETY_CAR_START))
            if start + sc_duration <= config.laps:
                events.append(RaceEvent(start + sc_duration, EventType.SAFETY_CAR_END))
        trial_conditions = replace(conditions, seed=seed, events=tuple(events))
        trials.append(Trial(seed, start, simulate(config, a, trial_conditions).total_time,
                            simulate(config, b, trial_conditions).total_time))
    ties = sum(math.isclose(t.a_total, t.b_total, rel_tol=0, abs_tol=1e-9) for t in trials)
    wins = sum(t.a_total < t.b_total and not math.isclose(t.a_total, t.b_total, rel_tol=0, abs_tol=1e-9) for t in trials)
    return MonteCarloResult(tuple(trials), describe(tuple(t.a_total for t in trials)),
                            describe(tuple(t.b_total for t in trials)), wins / runs, ties / runs)
