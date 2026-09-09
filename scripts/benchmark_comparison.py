"""Time comparison only. Preserve raw five-repeat measurements and provenance."""
from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import statistics
import sys
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pitwall.comparison import compare
from pitwall.defaults import default_config
from pitwall.models import Compound, PitStopPlan, Strategy

stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
out = ROOT / "evidence" / "benchmarks" / f"BENCH-COMPARE-{stamp}"
out.mkdir(parents=True)
record = {"evidence_id": out.name, "started_utc": stamp,
          "command": [sys.executable, *sys.argv], "platform": platform.platform(),
          "python": sys.version, "process_architecture": platform.machine(),
          "scope": "compare() including simulation and ranking, excluding GUI rendering and input construction",
          "warmup": "One comparison for each input size before its five measured runs",
          "repeats": 5, "measurements": [],
          "source_sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in sorted((ROOT / "src").rglob("*.py"))}}
record["source_sha256"]["scripts/benchmark_comparison.py"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
for count, laps in ((2, 50), (20, 50), (20, 500)):
    config = replace(default_config(), laps=laps)
    strategies = tuple(Strategy(f"Plan {i+1}", tuple(Compound)[i % 3],
                               (PitStopPlan(laps // 2, Compound.HARD),)) for i in range(count))
    compare(config, strategies)
    seconds = []
    for _ in range(5):
        start = perf_counter()
        results = compare(config, strategies)
        seconds.append(perf_counter() - start)
        assert len(results) == count and all(len(r.laps) == laps for r in results)
    row = {"strategies": count, "race_laps": laps, "lap_evaluations": count * laps,
           "inputs": "Default tyre/circuit/fuel parameters; rotating dry start compounds; one Hard stop after halfway; no events or random variation",
           "seconds": seconds, "minimum": min(seconds), "maximum": max(seconds),
           "mean": statistics.mean(seconds), "median": statistics.median(seconds)}
    record["measurements"].append(row)
    print(json.dumps(row), flush=True)
(out / "timings.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
(out / "output.txt").write_text("\n".join(json.dumps(r) for r in record["measurements"])+"\n", encoding="utf-8")
print(out.relative_to(ROOT))
