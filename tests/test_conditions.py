from dataclasses import replace
import pytest
from pitwall.conditions import Conditions
from pitwall.engine import simulate
from pitwall.events import RaceEvent, EventType, Weather
from pitwall.models import Strategy, Compound, PitStopPlan


def test_weather_transitions(config):
    strategy = Strategy("A", Compound.SOFT)
    dry = simulate(config, strategy)
    conditions = Conditions(events=(RaceEvent(2, EventType.WEATHER_CHANGE, Weather.WET),
                                    RaceEvent(4, EventType.WEATHER_CHANGE, Weather.DRY)))
    wet = simulate(config, strategy, conditions)
    assert [b.lap_time-a.lap_time for a,b in zip(dry.laps, wet.laps)] == pytest.approx([0,15,15,0,0])
    assert wet.total_time == pytest.approx(dry.total_time + 30)
    damp = simulate(config, strategy, Conditions(initial_weather=Weather.DAMP))
    assert damp.total_time == pytest.approx(dry.total_time + 20)


def test_weather_ties(config):
    events = (RaceEvent(1, EventType.WEATHER_CHANGE, Weather.WET),
              RaceEvent(1, EventType.WEATHER_CHANGE, Weather.DRY))
    assert all(l.weather == Weather.DRY for l in simulate(config, Strategy("A", Compound.SOFT), Conditions(events=events)).laps)
    with pytest.raises(ValueError, match="Event lap"):
        simulate(config, Strategy("A", Compound.SOFT), Conditions(events=(replace(events[0], lap=6),)))


def test_safety_car_manual(config):
    strategy = Strategy("A", Compound.SOFT, (PitStopPlan(2, Compound.HARD),))
    conditions = Conditions(events=(RaceEvent(2, EventType.SAFETY_CAR_START), RaceEvent(4, EventType.SAFETY_CAR_END)))
    result = simulate(config, strategy, conditions)
    assert [l.safety_car for l in result.laps] == [False, True, True, False, False]
    assert result.laps[1].pit_loss == 11.25
    assert result.total_time == pytest.approx(480.85 + 38.75)


@pytest.mark.parametrize("factor", [-1, 1.01, float('nan')])
def test_invalid_safety_factor(factor):
    with pytest.raises(ValueError, match="factor"):
        Conditions(safety_car_pit_factor=factor)
