from dataclasses import replace
import pytest
from pitwall.comparison import compare, summary
from pitwall.models import Compound, Strategy, PitStopPlan


def test_manual_comparison(config):
    soft = Strategy("Soft", Compound.SOFT)
    stop = Strategy("Stop", Compound.SOFT, (PitStopPlan(2, Compound.HARD),))
    results = compare(config, (stop, soft))
    assert [r.strategy.name for r in results] == ["Soft", "Stop"]
    assert results[1].total_time - results[0].total_time == pytest.approx(23.85)
    metrics = summary(results[0])
    assert metrics["average"] == pytest.approx(91.4)
    assert metrics["fastest"] == pytest.approx(90.8)
    assert metrics["slowest"] == 92
    assert metrics["stints"] == (5,)
    assert summary(results[1])["stints"] == (2, 3)
    assert summary(results[1])["pit_loss"] == 22.5


def test_tie_order(config):
    first = Strategy("Z", Compound.SOFT)
    second = replace(first, name="A")
    assert [r.strategy for r in compare(config, (first, second))] == [first, second]


def test_invalid_comparison(config):
    strategy = Strategy("A", Compound.SOFT)
    for strategies in ((), (strategy,), (strategy,)*21):
        with pytest.raises(ValueError, match="between"):
            compare(config, strategies)
    with pytest.raises(ValueError, match="unique"):
        compare(config, (strategy, replace(strategy, name=" a ")))
