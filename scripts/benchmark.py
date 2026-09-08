"""Genuine timings with raw repeats; candidate prefixes are throughput tests only."""
from dataclasses import asdict
from datetime import datetime, timezone
from itertools import islice
import ctypes
import json
from pathlib import Path
import platform
import statistics
import sys
from time import perf_counter
import winreg

root = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'src'))
from pitwall.defaults import default_config
from pitwall.models import Strategy, Compound, PitStopPlan
from pitwall.conditions import Conditions
from pitwall.engine import simulate
from pitwall.optimiser import candidates, optimise, SearchSettings
from pitwall.monte_carlo import monte_carlo

out = root/'evidence'/'benchmarks'/datetime.now(timezone.utc).strftime('BENCH-01-%Y%m%dT%H%M%S%fZ')
out.mkdir(parents=True)
config = default_config()
a = Strategy('One stop',Compound.MEDIUM,(PitStopPlan(25,Compound.HARD),))
b = Strategy('Two stops',Compound.SOFT,(PitStopPlan(15,Compound.MEDIUM),PitStopPlan(32,Compound.HARD)))
conditions = Conditions(seed=42,variation=.3)


class MemoryStatus(ctypes.Structure):
    _fields_ = [('length',ctypes.c_ulong),('load',ctypes.c_ulong),*[(k,ctypes.c_ulonglong) for k in (
        'total_physical','available_physical','total_pagefile','available_pagefile','total_virtual','available_virtual','extended')]]


memory = MemoryStatus()
memory.length = ctypes.sizeof(memory)
ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'HARDWARE\DESCRIPTION\System\CentralProcessor\0') as key:
    cpu = winreg.QueryValueEx(key,'ProcessorNameString')[0]
record = dict(started_utc=datetime.now(timezone.utc).isoformat(),machine=dict(cpu=cpu,ram_bytes=memory.total_physical,
    platform=platform.platform(),python=sys.version,process_architecture=platform.machine()),race_laps=50,
    repeats=3,warmup='One unmeasured single-race run',measurements=[])
simulate(config,a)


def measure(label,count,fn):
    timings=[]
    for _ in range(3):
        start=perf_counter()
        fn()
        timings.append(perf_counter()-start)
    row=dict(label=label,count=count,seconds=timings,minimum=min(timings),maximum=max(timings),
             mean=statistics.mean(timings),median=statistics.median(timings))
    record['measurements'].append(row)
    (out/'timings.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    print(f"{label} {count}: mean {row['mean']:.6f} s",flush=True)


for count in (1,100,500,1000):
    def races():
        for _ in range(count): simulate(config,a)
    measure('sequential races',count,races)
for count in (10,100,1000):
    plans=tuple(islice(candidates(config,SearchSettings()),count))
    def scoring():
        for plan in plans: simulate(config,plan)
    measure('candidate prefix scoring (not full search)',len(plans),scoring)
measure('complete default search',len(tuple(candidates(config,SearchSettings()))),lambda: optimise(config,Conditions(),SearchSettings()))
for count in (100,500,1000):
    measure('paired Monte Carlo trials',count,lambda: monte_carlo(config,a,b,conditions,count,.3,3))
print(out)
