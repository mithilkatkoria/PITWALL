from dataclasses import replace
import pytest
from pitwall.physics import degradation, fuel_effect, lap_time


@pytest.mark.parametrize("age,expected", [(0, 0), (1, .2), (3, .6)])
def test_manual_degradation(config, age, expected):
    assert degradation(config.tyres[0], age) == pytest.approx(expected)


def test_zero_degradation(config):
    assert degradation(replace(config.tyres[0], degradation_rate=0), 500) == 0


@pytest.mark.parametrize("age", [-1, .5, True])
def test_invalid_age(config, age):
    with pytest.raises(ValueError, match="Tyre age"):
        degradation(config.tyres[0], age)


def test_fuel_manual(config):
    assert [fuel_effect(config, lap) for lap in range(1, 6)] == [2, 1.5, 1, .5, 0]
    assert fuel_effect(replace(config, laps=1), 1) == 0


@pytest.mark.parametrize("lap", [0, 6, 1.5, True])
def test_invalid_lap(config, lap):
    with pytest.raises(ValueError, match="Lap number"):
        fuel_effect(config, lap)


def test_lap_manual(config):
    assert lap_time(config, config.tyres[0], 3, 2, 22.5) == pytest.approx((114.6, .6, 1.5))
    with pytest.raises(ValueError, match="Pit loss"):
        lap_time(config, config.tyres[0], 0, 1, -1)
