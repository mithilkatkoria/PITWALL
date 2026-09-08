"""Experiments, persistence and cancellable workers layered on the first GUI."""
from dataclasses import asdict
import json
from pathlib import Path
import threading
from datetime import datetime, timezone
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
    QComboBox, QSpinBox, QLineEdit, QPlainTextEdit, QPushButton, QLabel,
    QFileDialog, QScrollArea)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from .gui import MainWindow, populate
from .conditions import Conditions
from .events import EventType, RaceEvent, Weather
from .monte_carlo import monte_carlo
from .optimiser import SearchSettings, optimise, baselines
from .persistence import Scenario, load_scenario, save_scenario, to_data, enum_json


def parse_events(text: str):
    if not text.strip():
        return ()
    events = []
    for entry in text.split(','):
        try:
            lap, command = entry.strip().split(':')
            if command.strip().upper() in ("SC_START", "SC_END"):
                kind = EventType.SAFETY_CAR_START if command.strip().upper() == "SC_START" else EventType.SAFETY_CAR_END
                event = RaceEvent(int(lap), kind)
            else:
                event = RaceEvent(int(lap), EventType.WEATHER_CHANGE, Weather(command.strip().capitalize()))
            events.append(event)
        except ValueError as exc:
            raise ValueError(f"Invalid event '{entry}'. Use 10:Wet, 15:SC_START, 18:SC_END.") from exc
    return tuple(events)


class ExperimentWorker(QThread):
    completed = Signal(object)
    failed = Signal(str)

    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self.cancellation = threading.Event()

    def run(self):
        try:
            self.completed.emit(self.task(self.cancellation.is_set))
        except (ValueError, InterruptedError) as exc:
            self.failed.emit(str(exc))
        except Exception as exc:
            self.failed.emit(f"Unexpected {type(exc).__name__}: {exc}")


