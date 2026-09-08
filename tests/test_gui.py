import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import pytest
from PySide6.QtWidgets import QApplication
from pitwall.gui import MainWindow, parse_stops


@pytest.fixture
def window():
    app = QApplication.instance() or QApplication([])
    widget = MainWindow()
    widget.show()
    app.processEvents()
    yield widget
    widget.close()


def test_parser():
    assert parse_stops("", 2.5) == ()
    assert [s.lap for s in parse_stops("1:soft, 3:HARD", 2.5)] == [1, 3]
    for text in ("oops", "1:wet", "0:Hard", "2:Hard,", "2.5:Soft"):
        with pytest.raises(ValueError, match="Invalid stop"):
            parse_stops(text, 2.5)


def test_real_gui_comparison_and_invalidation(window):
    window.compare_button.click()
    assert len(window.results) == 2
    assert len(window.axes.lines) == 2
    assert all(len(line.get_ydata()) == 50 for line in window.axes.lines)
    assert window.lap_table.rowCount() == 50
    assert window.ranking.rowCount() == 2
    window.laps.setValue(40)
    assert not window.results
    assert window.ranking.rowCount() == 0
    assert len(window.axes.lines) == 0


def test_invalid_stop_error_and_recovery(window):
    window.strategies.item(0, 2).setText("0:Hard")
    window.compare_button.click()
    assert "Input error" in window.status.text()
    assert not window.results
    window.strategies.item(0, 2).setText("25:Hard")
    window.compare_button.click()
    assert len(window.results) == 2


def test_single_and_add_remove(window):
    window.strategies.selectRow(0)
    window.simulate_button.click()
    assert len(window.results) == 1
    window.add_strategy()
    assert window.strategies.rowCount() == 3
    window.remove_strategy()
    assert window.strategies.rowCount() == 2
