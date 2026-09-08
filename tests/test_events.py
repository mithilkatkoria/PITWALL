import pytest
from pitwall.events import EventQueue, RaceEvent, EventType, Weather


def test_order_and_ties():
    a = RaceEvent(2, EventType.SAFETY_CAR_START)
    b = RaceEvent(1, EventType.WEATHER_CHANGE, Weather.WET)
    c = RaceEvent(2, EventType.SAFETY_CAR_END)
    queue = EventQueue((a, b, c), 5)
    assert queue.at_lap(1) == (b,)
    assert queue.at_lap(2) == (a, c)
    assert queue.at_lap(5) == ()


def test_bad_events():
    with pytest.raises(ValueError, match="Event lap"):
        RaceEvent(0, EventType.SAFETY_CAR_START)
    with pytest.raises(ValueError, match="Unknown"):
        RaceEvent(1, "rain")
    with pytest.raises(ValueError, match="requires"):
        RaceEvent(1, EventType.WEATHER_CHANGE)
    with pytest.raises(ValueError, match="cannot"):
        RaceEvent(1, EventType.SAFETY_CAR_START, Weather.WET)
    with pytest.raises(ValueError, match="Event lap"):
        EventQueue((RaceEvent(6, EventType.SAFETY_CAR_START),), 5)
    assert EventQueue((), 1).at_lap(1) == ()
