"""Refresh documentation hashes without rewriting captured evidence or Git history."""
from pathlib import Path
import csv,hashlib,sys
ROOT=Path(__file__).resolve().parents[2]
audit=ROOT/'report/mark-audit.md'
text=audit.read_text(encoding='utf-8')
if '| Current evidence |' in text:
    sections=['1.1-1.3','1.3','1.4; 5.8; App F','1.5','1.7','1.8; 5.10','1.9','1.10; 5.2','2.1','2.2-2.3','2.6','2.8-2.9','2.3-2.5; 2.7','2.10; 3','2.11; 4','3.1-3.15; App G','2.2-2.5; 3','3.6; 3.14','3.17; App B','3.16','4.1-4.5','5.2','5.7-5.8','5.9-5.10','5.11']
    lines=['# Provisional OCR/centre criteria audit','','Source: the checklist transcribed in the supplied brief. The separate Full Mark Criteria document has not been received. Section references refer to the PITWALL master DOCX/PDF. EVIDENCED means an artefact exists, not that its quality or authorship has been accepted. No marks are awarded.','','| Criterion | Document section | Evidence used | Status | Remaining work |','|---|---|---|---|---|']
    i=0
    for line in text.splitlines():
        if line.startswith('|3.'):
            cells=[c.strip() for c in line.strip('|').split('|')]
            status,sep,remaining=cells[3].partition(':')
            if not sep:remaining='Candidate review against the actual centre checklist.'
            if cells[0].startswith('3.4.2'):remaining+=' SC05 strict tolerance is not explicitly established; SC04, SC13 and SC14 remain partial.'
            lines.append('| '+' | '.join([cells[0],sections[i],cells[2],status,remaining.strip()])+' |');i+=1
    lines+=['','The brief allocates 15 marks to coded development and 10 to testing to inform development, but does not supply complete 3.3 subcriterion numbering. Integrate the actual centre checklist before final submission.']
    audit.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
audit.write_text(audit.read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
missing=ROOT/'report/missing-evidence.md'
text=missing.read_text(encoding='utf-8').replace('includes17','includes 17')
if 'SC05' not in text:
    text+='\nThe complete master DOCX/PDF now covers sections 1-7 and Appendices A-K. Remaining explicit verification gap: SC05 specifies 1e-9 seconds, whereas the recorded oracle uses default pytest.approx tolerance. The report marks this PARTIALLY MET. No test code was changed to close the gap.\n\nCandidate input belongs in section 1.4 (stakeholders), each section 3 iteration reflection, section 4.5 (genuine usability), sections 5.7-5.8 (human evaluation), Appendix F (factual forms) and Appendix K/the assistance log (actual follow-up). The centre checklist and declaration requirements remain pending.\n'
missing.write_text(text,encoding='utf-8',newline='\n')
p=ROOT/'report/evidence-index.csv'
with p.open(encoding='utf-8') as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
if '--final' in sys.argv:
    known={r['File'] for r in rows}
    paths=['report/PITWALL_Mithil_Katkoria_H446_NEA_MASTER.docx','report/PITWALL_Mithil_Katkoria_H446_NEA_MASTER.pdf','report/final-submission-trim-plan.md','report/documentation-cleanup.md','report/authoring/build_master.py','report/authoring/export_word.ps1','report/authoring/check_master.py','report/authoring/update_catalogue.py','report/authoring/architecture.png','report/authoring/classes.png','report/authoring/report-manifest.json','report/authoring/preservation-baseline.json','report/authoring/verification.json']
    for path in paths:
        if path not in known:rows.append({'Evidence ID':f'E{len(rows)+1:04}','Category':'Report output or reproducible authoring record','File':path})
for r in rows:
    data=(ROOT/r['File']).read_bytes();r['Bytes']=len(data);r['SHA256']=hashlib.sha256(data).hexdigest()
with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
print(f'Updated {len(rows)} index entries; no original entry removed.')
