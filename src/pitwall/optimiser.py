"""Complete enumeration inside explicit bounded search space, never real-world optimum."""
from dataclasses import dataclass, replace
from itertools import combinations, product
from .conditions import Conditions
from .engine import simulate
from .models import Compound, PitStopPlan, RaceConfig, Strategy, integer, number

MAX_CANDIDATES = 10_000
MAX_SEARCH_LAPS = 2_000_000


@dataclass(frozen=True)
class SearchSettings:
    max_stops: int = 2
    minimum_stint: int = 5
    pit_step: int = 5
    stationary_time: float = 2.5

    def __post_init__(self):
        integer(self.max_stops, "Maximum stops", 0, 2)
        integer(self.minimum_stint, "Minimum stint", 1, 500)
        integer(self.pit_step, "Pit step", 1, 500)
        number(self.stationary_time, "Stationary time")


@dataclass(frozen=True)
class CandidateScore:
    strategy: Strategy
    total_time: float


def candidates(config: RaceConfig, settings: SearchSettings):
    if settings.minimum_stint > config.laps:
        raise ValueError("Minimum stint cannot exceed race length")
    grid = range(settings.minimum_stint, config.laps - settings.minimum_stint + 1, settings.pit_step)
    serial = 0
    for count in range(settings.max_stops + 1):
        for stops in combinations(grid, count):
            bounds = (0, *stops, config.laps)
            if any(b-a < settings.minimum_stint for a,b in zip(bounds, bounds[1:])):
                continue
            for compounds in product(Compound, repeat=count + 1):
                serial += 1
                yield Strategy(f"Candidate {serial}", compounds[0], tuple(
                    PitStopPlan(lap, tyre, settings.stationary_time) for lap,tyre in zip(stops, compounds[1:])))


def optimise(config: RaceConfig, conditions: Conditions, settings: SearchSettings,
             cancelled=lambda: False) -> tuple[CandidateScore, ...]:
    scores = []
    deterministic = replace(conditions, variation=0)
    for candidate in candidates(config, settings):
        if cancelled():
            raise InterruptedError("Search cancelled")
        count = len(scores) + 1
        if count > MAX_CANDIDATES or count * config.laps > MAX_SEARCH_LAPS:
            raise ValueError("Search exceeds work limit. Increase pit step/minimum stint or reduce maximum stops.")
        scores.append(CandidateScore(candidate, simulate(config, candidate, deterministic).total_time))
    return tuple(sorted(scores, key=lambda s: s.total_time))


def baselines(config: RaceConfig, conditions: Conditions, stationary: float = 2.5) -> tuple[CandidateScore, ...]:
    plans = [Strategy("Baseline: Hard no-stop", Compound.HARD)]
    if config.laps > 1:
        plans.append(Strategy("Baseline: halfway", Compound.MEDIUM,
                              (PitStopPlan(config.laps//2, Compound.HARD, stationary),)))
    life = config.tyre(Compound.MEDIUM).recommended_life
    stops = tuple(PitStopPlan(lap, Compound.MEDIUM, stationary) for lap in (life, 2*life) if lap < config.laps)
    plans.append(Strategy("Baseline: recommended life (max 2 stops)", Compound.MEDIUM, stops))
    return tuple(CandidateScore(s, simulate(config, s, replace(conditions, variation=0)).total_time) for s in plans)
