"""Build the evidence-based master report without changing application code."""
from pathlib import Path
import ast,csv,hashlib,json,re,subprocess,textwrap
import xml.etree.ElementTree as ET
from datetime import datetime,timezone
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'report'; WORK=OUT/'authoring'; WORK.mkdir(exist_ok=True)
NAME='PITWALL_Mithil_Katkoria_H446_NEA_MASTER'
def read(p): return (ROOT/p).read_text(encoding='utf-8-sig')
index=list(csv.DictReader((OUT/'evidence-index.csv').open(encoding='utf-8')))
assert all((ROOT/r['File']).exists() and hashlib.sha256((ROOT/r['File']).read_bytes()).hexdigest()==r['SHA256'] for r in index)
baseline={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for folder in ('src','tests','evidence','scenarios') for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
(WORK/'preservation-baseline.json').write_text(json.dumps(baseline,indent=2))
history=subprocess.check_output(['git','log','--reverse','--format=%h|%aI|%s'],cwd=ROOT,text=True).splitlines()
final=sorted((ROOT/'evidence/test-runs').glob('TEST-FINAL-*/results.xml'))[-1]
cases=list(ET.parse(final).getroot().iter('testcase'))
assert len(cases)==86 and not any(c.find('failure') is not None or c.find('error') is not None for c in cases)
runs=[]
for p in sorted((ROOT/'evidence/test-runs').glob('*/results.xml')):
    cs=list(ET.parse(p).getroot().iter('testcase')); fails=sum(c.find('failure') is not None or c.find('error') is not None for c in cs)
    runs.append((p.parent.name,len(cs),fails,p.relative_to(ROOT).as_posix()))
bench=json.loads(read('evidence/benchmarks/BENCH-01-20260908T212651988284Z/timings.json'))
shot=ROOT/'evidence/screenshots/FIG-I16-20260908T213427339706Z'
search=json.loads((shot/'search-run.json').read_text()); mc=json.loads((shot/'monte-carlo-run.json').read_text())
doc=Document(); sec=doc.sections[0]
sec.page_width=Inches(8.27);sec.page_height=Inches(11.69)
sec.top_margin=sec.bottom_margin=Inches(.7);sec.left_margin=sec.right_margin=Inches(.7)
sec.header_distance=sec.footer_distance=Inches(.3)
for st in ('Normal','Body Text','Caption','Heading 1','Heading 2','Heading 3','Title','Subtitle'):
    s=doc.styles[st];s.font.name='Calibri';s.font.color.rgb=RGBColor(0,0,0)
doc.styles['Normal'].font.size=Pt(10.5)
doc.styles['Normal'].paragraph_format.space_after=Pt(6)
doc.styles['Normal'].paragraph_format.line_spacing=1.08
for st,size in [('Heading 1',17),('Heading 2',13),('Heading 3',11)]:
    doc.styles[st].font.size=Pt(size);doc.styles[st].paragraph_format.space_before=Pt(12);doc.styles[st].paragraph_format.space_after=Pt(6)
    doc.styles[st].paragraph_format.keep_with_next=True
doc.styles['Caption'].font.size=Pt(9)
header=sec.header.paragraphs[0];header.text='PITWALL | H446-03 | Mithil Katkoria | 0460';header.style='Caption'
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
footer.add_run('Page ')
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
figures=[];tables=[];headings=[];sources=[]
def clean(t):
    t=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1 (\2)',str(t));t=t.replace('**','').replace('`','')
    t=re.sub(r'\b(on|includes|shows|after|total|by|average|averaged|recorded|and|an|in|with|of|the|captured|reported|Windows|Python|RAM|Analysis|Design|Evaluation|Development|Solution|Testing|are|is|giving|saves|adds|contains|times|plus|laps|lap|age)(?=\d)',r'\1 ',t)
    return t.replace('\u2014',', ').replace('\u2011','-').replace('\u2192',' -> ')
def para(t='',style=None): return doc.add_paragraph(clean(t),style)
def heading(t,level=2):
    doc.add_heading(t,level);headings.append((level,t))
def label(t,body):
    p=doc.add_paragraph();p.add_run(t+'. ').bold=True;p.add_run(clean(body));return p
def page():doc.add_page_break()
def table(title,headers,rows,widths=None):
    n=len(tables)+1;cap=f'Table {n}: {title}';tables.append(cap)
    p=para(cap,'Caption');p.paragraph_format.keep_with_next=True
    t=doc.add_table(rows=1,cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    widths=widths or [6.85/len(headers)]*len(headers)
    for c,w in zip(t.columns,widths):c.width=Inches(w)
    for i,h in enumerate(headers):t.rows[0].cells[i].text=clean(h)
    trPr=t.rows[0]._tr.get_or_add_trPr();trPr.append(OxmlElement('w:tblHeader'))
    for row in rows:
        for i,val in enumerate(row):t.add_row() if False else None
        cells=t.add_row().cells
        for i,val in enumerate(row):cells[i].text=clean(val)
    for ri,row in enumerate(t.rows):
        pr=row._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
        for ci,c in enumerate(row.cells):
            c.width=Inches(widths[ci]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tcPr=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
            for edge in ('top','left','bottom','right'):
                el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');b.append(el)
            tcPr.append(b);sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'DCE6EF' if ri==0 else ('F4F6F8' if ri%2==0 else 'FFFFFF'));tcPr.append(sh)
            margins=OxmlElement('w:tcMar')
            for edge in ('top','left','bottom','right'):
                el=OxmlElement('w:'+edge);el.set(qn('w:w'),'75');el.set(qn('w:type'),'dxa');margins.append(el)
            tcPr.append(margins)
            for p in c.paragraphs:
                p.paragraph_format.space_after=Pt(2);p.paragraph_format.line_spacing=1.0
                for r in p.runs:r.font.size=Pt(9);r.bold=ri==0
    para()
    return n
def code(text,title):
    para(title,'Caption')
    for line in text.splitlines():
        for part in textwrap.wrap(line,width=100,replace_whitespace=False,drop_whitespace=False) or ['']:
            p=doc.add_paragraph();p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=1
            r=p.add_run(part);r.font.name='Consolas';r.font.size=Pt(8)
    para()
def extract(file,symbol,maxlines=20):
    source=read(file);tree=ast.parse(source)
    target=next((n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==symbol),None)
    if target is None:return
    start=target.lineno;end=min(target.end_lineno,start+maxlines-1)
    code('\n'.join(f'{i}: {line}' for i,line in enumerate(source.splitlines(),1) if start<=i<=end),f'Code extract: {file}, lines {start}-{end} ({"complete" if end==target.end_lineno else "selected opening"} {symbol})')
def figure(path,title,discussion,width=6.5):
    n=len(figures)+1;para(f'Figure {n} {discussion}')
    p=doc.add_paragraph();p.paragraph_format.keep_with_next=True;p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(str(path),width=Inches(width))
    cap=f'Figure {n}: {title}';figures.append(cap);para(cap,'Caption')
def md(content,table_prefix='Supporting record'):
    lines=content.splitlines();i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('```'):
            lang=line[3:];block=[];i+=1
            while i<len(lines) and not lines[i].strip().startswith('```'):block.append(lines[i]);i+=1
            if lang!='mermaid':code('\n'.join(block),'Recorded pseudocode or example')
        elif line.startswith('|') and i+1<len(lines) and re.match(r'^\|[- :|]+\|$',lines[i+1].strip()):
            headers=[x.strip() for x in line.strip('|').split('|')];rows=[];i+=2
            while i<len(lines) and lines[i].strip().startswith('|'):
                rows.append([x.strip() for x in lines[i].strip().strip('|').split('|')]);i+=1
            table(table_prefix,headers,rows);continue
        elif line.startswith('#'):
            if line.startswith('# '):pass
            else:para(line.lstrip('# '),'Heading 3')
        else:para(line)
        i+=1
def part(path,start,end=None):
    s=read(path);s=s.split(start,1)[1];return s.split(end,1)[0] if end else s

# Front matter. TOC and lists are populated by Word fields after layout.
para('OCR A Level Computer Science H446-03','Subtitle');para('Programming Project','Subtitle')
para('PITWALL','Title');para('Motorsport Race Strategy Simulation and Optimisation System','Subtitle')
para('Candidate: Mithil Katkoria\nCandidate number: 0460\nCentre number: 12709')
para('NEA master document')
para('PITWALL compares race strategies using an explainable mathematical model. This report presents the problem, design, implementation, recorded tests and evaluation, followed by supporting appendices.')
para('The current evidence supports computational correctness within the stated model. Stakeholder investigation and human usability results remain to be collected. Precise placeholders identify these gaps.')
page();para('Contents','Title')
toc=OxmlElement('w:fldSimple');toc.set(qn('w:instr'),'TOC \\o "1-2" \\h \\z \\u');doc.add_paragraph()._p.append(toc)
p=para('List of figures','Title');p.paragraph_format.page_break_before=True;figure_list_anchor=doc.add_paragraph()
para('List of tables','Title');table_list_anchor=doc.add_paragraph()
para('Abbreviations','Heading 2');para('GUI: graphical user interface. JSON: JavaScript Object Notation. RNG: random number generator. SC: safety car in model settings; SC01 to SC14: success criteria. FR: functional requirement. NEA: non-exam assessment. UTC: coordinated universal time.')
page();heading('1 Analysis of the problem',1)
sections=[('1.1 Introduction','PITWALL is a desktop race-strategy simulator. A strategy identifies the starting tyre and the lap after which each pit stop occurs. The program calculates the consequence of those decisions over the full race and allows alternatives to be compared under the same assumptions.'),
('1.2 Description of the problem','A fresh Soft tyre can be quicker than a Hard tyre, but its pace can deteriorate more rapidly. Remaining on an old set saves pit time immediately but can lose time on every later lap. Race length changes whether a pit stop has enough time to pay back its cost. Fuel and driver pace also affect the total. Weather and safety-car periods add changing conditions, so a plan that is best in a dry race may be less effective when the timing of an event changes.\n\nManual calculation is practical for a five-lap example, but becomes repetitive across many stop laps and tyre sequences. It is easy to count a pit loss twice or reset tyre age on the wrong lap. A computer can apply one defined rule consistently and retain the components for inspection.'),
('1.3 Why computation is appropriate','Abstraction removes wheel-to-wheel physics and represents a single car with a few time penalties. This keeps the model understandable but limits real-world prediction. Decomposition separates input validation, lap calculation, event state, comparison and presentation. Selection determines whether a stop or event applies. Iteration repeats the lap model and then repeats whole races for candidate strategies or uncertainty trials. Visualisation exposes tyre trends and pit spikes that are difficult to see in a total alone. These techniques solve specific parts of the problem rather than being included only as terminology.')]
for h,t in sections:heading(h);para(t)
heading('1.4 Stakeholders');para('Appropriate stakeholder types include motorsport enthusiasts learning strategy trade-offs, sim-racing users comparing plans, and Computer Science students or teachers reviewing the model. These are proposed categories, not invented interview participants. No named participant or response is recorded.')
table('Proposed stakeholder involvement',['Type','Use and information needed','Response'],[['Motorsport enthusiast','Interpret pit timing and compound trade-offs','[GENUINE STAKEHOLDER RESPONSE REQUIRED]'],['Sim-racing user','Assess which simplifications affect usefulness','[GENUINE STAKEHOLDER RESPONSE REQUIRED]'],['Student or teacher','Explain algorithms and check clarity','[GENUINE STAKEHOLDER RESPONSE REQUIRED]']],[1.3,3.5,2.05])
para('Prepared questions ask which decisions users want to explore, which inputs they understand, what output helps comparison, how errors should appear, which simplifications could mislead them, and whether a pit-lap spike is clear. Appendix F provides a ready-to-use record and task sheet.')
heading('1.5 Research into existing solutions');md(read('docs/analysis/research.md'),'Existing solution comparison')
heading('1.6 Proposed computational solution');para('The solution builds from validated race and tyre inputs to a deterministic engine. Comparison runs each plan using the same configuration. Conditions add scheduled weather and safety-car events. A local seeded generator controls lap variation. Monte Carlo repeats a paired comparison and records trial seeds; bounded optimisation enumerates legal plans and ranks their totals. JSON preserves scenarios, and the GUI displays results and allows long runs to be cancelled. These functions are implemented, but their suitability for actual users still needs genuine feedback.')
heading('1.7 Essential features');md(part('docs/analysis/requirements.md','## First milestone','## Measurable'),'Requirements from the project brief')
para('The source of FR01 to FR12 is the supplied project brief. The priorities above describe the recorded development order, not missing implementation: the later features were subsequently built. No requirement is attributed to an unconsulted stakeholder.')
heading('1.8 Scope limitations');para('The initial scope prioritised dry deterministic calculation. The implemented extension still uses only dry compounds, linear degradation and a single-car model. Weather adds equal penalties to all available tyres; safety car changes lap delay and relative pit loss without field bunching. Parameters are illustrative, not proprietary telemetry. Bounded search deliberately excludes off-grid and more-than-two-stop plans. These limits are evaluated in Section 5.10.')
heading('1.9 Hardware and software requirements');table('Development and end-user environment',['Area','Recorded or required environment','Justification'],[['Developer hardware',bench['machine']['cpu']+'; '+str(bench['machine']['ram_bytes'])+' bytes RAM','Actual benchmark machine, not a minimum specification'],['Developer software','Windows 11; Python 3.14 AMD64; PySide6; Matplotlib; pytest; Git','Desktop UI, graphing, automated checks and genuine history'],['End user','Tested Python environment and a readable desktop display','Source distribution currently requires dependencies; minimum hardware unmeasured'],['Installation','Short virtual-environment path on Windows','Avoids recorded PySide6 path-length installation problem']],[1.1,3.4,2.35])
para('Python expresses the calculations without a compiled build step. Dataclasses and enums are standard-library structures. Qt supplies desktop controls and a worker thread; Matplotlib renders result graphs [R06, R07]. JSON supports a small offline scenario without database administration. The development machine uses an AMD64 Python process on Snapdragon hardware, so the timings must not be described as native ARM measurements.')
heading('1.10 Success criteria');md(part('docs/analysis/requirements.md','## Measurable success criteria','## Stakeholders'),'First milestone success criteria');md(part('docs/analysis/advanced-success-criteria.md','| ID |'),'Advanced success criteria') if False else None
md(read('docs/analysis/advanced-success-criteria.md'),'Advanced success criteria')

page();heading('2 Design of the solution',1);heading('2.1 Problem decomposition')
para('The problem is decomposed into: describing valid conditions; predicting one lap; tracking tyre age and accumulated time; applying decisions and changing conditions; comparing complete outcomes; exploring uncertain outcomes; searching a finite decision space; preserving inputs; and making results readable. Validation affects every part because invalid inputs can otherwise produce convincing but meaningless outputs.')
heading('2.2 Overall system structure');para('The actual dependency direction runs from GUI to validated models and analysis functions. Computational modules do not import Qt. There is no separate controller module: AdvancedWindow collects an immutable snapshot and calls the engine or worker. Figure 1 shows these existing modules.')
def diagram(name,boxes,edges):
    im=Image.new('RGB',(1500,900),'white');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
    for a,b in edges:
        x,y,w,h,_=boxes[a];u,v,ww,hh,_=boxes[b];start=(x+w/2,y+h);end=(u+ww/2,v)
        d.line([start,end],fill='#536575',width=3);d.polygon([end,(end[0]-8,end[1]-12),(end[0]+8,end[1]-12)],fill='#536575')
    for x,y,w,h,t in boxes:
        d.rectangle((x,y,x+w,y+h),fill='#edf2f6',outline='#536575',width=2);d.multiline_text((x+16,y+16),t,fill='black',font=font,spacing=8)
    p=WORK/name;im.save(p);return p
boxes=[(410,20,680,100,'MainWindow / AdvancedWindow\nPySide6 controls and Matplotlib'),(50,220,410,100,'comparison / monte_carlo\noptimiser'),(550,220,410,100,'ExperimentWorker\nQThread and cancellation'),(1060,220,390,100,'persistence\nScenario JSON'),(380,440,630,110,'engine.simulate\nRaceState -> per-lap results'),(60,690,400,110,'physics\nwear / fuel / lap time'),(540,690,420,110,'events / conditions\nheap and environment'),(1050,690,390,110,'models\ntyped data / validation')]
figure(diagram('architecture.png',boxes,[(0,1),(0,2),(0,3),(1,4),(2,4),(4,5),(4,6),(4,7),(3,7)]),'Implemented module architecture','shows how input, calculation and presentation are separated. This diagram was prepared for this report from current source, not presented as an original wireframe.')
heading('2.3 Class design');para('The class inventory below is extracted from the current Python syntax tree. Constructor validation usually lives in __post_init__. Frozen dataclasses reduce accidental input mutation, although dictionaries inside MonteCarloResult remain mutable; frozen does not imply deep immutability.')
for module in ('models','events','conditions','monte_carlo','optimiser','persistence'):
    tree=ast.parse(read(f'src/pitwall/{module}.py'));rows=[]
    for node in tree.body:
        if isinstance(node,ast.ClassDef):
            attrs=[n.target.id+': '+ast.unparse(n.annotation) for n in node.body if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name)]
            methods=[n.name for n in node.body if isinstance(n,ast.FunctionDef)]
            rows.append([node.name,'; '.join(attrs) or 'Enum values or private queue state','; '.join(methods) or 'Data record'])
    table('Classes in '+module,['Class','Key attributes','Methods'],rows,[1.35,3.65,1.85])
