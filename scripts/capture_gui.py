"""Capture the actual running Qt widget, not a mock-up or a generated image."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "src"))
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from pitwall.gui import MainWindow
from pitwall.comparison import summary

app = QApplication([])
window = MainWindow()
window.show()
window.run(True)
out = root / "evidence" / "screenshots" / datetime.now(timezone.utc).strftime("FIG-I07-%Y%m%dT%H%M%S%fZ")
out.mkdir(parents=True)


def capture():
    if not window.results:
        raise RuntimeError("No results to capture")
    window.canvas.draw()
    if not window.grab().save(str(out / "application.png")):
        raise RuntimeError("Qt screenshot could not be saved")
    (out / "capture.json").write_text(json.dumps({
        "method": "QWidget.grab of actual running MainWindow after deterministic comparison",
        "platform": app.platformName(), "captured_utc": datetime.now(timezone.utc).isoformat(),
        "summaries": [summary(r) for r in window.results],
        "lap_output": [{"strategy": r.strategy.name, "times": [l.lap_time for l in r.laps]} for r in window.results],
        "limitation": "Automated application capture, not evidence of human usability testing",
    }, indent=2), encoding="utf-8")
    print(out)
    window.close()
    app.quit()


QTimer.singleShot(1200, capture)
raise SystemExit(app.exec())
