from dataclasses import replace
from itertools import product
import json
import pytest
from pitwall.conditions import Conditions
from pitwall.comparison import compare
from pitwall.engine import simulate
from pitwall.events import RaceEvent, EventType
from pitwall.models import Compound, Strategy, PitStopPlan
from pitwall.monte_carlo import monte_carlo
from pitwall.optimiser import SearchSettings, optimise
from pitwall.persistence import Scenario, save_scenario, load_scenario


@pytest.mark.parametrize('field', ['events','planned_stops'])
def test_json_collection_types(config,tmp_path,field):
    path = tmp_path/'bad.json'
    save_scenario(path,Scenario(config,Conditions(),(Strategy('A',Compound.SOFT),)))
    data = json.loads(path.read_text())
    target = data['conditions'] if field == 'events' else data['strategies'][0]
    target[field] = {}  # An object must not be accepted as an empty list.
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        load_scenario(path)


def test_independent_search_oracle(config):
    race = replace(config,laps=4,initial_fuel_penalty=0,circuit=replace(config.circuit,pit_lane_loss=0))
    expected = []
    # Independent direct arithmetic, not calls to simulate/candidates.
    for start in Compound:
        t = race.tyre(start)
        expected.append(sum(90+t.base_pace_delta+t.degradation_rate*age for age in range(4)))
        for stop in (1,2,3):
            for end in Compound:
                u = race.tyre(end)
                expected.append(sum(90+t.base_pace_delta+t.degradation_rate*age for age in range(stop))+
                                sum(90+u.base_pace_delta+u.degradation_rate*age for age in range(4-stop)))
    scores = optimise(race,Conditions(),SearchSettings(1,1,1,0))
    assert [s.total_time for s in scores] == pytest.approx(sorted(expected))


def test_trial_reconstruction(config):
    a,b = Strategy('A',Compound.SOFT),Strategy('B',Compound.HARD)
    cond = Conditions(seed=789,variation=.7)
    result = monte_carlo(config,a,b,cond,3,1,2)
    for trial in result.trials:
        events = [RaceEvent(trial.safety_car_start,EventType.SAFETY_CAR_START)]
        if trial.safety_car_start+2 <= config.laps:
            events.append(RaceEvent(trial.safety_car_start+2,EventType.SAFETY_CAR_END))
        replay = replace(cond,seed=trial.seed,events=tuple(events))
        assert simulate(config,a,replay).total_time == trial.a_total
        assert simulate(config,b,replay).total_time == trial.b_total


def test_maximum_comparison(config):
    race = replace(config,laps=500)
    strategies = tuple(Strategy(f'S{i}',Compound.HARD) for i in range(20))
    results = compare(race,strategies)
    assert len(results) == 20 and all(len(r.laps)==500 for r in results)
    assert len({r.total_time for r in results}) == 1