para('RaceConfig owns Circuit, Driver and the three TyreCompound definitions. Strategy contains PitStopPlan objects. StrategyResult refers to its Strategy and lap tuple. EnvironmentalLapResult inherits LapResult. Scenario joins config, conditions and strategies. AdvancedWindow extends MainWindow and owns ExperimentWorker. These are the relationships shown in the UML views in Appendix A.')
heading('2.4 Data structures');table('Structures and alternatives',['Structure and use','Reason','Alternative'],[['Tuple: tyres, stops, events and lap records','Fixed input/result sequences support reproducibility','Lists allow easier mutation but weaker boundaries'],['List: results, scores and trials during construction','Append then convert or sort','Preallocation adds bookkeeping without measured need'],['Dictionary: stops keyed by lap','Average constant-time stop lookup','Scanning all stops every lap'],['Tuple-keyed heap: EventQueue','Chronological order with sequence tie-break','Sort once for current static schedules'],['Enum: compound, weather, event type','Restricts valid named states','Unrestricted strings permit spelling errors'],['Dataclass: model and result records','Groups typed fields and validation','Parallel lists risk mismatched positions']],[2.1,2.6,2.15])
para('RaceConfig.tyre actually searches its three-element tuple using next; it is not a dictionary lookup. With exactly three compounds this cost is bounded. This distinction matters when explaining the actual implementation.')
heading('2.5 Important variables');table('Variables and units',['Variable','Type and range','Purpose'],[['laps','int, 1..500','Race distance'],['tyre_age','int, >=0','Completed laps on current set before this lap'],['base_lap_time','finite number >0, seconds','Reference racing pace'],['degradation_rate','finite number >=0, seconds per tyre lap','Linear wear slope'],['cumulative_time','finite number >=0, seconds','Accumulated total'],['seed','int, 0..2^32-1','Replayable generator state'],['variation','finite number >=0 and below base lap time','Uniform signed noise amplitude'],['safety_car_pit_factor','number 0..1','Relative pit-loss multiplier'],['minimum_stint / pit_step','int, 1..500','Search constraints'],['revision','integer counter in AdvancedWindow','Reject output for changed inputs']],[2.1,2.25,2.5])
heading('2.6 Algorithm design');para('The existing repository IDs are retained to avoid breaking traceability: A01 lap time, A02 degradation, A03 fuel, A04 strategy validation, A05 simulation, A06 events, A07 weather, A08 safety car, A09 comparison, A10 generation, A11 optimisation, A12 Monte Carlo, A13 statistics and A14 scenario validation. The numbering examples in the report brief were illustrative.')
designs=[('A01 and A03 Lap and fuel','I03-lap.md'),('A02 Tyre degradation','I02-tyres.md'),('A04 Strategy validation',None),('A05 Race and pit processing','I04-I05-engine.md'),('A06 Event queue','I08-events.md'),('A07 Weather','I09-weather.md'),('A08 Safety car','I10-safety-car.md'),('A09 Comparison','I06-comparison.md'),('A10 and A11 Search','I13-optimiser.md'),('A12 and A13 Repeated trials and statistics','I12-monte-carlo.md'),('A14 Scenario persistence','I15-persistence.md')]
for title,file in designs:
    para(title,'Heading 3')
    if file:md(read('docs/design/'+file),'Algorithm example or test data')
    else:md(part('docs/design/architecture.md','Language-independent A04/A14 validation:','Later iterations'))
