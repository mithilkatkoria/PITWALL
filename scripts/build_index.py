"""Index real files and actual JUnit test outcomes, without inventing evidence."""
import csv
import hashlib
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

root=Path(__file__).resolve().parents[1]
report=root/'report'
report.mkdir(exist_ok=True)
history=root/'evidence'/'git-history.txt'
history.write_text(subprocess.check_output(['git','log','--format=fuller','--stat'],cwd=root,text=True),encoding='utf-8')

with (report/'evidence-index.csv').open('w',newline='',encoding='utf-8') as stream:
    writer=csv.writer(stream)
    writer.writerow(['Evidence ID','Category','File','Bytes','SHA256'])
    serial=0
    for folder in ('docs','src','tests','evidence','scenarios'):
        for path in sorted((root/folder).rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts:
                continue
            serial+=1
            category={'docs':'Planning or factual documentation','src':'Real code','tests':'Real test code',
                      'scenarios':'Illustrative input scenario','evidence':'Actual captured output or history'}[folder]
            if 'stakeholder' in path.parts and path.name == 'README.md':
                category='Clearly labelled placeholder; no stakeholder response'
            writer.writerow([f'E{serial:04}',category,path.relative_to(root).as_posix(),path.stat().st_size,
                             hashlib.sha256(path.read_bytes()).hexdigest()])

latest=sorted((root/'evidence'/'test-runs').glob('TEST-FINAL-*/results.xml'))[-1]
mapping={'test_models':'FR01 FR02 FR03 FR04','test_physics':'FR02 FR05','test_engine':'FR03 FR05 FR06',
         'test_comparison':'FR07','test_gui':'FR01 FR02 FR03 FR04 FR08','test_events':'FR10',
         'test_conditions':'FR10','test_randomness':'FR11','test_monte_carlo':'FR11','test_optimiser':'FR12',
         'test_persistence':'FR09','test_advanced_gui':'FR09 FR10 FR11 FR12','test_final_robustness':'FR04 FR07 FR09 FR11 FR12'}
with (report/'test-results.csv').open('w',newline='',encoding='utf-8') as stream:
    writer=csv.writer(stream)
    writer.writerow(['Test ID','Iteration','Requirement','Purpose','Input','Expected result','Actual result','Pass/Fail','Evidence','Remedial action','Retest'])
    for index,case in enumerate(ET.parse(latest).getroot().iter('testcase'),1):
        module=case.attrib.get('classname','').split('.')[-1]
        name=case.attrib['name']
        failed=case.find('failure') is not None or case.find('error') is not None
        skipped=case.find('skipped') is not None
        status='FAIL' if failed else 'SKIPPED' if skipped else 'PASS'
        writer.writerow([f'TEST-FINAL-{index:03}','Final regression and independent checks',mapping.get(module,'Needs review'),
                         name,f'tests/{module}.py::{name}',f'Assertions and fixtures in tests/{module}.py',
                         'Assertions passed' if status=='PASS' else status,status,latest.relative_to(root).as_posix(),
                         'FAIL-I17-01 for JSON container cases; otherwise N/A' if module=='test_final_robustness' else 'N/A',
                         'Final actual execution'])

rows=[
 ('FR01','SC01','architecture.md','A14','RaceConfig','1','test_models.py'),
 ('FR02','SC02','I02-tyres.md','A02','TyreCompound','1/2','test_physics.py'),
 ('FR03','SC03','I04-I05-engine.md','A04 A05','Strategy PitStopPlan','4/5','test_engine.py'),
 ('FR04','SC04','architecture.md','A04 A14','Validated models','1/17','test_models.py'),
 ('FR05','SC05','I03-lap.md','A01 A03 A05','RaceState','3/5','test_engine.py'),
 ('FR06','SC06','I04-I05-engine.md','A05','LapResult StrategyResult','5/7','test_engine.py'),
 ('FR07','SC07','I06-comparison.md','A09','StrategyResult','6','test_comparison.py'),
 ('FR08','SC08','I07-gui.md','A09','MainWindow','7','test_gui.py'),
 ('FR09','SC09','I15-persistence.md','A14','Scenario','15/17','test_persistence.py'),
 ('FR10','SC10','I08-events.md; I09-weather.md; I10-safety-car.md','A06 A07 A08','EventQueue Conditions','8/9/10','test_conditions.py'),
 ('FR11','SC11 SC13 SC14','I12-monte-carlo.md','A12 A13','Trial MonteCarloResult','11/12/16','test_monte_carlo.py'),
 ('FR12','SC12 SC13 SC14','I13-optimiser.md','A10 A11','SearchSettings CandidateScore','13/16','test_optimiser.py'),
]
with (report/'traceability.csv').open('w',newline='',encoding='utf-8') as stream:
    writer=csv.writer(stream)
    writer.writerow(['Requirement','Stakeholder Source','Success Criterion','Design Section','Algorithm','Class','Iteration','Development Test','Final Test','Evidence','Evaluation'])
    for requirement,criterion,design,algorithm,classes,iteration,test in rows:
        writer.writerow([requirement,'User brief; genuine stakeholder response pending',criterion,'docs/design/'+design,algorithm,classes,iteration,
                         'tests/'+test,'Latest full regression plus tests/test_final_robustness.py where applicable',latest.relative_to(root).as_posix(),
                         'docs/evaluation/review.md'])
print(f'Indexed {serial} existing files and {sum(1 for _ in ET.parse(latest).getroot().iter("testcase"))} actual final test cases.')
