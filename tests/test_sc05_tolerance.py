"""SC05: absolute error at most 1e-9 seconds, with no relative tolerance."""
from pitwall.engine import simulate
from pitwall.models import Compound, PitStopPlan, Strategy


def test_five_lap_oracle_absolute_tolerance(config):
    tolerance_seconds = 1e-9
    strategy = Strategy("SC05 oracle", Compound.SOFT, (PitStopPlan(2, Compound.HARD),))
    result = simulate(config, strategy)
    expected_laps = [92.0, 114.2, 92.0, 91.55, 91.1]
    expected_cumulative = [92.0, 206.2, 298.2, 389.75, 480.85]
    assert len(result.laps) == len(expected_laps) == 5
    errors = []
    for lap, expected, cumulative in zip(result.laps, expected_laps, expected_cumulative):
        lap_error = abs(lap.lap_time - expected)
        cumulative_error = abs(lap.cumulative_time - cumulative)
        print(f"lap={lap.lap_number} actual={lap.lap_time:.17g} expected={expected:.17g} "
              f"absolute_error={lap_error:.17g} cumulative_error={cumulative_error:.17g}")
        assert lap_error <= tolerance_seconds
        assert cumulative_error <= tolerance_seconds
        errors.extend((lap_error, cumulative_error))
    assert abs(result.total_time - 480.85) <= tolerance_seconds
    assert simulate(config, strategy) == result
    print(f"SC05 absolute tolerance={tolerance_seconds:.17g} s; maximum error={max(errors):.17g} s")