para('Current-code refinement: EventQueue builds a list and heapifies it in O(E), rather than pushing every item separately. Consuming all events is O(E log E) [R04]. A race takes O(N + E log E) with fixed three-compound lookup. Monte Carlo also sorts samples for median, adding O(R log R) summary work [R05, R08]. Candidate search adds O(C log C) sorting after C race simulations. These are analyses of the actual code, not measured timing formulas.')
para('Seeded variation uses a private Random(seed), one uniform draw per lap, and a zero-noise shortcut. Equal seeds reproduce results in the recorded environment. Because the same additive draw is used for both strategies, noise alone cancels in their gap; random safety-car timing changes pit opportunity. Pit processing occurs after racing lap L, while environmental events are applied before it.')
heading('2.7 Validation design');md(part('docs/design/architecture.md','## Core classes and units','## Decisions'),'Core data responsibilities')
para('Presence checks reject empty names. Type checks reject boolean race lengths even though bool is an int subclass in Python. Range checks reject negative and nonfinite values. Lookup checks require supported enums and exactly one tyre definition of each type. Logical checks reject duplicated, unordered and final-lap stops. JSON checks require exact fields and arrays before validating elements. The final collection-type defect and fix are documented in Section 3.16.')
heading('2.8 Usability design');md(read('docs/design/I07-gui.md'))
heading('2.9 Current interface design');para('No historical wireframe file was found. The following actual screenshot documents the implemented interface. It is not retrospective design evidence. Tabs separate comparison, per-lap detail, conditions and experiments. Input changes clear stale results; background work uses snapshots and revision checks. Text syntax saves space but needs genuine user evaluation.')
figure(shot/'01-comparison.png','Current strategy comparison interface','shows the default two-strategy comparison and its pit-lap spikes. The totals are model outputs, not real-race observations.')
heading('2.10 Iterative test plan');table('Typical boundary and erroneous tests',['Area','Typical','Boundary','Erroneous and purpose'],[['Race input','5 laps','1 and 500','0,501,bool: enforce finite scope'],['Tyre wear','age3,rate0.2 ->0.6','age0 or zero rate','negative/fractional age'],['Stops','lap2 in five laps','first and penultimate laps','duplicate,unordered,final stop'],['Events','rain then dry','same-lap sequence','missing payload/outside race'],['Monte Carlo','100 trials,seed42','one trial,zero noise','0,1001,invalid seed'],['JSON','full round-trip','1 MiB bound','malformed,duplicates,wrong arrays']],[1.15,1.6,1.7,2.4])
heading('2.11 Post-development test plan');md(read('docs/design/I17-verification.md'));para('Section 4 reports the preserved executions separately from this plan. No fresh software tests are claimed by document generation. Human usability tasks remain planned in Appendix F.')

