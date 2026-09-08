from dataclasses import replace
import pytest
from pitwall.models import *


@pytest.mark.parametrize("laps", [1, 500])
def test_race_boundaries(config, laps):
    assert replace(config, laps=laps).laps == laps


@pytest.mark.parametrize("laps", [0, -1, 501, 2.5, True, "5"])
def test_invalid_race_length(config, laps):
    with pytest.raises(ValueError, match="Race length"):
        replace(config, laps=laps)


@pytest.mark.parametrize("value", [-1, float('nan'), float('inf'), True, "fast"])
def test_invalid_parameters(config, value):
    with pytest.raises(ValueError, match="Degradation"):
        replace(config.tyres[0], degradation_rate=value)
    with pytest.raises(ValueError, match="Pit-lane"):
        replace(config.circuit, pit_lane_loss=value)
    with pytest.raises(ValueError, match="fuel"):
        replace(config, initial_fuel_penalty=value)


def test_missing_and_duplicate_tyres(config):
    for tyres in (config.tyres[:2], (config.tyres[0],)*3, list(config.tyres)):
        with pytest.raises(ValueError, match="exactly once"):
            replace(config, tyres=tyres)


@pytest.mark.parametrize("start", [None, "SOFT", 0])
def test_invalid_start(start):
    with pytest.raises(ValueError, match="Compound"):
        Strategy("Invalid", start)


def test_stop_order_and_race_end(config):
    stop = PitStopPlan(2, Compound.HARD)
    for stops in ((stop, stop), (replace(stop, lap=3), stop)):
        with pytest.raises(ValueError, match="increasing"):
            Strategy("Bad", Compound.SOFT, stops)
    for lap in (5, 6):
        with pytest.raises(ValueError, match="final lap"):
            Strategy("Bad", Compound.SOFT, (replace(stop, lap=lap),)).validate_for(config)
    Strategy("Good", Compound.SOFT, (stop,)).validate_for(config)


def test_zero_and_negative_inputs(config):
    with pytest.raises(ValueError, match="Pit lap"):
        PitStopPlan(0, Compound.HARD)
    with pytest.raises(ValueError, match="Stationary"):
        PitStopPlan(1, Compound.HARD, -1)
    with pytest.raises(ValueError, match="Base lap"):
        replace(config.circuit, base_lap_time=0)
    with pytest.raises(ValueError, match="Recommended"):
        replace(config.tyres[0], recommended_life=0)


def test_results_and_state_validation():
    with pytest.raises(ValueError, match="Tyre age"):
        RaceState(0, Compound.SOFT, -1, 0)
    with pytest.raises(ValueError, match="non-empty"):
        StrategyResult(Strategy("Empty", Compound.SOFT), ())
    with pytest.raises(ValueError, match="Cumulative"):
        LapResult(1, 90, 89, Compound.SOFT, 0, 0, 0, False, 0)
