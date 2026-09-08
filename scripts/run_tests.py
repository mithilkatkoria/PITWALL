"""Preserve actual pytest stdout, JUnit results and run metadata without overwriting."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
label = sys.argv[1]
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
out = root / "evidence" / "test-runs" / f"{label}-{stamp}"
out.mkdir(parents=True)
command = [sys.executable, "-m", "pytest", "-v", f"--junitxml={out / 'results.xml'}", *sys.argv[2:]]
result = subprocess.run(command, cwd=root, capture_output=True, text=True)
(out / "output.txt").write_text(result.stdout + result.stderr, encoding="utf-8")
hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
          for folder in ("src", "tests") for p in sorted((root / folder).rglob("*.py"))}
(out / "metadata.json").write_text(json.dumps({"started_utc": stamp, "command": command,
    "exit_code": result.returncode, "python": sys.version, "platform": platform.platform(),
    "source_sha256": hashes}, indent=2), encoding="utf-8")
print(result.stdout, result.stderr)
print(f"Evidence: {out.relative_to(root)}")
raise SystemExit(result.returncode)