page();heading('3 Development and testing',1)
para('The recorded sequence is I01, I02, I03, combined I04/I05, I06, I07, I08, I09, I10, I11, I12, I13, I15, combined I14/I16, I17. Pit integration was combined with the full loop; persistence preceded the final GUI/chart integration. Seven genuine commits cover these stages rather than one commit per iteration. All recorded implementation commits are on 8 September 2026; this report does not invent a multi-week history. Appendix G lists the exact commit timestamps.')
iteration_specs=[('I01','Core models','models.py','integer','FR01 FR02 FR03 FR04','SC01 SC02 SC03 SC04','architecture.md'),('I02','Tyre degradation','physics.py','degradation','FR02','SC02','I02-tyres.md'),('I03','Lap and fuel calculation','physics.py','fuel_effect','FR05 FR06','SC05 SC06','I03-lap.md'),('I04-I05','Pit stops and dry race','engine.py','simulate','FR03 FR05 FR06','SC03 SC05 SC06','I04-I05-engine.md'),('I06','Strategy comparison','comparison.py','summary','FR07','SC07','I06-comparison.md'),('I07','First desktop milestone','gui.py','parse_stops','FR01 FR08','SC01 SC08','I07-gui.md'),('I08','Event queue','events.py','EventQueue','FR10','SC10','I08-events.md'),('I09','Weather effects','conditions.py','weather_loss','FR10','SC10','I09-weather.md'),('I10','Safety car','conditions.py','Conditions','FR10','SC10','I10-safety-car.md'),('I11','Seeded variation','engine.py','simulate','FR11','SC11','I11-randomness.md'),('I12','Monte Carlo and statistics','monte_carlo.py','describe','FR11','SC11','I12-monte-carlo.md'),('I13','Bounded optimisation','optimiser.py','candidates','FR12','SC12','I13-optimiser.md'),('I15','JSON persistence','persistence.py','save_scenario','FR09','SC09','I15-persistence.md'),('I14-I16','Advanced GUI and charts','advanced_gui.py','accept_experiment','FR09 FR11 FR12','SC09 SC11 SC12 SC14','I14-I16-interface.md'),('I17','Robustness and verification','persistence.py','array','FR04 FR09','SC04 SC09 SC13 SC14','I17-verification.md')]
for i,(ident,title,file,symbol,fr,sc,design) in enumerate(iteration_specs,1):
    heading(f'3.{i} {title}')
    label('Objective and links',f'{ident}: {title}. Requirements {fr}; success criteria {sc}. Design: docs/design/{design}.')
    label('Implementation and recorded review','The following preserved iteration account records the implementation, expected and actual results, alternatives and next step. Its claims are bounded by the linked execution evidence.')
    md(read('docs/iterations/'+ident+'.md'))
    extract('src/pitwall/'+file,symbol,16)
    label('Code explanation',{'integer':'The strict type check excludes bool and fractions before range validation. This prevents misleading race lengths from reaching simulation.', 'degradation':'The rate multiplies completed tyre age; validation checks the input age and the finite calculated loss.', 'fuel_effect':'The one-lap branch avoids division by zero. Other races decrease the initial penalty linearly to zero.', 'simulate':'Validation occurs before iteration. State and stop lookup are local to each run; events are processed at the start of a lap.', 'summary':'Metrics come from recorded lap times and stop boundaries. Pit laps remain included in fastest, slowest and average values.', 'parse_stops':'The parser converts text into typed stops; Strategy validation then checks ordering and the race boundary.', 'EventQueue':'The sequence number prevents ambiguous same-lap ordering and avoids comparing RaceEvent objects.', 'weather_loss':'An explicit lookup selects the environmental time penalty. It does not model a wet tyre advantage.', 'Conditions':'Configuration validation keeps penalties finite and restricts the pit factor and seed.', 'describe':'Summary statistics are calculated from actual totals. Population standard deviation describes the supplied trial population.', 'candidates':'Combinations choose ordered distinct stop laps; product enumerates compound sequences. Minimum-stint checks remove illegal combinations.', 'save_scenario':'The serialised contract is validated before a temporary sibling file replaces the destination.', 'accept_experiment':'The revision guard discards results for changed inputs before charts or output text are populated.', 'array':'The type guard rejects objects even when empty, closing the exact reproduced decoder gap.'}[symbol])
    label('Extract provenance','This is the current-source version, with line numbers, not a claim that every later extension existed at this earlier stage. The preserved run metadata identifies the source hashes used for each actual test run.')
    if ident=='I07':figure(ROOT/'evidence/screenshots/FIG-I07-20260908T210757444690Z/application.png','First deterministic GUI milestone','shows the actual first-milestone comparison before the advanced controls were integrated.')
    if ident=='I14-I16':figure(shot/'05-search-results.png','Completed bounded-search result','shows the number of legal candidates and baseline reference totals produced by the actual run.')
    label('Stakeholder review','[GENUINE STAKEHOLDER REVIEW REQUIRED]')
    label('Candidate reflection','[CANDIDATE REVIEW AND EXPLANATION REQUIRED]')
