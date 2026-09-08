from dataclasses import replace
import pytest
from pitwall.conditions import Conditions
from pitwall.optimiser import candidates, optimise, SearchSettings, baselines
from pitwall.models import Compound


def test_tiny_space(config):
    race = replace(config, laps=3)
    plans = tuple(candidates(race, SearchSettings(1,1,1)))
    assert len(plans) == 21
    assert len({(p.starting_compound,p.planned_stops) for p in plans}) == 21
    for p in plans:
        p.validate_for(race)
    scores = optimise(replace(config,laps=2), Conditions(), SearchSettings(1,1,1))
    assert len(scores) == 12
    assert scores[0].strategy.starting_compound == Compound.SOFT
    assert scores[0].strategy.planned_stops == ()
    assert scores[0].total_time == pytest.approx(182.2)
    assert [s.total_time for s in scores] == sorted(s.total_time for s in scores)


def test_minimum_stints_and_baselines(config):
    for plan in candidates(config,SearchSettings(2,2,1)):
        bounds = [0,*(s.lap for s in plan.planned_stops),config.laps]
        assert all(b-a >= 2 for a,b in zip(bounds,bounds[1:]))
    assert len(baselines(config,Conditions())) == 3
    with pytest.raises(ValueError,match="Minimum stint"):
        tuple(candidates(config,SearchSettings(2,6,1)))


def test_limit_and_cancel(config, monkeypatch):
    monkeypatch.setattr('pitwall.optimiser.MAX_CANDIDATES', 2)
    with pytest.raises(ValueError,match="work limit"):
        optimise(config,Conditions(),SearchSettings(0,1,1))
    with pytest.raises(InterruptedError):
        optimise(config,Conditions(),SearchSettings(0,1,1),cancelled=lambda: True)
