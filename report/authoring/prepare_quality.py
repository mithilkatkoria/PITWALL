"""Assemble final quality records and blank human evidence packs from real results."""
from pathlib import Path
import csv,hashlib,json,re,shutil
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
def write(path,text):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8',newline='\n')
def read(path):return (ROOT/path).read_text(encoding='utf-8')
focused=sorted((ROOT/'evidence/test-runs').glob('TEST-SC05-*/results.xml'))[-1]
final=sorted((ROOT/'evidence/test-runs').glob('TEST-QUALITY-FINAL-*/results.xml'))[-1]
cases=list(ET.parse(final).getroot().iter('testcase'))
assert len(cases)==87 and all(c.find('failure') is None and c.find('error') is None for c in cases)
benchpath=sorted((ROOT/'evidence/benchmarks').glob('BENCH-COMPARE-*/timings.json'))[-1]
bench=json.loads(benchpath.read_text())
rel=lambda p:p.relative_to(ROOT).as_posix()
blank='[GENUINE RESPONSE REQUIRED]'
identity='Status: HUMAN INPUT REQUIRED. This form has not been completed.\n\nParticipant alias: [REQUIRED]\nSession date: [REQUIRED]\nRole/experience: [REQUIRED]\nConsent record held privately: [REQUIRED]\n\nUse an alias in project records. Keep identifying details and consent records in private-evidence/, outside the public release. Do not backdate a session or describe a post-prototype interview as original research.'
questions=['What race-strategy decisions would you want to explore?','Which race and tyre inputs make sense to you?','Which outputs would be most useful, and why?','What do you think the stop syntax 15:Medium means?','What is confusing or missing?','Which simplification could make the results misleading?','Which improvement matters most, and why?']
write('docs/stakeholder/initial-interview-form.md','# Stakeholder interview\n\n'+identity+'\n\nStage: [INITIAL OR POST-PROTOTYPE, RECORD ACTUAL STAGE]\n\n'+'\n\n'.join(f'{i}. {q}\n\n{blank}\n\nResponse space: ______________________________' for i,q in enumerate(questions,1)))
write('docs/stakeholder/requirements-followup.md','# Requirements follow-up\n\n'+identity+'\n\n| Response reference | Need in participant words | Existing FR / SC | Proposed change and reason | Priority from participant | Acceptance condition | Confirmed date |\n|---|---|---|---|---|---|---|\n| [REQUIRED] | [REQUIRED] | [REQUIRED] | [REQUIRED] | [REQUIRED] | [REQUIRED] | [REQUIRED] |\n\nAsk the participant to confirm this interpretation. Keep disagreement or rejected suggestions and explain the decision. Do not mark requirements agreed until agreement is recorded.')
write('docs/stakeholder/post-prototype-review.md','# Post-prototype review\n\n'+identity+'\n\nBuild/version shown: [REQUIRED]\nScenario used: [REQUIRED]\n\n1. What did the prototype help you understand?\n\n'+blank+'\n\n2. Which result or control was difficult to interpret?\n\n'+blank+'\n\n3. Which single improvement should be prioritised? Why?\n\n'+blank+'\n\n4. After an implemented change, did it solve the reported difficulty? Record the actual follow-up date and version.\n\n'+blank)
tasks=['Launch PITWALL.','Configure a short five-lap race.','Create two named strategies.','Add a valid stop after lap 2.','Compare both strategies.','Identify the faster plan and its time advantage.','Explain the pit spike on the graph.','Enter a stop after the final lap and interpret the error.','Add an event and explain when it takes effect.','Run a 100-trial Monte Carlo experiment.','Explain what the win percentage means.','Start optimisation and cancel it; describe the feedback and whether further input is possible.','Save a scenario.','Change a setting, then reload the scenario and check the restored inputs.']
write('docs/usability/usability-task-sheet.md','# Usability task sheet\n\nStatus: PLANNED. No completed session is claimed. Use participant aliases and record build, machine, display scale and date on the observation form. Explain that PITWALL is an illustrative simulator. Let the user attempt each task; record any hints rather than silently coaching.\n\n'+'\n\n'.join(f'{i}. {t}' for i,t in enumerate(tasks,1))+'\n\nFor task 12, if work finishes before cancellation is attempted, record that fact. Do not label it a successful cancellation observation. Use a larger legal search for another attempt and record the changed settings. Timing is optional and must be measured live, never estimated afterwards.')
write('docs/usability/usability-observation-form.md','# Usability observations\n\n'+identity+'\n\nBuild: [REQUIRED]\nDevice / OS / display scale: [REQUIRED]\nScenario / settings: [REQUIRED]\nObserver alias: [REQUIRED]\n\n| Task | Completion | Mistakes | Confusion | Help required | Measured seconds or Not measured | Verbatim comment |\n|---|---|---|---|---|---|---|\n'+'\n'.join(f'| {i} | [PENDING] | [PENDING] | [PENDING] | [PENDING] | [PENDING] | [PENDING] |' for i in range(1,15))+'\n\nSC04 error meaning in participant words: [PENDING]\nSC14 response/cancellation observations, with task settings: [PENDING]')
write('docs/usability/usability-summary-template.md','# Usability summary\n\nStatus: HUMAN INPUT REQUIRED. Do not summarise unused forms as results.\n\nCompleted session references: [REQUIRED]\nNumber of genuine participants: [REQUIRED]\n\n| Finding and observed task | Evidence / quotation reference | Effect on SC04 / SC08 / SC14 | Proposed change | Retest result |\n|---|---|---|---|---|\n| [REQUIRED] | [REQUIRED] | [REQUIRED] | [REQUIRED] | [PENDING] |\n\nDescribe disagreements, assistance provided and session limitations. Distinguish an observed problem from a proposed improvement. Update evaluation only after the evidence exists.')
write('docs/candidate/candidate-reflection-template.md','# Candidate iteration reflection\n\nStatus: CANDIDATE INPUT REQUIRED. Complete a copy for each genuine recorded stage; keep the real review date. A present-day explanation is not a historical diary entry.\n\nCandidate: Mithil Katkoria\nIteration / files: [REQUIRED]\nDate personally reviewed: [REQUIRED]\n\n'+ '\n\n'.join(q+'\n\n[CANDIDATE FACTUAL INPUT REQUIRED]' for q in ['What did you personally review, change or test?','Explain the code choice in your own words.','Which recorded test did you inspect or actually run? Give its evidence ID.','What worked well, based on that evidence?','What was difficult for you personally? If nothing is recalled, say so.','Which alternative can you explain and why would you choose it?','What limitation or uncertainty remains?','Which stakeholder response, if any, affected this stage?','Which assistance was used and what can you now explain independently?']))
areas=[('Tyre degradation','physics.py: degradation'),('Fuel model','physics.py: fuel_effect'),('Pit-stop semantics','engine.py: simulate'),('Race loop','engine.py: simulate'),('Event heap','events.py: EventQueue'),('Weather state','conditions.py; engine.py'),('Safety-car model','conditions.py; engine.py'),('Random seed','engine.py; conditions.py'),('Monte Carlo','monte_carlo.py'),('Statistics','monte_carlo.py: describe'),('Bounded candidate generation','optimiser.py: candidates'),('Optimisation','optimiser.py: optimise'),('Persistence','persistence.py'),('GUI worker and cancellation','advanced_gui.py'),('Validation','models.py; persistence.py; gui.py')]
write('docs/candidate/algorithm-understanding-check.md','# Algorithm understanding check\n\nStatus: CANDIDATE INPUT REQUIRED. Every item is incomplete until Mithil records a genuine explanation and date. Source paths below are relative to src/pitwall/.\n\n'+'\n\n'.join('## '+area+'\n\nSource: '+source+'\nReview date: [PENDING]\nStatus: INCOMPLETE\n\n'+'\n'.join('- '+q+': [CANDIDATE EXPLANATION REQUIRED]' for q in ['What it does','Why it exists','Inputs','Outputs','Algorithm steps','Data structure','Edge case and expected result','Alternative','One limitation']) for area,source in areas))
write('docs/design/design-provenance.md','''# Design provenance

## Original or recorded design

The I01-I17 design files and actual Git history are retained. Their existence alone does not prove every paragraph preceded every edit. Run metadata supplies source hashes at execution time; seven same-day commits provide coarse checkpoints. The report distinguishes the documented combined stages and actual order.

## Post-implementation architecture documentation

Implemented-structure diagrams and the master report class inventory were derived from current source. They explain the completed program and are not original wireframes. Existing-system research is a post-prototype review, with its later timing retained.

## New prospective design

No feedback-driven software iteration is claimed. When a genuine response identifies a need, record its alias and evidence reference, update the requirement, write design and test expectations before coding, implement one justified change, run tests, retain any actual failures and request a real follow-up review. Candidate reflection must use the real dates. The final computational verification plan is separate from such an iteration.
''')
write('docs/testing/final-quality-results.md',f'''# Final quality verification

SC05 focused run: {rel(focused.parent)}. One test passed. Absolute tolerance is 1e-9 seconds with no relative component. Every recorded lap and cumulative value had zero difference from its expected Python float value; this is not a claim of infinite decimal precision. The test also checks total time and deterministic replay.

Full regression: {rel(final.parent)}. All 87 collected cases passed. The old 86-case run and both I17 failing assertions remain preserved.

Comparison-only measurements: {rel(benchpath)}. Five repeats after one warm-up per size. Input construction and GUI drawing are excluded. No new speed threshold was invented. Raw output, environment, command and source hashes are retained.

| Strategies | Laps | Minimum s | Maximum s | Mean s | Median s |
|---|---|---|---|---|---|
'''+ '\n'.join(f"| {r['strategies']} | {r['race_laps']} | {r['minimum']:.9f} | {r['maximum']:.9f} | {r['mean']:.9f} | {r['median']:.9f} |" for r in bench['measurements'])+'\n\nSC05 and the missing SC13 computational evidence are now satisfied for the tested cases. SC04 and SC14 still need genuine human evidence. No application source was changed and no new feedback-driven iteration was fabricated.')
review=read('docs/evaluation/review.md')
review=re.sub(r'^\| SC05 .*$', '| SC05 | FULLY MET | Explicit absolute 1e-9-second oracle passes for every lap, cumulative time and total; exact replay passes. See docs/testing/final-quality-results.md |',review,flags=re.M)
review=re.sub(r'^\| SC13 .*$', '| SC13 | FULLY MET | Original search/Monte Carlo targets passed; separate five-repeat comparison timings now recorded. GUI latency and other machines remain outside these measurements. See docs/testing/final-quality-results.md |',review,flags=re.M)
write('docs/evaluation/review.md',review)
log=read('docs/assistance-log.md')
if 'final quality pass' not in log:log=log.replace('\nSource review', '\n| 2026-09-08, final quality pass | Added explicit tolerance verification and comparison benchmark; prepared blank human forms, final report and local release files | `tests/test_sc05_tolerance.py`, `scripts/benchmark_comparison.py`, `docs/`, `report/`, public packaging | Candidate requested quality pass; personal explanations, human sessions and centre approval remain pending |\n\nSource review')
write('docs/assistance-log.md',log)
write('report/missing-evidence.md','''# Remaining evidence and approvals

- Genuine stakeholder responses and requirements follow-up: docs/stakeholder/. Record actual post-prototype timing.
- Genuine usability sessions, especially SC04 error interpretation and SC14 responsiveness/cancellation: docs/usability/.
- Candidate explanations and dated reflection: docs/candidate/. All 15 understanding topics remain incomplete.
- A genuine feedback-driven prospective iteration, only when feedback justifies a change. No iteration is invented now.
- The candidate's separate Full Mark Criteria file was not located in the workspace or attachments. Official OCR content and marking bands were checked; centre-specific additions still need integration.
- Teacher/centre approval, candidate authentication and required declaration format.
- Publication permission covering timing, assessed work, stakeholder privacy and any centre-only material. No repository or release has been published.
- Target-user installation, display scaling, GUI latency and independent real-race calibration remain unverified limitations.

Resolved technical gaps: SC05 explicit 1e-9-second assertions and SC13 separate comparison measurements now have genuine passing/output records. SC04 and SC14 remain PARTIALLY MET. The master report contains precise placeholders in 1.4, iteration reflections, 4.5, 5.7-5.8 and Appendix F. The factual assistance log remains in docs/assistance-log.md.
''')
entries=[
('3.1.1(a)','Computational problem','1.1-1.3','Requirements and model explanation','STRONG','Candidate justification unverified','Explain repeated scenario evaluation and parameter trade-offs','Review only','Candidate'),
('3.1.1(b)','Computational approach','1.3','Decomposition, state and iteration','STRONG','Personal reasoning missing','Complete understanding check','Review only','Candidate'),
('3.1.2(a)','Stakeholders','1.4; 5.8','Relevant groups and blank interviews','HUMAN INPUT REQUIRED','Needs not confirmed by real people','Conduct interview and requirements follow-up','Forms prepared','Stakeholder'),
('3.1.3(a)','Research','1.5','Three cited post-prototype reviews','PARTIAL','Later research cannot explain original choices','Candidate review; use future findings prospectively','Provenance fixed','Candidate'),
('3.1.3(b)','Essential features','1.7','FR01-FR12 with rationale','STRONG','User priorities provisional','Confirm requirements with stakeholder','Technical mapping complete','Stakeholder'),
('3.1.3(c)','Limitations','1.8; 5.10','Model and deployment limits','STRONG','User impact unconfirmed','Discuss real user consequences','Technical review complete','Candidate'),
('3.1.4(a)','Requirements','1.9','Runtime, hardware and benchmark environment','STRONG','Target device untested','Validate on intended user machine','Current environment checked','Human'),
('3.1.4(b)','Success criteria','1.10; 5.2','SC01-SC14 and explicit evidence','STRONG','User acceptance pending','Confirm success criteria with stakeholder','SC05/SC13 resolved','Stakeholder'),
('3.2.1(a)','Decomposition','2.1','Problem and component breakdown','STRONG','Candidate reasoning pending','Explain boundaries and state','Documentation complete','Candidate'),
('3.2.2(a)','Structure','2.2-2.3','Current-source architecture and models','PARTIAL','Some documentation retrospective','Preserve labels; prospective design only after feedback','Provenance complete','Candidate and stakeholder'),
('3.2.2(b)','Algorithms','2.6','A01-A14 and source extracts','STRONG','Personal algorithm defence pending','Complete all 15 understanding topics','Technical mapping complete','Candidate'),
('3.2.2(c)','Usability design','2.8-2.9','GUI captures, labels, validation and worker design','PARTIAL','No audience review','Run task sheet and act on actual findings','Forms prepared','Human'),
('3.2.2(d)','Data and validation','2.3-2.5; 2.7','Typed models, variables, strict schema','STRONG','Candidate explanation pending','Explain edge cases and alternatives','87 tests pass','Candidate'),
('3.2.3(a)','Test data','2.10-2.11; 4','Recorded stage plans and final quality plan','STRONG','Human usability unperformed','Complete planned human tasks','Computational work complete','Human'),
('3.3.1(a)','Iterative process','3.1-3.15; App G','Recorded stages, source, seven commits','CANDIDATE INPUT REQUIRED','Personal reflection/authorship not established','Complete dated factual reflections','Cannot supply personal history','Candidate'),
('3.3.1(b)','Prototypes','3.6; 3.14','First and advanced genuine GUI captures','STRONG','Not every stage has a screenshot','Explain preserved versions; do not fabricate missing captures','Existing evidence integrated','Candidate'),
('3.3.2(a)','Development tests','3.17; App B','17 original runs plus two new runs','STRONG','Candidate rationale pending','Explain meaningful expected results','19 runs indexed','Candidate'),
('3.3.2(b)','Remedial action','3.16','I17 JSON failure, remedy, retest and regression','STRONG','Candidate understanding pending','Explain empty-container cause and remedy','Original failure retained','Candidate'),
('3.4.1(a)','Final robustness','4.1-4.4','87 passing cases and genuine timings','STRONG','Finite tests cannot prove absence of defects','Review coverage limits','Computational gaps closed','Candidate review'),
('3.4.1(b)','Usability tests','4.5','Blank 14-task protocol','HUMAN INPUT REQUIRED','No participant results','Run sessions and preserve observations','Forms only','Human'),
('3.4.2(a)','Success evaluation','5.2','Criterion evidence and explicit judgements','PARTIAL','SC04/SC14 and human acceptance pending','Update after real sessions','SC05/SC13 updated','Human and candidate'),
('3.4.3(a)','Usability effectiveness','5.7-5.8','Real captures and automated GUI tests','HUMAN INPUT REQUIRED','Appearance is not proof of ease of use','Evaluate observed task outcomes','Cannot invent observations','Human'),
('3.4.4(a)','Maintenance','5.9','Six concrete module/change concerns','STRONG','Personal judgement pending','Explain consequences and regression needs','Technical review complete','Candidate'),
('3.4.4(b)','Further development','5.10-5.11','Eight limitations and possible changes','STRONG','Priorities not user-confirmed','Choose one only after actual feedback','No speculative implementation','Stakeholder and candidate')]
source='Official OCR H446 specification downloaded 8 September 2026: https://www.ocr.org.uk/Images/170844-specification-accredited-a-level-gce-computer-science-h446.pdf . Content pages 13-14 (PDF 19-20) and marking grids 22-25 (PDF 28-31) were checked. The downloaded document has version 3.0/2026 content headers and retained 2.6/2023 grid headers. The separate centre Full Mark Criteria document was not located. This audit cannot claim integration of unseen centre additions.'
lines=['# Final criteria audit','',source,'','Status describes available evidence, not awarded marks. COMPLETE is reserved for finished technical actions. STRONG still requires candidate authentication and centre judgement. No full-marks promise is made.','','| Criterion | Current evidence | Document section | Current strength / status | Current risk | Exact action | Automatic work | Human input |','|---|---|---|---|---|---|---|---|']
for ident,name,section,evidence,status,risk,action,auto,human in entries:lines.append('| '+' | '.join([ident+' '+name,evidence,section,status,risk,action,auto,human])+' |')
lines+=['','## Marking-band review','','Analysis (10): technical rationale and research exist; authentic needs and candidate reasoning remain the priority. Design (15): algorithms and data are explained; historical timing is qualified. Coded development (15): modular source and real chronology exist; personal review is missing. Development testing (10): genuine runs and justified JSON remedy remain. Evaluation testing (5): final computational checks exist, human sessions do not. Evaluation of solution (15): criterion judgements and technical improvements exist; usability conclusions remain provisional. These are review findings, not scores.','','## Completed technical actions','','COMPLETE: explicit SC05 test; separate SC13 benchmark; full 87-case regression; eight blank human packs; design provenance labels; official OCR numbering correction; local portfolio packaging. No application feature was added.','','## Centre and publication gates','','TEACHER INPUT REQUIRED: supply/identify the actual centre checklist, confirm authentication and declaration requirements, and approve publication. HUMAN INPUT REQUIRED: confirm privacy and permissions for any future completed forms. No centre source document is redistributed.']
write('report/FINAL_CRITERIA_AUDIT.md','\n'.join(lines))
write('report/mark-audit.md','# OCR criterion mapping\n\n'+source+'\n\nSee FINAL_CRITERIA_AUDIT.md for strengths, risks, actions and responsibility. Earlier separate 3.2.3(b) was a brief subdivision; official 3.2.3(a) covers both test phases. Official 3.3.1 and 3.3.2 numbering is now integrated.\n\n| Criterion | Document section | Evidence used | Status | Remaining work |\n|---|---|---|---|---|\n'+'\n'.join('| '+' | '.join([i+' '+n,s,e,st,a])+' |' for i,n,s,e,st,r,a,au,h in entries))
write('docs/analysis/final-review-impact.md','''# Post-prototype review and next decisions

The problem is to compare complete race plans, not merely select the fastest fresh tyre. A faster compound may lose its advantage through wear or an additional pit stop. PITWALL keeps a common race configuration, evaluates each racing lap and ranks accumulated times so a user can inspect that trade-off.

Computation is useful because the same arithmetic must be applied consistently across many lap and stop combinations. Decomposition separates input validation, lap components, state transitions and result comparison. A priority queue preserves chronological events and deterministic ties. Bounded enumeration gives a checkable best plan inside an explicit search space. Seeded trials help explore variation but cannot calibrate the model by repetition alone.

The three existing-system reviews were recorded after the prototype. Their value is in reviewing scope: TUM's richer simulator highlights PITWALL's single-car simplification; FastF1 highlights the need for provenance before using real data; F1 Manager suggests clearer presentation but is not evidence for physical parameters. These findings support review exercises and possible future changes, not a rewritten claim that they created the original design. Genuine participant priorities are still required before choosing a new feature.
''')
write('docs/portfolio-description.md','''# Portfolio description

PITWALL is a Python/PySide6 motorsport race-strategy simulator that models tyre degradation, pit stops, weather and safety-car conditions, compares strategies, runs seeded Monte Carlo experiments and performs bounded strategy optimisation.

The desktop application combines an inspectable lap-by-lap model with charts, scenario persistence and background experiments. Immutable data models and strict validation separate the simulation from its interface. A stable event heap processes changing conditions, paired seeded trials explore uncertainty, and bounded enumeration compares legal stop plans. Automated tests include independent arithmetic examples, boundary cases, reproducibility, persistence and GUI integration. The model uses illustrative parameters and is intended for educational exploration rather than real race prediction.
''')
write('LICENSE','''MIT License

Copyright (c) 2026 Mithil Katkoria

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''')
write('docs/licensing.md','# Licensing scope\n\nThe MIT licence applies to original PITWALL software and original documentation only, to the extent the copyright holder has the rights to license them. It does not relicense third-party packages, OCR/centre documents, quoted external material, stakeholder responses or teacher comments. Dependencies retain their own licences and are installed separately. The NEA PDF is provided for educational/portfolio reference only; no licence to third-party material is granted. Centre publication approval remains pending.')
ignore=read('.gitignore')
write('.gitignore',ignore+'\n# Private records and local report/release working files\n.env\n.env.*\n!.env.example\n*.pem\n*.key\nprivate-evidence/\n**/completed-private/\nreport/public-release/\nreport/authoring/render*/\n.venv-public-check/\n')
write('NEA/README.md','# PITWALL NEA document\n\nThis document relates to the PITWALL race-strategy simulator and is prepared for educational and portfolio reference. Project assumptions and limitations are documented in the report. Source code is included in this repository.\n\nThe PDF is staged locally; public publication is pending teacher/centre permission. It contains no completed stakeholder or consent forms. Genuine human evidence and candidate authentication remain outstanding. See docs/assistance-log.md for the factual development record and docs/licensing.md for licensing scope.')
write('docs/release-v1.0.0.md','''# PITWALL v1.0.0

Release status: prepared locally, not published.

PITWALL compares motorsport race strategies in a Python/PySide6 desktop application. Features include tyre and fuel calculations, ordered pit stops, weather and safety-car events, seeded paired Monte Carlo trials, bounded optimisation, charts, strict JSON scenarios and cancellable workers.

Install Python 3.14 on Windows, create a short-path virtual environment, install requirements-lock.txt and run main.py as described in README.md. The recorded full suite passes 87 cases.

Known limitations: illustrative uncalibrated parameters, single-car free track, dry compounds only, simplified safety-car state, constrained search and uncompleted genuine user testing. Other operating systems and native ARM Python have not been verified.

Do not attach or publish the NEA PDF until centre/teacher publication permission and privacy review are confirmed.
''')
readme=read('README.md')
readme=readme.replace('## Main features','## Features').replace('## Technical architecture','## Architecture').replace('## Usage','## Running').replace('## Project documentation','## Project Documentation')
readme=readme.replace('**86 tests**','**87 tests**').replace('The development workspace\'s local `.venv` has an incomplete GUI dependency installation; use the short-path environment above.','Use the short-path environment above if Qt installation fails in a deeply nested workspace.')
readme=readme.replace('Git attributes preserve exact file bytes across Windows checkouts. Rebuild indexes after new evidence with `scripts/build_index.py` using the same Python runtime.','The original development evidence is retained separately. The new comparison benchmark is `scripts/benchmark_comparison.py`; it measures computation without GUI rendering.')
intro,rest=readme.split('## Screenshots',1);intro=intro.replace('PITWALL is a Python','## Overview\n\nPITWALL is a Python',1)
sections={'Screenshots': '## Screenshots'+rest}
parts=re.split(r'(?m)^## ',intro+sections['Screenshots']); lead=parts[0]; partsmap={p.split('\n',1)[0]:p.split('\n',1)[1] for p in parts[1:]}
partsmap['How It Works']='\nInputs are validated and converted into immutable models. The engine advances one lap at a time, applies scheduled conditions, calculates time components and records each result. Comparison ranks total times; experiments repeat this same model. Pit stops happen after their numbered racing lap, while events happen before it.\n'
partsmap['Example Scenarios']='\nLoad [dry comparison](scenarios/dry-comparison.json) to explore different stop plans. Other JSON files in [scenarios](scenarios/) demonstrate saved inputs. Scenario values are illustrative.\n'
partsmap['Project Documentation']='\nThe [NEA document](NEA/README.md), [architecture](docs/design/implemented-structure.md) and [technical evaluation](docs/evaluation/review.md) explain the project. Development records, source references and required declarations are maintained in the documentation, including the [assistance log](docs/assistance-log.md).\n'
partsmap['Licence']='\nOriginal PITWALL software is available under the [MIT License](LICENSE). See [licensing scope](docs/licensing.md) for exclusions.\n'
partsmap['Algorithms']=partsmap['Algorithms'].replace('The [algorithm index](report/master-evidence-pack.md#algorithm-index) links to pseudocode, assumptions and complexity notes.','Pseudocode and complexity notes are in [design records](docs/design/architecture.md).')
partsmap['Testing']=re.sub(r'See \[test results\].*?\.', 'See [final verification](docs/testing/final-quality-results.md).',partsmap['Testing'])
readme=lead+'\n'.join('## '+name+'\n'+partsmap[name].strip()+'\n' for name in ['Overview','Features','Screenshots','How It Works','Algorithms','Architecture','Installation','Running','Testing','Example Scenarios','Limitations','Project Documentation','Licence'])
shots=ROOT/'evidence/screenshots/FIG-I16-20260908T213427339706Z'
(ROOT/'screenshots').mkdir(exist_ok=True)
for old,new in [('01-comparison.png','comparison.png'),('08-monte-carlo-chart.png','monte-carlo.png')]:
    shutil.copy2(shots/old,ROOT/'screenshots'/new);readme=readme.replace('evidence/screenshots/FIG-I16-20260908T213427339706Z/'+old,'screenshots/'+new)
write('README.md',readme)
write('report/authoring/quality-manifest.json',json.dumps({'focused':rel(focused),'final':rel(final),'comparison':rel(benchpath),'test_count':87,'ocr_criteria_count':24},indent=2))
print('Prepared eight blank human packs, 24-criterion audit and local publication documents.')