heading('3.16 Genuine failures and remedial action');md(read('docs/testing/FAIL-I17-01.md'));md(read('docs/testing/FAIL-I17-02.md'))
failure=next(p for p in (ROOT/'evidence/test-runs').glob('TEST-I17-ROBUSTNESS-*/output.txt'))
raw=failure.read_text();lines=raw.splitlines();selected=[l for l in lines if 'FAILED' in l or 'DID NOT RAISE' in l or '2 failed' in l]
code('\n'.join(selected),'Verbatim lines from '+failure.relative_to(ROOT).as_posix())
para('The two failing assertions expected ValueError when {} replaced an events or planned_stops array. Iterating an empty dictionary produced no element checks. The selected remedy validates the container before its contents. A schema dependency was an alternative, but an explicit list check fits this small schema. The unchanged reproduction tests passed in the 84-test retest and the final 86-test run. The capture-harness failure is separately supported by a factual transcription and retained partial output, not a fabricated pytest screenshot.')
heading('3.17 Recorded test progression');table('All preserved execution runs',['Run ID','Cases','Failures'],[(r[0],r[1],r[2]) for r in runs],[5.3,.75,.8]);para('Repeated regression tests occur in several runs; these counts must not be added and described as unique tests. Appendix B lists the final 86 collected cases, including parameterised cases. Source hashes and exact commands remain in each run directory.')

page();heading('4 Post-development testing',1);heading('4.1 Functional testing')
para('The final recorded regression contains 86 passing cases. The rows below reference actual tests and assertions rather than invented manual sessions. Test functions may assert several related conditions. Native file-dialog interaction has not been manually tested; the persistence functions and widget conversion are covered.')
functional=[('F01','SC05 SC06','test_five_lap_manual_oracle','5 laps; Soft to Hard after2','92,114.2,92,91.55,91.1; total480.85'),('F02','SC07','test_manual_comparison','No-stop Soft versus pit plan','Soft faster by23.85; average91.4'),('F03','SC08','test_real_gui_comparison_and_invalidation','Click compare; edit laps','2 lines,50 points each; results clear'),('F04','SC09','test_roundtrip','Save/load seed,events,service time','Exact Scenario equality'),('F05','SC10','test_safety_car_manual','SC laps2-3; stop after2','Pit11.25; total519.6'),('F06','SC11','test_deterministic_and_replay','100 fixed trials; seeded replay','Repeatable totals and ties'),('F07','SC12','test_independent_search_oracle','4-lap tiny enumeration','Complete scores match direct arithmetic'),('F08','SC14','test_worker_cancellation','Start1000 trials and cancel','No completed output; cancelled status')]
for id,sc,test,steps,expected in functional:
    matching=[c for c in cases if c.attrib['name']==test];assert matching,test
functionalrows=[]
for (ident,sc,test,steps,expected),feature in zip(functional,['Race','Compare','GUI','JSON','SC event','Monte Carlo','Search','Cancel']):
    case_number=next(i for i,c in enumerate(cases,1) if c.attrib['name']==test)
    functionalrows.append([ident,sc,feature,steps,expected,'Assertions matched expected values.','PASS',f'Appendix B, case {case_number:03}'])
