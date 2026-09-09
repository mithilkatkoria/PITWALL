# Publication readiness and exact actions

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
