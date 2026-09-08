"""Deterministic chronological event queue with stable input-order ties."""
from dataclasses import dataclass
from enum import Enum
import heapq
from .models import integer


class Weather(Enum):
    DRY = "Dry"
    DAMP = "Damp"
    WET = "Wet"


class EventType(Enum):
    WEATHER_CHANGE = "Weather change"
    SAFETY_CAR_START = "Safety car start"
    SAFETY_CAR_END = "Safety car end"


@dataclass(frozen=True)
class RaceEvent:
    lap: int
    kind: EventType
    weather: Weather | None = None

    def __post_init__(self):
        integer(self.lap, "Event lap", 1)
        if not isinstance(self.kind, EventType):
            raise ValueError("Unknown event type")
        if self.kind == EventType.WEATHER_CHANGE:
            if not isinstance(self.weather, Weather):
                raise ValueError("Weather change requires Dry, Damp or Wet")
        elif self.weather is not None:
            raise ValueError("Safety-car event cannot carry weather")


class EventQueue:
    def __init__(self, events: tuple[RaceEvent, ...], laps: int):
        if not isinstance(events, tuple) or not all(isinstance(e, RaceEvent) for e in events):
            raise ValueError("Events must be a tuple of RaceEvent objects")
        for event in events:
            integer(event.lap, "Event lap", 1, laps)
        self._heap = [(event.lap, index, event) for index, event in enumerate(events)]
        heapq.heapify(self._heap)

    def at_lap(self, lap: int) -> tuple[RaceEvent, ...]:
        due = []
        while self._heap and self._heap[0][0] <= lap:
            due.append(heapq.heappop(self._heap)[2])
        return tuple(due)
