from dataclasses import replace
import pytest
from pitwall.engine import simulate
from pitwall.models import Compound, PitStopPlan, Strategy


def test_five_lap_manual_oracle(config):
    strategy = Strategy("Manual stop", Compound.SOFT, (PitStopPlan(2, Compound.HARD),))
    result = simulate(config, strategy)
    assert [l.lap_time for l in result.laps] == pytest.approx([92, 114.2, 92, 91.55, 91.1])
    assert [l.cumulative_time for l in result.laps] == pytest.approx([92, 206.2, 298.2, 389.75, 480.85])
    assert [l.tyre_age for l in result.laps] == [0, 1, 0, 1, 2]
    assert [l.compound for l in result.laps] == [Compound.SOFT]*2 + [Compound.HARD]*3
    assert sum(l.pit_loss for l in result.laps) == 22.5
    assert result.total_time == pytest.approx(sum(l.lap_time for l in result.laps))
    assert simulate(config, strategy) == result


def test_no_stop_manual(config):
    result = simulate(config, Strategy("No stop", Compound.SOFT))
    assert [l.lap_time for l in result.laps] == pytest.approx([92, 91.7, 91.4, 91.1, 90.8])
    assert result.total_time == pytest.approx(457)


@pytest.mark.parametrize("laps", [1, 500])
def test_race_boundaries(config, laps):
    result = simulate(replace(config, laps=laps), Strategy("Boundary", Compound.HARD))
    assert len(result.laps) == laps
    assert result.laps[-1].lap_number == laps


def test_consecutive_same_compound_stops(config):
    strategy = Strategy("Repeated", Compound.SOFT, tuple(PitStopPlan(l, Compound.SOFT) for l in (1, 2, 4)))
    result = simulate(config, strategy)
    assert [l.tyre_age for l in result.laps] == [0, 0, 0, 1, 0]
    assert sum(l.pit_stop for l in result.laps) == 3


def test_final_stop_rejected(config):
    with pytest.raises(ValueError, match="final lap"):
        simulate(config, Strategy("Bad", Compound.SOFT, (PitStopPlan(5, Compound.HARD),)))


def test_zero_pit_loss(config):
    config = replace(config, circuit=replace(config.circuit, pit_lane_loss=0))
    result = simulate(config, Strategy("Free stop", Compound.SOFT, (PitStopPlan(1, Compound.HARD, 0),)))
    assert result.laps[0].pit_stop and result.laps[0].pit_loss == 0


def test_overflow_rejected(config):
    config = replace(config, circuit=replace(config.circuit, base_lap_time=1e308))
    with pytest.raises(ValueError, match="finite"):
        simulate(config, Strategy("Huge", Compound.SOFT))
