from dataclasses import replace
import random
import pytest
from pitwall.conditions import Conditions
from pitwall.engine import simulate
from pitwall.models import Strategy, Compound


def test_seed_reproduction(config):
    strategy = Strategy("A", Compound.SOFT)
    conditions = Conditions(seed=42, variation=.5)
    global_state = random.getstate()
    a = simulate(config, strategy, conditions)
    assert a == simulate(config, strategy, conditions)
    assert a != simulate(config, strategy, replace(conditions, seed=43))
    assert all(-.5 <= l.random_variation <= .5 for l in a.laps)
    assert random.getstate() == global_state
    assert simulate(config, strategy).total_time == pytest.approx(457)


@pytest.mark.parametrize("seed", [-1, 2**32, True, 1.5, "42"])
def test_bad_seed(seed):
    with pytest.raises(ValueError, match="Seed"):
        Conditions(seed=seed)


def test_bad_amplitude(config):
    with pytest.raises(ValueError, match="Variation"):
        simulate(config, Strategy("A", Compound.SOFT), Conditions(variation=90))
