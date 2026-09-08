import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from dataclasses import replace
import time
import pytest
from PySide6.QtWidgets import QApplication
from pitwall.advanced_gui import AdvancedWindow, parse_events
from pitwall.conditions import Conditions
from pitwall.models import Strategy, Compound
from pitwall.persistence import Scenario


@pytest.fixture
def advanced():
    app = QApplication.instance() or QApplication([])
    window = AdvancedWindow()
    yield window
    if window.worker is not None:
        window.cancel_run()
        window.worker.wait(5000)
    window.close()


def test_events_parser():
    assert len(parse_events('2:Wet, 3:SC_START, 5:SC_END')) == 3
    for text in ('bad','1:snow','0:Dry'):
        with pytest.raises(ValueError,match='Invalid event'):
            parse_events(text)


def test_gui_scenario_roundtrip(advanced,config):
    scenario = Scenario(config,Conditions(seed=42,events=parse_events('2:Wet')),
                        (Strategy('A',Compound.SOFT),Strategy('B',Compound.HARD)))
    advanced.apply_scenario(scenario)
    assert advanced.scenario() == scenario
    bad = replace(scenario,config=replace(config,circuit=replace(config.circuit,base_lap_time=90.00001)))
    with pytest.raises(ValueError,match='precision'):
        advanced.apply_scenario(bad)
    assert advanced.scenario() == scenario


def wait_for_job(window):
    deadline = time.monotonic()+15
    while time.monotonic()<deadline:
        QApplication.processEvents()
        if window.worker is not None and not window.worker.isRunning():
            QApplication.processEvents()
            return
        time.sleep(.01)
    pytest.fail('Worker timed out')


def test_async_search_and_mc(advanced,config):
    advanced.apply_scenario(Scenario(config,Conditions(),(Strategy('A',Compound.SOFT),Strategy('B',Compound.HARD))))
    advanced.max_stops.setValue(1)
    advanced.minimum_stint.setValue(1)
    advanced.pit_step.setValue(1)
    advanced.start_experiment('search')
    wait_for_job(advanced)
    assert advanced.experiment_data['result']['candidate_count'] == 39
    assert len(advanced.experiment_figure.axes[0].patches) == 10
    advanced.start_experiment('monte_carlo')
    wait_for_job(advanced)
    assert len(advanced.experiment_data['result']['trials']) == 100