class AdvancedWindow(MainWindow):
    def __init__(self):
        self.revision = 0
        self.worker = None
        self.experiment_data = None
        self.loaded_names = ("Custom circuit", "Custom driver")
        super().__init__()
        container = QWidget()
        layout = QVBoxLayout(container)
        form = QFormLayout()
        self.weather = QComboBox()
        self.weather.addItems([w.value for w in Weather])
        self.weather.currentIndexChanged.connect(self.invalidate)
        self.damp = self.numeric(4)
        self.wet = self.numeric(15)
        self.sc_penalty = self.numeric(25)
        self.sc_factor = self.numeric(.5,0,1)
        self.seed = QLineEdit("42")
        self.seed.textChanged.connect(self.invalidate)
        self.noise = self.numeric(0)
        self.events_text = QLineEdit()
        self.events_text.setPlaceholderText("10:Wet, 15:SC_START, 18:SC_END, 25:Dry")
        self.events_text.textChanged.connect(self.invalidate)
        for name,widget in (("Initial weather",self.weather),("Damp penalty (s)",self.damp),
                            ("Wet penalty (s)",self.wet),("SC lap penalty (s)",self.sc_penalty),
                            ("SC pit-loss factor",self.sc_factor),("Seed (0..4294967295)",self.seed),
                            ("Uniform variation +/- s",self.noise),("Events before lap",self.events_text)):
            form.addRow(name,widget)
        layout.addLayout(form)
        warning = QLabel("All tyres are dry compounds; rain penalties apply equally. Events run in lap order, with input order for ties.\nRandom SC commands are appended after fixed commands. Overlapping periods are not stacked.")
        warning.setWordWrap(True)
        layout.addWidget(warning)
        experiments = QFormLayout()
        self.runs = QComboBox()
        self.runs.addItems(["100","500","1000"])
        self.runs.currentIndexChanged.connect(self.invalidate)
        self.sc_probability = self.numeric(.3,0,1)
        self.duration = self.int_input(3,1,500)
        self.max_stops = self.int_input(2,0,2)
        self.minimum_stint = self.int_input(5,1,500)
        self.pit_step = self.int_input(5,1,500)
        for name,widget in (("Monte Carlo trials (first 2 rows)",self.runs),
                            ("Chance of generated SC per race",self.sc_probability),("Generated SC duration (laps)",self.duration),
                            ("Search maximum stops",self.max_stops),("Search minimum stint",self.minimum_stint),("Search pit-grid step",self.pit_step)):
            experiments.addRow(name,widget)
        layout.addLayout(experiments)
        row = QHBoxLayout()
        self.mc_button = QPushButton("MONTE CARLO")
        self.mc_button.clicked.connect(lambda: self.start_experiment("monte_carlo"))
        self.search_button = QPushButton("OPTIMISE")
        self.search_button.clicked.connect(lambda: self.start_experiment("search"))
        self.cancel_button = QPushButton("CANCEL RUN")
        self.cancel_button.clicked.connect(self.cancel_run)
        self.cancel_button.setEnabled(False)
        for button in (self.mc_button,self.search_button,self.cancel_button):
            row.addWidget(button)
        layout.addLayout(row)
        layout.addWidget(QLabel("Search uses fixed events with variation disabled. Best means best inside the examined search space."))
        layout.addStretch()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        self.tabs.addTab(scroll,"Conditions & experiments")
        self.experiment_output = QPlainTextEdit()
        self.experiment_output.setReadOnly(True)
        self.tabs.addTab(self.experiment_output,"Experiment results")
        self.experiment_figure = Figure(facecolor="#111d2c",layout="constrained")
        self.experiment_canvas = FigureCanvasQTAgg(self.experiment_figure)
        self.tabs.addTab(self.experiment_canvas,"Experiment chart")
        for label,action in (("SAVE",self.save_dialog),("LOAD",self.load_dialog),("EXPORT RUN",self.export_dialog)):
            button = QPushButton(label)
            button.clicked.connect(action)
            self.actions.addWidget(button)
        self.lap_table.setColumnCount(12)
        self.lap_table.setHorizontalHeaderLabels(["Lap","Time (s)","Total (s)","Tyre","Age","Wear","Fuel","Pit","Weather","Wet loss","SC loss","Noise"])

    def int_input(self,value,minimum,maximum):
        widget = QSpinBox()
        widget.setRange(minimum,maximum)
        widget.setValue(value)
        widget.valueChanged.connect(self.invalidate)
        return widget

    def invalidate(self,*args):
        self.revision += 1
        super().invalidate(*args)
        self.experiment_data = None
        if hasattr(self,'experiment_output'):
            self.experiment_output.clear()
            self.experiment_figure.clear()
            self.experiment_canvas.draw_idle()

    def read_config(self):
        from dataclasses import replace
        config = super().read_config()
        return replace(config,circuit=replace(config.circuit,name=self.loaded_names[0]),
                       driver=replace(config.driver,name=self.loaded_names[1]))

    def read_conditions(self):
        if not hasattr(self,'weather'):
            return Conditions()
        try:
            seed = int(self.seed.text())
        except ValueError as exc:
            raise ValueError("Seed must be an integer from 0 to 4294967295") from exc
        return Conditions(Weather(self.weather.currentText()),parse_events(self.events_text.text()),
                          self.damp.value(),self.wet.value(),self.sc_penalty.value(),self.sc_factor.value(),seed,self.noise.value())

    def scenario(self):
        return Scenario(self.read_config(),self.read_conditions(),tuple(self.read_strategy(r) for r in range(self.strategies.rowCount())))

    def show_laps(self,index):
        if self.lap_table.columnCount() != 12:
            return super().show_laps(index)
        if 0 <= index < len(self.results):
            populate(self.lap_table,[[l.lap_number,l.lap_time,l.cumulative_time,l.compound.value,l.tyre_age,
                l.degradation_loss,l.fuel_effect,l.pit_loss,l.weather.value,l.weather_effect,l.safety_car_effect,l.random_variation]
                for l in self.results[index].laps])

    def start_experiment(self,kind):
        if self.worker is not None and self.worker.isRunning():
            self.status.setText("A run is already active. Cancel it or wait for completion.")
            return
        try:
            scenario = self.scenario()
            if kind == "search":
                settings = SearchSettings(self.max_stops.value(),self.minimum_stint.value(),self.pit_step.value(),self.stationary.value())
                controls = asdict(settings)
                def task(cancelled):
                    scores = optimise(scenario.config,scenario.conditions,settings,cancelled)
                    return (scores,baselines(scenario.config,scenario.conditions,settings.stationary_time))
            else:
                if len(scenario.strategies) < 2:
                    raise ValueError("Monte Carlo requires at least two strategies")
                runs,probability,duration = int(self.runs.currentText()),self.sc_probability.value(),self.duration.value()
                controls = dict(runs=runs,sc_probability=probability,sc_duration=duration)
                def task(cancelled):
                    return monte_carlo(scenario.config,*scenario.strategies[:2],scenario.conditions,runs,probability,duration,cancelled)
        except ValueError as exc:
            self.status.setText(f"Input error: {exc}")
            return
        self.invalidate()
        revision = self.revision
        self.worker = ExperimentWorker(task,self)
        self.worker.completed.connect(lambda result: self.accept_experiment(kind,scenario,controls,revision,result))
        self.worker.failed.connect(self.status.setText)
        self.worker.finished.connect(lambda: self.cancel_button.setEnabled(False))
        self.cancel_button.setEnabled(True)
        self.status.setText("Running. You can cancel; editing inputs discards this run's displayed result.")
        self.worker.start()

    def accept_experiment(self,kind,scenario,controls,revision,result):
        if revision != self.revision:
            self.status.setText("Run completed for older inputs. Result discarded; run again for current inputs.")
            return
        self.experiment_figure.clear()
        ax = self.experiment_figure.add_subplot(111)
        ax.set_facecolor('#111d2c')
        ax.tick_params(colors='#bbccdf')
        if kind == "search":
            scores,refs = result
            best = scores[0]
            plan = best.strategy
            stops = ', '.join(f"{p.lap}:{p.compound.value}" for p in plan.planned_stops) or 'none'
            text = f"Examined {len(scores)} legal candidates.\nBest within this search: {best.total_time:.3f} s\nStart: {plan.starting_compound.value}; stops after lap: {stops}\nVariation disabled; fixed events retained.\n\nSeparate baseline references:\n"
            text += '\n'.join(f"{r.strategy.name}: {r.total_time:.3f} s (gap to best {r.total_time-best.total_time:+.3f} s)" for r in refs)
            top = scores[:10]
            ax.bar(range(1,len(top)+1),[s.total_time for s in top],color='#50e3b4')
            ax.set_xlabel('Candidate rank (top 10)',color='#bbccdf')
            ax.set_ylabel('Total race time (s)',color='#bbccdf')
            payload = dict(candidate_count=len(scores),scores=[asdict(s) for s in scores],baselines=[asdict(s) for s in refs])
        else:
            a,b = scenario.strategies[:2]
            text = f"{len(result.trials)} paired trials\nA: {a.name}\nB: {b.name}\nP(A beats B): {result.a_win_probability:.1%}\nP(tie): {result.tie_probability:.1%}\nPopulation standard deviation shown.\n\n"
            for name,stats in ((a.name,result.a_statistics),(b.name,result.b_statistics)):
                text += name + '\n' + '\n'.join(f"  {k}: {v:.3f} s" for k,v in stats.items()) + '\n'
            for name,totals,colour in ((a.name,[t.a_total for t in result.trials],'#50e3b4'),(b.name,[t.b_total for t in result.trials],'#ffcc66')):
                ax.hist(totals,bins=min(20,len(totals)),alpha=.55,label=name,color=colour)
            ax.legend(facecolor='#182739',labelcolor='#e4edf7')
            ax.set_xlabel('Total race time (s)',color='#bbccdf')
            ax.set_ylabel('Trial count',color='#bbccdf')
            payload = asdict(result)
        self.experiment_canvas.draw()
        self.experiment_output.setPlainText(text)
        self.tabs.setCurrentWidget(self.experiment_output)
        self.experiment_data = dict(kind=kind,completed_utc=datetime.now(timezone.utc).isoformat(),
                                    scenario=to_data(scenario),controls=controls,result=payload)
        self.status.setText("Run complete. Inspect results/chart or export the complete run as JSON.")

    def cancel_run(self):
        if self.worker is not None:
            self.worker.cancellation.set()
            self.status.setText("Cancellation requested.")

    def closeEvent(self,event):
        if self.worker is not None and self.worker.isRunning():
            self.cancel_run()
            event.ignore()
        else:
            event.accept()

    def save_dialog(self):
        try:
            scenario = self.scenario()
            name,_ = QFileDialog.getSaveFileName(self,"Save scenario","scenario.json","JSON (*.json)")
            if name:
                save_scenario(Path(name),scenario)
                self.status.setText("Scenario saved.")
        except (ValueError,OSError) as exc:
            self.status.setText(f"Save error: {exc}")

    def load_dialog(self):
        name,_ = QFileDialog.getOpenFileName(self,"Load scenario","","JSON (*.json)")
        if name:
            try:
                self.apply_scenario(load_scenario(Path(name)))
                self.status.setText("Scenario loaded. Run to calculate results.")
            except (ValueError,OSError) as exc:
                self.status.setText(f"Load error: {exc}")

    def apply_scenario(self,scenario):
        config,cond = scenario.config,scenario.conditions
        assignments = [(self.laps,config.laps),(self.base,config.circuit.base_lap_time),(self.lane,config.circuit.pit_lane_loss),
                       (self.driver,config.driver.pace_delta),(self.fuel,config.initial_fuel_penalty),(self.damp,cond.damp_penalty),
                       (self.wet,cond.wet_penalty),(self.sc_penalty,cond.safety_car_penalty),(self.sc_factor,cond.safety_car_pit_factor),(self.noise,cond.variation)]
        for tyre in config.tyres:
            assignments.extend(zip(self.tyre_inputs[tyre.name],(tyre.base_pace_delta,tyre.degradation_rate,tyre.recommended_life)))
        for widget,value in assignments:
            if value < widget.minimum() or value > widget.maximum() or (hasattr(widget,'decimals') and round(value,widget.decimals()) != value):
                raise ValueError("Scenario value exceeds this GUI's range or three-decimal precision; current inputs retained")
        for widget,value in assignments:
            widget.setValue(value)
        self.loaded_names = (config.circuit.name,config.driver.name)
        self.weather.setCurrentText(cond.initial_weather.value)
        self.seed.setText(str(cond.seed))
        commands = {EventType.SAFETY_CAR_START:'SC_START',EventType.SAFETY_CAR_END:'SC_END'}
        self.events_text.setText(', '.join(f"{e.lap}:{e.weather.value if e.weather is not None else commands[e.kind]}" for e in cond.events))
        self.strategies.setRowCount(0)
        for strategy in scenario.strategies:
            stops = ', '.join(f"{p.lap}:{p.compound.value}:{p.stationary_time}" for p in strategy.planned_stops)
            self.add_strategy(name=strategy.name,start=strategy.starting_compound,stops=stops)
        self.invalidate()

    def export_dialog(self):
        if self.experiment_data is None:
            self.status.setText("Complete an experiment first, then export its run.")
            return
        name,_ = QFileDialog.getSaveFileName(self,"Export run","pitwall-run.json","JSON (*.json)")
        if name:
            try:
                Path(name).write_text(json.dumps(self.experiment_data,default=enum_json,allow_nan=False,indent=2),encoding='utf-8')
                self.status.setText("Complete experiment run exported.")
            except (ValueError,OSError) as exc:
                self.status.setText(f"Export error: {exc}")
