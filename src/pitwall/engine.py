"""Deterministic race loop. Stops occur after racing the specified lap."""
from .models import LapResult, RaceConfig, RaceState, Strategy, StrategyResult
from .physics import lap_time
from .conditions import Conditions, EnvironmentalLapResult
from .events import EventQueue, EventType
import random


def simulate(config: RaceConfig, strategy: Strategy, conditions: Conditions | None = None) -> StrategyResult:
    strategy.validate_for(config)
    conditions = conditions or Conditions()
    if conditions.variation >= config.circuit.base_lap_time:
        raise ValueError("Variation amplitude must be below base lap time")
    rng = random.Random(conditions.seed)
    queue = EventQueue(conditions.events, config.laps)
    weather = conditions.initial_weather
    safety_car = False
    stops = {stop.lap: stop for stop in strategy.planned_stops}
    state = RaceState(0, strategy.starting_compound, 0, 0.0)
    results = []
    for lap in range(1, config.laps + 1):
        for event in queue.at_lap(lap):
            if event.kind == EventType.WEATHER_CHANGE:
                weather = event.weather
            elif event.kind == EventType.SAFETY_CAR_START:
                safety_car = True
            elif event.kind == EventType.SAFETY_CAR_END:
                safety_car = False
        stop = stops.get(lap)
        pit_loss = config.circuit.pit_lane_loss + stop.stationary_time if stop else 0.0
        if safety_car:
            pit_loss *= conditions.safety_car_pit_factor
        time, wear, fuel = lap_time(config, config.tyre(state.compound), state.tyre_age, lap, pit_loss)
        weather_loss = conditions.weather_loss(weather)
        safety_loss = conditions.safety_car_penalty if safety_car else 0.0
        noise = rng.uniform(-conditions.variation, conditions.variation) if conditions.variation else 0.0
        time += weather_loss + safety_loss + noise
        cumulative = state.cumulative_time + time
        results.append(EnvironmentalLapResult(lap, time, cumulative, state.compound,
                                 state.tyre_age, wear, fuel, stop is not None, pit_loss,
                                 weather, weather_loss, safety_car, safety_loss, noise))
        state = RaceState(lap, stop.compound if stop else state.compound,
                          0 if stop else state.tyre_age + 1, cumulative)
    return StrategyResult(strategy, tuple(results))
