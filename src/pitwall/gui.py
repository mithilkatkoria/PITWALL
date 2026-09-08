"""First desktop milestone. Widgets display only real simulation results."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDoubleSpinBox, QFormLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QMainWindow, QPushButton,
    QSpinBox, QSplitter, QTableWidget, QTableWidgetItem, QTabWidget,
    QVBoxLayout, QWidget, QAbstractItemView, QScrollArea,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from .comparison import MAX_STRATEGIES, compare, summary
from .defaults import default_config
from .engine import simulate
from .models import Circuit, Compound, Driver, PitStopPlan, RaceConfig, Strategy, TyreCompound


def parse_stops(text: str, stationary: float) -> tuple[PitStopPlan, ...]:
    if not text.strip():
        return ()
    stops = []
    for entry in text.split(','):
        try:
            lap, tyre = entry.split(':')
            stops.append(PitStopPlan(int(lap.strip()), Compound(tyre.strip().capitalize()), stationary))
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Invalid stop '{entry.strip()}'. Use 15:Medium, 35:Hard with positive lap numbers.") from exc
    return tuple(stops)


def table(headers: list[str], editable: bool = False) -> QTableWidget:
    widget = QTableWidget(0, len(headers))
    widget.setHorizontalHeaderLabels(headers)
    widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    widget.verticalHeader().hide()
    widget.setAlternatingRowColors(True)
    if not editable:
        widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    return widget


def populate(widget: QTableWidget, rows: list[list]) -> None:
    widget.setRowCount(len(rows))
    for row, values in enumerate(rows):
        for col, value in enumerate(values):
            text = f"{value:.3f}" if isinstance(value, float) else str(value)
            widget.setItem(row, col, QTableWidgetItem(text))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.results = ()
        self.setWindowTitle("PITWALL | Race strategy lab")
        self.resize(1440, 960)
        self.setMinimumSize(1100, 780)
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(24, 18, 24, 18)
        title = QLabel("PITWALL  /  RACE STRATEGY LAB")
        title.setObjectName("title")
        layout.addWidget(title)
        layout.addWidget(QLabel("DETERMINISTIC DRY RACE     |     Single-car model     |     Illustrative parameters, not telemetry"))
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter, 1)

        settings = QWidget()
        left = QVBoxLayout(settings)
        left.setContentsMargins(0, 8, 12, 0)
        race_group = QGroupBox("01  RACE CONFIGURATION")
        form = QFormLayout(race_group)
        self.laps = QSpinBox()
        self.laps.setRange(1, 500)
        self.laps.setValue(50)
        self.laps.valueChanged.connect(self.invalidate)
        self.base = self.numeric(90, .001, 1000)
        self.lane = self.numeric(20)
        self.stationary = self.numeric(2.5)
        self.fuel = self.numeric(3)
        self.driver = self.numeric(0)
        for name, widget in (("Race length (laps)", self.laps), ("Base lap (s)", self.base),
                             ("Pit lane loss (s)", self.lane), ("Stationary time (s)", self.stationary),
                             ("Initial fuel penalty (s)", self.fuel), ("Driver penalty (s)", self.driver)):
            form.addRow(name, widget)
        left.addWidget(race_group)
        self.tyre_inputs = {}
        for tyre in default_config().tyres:
            box = QGroupBox(f"{tyre.name.value.upper()} TYRE")
            tf = QFormLayout(box)
            pace = self.numeric(tyre.base_pace_delta)
            rate = self.numeric(tyre.degradation_rate, 0, 100)
            life = QSpinBox()
            life.setRange(1, 500)
            life.setValue(tyre.recommended_life)
            life.valueChanged.connect(self.invalidate)
            tf.addRow("Pace penalty (s)", pace)
            tf.addRow("Wear (s / tyre lap)", rate)
            tf.addRow("Suggested life (laps)", life)
            self.tyre_inputs[tyre.name] = (pace, rate, life)
            left.addWidget(box)
        note = QLabel("Suggested life is informational.\nStops happen AFTER the specified lap.\nNew tyres start the next lap at age 0.")
        note.setWordWrap(True)
        left.addWidget(note)
        left.addStretch()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(settings)
        splitter.addWidget(scroll)

        workspace = QWidget()
        right = QVBoxLayout(workspace)
        right.setContentsMargins(8, 8, 0, 0)
        self.headline = QLabel("Configure a race. Compare the trade-offs.")
        self.headline.setObjectName("headline")
        right.addWidget(self.headline)
        tabs = QTabWidget()
        right.addWidget(tabs, 1)
        self.figure = Figure(facecolor="#111d2c", layout="constrained")
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axes = self.figure.add_subplot(111)
        tabs.addTab(self.canvas, "Lap-time graph")
        self.ranking = table(["Strategy", "Total (s)", "Stops", "Avg (s)", "Fastest (s)", "Slowest (s)", "Pit (s)", "Stints"])
        tabs.addTab(self.ranking, "Comparison metrics")
        detail = QWidget()
        dl = QVBoxLayout(detail)
        self.result_choice = QComboBox()
        self.result_choice.currentIndexChanged.connect(self.show_laps)
        dl.addWidget(self.result_choice)
        self.lap_table = table(["Lap", "Time (s)", "Total (s)", "Tyre", "Age", "Wear (s)", "Fuel (s)", "Pit (s)"])
        dl.addWidget(self.lap_table)
        tabs.addTab(detail, "Every lap")
        right.addWidget(QLabel("All times and metrics include pit laps. Graph spikes show the full pit loss."))

        strategies_box = QGroupBox("02  STRATEGIES")
        sl = QVBoxLayout(strategies_box)
        sl.addWidget(QLabel("Pit stops: 15:Medium, 35:Hard    |    Leave blank for no stops    |    Enter laps in increasing order"))
        self.strategies = table(["Name", "Starting tyre", "Stops after lap"], editable=True)
        self.strategies.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.strategies.setMinimumHeight(115)
        self.strategies.setMaximumHeight(165)
        self.strategies.itemChanged.connect(self.invalidate)
        sl.addWidget(self.strategies)
        buttons = QHBoxLayout()
        for text, action in (("+ Add strategy", self.add_strategy), ("Remove selected", self.remove_strategy)):
            button = QPushButton(text)
            button.clicked.connect(action)
            buttons.addWidget(button)
        buttons.addStretch()
        sl.addLayout(buttons)
        right.addWidget(strategies_box)
        actions = QHBoxLayout()
        self.simulate_button = QPushButton("SIMULATE SELECTED")
        self.simulate_button.clicked.connect(lambda: self.run(False))
        self.compare_button = QPushButton("COMPARE ALL")
        self.compare_button.setObjectName("primary")
        self.compare_button.clicked.connect(lambda: self.run(True))
        actions.addWidget(self.simulate_button)
        actions.addWidget(self.compare_button)
        right.addLayout(actions)
        self.status = QLabel("Ready. Configure inputs, then simulate or compare.")
        self.status.setWordWrap(True)
        self.status.setMinimumHeight(42)
        right.addWidget(self.status)
        splitter.addWidget(workspace)
        splitter.setSizes([310, 1070])

        self.setStyleSheet("""
            QWidget { background: #0b1420; color: #e4edf7; font-family: 'Segoe UI'; font-size: 12px; }
            QLabel#title { font-size: 25px; font-weight: 800; color: #50e3b4; padding-bottom: 4px; }
            QLabel#headline { font-size: 20px; font-weight: 700; padding: 6px; }
            QGroupBox { border: 1px solid #2c3d50; border-radius: 6px; margin-top: 12px; padding: 12px 8px 8px; font-weight: 600; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; color: #8da8c4; }
            QSpinBox, QDoubleSpinBox, QComboBox { background: #182739; border: 1px solid #3a5169; padding: 5px; min-height: 20px; }
            QTableWidget { background: #111d2c; alternate-background-color: #172537; gridline-color: #2c3d50; selection-background-color: #2a5a67; }
            QHeaderView::section { background: #203247; padding: 7px; border: 0; }
            QPushButton { background: #203247; border: 1px solid #3a5169; border-radius: 4px; padding: 10px 14px; font-weight: 600; }
            QPushButton:hover { background: #34506c; }
            QPushButton#primary { background: #50e3b4; color: #071812; border: 0; }
            QTabBar::tab { background: #182739; padding: 10px 16px; }
            QTabBar::tab:selected { color: #50e3b4; background: #263b51; }
            QTabWidget::pane { border: 1px solid #2c3d50; }
            QScrollArea { border: 0; }
        """)
        self.add_strategy(name="One stop", start=Compound.MEDIUM, stops="25:Hard")
        self.add_strategy(name="Two stops", start=Compound.SOFT, stops="15:Medium, 32:Hard")
        self.strategies.selectRow(0)
        self.invalidate()

    def numeric(self, value, minimum=0, maximum=1000):
        widget = QDoubleSpinBox()
        widget.setDecimals(3)
        widget.setRange(minimum, maximum)
        widget.setValue(value)
        widget.valueChanged.connect(self.invalidate)
        return widget

    def style_axes(self):
        self.axes.set_facecolor("#111d2c")
        self.axes.set_xlabel("Race lap", color="#bbccdf")
        self.axes.set_ylabel("Lap time (seconds)", color="#bbccdf")
        self.axes.tick_params(colors="#bbccdf")
        for spine in self.axes.spines.values():
            spine.set_color("#3a5169")
        self.axes.grid(alpha=.18, color="#8da8c4")

    def invalidate(self, *args):
        if not hasattr(self, 'status'):
            return
        self.results = ()
        self.result_choice.clear()
        self.ranking.setRowCount(0)
        self.lap_table.setRowCount(0)
        self.axes.clear()
        self.style_axes()
        self.canvas.draw_idle()
        self.headline.setText("Inputs ready. Run to see current results.")
        self.status.setStyleSheet("color: #b8cadd")
        self.status.setText("Results cleared after input changes. Simulate or compare to calculate.")

    def add_strategy(self, checked=False, name=None, start=Compound.SOFT, stops=""):
        if self.strategies.rowCount() >= MAX_STRATEGIES:
            self.status.setText(f"Maximum {MAX_STRATEGIES} strategies. Remove a row to add another.")
            return
        row = self.strategies.rowCount()
        self.strategies.insertRow(row)
        self.strategies.setItem(row, 0, QTableWidgetItem(name or f"Strategy {row + 1}"))
        choice = QComboBox()
        choice.addItems([c.value for c in Compound])
        choice.setCurrentText(start.value)
        choice.currentIndexChanged.connect(self.invalidate)
        self.strategies.setCellWidget(row, 1, choice)
        self.strategies.setItem(row, 2, QTableWidgetItem(stops))
        self.strategies.selectRow(row)
        self.invalidate()

    def remove_strategy(self):
        row = self.strategies.currentRow()
        if row >= 0:
            self.strategies.removeRow(row)
            self.invalidate()

    def read_config(self):
        tyres = tuple(TyreCompound(c, p.value(), d.value(), l.value())
                      for c, (p, d, l) in self.tyre_inputs.items())
        return RaceConfig(self.laps.value(), Circuit("Custom circuit", self.base.value(), self.lane.value()),
                          Driver("Custom driver", self.driver.value()), tyres, self.fuel.value())

    def read_strategy(self, row):
        if row < 0 or row >= self.strategies.rowCount():
            raise ValueError("Select a strategy row first")
        return Strategy(self.strategies.item(row, 0).text().strip(),
                        Compound(self.strategies.cellWidget(row, 1).currentText()),
                        parse_stops(self.strategies.item(row, 2).text(), self.stationary.value()))

    def run(self, comparison=True):
        self.invalidate()
        try:
            config = self.read_config()
            if comparison:
                strategies = tuple(self.read_strategy(r) for r in range(self.strategies.rowCount()))
                self.results = compare(config, strategies)
            else:
                self.results = (simulate(config, self.read_strategy(self.strategies.currentRow())),)
        except ValueError as exc:
            self.status.setStyleSheet("color: #ffab91")
            self.status.setText(f"Input error: {exc}")
            return
        self.axes.clear()
        self.style_axes()
        colours = ["#50e3b4", "#ffcc66", "#80b8ff", "#ef8cc6"]
        styles = ['-', '--', '-.', ':']
        rows = []
        for index, result in enumerate(self.results):
            self.axes.plot([l.lap_number for l in result.laps], [l.lap_time for l in result.laps],
                           label=result.strategy.name, color=colours[index % len(colours)],
                           linestyle=styles[(index // len(colours)) % len(styles)], linewidth=1.8)
            metrics = summary(result)
            rows.append([metrics[k] for k in ("name", "total", "stops", "average", "fastest", "slowest", "pit_loss")] +
                        [" / ".join(map(str, metrics["stints"]))])
        self.axes.legend(facecolor="#182739", labelcolor="#e4edf7", fontsize=9)
        self.canvas.draw()
        populate(self.ranking, rows)
        self.result_choice.addItems([r.strategy.name for r in self.results])
        winner = self.results[0]
        self.headline.setText(f"{winner.strategy.name}  |  {winner.total_time:,.3f} s")
        gap = self.results[1].total_time - winner.total_time if len(self.results) > 1 else None
        message = f"Calculated {len(self.results)} strategies x {config.laps} laps. "
        if gap is not None:
            message += f"Gap to second: {gap:.3f} s. "
        self.status.setText(message + "Results apply to these model inputs only.")
        self.status.setStyleSheet("color: #50e3b4")

    def show_laps(self, index):
        if 0 <= index < len(self.results):
            populate(self.lap_table, [[l.lap_number, l.lap_time, l.cumulative_time, l.compound.value,
                                      l.tyre_age, l.degradation_loss, l.fuel_effect, l.pit_loss]
                                     for l in self.results[index].laps])


def main():
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()
    return app.exec()