table('Functional verification',['Test ID','Success criterion','Feature','Input / steps','Expected','Actual','Pass / fail','Evidence'],functionalrows,[.45,.6,.7,1.15,1.25,1.05,.45,1.2])
para('All entries above are supported by '+final.relative_to(ROOT).as_posix()+'. Appendix B maps the exact test inventory; assertions reside in tests/test_engine.py, test_comparison.py, test_gui.py, test_persistence.py, test_conditions.py, test_monte_carlo.py, test_final_robustness.py and test_advanced_gui.py.')
heading('4.2 Robustness testing');table('Recorded invalid and boundary cases',['Area','Input','Expected and actual','Evidence test'],[['Race','0,-1,501,2.5,True','ValueError; PASS','test_invalid_race_length'],['Stops','Duplicate,unordered,final lap','Rejected; PASS','test_stop_order_and_race_end'],['Events','Unknown command or invalid lap','Rejected; PASS','test_events_parser / test_bad_events'],['JSON','Malformed,missing,duplicates,NaN','Rejected; PASS','test_malformed'],['Schema','2,True,string1; oversized file','Rejected; PASS','test_schema_and_model_validation'],['Containers','{} in events/stops','Initially accepted; fixed and PASS','test_json_collection_types'],['Monte Carlo','0,-1,1001,True','Rejected; PASS','test_invalid_counts_and_cancel'],['Search','Lowered cap; cancellation callback','Explicit error/interruption; PASS','test_limit_and_cancel'],['Large comparison','20 strategies x500 laps','20 equal complete results; PASS','test_maximum_comparison']],[1,1.6,2.15,2.1])
heading('4.3 Performance testing');para('BENCH-01 records three repeats after one unmeasured single-race warm-up. Each race has 50 laps. Timings use perf_counter and include computational result construction, not GUI rendering. The CPU is '+bench['machine']['cpu']+'. Physical RAM is '+str(bench['machine']['ram_bytes'])+' bytes. Python is '+bench['machine']['python']+'.')
table('Raw measured seconds and summary',['Operation / count','Trial 1','Trial 2','Trial 3','Min','Max','Mean'],[[r['label']+' / '+str(r['count']),*[f'{v:.6f}' for v in r['seconds']],f"{r['minimum']:.6f}",f"{r['maximum']:.6f}",f"{r['mean']:.6f}"] for r in bench['measurements']],[1.93,.82,.82,.82,.82,.82,.82])
para('The complete default search examined 1,056 candidates and averaged1.161633 seconds. The 1,000 paired-trial Monte Carlo run averaged2.099058 seconds. Both are below the recorded10-second and30-second targets on this machine. Prefix scoring benchmarks measure throughput on the first candidates, not complete optimisation. Background load and power state were not controlled, so results cannot establish minimum hardware or another device\'s latency. Appendix D retains the raw JSON precision.')
heading('4.4 Manual verification');md(part('docs/design/I04-I05-engine.md','## Independent manual oracle TEST-I05'),'Five-lap independent expected calculation')
para('For lap2, 90 base +0 Soft pace +0.2 wear +1.5 fuel +22.5 pit =114.2 seconds. The new Hard set starts lap3 at age0:90+1+0+1=92. The sum is480.85. With a safety car on laps2 and3, the model adds50 seconds but saves11.25 seconds on the pit loss, giving519.6. These are manual expected calculations matched by executed assertions, not a claim of a separate human testing session.')
para('For statistics [1,2,3], mean and median are2. Squared deviations are1,0,1; population variance is2/3 and standard deviation is sqrt(2/3). The optimiser\'s three-lap, maximum-one-stop space contains3 no-stop plans plus2 legal stop laps times9 compound pairs, giving21. The independently calculated four-lap score distribution is also tested.')
heading('4.5 Usability testing');para('[USABILITY TESTING MUST BE COMPLETED WITH GENUINE USERS]');md(read('docs/testing/manual-usability.md'),'Unconducted usability task sheet');para('Use neutral instructions and record actual help, mistakes, completion and comments. Ask the participant to interpret a pit spike and explain what an88% simulated win frequency means. Do not imply it forecasts a real race. Appendix F includes blank response space and stakeholder follow-up.')

page();heading('5 Evaluation',1);heading('5.1 Overall evaluation');para('PITWALL solves the computational comparison problem within its simplified assumptions. It accepts defined strategies, calculates each lap, ranks outcomes and explores bounded choices and uncertainty. The 86 recorded passing tests, preserved failure/fix sequence, actual GUI captures and benchmarks support these functions. The wider success claim remains conditional because genuine stakeholder needs and usability have not yet been evaluated.')
heading('5.2 Evaluation against success criteria')
criteria={}
for source in ('docs/analysis/requirements.md','docs/analysis/advanced-success-criteria.md'):
    for line in read(source).splitlines():
        if re.match(r'^\|\s*SC\d+',line):
            cells=[c.strip() for c in line.strip('|').split('|')];criteria[cells[0]]=cells[2] if 'advanced-' in source else cells[1]
evaluation=[]
for line in part('docs/evaluation/review.md','## Success criteria','## Actual performance').splitlines():
    if re.match(r'^\|\s*SC\d+',line):
        ident,judgement,evidence=[c.strip() for c in line.strip('|').split('|')]
        remaining={'SC04':'Run genuine error-message usability tasks.','SC05':'Record the explicit 1e-9 oracle tolerance.','SC08':'Obtain audience interpretation evidence.','SC13':'Measure comparison latency separately.','SC14':'Record manual responsiveness and cancellation.'}.get(ident,'Candidate review and target-user acceptance.')
        evaluation.append([ident,criteria.get(ident,''),evidence,judgement,'Supported only within the tested model and recorded assertions.',remaining])
