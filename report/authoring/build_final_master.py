"""Extend the retained master builder with the genuine final quality evidence."""
from pathlib import Path
import csv,hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]
manifest=json.loads((ROOT/'report/authoring/quality-manifest.json').read_text())
# Refresh existing entries only; original evidence bytes are independently checked.
baseline=json.loads((ROOT/'report/authoring/preservation-baseline.json').read_text())
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in baseline.items())
catalogue=ROOT/'report/evidence-index.csv'
with catalogue.open(encoding='utf-8') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
for row in rows:
    data=(ROOT/row['File']).read_bytes();row['Bytes']=len(data);row['SHA256']=hashlib.sha256(data).hexdigest()
with catalogue.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
source=(ROOT/'report/authoring/build_master.py').read_text(encoding='utf-8')
source=source.replace("WORK=OUT/'authoring'", "WORK=OUT/'final-authoring'")
source=source.replace("NAME='PITWALL_Mithil_Katkoria_H446_NEA_MASTER'", "NAME='PITWALL_Mithil_Katkoria_H446_NEA_FINAL_MASTER'")
source=source.replace("glob('TEST-FINAL-*/results.xml')", "glob('TEST-QUALITY-FINAL-*/results.xml')")
source=source.replace('assert len(cases)==86','assert len(cases)==87').replace('assert len(auditrows)==25','assert len(auditrows)==24')
source=source.replace('final 86 collected cases','final 87 collected cases').replace('regression contains 86 passing cases','regression contains 87 passing cases').replace('The 86 recorded passing tests','The 87 recorded passing tests').replace('XML records86 cases','XML records 87 cases')
source=source.replace("'SC05':'Record the explicit 1e-9 oracle tolerance.'", "'SC05':'Preserve the explicit tolerance regression.'").replace("'SC13':'Measure comparison latency separately.'", "'SC13':'Verify GUI latency and other target machines separately.'")
source=re.sub(r"^para\('SC05 is partially met:.*?\)\n", "para('SC05 is now FULLY MET for the recorded five-lap example: a new explicit absolute 1e-9-second test checks each lap, cumulative time and total, with exact replay. Section 4.6 records the executed evidence. The original looser test remains intact.')\n",source,flags=re.M)
source=re.sub(r"^para\('SC13 remains partially met.*?\)\n", "para('SC13 computational evidence is now complete: separate comparison timings supplement the recorded search and Monte Carlo benchmarks. These measurements exclude GUI rendering. SC04 and SC14 remain PARTIALLY MET because genuine error-interpretation and responsiveness observations are missing.')\n",source,flags=re.M)
source=source.replace("'Supported only within the tested model and recorded assertions.'", "'Illustrative model; human acceptance pending.'")
source=source.replace("para('NEA master document')", "para('NEA final master document')")
# Remove the inherited title rule; keep the existing A4 coursework layout.
source=source.replace("figures=[];tables=[];headings=[];sources=[]", """for st in ('Title','Subtitle'):
    for border in doc.styles[st].element.xpath('.//w:pBdr'):
        border.getparent().remove(border)
figures=[];tables=[];headings=[];sources=[]

def portable(text):
    text=str(text).replace(str(ROOT),'[PROJECT]').replace(ROOT.as_posix(),'[PROJECT]')
    text=re.sub(r'C:[\\\\/][^\\n\\\"]*?python.exe','[PYTHON]',text,flags=re.I)
    return text
""")
source=source.replace("def clean(t):\n", "def clean(t):\n    t=portable(t)\n")
source=source.replace("def code(text,title):\n", "def code(text,title):\n    text=portable(text)\n")
source=source.replace("'Final pytest output tail'", "'Final pytest output tail with local paths abbreviated'")
source=source.replace("page();heading('2 Design", "page();heading('2 Design")
source=source.replace("heading('2.1 Problem decomposition')", "md(read('docs/design/design-provenance.md'));heading('2.1 Problem decomposition')")
source=source.replace("heading('1.6 Proposed computational solution')", "para('Post-prototype review and next decisions','Heading 3');md(read('docs/analysis/final-review-impact.md'));heading('1.6 Proposed computational solution')")
source=source.replace('No fresh software tests are claimed by document generation.', 'Section 4.6 separately records the new final-quality test executions and comparison measurements.')
insert="""
heading('4.6 Final quality verification')
md(read('docs/testing/final-quality-results.md'),'Comparison latency summary')
quality=json.loads(read('report/authoring/quality-manifest.json'))
comparison=json.loads(read(quality['comparison']))
table('Raw comparison repeats in seconds',['Strategies / laps','Repeat 1','Repeat 2','Repeat 3','Repeat 4','Repeat 5'],[[str(r['strategies'])+' / '+str(r['race_laps']),*[f'{x:.9f}' for x in r['seconds']]] for r in comparison['measurements']],[1.35,1.1,1.1,1.1,1.1,1.1])
para('Only compare() is timed. Each input uses default circuit, tyre and fuel settings, rotating dry starting compounds and one Hard stop at halfway. No events or random variation are enabled. Five repetitions and one warm-up per size show local variability; they do not measure human responsiveness or establish a new acceptance threshold.')
code(read('tests/test_sc05_tolerance.py'),'Executed explicit SC05 tolerance test')
focused_path=ROOT/quality['focused']
focused_text=(focused_path.parent/'output.txt').read_text()
code('\\n'.join(line for line in focused_text.splitlines() if line.startswith('lap=') or 'absolute_error=' in line or 'SC05 absolute' in line),'Recorded SC05 differences')
para('The focused run is '+focused_path.parent.relative_to(ROOT).as_posix()+'. The full run is '+quality['final']+'. Both retain output, XML, command, environment and source hashes. Original test and failure records remain unchanged. This is verification of the existing program, not a new stakeholder-led software iteration.')
"""
source=source.replace("page();heading('5 Evaluation',1)",insert+"\npage();heading('5 Evaluation',1)")
start=source.index("heading('Appendix F Stakeholder and candidate forms')")
end=source.index("heading('Appendix G Git development summary')",start)
source=source[:start]+"""heading('Appendix F Human evidence packs')
para('All eight forms below are ready to use but uncompleted. Completed consent and identifying information belong in private-evidence/, not a public repository. Record actual dates and participant aliases. A post-prototype response cannot be presented as an initial interview.')
for form in ('docs/stakeholder/initial-interview-form.md','docs/stakeholder/requirements-followup.md','docs/stakeholder/post-prototype-review.md','docs/usability/usability-task-sheet.md','docs/usability/usability-observation-form.md','docs/usability/usability-summary-template.md','docs/candidate/candidate-reflection-template.md'):
    para(read(form).splitlines()[0].lstrip('# '),'Heading 3');md(read(form),'Blank human evidence form')
para('The algorithm-understanding checklist is docs/candidate/algorithm-understanding-check.md. Every topic below is INCOMPLETE. For each, Mithil must record a genuine explanation of purpose, inputs, outputs, algorithm, data structure, edge case, alternative and limitation, with the actual review date.')
table('Candidate understanding topics',['Topic','Current source','Status'],[(a,b,'INCOMPLETE') for a,b in [('Tyre degradation','physics.py'),('Fuel model','physics.py'),('Pit-stop semantics','engine.py'),('Race loop','engine.py'),('Event heap','events.py'),('Weather state','conditions.py / engine.py'),('Safety-car model','conditions.py / engine.py'),('Random seed','engine.py / conditions.py'),('Monte Carlo','monte_carlo.py'),('Statistics','monte_carlo.py'),('Bounded generation','optimiser.py'),('Optimisation','optimiser.py'),('Persistence','persistence.py'),('GUI worker / cancellation','advanced_gui.py'),('Validation','models.py / persistence.py / gui.py')]],[2,3.3,1.55])
para('No new feature is selected now. A genuine future iteration must cite the feedback, update a requirement, record design and expected tests before implementation, retain actual execution and failures, then obtain a real follow-up review.')
"""+source[end:]
source=source.replace("The brief gives15 development and10 testing marks but no full3.3 subcriterion numbering; do not invent exact codes.","Official content numbering is now mapped in report/FINAL_CRITERIA_AUDIT.md.")
source=re.sub(r"^para\('The transcribed allocation is.*?\)\n", "para('Official OCR content points 3.1 through 3.4 and the published marking bands were checked against the specification downloaded on 8 September 2026. The 24-point mapping above uses the official numbering. The separate centre Full Mark Criteria document was not found, so centre-specific integration is TEACHER INPUT REQUIRED. The full strengths, risks, actions and human responsibilities are in report/FINAL_CRITERIA_AUDIT.md. No mark is awarded by this review.')\n",source,flags=re.M)
source=source.replace("for id,org,title,url,note in refs:","refs.append(('R09','OCR','H446 specification','https://www.ocr.org.uk/Images/170844-specification-accredited-a-level-gce-computer-science-h446.pdf','Content printed pages 13-14 and marking grids 22-25 checked; downloaded content headers 3.0/2026, retained grid headers 2.6/2023'))\nfor id,org,title,url,note in refs:")
source=source.replace("heading('Appendix K Development declaration')", "page();heading('Appendix K Development declaration')")
source=source.replace("# Populate figure/table lists", "para('The public release is staged locally. Publication is pending centre permission and privacy approval. Local absolute paths in report excerpts are abbreviated as [PROJECT] or [PYTHON]; original execution records remain intact in the private evidence repository.')\n\n# Populate figure/table lists")
exec(compile(source,str(ROOT/'report/authoring/build_master.py'),'exec'))
