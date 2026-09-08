"""Explicit environmental assumptions, independent of the base race configuration."""
from dataclasses import dataclass
from .events import EventQueue, RaceEvent, Weather
from .models import LapResult, number, integer
import math


@dataclass(frozen=True)
class Conditions:
    initial_weather: Weather = Weather.DRY
    events: tuple[RaceEvent, ...] = ()
    damp_penalty: float = 4.0
    wet_penalty: float = 15.0
    safety_car_penalty: float = 25.0
    safety_car_pit_factor: float = 0.5
    seed: int = 0
    variation: float = 0.0

    def __post_init__(self):
        if not isinstance(self.initial_weather, Weather):
            raise ValueError("Initial weather must be Dry, Damp or Wet")
        EventQueue(self.events, 500)
        number(self.damp_penalty, "Damp penalty")
        number(self.wet_penalty, "Wet penalty")
        number(self.safety_car_penalty, "Safety-car penalty")
        number(self.safety_car_pit_factor, "Safety-car pit factor")
        if self.safety_car_pit_factor > 1:
            raise ValueError("Safety-car pit factor must be between 0 and 1")
        integer(self.seed, "Seed", 0, 2**32 - 1)
        number(self.variation, "Variation amplitude")

    def weather_loss(self, weather: Weather) -> float:
        return {Weather.DRY: 0.0, Weather.DAMP: self.damp_penalty, Weather.WET: self.wet_penalty}[weather]


@dataclass(frozen=True)
class EnvironmentalLapResult(LapResult):
    weather: Weather = Weather.DRY
    weather_effect: float = 0.0
    safety_car: bool = False
    safety_car_effect: float = 0.0
    random_variation: float = 0.0

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.weather, Weather):
            raise ValueError("Lap weather must be valid")
        number(self.weather_effect, "Weather effect")
        if type(self.safety_car) is not bool:
            raise ValueError("Safety-car flag must be boolean")
        number(self.safety_car_effect, "Safety-car effect")
        if isinstance(self.random_variation, bool) or not isinstance(self.random_variation, (float, int)) or not math.isfinite(self.random_variation):
            raise ValueError("Random variation must be finite")
