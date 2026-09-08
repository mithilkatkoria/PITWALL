"""Validated immutable data. Times are seconds; lap indices are one-based."""
from dataclasses import dataclass
from enum import Enum
import math

MAX_LAPS = 500  # Bound interactive work, not a motorsport rule.


def number(value: float, name: str, positive: bool = False) -> None:
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or value < 0 or (positive and value == 0)):
        raise ValueError(f"{name} must be a finite {'positive' if positive else 'non-negative'} number")


def integer(value: int, name: str, minimum: int = 0, maximum: int | None = None) -> None:
    if type(value) is not int or value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"{name} must be an integer from {minimum} to {maximum if maximum is not None else 'unbounded'}")


def named(value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Name must be non-empty text")


class Compound(Enum):
    SOFT = "Soft"
    MEDIUM = "Medium"
    HARD = "Hard"


def compound(value: Compound) -> None:
    if not isinstance(value, Compound):
        raise ValueError("Compound must be Soft, Medium or Hard")


@dataclass(frozen=True)
class Circuit:
    name: str
    base_lap_time: float
    pit_lane_loss: float

    def __post_init__(self):
        named(self.name)
        number(self.base_lap_time, "Base lap time", positive=True)
        number(self.pit_lane_loss, "Pit-lane loss")


@dataclass(frozen=True)
class Driver:
    name: str
    pace_delta: float = 0.0

    def __post_init__(self):
        named(self.name)
        number(self.pace_delta, "Driver pace penalty")


@dataclass(frozen=True)
class TyreCompound:
    name: Compound
    base_pace_delta: float
    degradation_rate: float
    recommended_life: int

    def __post_init__(self):
        compound(self.name)
        number(self.base_pace_delta, "Tyre pace penalty")
        number(self.degradation_rate, "Degradation rate")
        integer(self.recommended_life, "Recommended life", 1)


@dataclass(frozen=True)
class PitStopPlan:
    lap: int
    compound: Compound
    stationary_time: float = 2.5

    def __post_init__(self):
        integer(self.lap, "Pit lap", 1)
        compound(self.compound)
        number(self.stationary_time, "Stationary time")


@dataclass(frozen=True)
class Strategy:
    name: str
    starting_compound: Compound
    planned_stops: tuple[PitStopPlan, ...] = ()

    def __post_init__(self):
        named(self.name)
        compound(self.starting_compound)
        if not isinstance(self.planned_stops, tuple) or not all(isinstance(s, PitStopPlan) for s in self.planned_stops):
            raise ValueError("Planned stops must be a tuple of PitStopPlan objects")
        previous = 0
        for stop in self.planned_stops:
            if stop.lap <= previous:
                raise ValueError("Pit laps must be distinct and in increasing order")
            previous = stop.lap

    def validate_for(self, config: 'RaceConfig') -> None:
        for stop in self.planned_stops:
            if stop.lap >= config.laps:
                raise ValueError(f"Pit lap {stop.lap} must be before final lap {config.laps}")


@dataclass(frozen=True)
class RaceConfig:
    laps: int
    circuit: Circuit
    driver: Driver
    tyres: tuple[TyreCompound, ...]
    initial_fuel_penalty: float = 0.0

    def __post_init__(self):
        integer(self.laps, "Race length", 1, MAX_LAPS)
        if not isinstance(self.circuit, Circuit) or not isinstance(self.driver, Driver):
            raise ValueError("Race requires a Circuit and Driver")
        if (not isinstance(self.tyres, tuple) or len(self.tyres) != len(Compound)
                or not all(isinstance(t, TyreCompound) for t in self.tyres)
                or {t.name for t in self.tyres} != set(Compound)):
            raise ValueError("Define Soft, Medium and Hard exactly once")
        number(self.initial_fuel_penalty, "Initial fuel penalty")

    def tyre(self, name: Compound) -> TyreCompound:
        compound(name)
        return next(t for t in self.tyres if t.name == name)


@dataclass(frozen=True)
class RaceState:
    completed_laps: int
    compound: Compound
    tyre_age: int
    cumulative_time: float

    def __post_init__(self):
        integer(self.completed_laps, "Completed laps")
        compound(self.compound)
        integer(self.tyre_age, "Tyre age")
        number(self.cumulative_time, "Cumulative time")


@dataclass(frozen=True)
class LapResult:
    lap_number: int
    lap_time: float
    cumulative_time: float
    compound: Compound
    tyre_age: int
    degradation_loss: float
    fuel_effect: float
    pit_stop: bool
    pit_loss: float

    def __post_init__(self):
        integer(self.lap_number, "Lap number", 1)
        integer(self.tyre_age, "Tyre age")
        compound(self.compound)
        number(self.lap_time, "Lap time", positive=True)
        for field in ("cumulative_time", "degradation_loss", "fuel_effect", "pit_loss"):
            number(getattr(self, field), field)
        if type(self.pit_stop) is not bool:
            raise ValueError("Pit stop flag must be boolean")
        if self.cumulative_time < self.lap_time:
            raise ValueError("Cumulative time cannot be less than lap time")
        if not self.pit_stop and self.pit_loss != 0:
            raise ValueError("A non-pit lap cannot have pit loss")


@dataclass(frozen=True)
class StrategyResult:
    strategy: Strategy
    laps: tuple[LapResult, ...]

    def __post_init__(self):
        if not isinstance(self.strategy, Strategy):
            raise ValueError("Result requires a Strategy")
        if not isinstance(self.laps, tuple) or not self.laps or not all(isinstance(l, LapResult) for l in self.laps):
            raise ValueError("Result requires a non-empty tuple of lap results")

    @property
    def total_time(self) -> float:
        return self.laps[-1].cumulative_time