table('Success criterion judgements',['ID','Criterion','Evidence','Judgement','Scope / reason','Remaining work'],evaluation,[.45,1.5,1.45,1,1.15,1.3])
para('SC05 is partially met: the recorded five-lap test uses pytest.approx without an explicit tolerance, so its pass does not by itself establish the stricter 1e-9 seconds stated in the criterion. Exact repeatability is tested. No test or application code has been changed during report preparation.')
para('SC13 remains partially met because no separate comparison/UI-latency measurement was recorded, even though search and Monte Carlo targets passed. SC14 has stronger automated evidence in the final run for stale results and cancellation, but genuine responsiveness observations remain pending. SC04 error handling is tested; the clarity of the explanation to the audience is not established. Improvements are targeted manual tasks, not invented pass results.')
heading('5.3 Functional correctness');para('Race, tyre and fuel calculations match the small independent oracle. Stop checks prevent illegal ordering and the engine resets age on the following lap. Event tests establish chronological processing and stable ties. Comparison metrics include pit laps consistently. Monte Carlo reproduces seeds and trial schedules; statistics match known samples. Search matches a separate exhaustive arithmetic calculation in a tiny space. Save/load preserves typed scenarios and rejects malformed schema data after the genuine collection-type fix. These assertions support correctness of tested cases rather than proving the entire program bug-free.')
heading('5.4 Evaluation of algorithms');table('Algorithm strengths and trade-offs',['Algorithm','Strength','Limitation and alternative'],[['Race loop','O(N) without events; each component inspectable','No within-lap physics; fractional segments add complexity'],['Event heap','Stable chronological processing, O(E log E) total removals','Current static input could be sorted once more simply'],['Paired Monte Carlo','Replayable common conditions; trial audit retained','Uncalibrated distributions; add sensitivity study before richer uncertainty'],['Bounded enumeration','Every legal candidate in declared grid scored','Off-grid optimum may be missed; coarse-to-fine heuristic needs exact baseline'],['Strict JSON','Exact keys and model validation reject ambiguous inputs','Schema evolution needs explicit migrations']],[1.35,2.65,2.85])
para('Monte Carlo does not make the model more realistic merely by repeating it. With common additive noise the strategy gap is unchanged unless another effect interacts with the plan. Random safety-car timing provides that interaction through pit loss. The reported88% in the captured100-trial example is an empirical frequency under the selected seed and probability, not a calibrated probability of real success.')
heading('5.5 Performance');para('Measured computational runs complete in seconds at the selected desktop scope. Increasing trial count approximately increases repeated work; increasing pit-lap choices can grow the search much faster because pairs of stop laps and compound sequences multiply. Limits protect the interface from uncontrolled enumeration. Worker cancellation is checked between trials/candidates, not in the middle of each lap. A single very long operation could therefore delay cancellation until its current simulation finishes, though laps are capped.')
heading('5.6 Robustness');para('The empty-object decoder failure demonstrates why testing must include structurally wrong but syntactically valid JSON. Checking each member did not validate the collection itself. The repair is narrow and the reproduction tests remain in the suite. Other checks cover finite numbers, types, boundaries and oversized files. The GUI refuses values it cannot represent at three decimal places rather than silently clamping a loaded scenario. Further testing should include native file-dialog cancellation, failed disk writes and target-machine scaling.')
heading('5.7 Usability');para('[FINAL USABILITY EVALUATION PENDING GENUINE USER TESTING]');para('Actual captures show labelled controls, graph axes, tabs and output tables. Automated tests check error recovery, invalidation and cancellation. These features appear appropriate for the task, but no recorded participant has demonstrated that the stop/event syntax or experiment controls are easy to understand. The scrollable panel may hide advanced actions below the initial view.')
heading('5.8 Stakeholder evaluation');para('[GENUINE STAKEHOLDER EVALUATION REQUIRED]');para('Use the questions and forms in Appendix F. Record requirements changed by feedback and link each decision to a genuine response. Candidate review of algorithms and centre approval are separate outstanding inputs.')
heading('5.9 Maintenance');md(part('docs/evaluation/review.md','## Maintenance issues','## Limitations'),'Maintenance issues and technical changes')
heading('5.10 Limitations');md(part('docs/evaluation/review.md','## Limitations and technically grounded improvements','No final mark'),'Limitations and improvements')
para('Severity is high for claims about real race predictions: uncalibrated parameters, missing traffic and no wet tyres can change the correct decision. Severity is moderate for educational use: lap-boundary events and a simplified SC model are acceptable if explained. GUI precision and temporary runtime packaging are practical deployment limitations rather than physics errors. Search bounds are intentional and must always accompany the recommendation.')
heading('5.11 Future improvements');para('First collect genuine feedback and validate installation on an intended user\'s machine. A dedicated stop/event editor can remove syntax mistakes without changing the model. Next, add wet/intermediate compounds only with a documented suitability matrix and schema migration. A non-linear wear model needs a credible calibration dataset and new independent arithmetic tests. A multi-car model or union of overlapping SC intervals should be a separate designed iteration because it changes event semantics. A coarse-to-fine search could reduce work, but must be compared with exact tiny-space results and report which regions were examined.')
heading('5.12 Final conclusion');para('PITWALL demonstrates decomposition, typed data, validation, deterministic state updates, priority queues, repeated simulation and constrained search in a working desktop application. The evidence supports an explainable prototype that compares strategies consistently under its assumptions. Final acceptance requires candidate explanation, genuine user evidence and review against the actual centre checklist. The model remains an educational simulation, not professional race engineering software.')

page();heading('6 Bibliography',1)
refs=[('R01','TUMFTM','Race simulation repository','https://github.com/TUMFTM/race-simulation','Existing-solution review recorded 8 September 2026'),('R02','FastF1 maintainers','FastF1 repository and README','https://github.com/theOehrly/Fast-F1','Existing-solution review recorded 8 September 2026'),('R03','Frontier','F1 Manager Belgian Grand Prix guide','https://www.f1manager.com/nl-NL/2023/grand-prixs/belgian-grand-prix','Publisher guide, existing review'),('R03b','Frontier','F1 Races Brought To Life','https://www.f1manager.com/features/new/levensechte-f1-races','Publisher feature article, existing review'),('R04','Python Software Foundation','heapq documentation','https://docs.python.org/3/library/heapq.html','Priority queues and stable tie-breaks'),('R05','Python Software Foundation','random documentation','https://docs.python.org/3/library/random.html','Local seeded generators'),('R06','The Qt Company','QThread documentation','https://doc.qt.io/qtforpython-6/PySide6/QtCore/QThread.html','Worker thread and signals'),('R07','Matplotlib contributors','Backends documentation','https://matplotlib.org/stable/users/explain/figure/backends.html','Embedding figures'),('R08','Python Software Foundation','statistics documentation','https://docs.python.org/3/library/statistics.html','Mean, median and population standard deviation')]
para('References use organisation, title and URL. Publication dates are not invented. Existing-system sources were reviewed after the prototype; technical documentation was checked during report preparation. No source is claimed as an original design influence before the recorded research date.')
for id,org,title,url,note in refs:para(f'[{id}] {org}. {title}. {url}. {note}. Access record: 8 September 2026.')
para('Primary project sources are the actual files cited throughout: docs/design, docs/iterations, source and test files, test-run XML/text/metadata, benchmark JSON, scenario JSON and screenshot capture records. Git timestamps are reproduced in Appendix G. The assistance declaration is maintained in docs/assistance-log.md and reproduced once in Appendix K.')

