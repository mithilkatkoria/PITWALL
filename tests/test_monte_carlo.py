from dataclasses import replace
import math
import pytest
from pitwall.conditions import Conditions
from pitwall.models import Strategy, Compound
from pitwall.monte_carlo import describe, monte_carlo


def test_manual_statistics():
    values = describe((1.,2.,3.))
    assert values == pytest.approx(dict(mean=2, median=2, stdev=math.sqrt(2/3), minimum=1, maximum=3))
    with pytest.raises(ValueError, match="at least"):
        describe(())


def test_deterministic_and_replay(config):
    a = Strategy("A", Compound.SOFT)
    b = Strategy("B", Compound.HARD)
    result = monte_carlo(config, a, b, Conditions(), 100)
    assert all(t.a_total == pytest.approx(457) for t in result.trials)
    assert result.a_statistics["stdev"] == 0
    assert result.a_win_probability == 1
    conditions = Conditions(seed=17, variation=.5)
    x = monte_carlo(config, a, b, conditions, 10, .5)
    assert x == monte_carlo(config, a, b, conditions, 10, .5)
    ties = monte_carlo(config, a, replace(a, name="Same"), conditions, 10, 1)
    assert ties.tie_probability == 1 and ties.a_win_probability == 0


def test_invalid_counts_and_cancel(config):
    a,b = Strategy("A", Compound.SOFT), Strategy("B", Compound.HARD)
    for count in (0, -1, 1001, True):
        with pytest.raises(ValueError, match="count"):
            monte_carlo(config,a,b,Conditions(),count)
    with pytest.raises(ValueError, match="probability"):
        monte_carlo(config,a,b,Conditions(),1,1.5)
    with pytest.raises(InterruptedError):
        monte_carlo(config,a,b,Conditions(),1,cancelled=lambda: True)
