from dataclasses import replace
import json
import pytest
from pitwall.conditions import Conditions
from pitwall.events import RaceEvent, EventType, Weather
from pitwall.models import Strategy, Compound, PitStopPlan
from pitwall.persistence import Scenario, save_scenario, load_scenario


def test_roundtrip(config, tmp_path):
    scenario = Scenario(config,Conditions(seed=42,variation=.5,events=(RaceEvent(2,EventType.WEATHER_CHANGE,Weather.WET),)),
                        (Strategy("A",Compound.SOFT,(PitStopPlan(2,Compound.HARD,3),)),))
    path = tmp_path/'race.json'
    save_scenario(path,scenario)
    assert load_scenario(path) == scenario
    assert not list(tmp_path.glob('*.tmp'))


@pytest.mark.parametrize("text", ['{', '{}', '{"x":1,"x":2}', 'NaN', '[]'])
def test_malformed(tmp_path,text):
    path = tmp_path/'bad.json'
    path.write_text(text)
    with pytest.raises(ValueError):
        load_scenario(path)


def test_schema_and_model_validation(config,tmp_path):
    path = tmp_path/'race.json'
    save_scenario(path,Scenario(config,Conditions(),(Strategy("A",Compound.SOFT),)))
    original = json.loads(path.read_text())
    for version in (2,True,'1'):
        changed = dict(original,schema_version=version)
        path.write_text(json.dumps(changed))
        with pytest.raises(ValueError,match="schema"):
            load_scenario(path)
    original['config']['laps'] = 0
    path.write_text(json.dumps(original))
    with pytest.raises(ValueError,match="Race length"):
        load_scenario(path)
    path.write_bytes(b' '*1_048_577)
    with pytest.raises(ValueError,match="1 MiB"):
        load_scenario(path)
