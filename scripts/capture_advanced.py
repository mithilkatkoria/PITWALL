"""Capture actual Windows Qt views and export actual completed experiments."""
from dataclasses import replace
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'src'))
from pitwall.advanced_gui import AdvancedWindow
from pitwall.persistence import save_scenario,enum_json
from pitwall.events import RaceEvent,EventType,Weather

app=QApplication([])
window=AdvancedWindow()
window.show()
out=root/'evidence'/'screenshots'/datetime.now(timezone.utc).strftime('FIG-I16-%Y%m%dT%H%M%S%fZ')
out.mkdir(parents=True)
scenarios=root/'scenarios'
scenarios.mkdir(exist_ok=True)
save_scenario(scenarios/'dry-comparison.json',window.scenario())
scenario=window.scenario()
save_scenario(scenarios/'weather-safety-car.json',replace(scenario,conditions=replace(scenario.conditions,
    events=(RaceEvent(10,EventType.WEATHER_CHANGE,Weather.WET),RaceEvent(20,EventType.WEATHER_CHANGE,Weather.DRY),
            RaceEvent(24,EventType.SAFETY_CAR_START),RaceEvent(28,EventType.SAFETY_CAR_END)))))
record=dict(method='QWidget.grab of actual AdvancedWindow, Windows Qt platform',platform=app.platformName(),
            started_utc=datetime.now(timezone.utc).isoformat(),captures=[],limitation='Automated capture, not human usability evidence')
stage=0
deadline=time.monotonic()+90


def capture(name,index):
    window.tabs.setCurrentIndex(index)
    app.processEvents()
    if not window.grab().save(str(out/name)):
        raise RuntimeError('Capture failed')
    record['captures'].append(name)
    (out/'capture.json').write_text(json.dumps(record,indent=2),encoding='utf-8')


def advance():
    global stage
    if time.monotonic()>deadline:
        print('Capture timed out',file=sys.stderr)
        window.cancel_run()
        app.exit(1)
        return
    if stage==0:
        window.run(True)
        capture('01-comparison.png',0)
        capture('02-metrics.png',1)
        capture('03-laps.png',2)
        capture('04-controls.png',3)
        window.start_experiment('search')
        stage=1
    elif stage==1 and window.experiment_data is not None and not window.worker.isRunning():
        capture('05-search-results.png',4)
        capture('06-search-chart.png',5)
        (out/'search-run.json').write_text(json.dumps(window.experiment_data,default=enum_json,indent=2),encoding='utf-8')
        window.noise.setValue(.3)
        window.start_experiment('monte_carlo')
        stage=2
    elif stage==2 and window.experiment_data is not None and not window.worker.isRunning():
        capture('07-monte-carlo-results.png',4)
        capture('08-monte-carlo-chart.png',5)
        (out/'monte-carlo-run.json').write_text(json.dumps(window.experiment_data,default=enum_json,indent=2),encoding='utf-8')
        print(out)
        window.close()
        app.quit()
        return
    QTimer.singleShot(150,guarded_advance)


def guarded_advance():
    try:
        advance()
    except Exception:
        import traceback
        traceback.print_exc()
        window.cancel_run()
        if window.worker is not None:
            window.worker.wait(5000)
        app.exit(1)


QTimer.singleShot(800,guarded_advance)
raise SystemExit(app.exec())
