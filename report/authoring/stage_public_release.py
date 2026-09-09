"""Create a local allowlisted publication copy; never publish or rewrite history."""
from pathlib import Path
import csv,hashlib,json,re,shutil
import xml.etree.ElementTree as ET
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
stage=ROOT/'report/public-release/PITWALL';stage.mkdir(parents=True,exist_ok=True)
pdf=ROOT/'report/PITWALL_Mithil_Katkoria_H446_NEA_FINAL_MASTER.pdf'
target=ROOT/'NEA/PITWALL_Mithil_Katkoria_H446_NEA.pdf'
shutil.copy2(pdf,target)
paths=[ROOT/p for p in ['README.md','LICENSE','.gitignore','.gitattributes','requirements.txt','requirements-lock.txt','pytest.ini','main.py','launch.ps1']]
for directory in ['src','tests','scenarios','docs','screenshots','NEA','scripts']:
    paths.extend(p for p in (ROOT/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts and 'completed-private' not in p.parts)
assert not (stage/'.git').exists(), 'Do not replace a publication checkout with local staging.'
for p in paths:
    dest=stage/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
# PDF is staged but cannot be accidentally added by the documented private-source workflow.
ignore=stage/'.gitignore'
ignore.write_text(ignore.read_text()+'\n# Publication approval required before including assessed work\nNEA/*.pdf\n# Fresh execution output stays local in the public source checkout\nevidence/\n',encoding='utf-8',newline='\n')
issues=[]
signatures=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{30,}',r'AKIA[A-Z0-9]{16}',r'sk-[A-Za-z0-9]{35,}',r'[A-Z]:[\\/]Users[\\/]']
for p in stage.rglob('*'):
    if not p.is_file():continue
    if p.suffix.lower()=='.pdf':text='\n'.join(pg.extract_text() for pg in PdfReader(p).pages)
    elif p.suffix.lower() in {'.png','.jpg','.jpeg'}:continue
    else:
        try:text=p.read_text(encoding='utf-8')
        except UnicodeDecodeError:issues.append(str(p.relative_to(stage))+': unexpected binary');continue
    if any(re.search(s,text) for s in signatures):issues.append(str(p.relative_to(stage))+': review matched path/credential pattern')
# Validate the public README links to local files and screenshots.
for match in re.finditer(r'\]\(([^)]+)\)',(stage/'README.md').read_text()):
    link=match.group(1)
    if not link.startswith(('http:','https:','#')) and not (stage/link.split('#')[0]).exists():issues.append('README missing link: '+link)
assert not issues,issues
manifest=[{'path':p.relative_to(stage).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(stage.rglob('*')) if p.is_file()]
(ROOT/'report/final-authoring/public-files.json').write_text(json.dumps(manifest,indent=2))
text='''# Publication readiness and exact actions

Status: LOCAL FILES PREPARED. No GitHub repository, tag or release has been created. No remote was configured in the original repository. Public publication is not approved.

The allowlisted copy is report/public-release/PITWALL. It contains README.md, LICENSE, .gitignore, requirements.txt, requirements-lock.txt, main.py, launch.ps1, src/, tests/, scenarios/, docs/, screenshots/, NEA/, plus scripts/, pytest.ini and .gitattributes. Its original code bytes match the evidence repository. The staged PDF is a byte-for-byte copy of the final master and is ignored by Git until approval. The source repository's existing history is untouched.

Excluded from the publication copy: original .git history, raw evidence/ (including local paths in execution commands), old report versions, report authoring/render files, virtual environments/caches, environment files/keys, private-evidence/, completed-private/ and all third-party OCR/centre documents. Original evidence remains preserved locally. The included human forms are blank; no stakeholder identities, contact details, consent records or teacher comments were supplied. Pattern scanning found no credential signatures or absolute user-profile paths in the allowlisted files. This is a bounded scan, not a guarantee about future additions.

## Optional private repository now

Run these from the original PITWALL directory only after reviewing the staging manifest:

```powershell
Set-Location report/public-release/PITWALL
git init -b main
git add -- README.md LICENSE .gitignore .gitattributes requirements.txt requirements-lock.txt pytest.ini main.py launch.ps1 src tests scenarios docs screenshots scripts NEA/README.md
git diff --cached --check
git diff --cached --stat
git commit -m "Prepare PITWALL portfolio source"
gh repo create PITWALL --private --source . --remote origin --push
```

These commands create a new publication copy, not a rewrite of the original development repository. The assistance log remains included. Do not run git add -f on the NEA PDF yet.

## Public publication gate

The candidate must confirm all four points before changing visibility: teacher/centre permits publication before marking/submission; assessed NEA may be published; no private stakeholder information is included; no centre-only material is redistributed improperly. Retain the real approval privately. If any answer is unknown, keep the repository private and the PDF local.

After confirmation, in the publication checkout:

```powershell
git add -f -- NEA/PITWALL_Mithil_Katkoria_H446_NEA.pdf
git commit -m "Add approved NEA portfolio document"
git push origin main
gh repo edit --visibility public --accept-visibility-change-consequences
git tag -a v1.0.0 -m "PITWALL v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 NEA/PITWALL_Mithil_Katkoria_H446_NEA.pdf --verify-tag --title "PITWALL v1.0.0" --notes-file docs/release-v1.0.0.md --draft
```

Review the draft release and update its prepared-status wording before publishing it through GitHub. Do not attach the NEA PDF without permission. Commands assume authenticated gh, installed Git and an available repository name; if the name is already taken, resolve the exact destination first.
'''
(ROOT/'report/PUBLICATION_READINESS.md').write_text(text,encoding='utf-8',newline='\n')
# Keep every old catalogue row and append new factual documentation and evidence.
testcsv=ROOT/'report/test-results.csv'
with testcsv.open(encoding='utf-8') as f:r=csv.DictReader(f);testfields=r.fieldnames;testrows=list(r)
ids={r['Test ID'] for r in testrows}
for pattern,prefix in [('TEST-SC05-*','TEST-SC05'),('TEST-QUALITY-FINAL-*','TEST-QUALITY')]:
    xml=sorted((ROOT/'evidence/test-runs').glob(pattern+'/results.xml'))[-1]
    for i,case in enumerate(ET.parse(xml).getroot().iter('testcase'),1):
        ident=f'{prefix}-{i:03}'
        if ident in ids:continue
        assert case.find('failure') is None and case.find('error') is None
        testrows.append(dict(zip(testfields,[ident,'Final quality verification','SC05' if prefix=='TEST-SC05' else 'SC01-SC14 computational checks',case.attrib['name'],case.attrib.get('classname','')+'::'+case.attrib['name'],'Assertions in referenced test source','Assertions passed','PASS',xml.relative_to(ROOT).as_posix(),'N/A: no new failure','Recorded execution'])))
with testcsv.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=testfields,lineterminator='\n');w.writeheader();w.writerows(testrows)
catalogue=ROOT/'report/evidence-index.csv'
with catalogue.open(encoding='utf-8') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
known={r['File'] for r in rows}
new=[p for directory in ['docs','tests','scripts','screenshots','NEA','evidence'] for p in (ROOT/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
new += [ROOT/'README.md',ROOT/'LICENSE',ROOT/'report/FINAL_CRITERIA_AUDIT.md',ROOT/'report/PUBLICATION_READINESS.md',pdf,pdf.with_suffix('.docx')]
new += list((ROOT/'report/authoring').glob('*quality*.py'))+[ROOT/'report/authoring/build_final_master.py',ROOT/'report/authoring/export_final_word.ps1',Path(__file__)]+list((ROOT/'report/final-authoring').glob('*.json'))
for p in sorted(set(new)):
    name=p.relative_to(ROOT).as_posix()
    if name not in known:rows.append({'Evidence ID':f'E{len(rows)+1:04}','Category':'Final quality evidence or documentation','File':name});known.add(name)
for row in rows:
    data=(ROOT/row['File']).read_bytes();row['Bytes']=len(data);row['SHA256']=hashlib.sha256(data).hexdigest()
with catalogue.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
print(json.dumps({'staged_files':len(manifest),'catalogue_entries':len(rows),'scan_issues':issues,'published':False}))