page();heading('7 Appendices',1);heading('Appendix A Source and class relationships')
para('Selected implementation extracts appear in Section 3. The full source remains in src/pitwall and is hash-indexed; repeating every GUI line would add bulk without improving the main argument. The following UML-style class relationships and complete core formulas supplement those extracts.')
uml=[(50,25,420,150,'RaceConfig\nlaps, circuit, driver, tyres\ntyre(name)'),(550,25,420,150,'Strategy\nstart, planned_stops\nvalidate_for(config)'),(1030,25,420,150,'Conditions\nweather, events, seed\nweather_loss(state)'),(50,360,420,160,'Circuit / Driver\nTyreCompound\nvalidated parameters'),(550,360,420,160,'PitStopPlan\nlap, compound\nstationary_time'),(1030,360,420,160,'RaceEvent / EventQueue\nlap, kind, payload\nat_lap(lap)'),(400,680,700,150,'LapResult <- EnvironmentalLapResult\nStrategyResult contains lap tuple\nScenario contains config, conditions, strategies')]
figure(diagram('classes.png',uml,[(0,3),(1,4),(2,5)]),'Core class relationships','shows containment arrows between real input classes. The named inheritance relationship is explicit in the lower box; attributes and methods are detailed in Section 2.3.')
code(read('src/pitwall/physics.py'),'Complete physics.py as inspected for this report')
heading('Appendix B Automated test inventory');table('Final collected cases',['Number','Test case','Outcome'],[(f'{i:03}',c.attrib.get('classname','')+'::'+c.attrib['name'],'PASS') for i,c in enumerate(cases,1)],[.55,5.7,.6])
heading('Appendix C Execution and failure evidence');para('The full final output is in '+final.parent.relative_to(ROOT).as_posix()+'/output.txt. The XML records86 cases without failure/error nodes. Each run\'s metadata retains command, timestamp and source hashes. Section 3.17 lists all preserved runs; the following final summary is verbatim.')
finalout=(final.parent/'output.txt').read_text();code('\n'.join(finalout.splitlines()[-5:]),'Final pytest output tail')
para('Failure source: '+failure.relative_to(ROOT).as_posix()+'. Complete traceback and source hashes remain untouched. Capture-harness diagnosis: docs/testing/FAIL-I17-02.md; its limitation is a transcript record rather than a separate raw terminal file.')
heading('Appendix D Full benchmark values');code(json.dumps(bench,indent=2),'Verbatim benchmark JSON values')
heading('Appendix E Research materials');para('Section 1.5 contains the three comparative reviews and their ADOPT, ADAPT, REJECT and LEARN decisions. The original record remains docs/analysis/research.md. These sources led to the following review exercises after implementation.');md(read('docs/testing/research-review-exercises.md'))
heading('Appendix F Stakeholder and candidate forms')
para('Stakeholder identifier: [GENUINE PARTICIPANT REQUIRED]\nDate and consent: [GENUINE EVIDENCE REQUIRED]\nRelevant experience: [GENUINE RESPONSE REQUIRED]')
for question in ['Which strategy decision do you want to explore?','Which race inputs can you explain?','Which result makes comparison easiest?','What confused you during the tasks?','Which simplification would make the output misleading?','What change should be prioritised and why?']:
    label('Question',question);para('[GENUINE RESPONSE REQUIRED]\n\n')
para('Candidate review record: file/algorithm reviewed; date; explanation in own words; change made if any; test actually executed; remaining uncertainty. [CANDIDATE FACTUAL INPUT REQUIRED]')
para('[TEACHER APPROVAL PENDING]\nCentre checklist supplied on: [PENDING]\nRequired declaration format: [CENTRE GUIDANCE REQUIRED]')
heading('Appendix G Git development summary');table('Genuine commits in chronological order',['Commit','Recorded timestamp','Subject'],[h.split('|',2) for h in history],[.8,1.8,4.25]);para('These commits are evidence of actual version history, not proof that each design file preceded every edit. The iteration records and tool conversation provide finer-grained sequence. Documentation cleanup changes present at report preparation are uncommitted and are not misrepresented as an extra commit.')
heading('Appendix H Evidence catalogue and completeness audit');para(f'The pre-report evidence index contains {len(index)} entries. Every listed file and SHA256 hash was checked before report generation. The index includes code, planning records and clearly labelled placeholders as well as captured output; {len(index)} entries does not mean that many screenshots or completed human studies. report/evidence-index.csv remains the full catalogue.')
auditrows=[]
for line in read('report/mark-audit.md').splitlines():
    if re.match(r'^\|\s*3\.',line):
        cells=[c.strip() for c in line.strip('|').split('|')]
        auditrows.append(cells)
assert len(auditrows)==25
table('Criterion completeness and remaining work',['Criterion','Section','Evidence used','Status','Remaining work'],auditrows,[1.15,.6,2.2,1.05,1.85])
para('The transcribed allocation is Analysis10, Design15, Developing the Coded Solution15, Testing to Inform Development10 and Evaluation20, total70. The actual Full Mark Criteria document was not found. [CENTRE CHECKLIST INTEGRATION REQUIRED]. Human investigation, usability, candidate review and final centre judgement remain the highest risks. No mark is awarded by this audit.')
heading('Appendix I JSON contract and example');para('Schema version1 requires config, conditions and strategies, with exact field sets. Enum values are stored as strings. Arrays are explicitly checked after the genuine fix. There is no standalone formal JSON Schema file; the contract is implemented in persistence.py and validated by model constructors. Search/Monte Carlo controls are stored in experiment exports, not the base scenario.');code(read('scenarios/dry-comparison.json'),'Actual dry-comparison.json example')
heading('Appendix J Additional application screenshots')
for filename,title,discussion in [('02-metrics.png','Actual comparison metrics','shows totals, stop count, average, fastest and slowest laps, pit loss and stint lengths.'),('03-laps.png','Actual lap records','shows the per-lap model components for inspection.'),('04-controls.png','Conditions and experiment settings','shows the scrollable environment controls; controls below the visible region require scrolling.'),('07-monte-carlo-results.png','Actual paired Monte Carlo summary','shows100 recorded trials; A wins88% under the chosen illustrative settings.'),('08-monte-carlo-chart.png','Actual Monte Carlo histogram','plots the same recorded trial totals with shared bins.')]:
    figure(shot/filename,title,discussion)
heading('Appendix K Development declaration');md(read('docs/assistance-log.md'),'Factual assistance record');para('The record is maintained separately at docs/assistance-log.md. Candidate follow-up must be completed factually; this report does not replace the centre\'s declaration process.')

# Populate figure/table lists using exact captions. Page references are supplied by Word TOC fields.
for anchor,entries in ((figure_list_anchor,figures),(table_list_anchor,tables)):
    for text in entries:
        p=anchor.insert_paragraph_before(text);p.style='Caption'
doc.core_properties.title='PITWALL OCR H446-03 NEA Master'
doc.core_properties.subject='Motorsport race strategy simulation and optimisation'
doc.core_properties.author='Mithil Katkoria'
doc.save(OUT/(NAME+'.docx'))
manifest={'figures':len(figures),'tables':len(tables),'headings':headings,'test_cases':len(cases),'runs':runs,'baseline_index_entries':len(index),'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'generated_utc':datetime.now(timezone.utc).isoformat()}
(WORK/'report-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({k:manifest[k] for k in ('figures','tables','test_cases','baseline_index_entries')}))
