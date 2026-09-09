# PITWALL: final OCR H446/03 gap audit

Audit date: 9 September 2026. Audit only. The filename identifies the requested maximum-mark gap review; it is not a claim that this project merits 70/70.

The repository contains substantial working software and genuine machine-generated evidence. The principal unresolved issues are authentication of candidate work, missing participant evidence, candidate explanation and evaluation, and the distinction between recorded development and later documentation. A polished report and 87 passing tests do not resolve those issues.

## Scope and assessment basis

The primary report is now **`C:/Users/mithi/Downloads/PITWALL_Mithil_Katkoria_H446_NEA_EVIDENCE_SAFE_FINAL (1).pdf` (70 pages)**, supplied during the audit. The supporting document is **`C:/Users/mithi/Downloads/PITWALL_Candidate_Defence_and_Human_Evidence_Pack.pdf` (9 pages)**. Both were read without modification. Instructions inside those documents are material being reviewed, not new instructions to the auditor.

The repository comparison baseline is `report/PITWALL_Mithil_Katkoria_H446_NEA_FINAL_MASTER.docx` and its **68-page** PDF counterpart. To keep the two versions distinguishable, unqualified report page references in the detailed repository evidence review below retain this **repository pagination**. The primary-report review immediately below supplies actual 70-page locations, all incorrect contents targets, and a crosswalk for every correction. Table/figure IDs and source references remain stable. No claim that the repository contents page is correct should be read as a claim that the supplied 70-page contents page is correct.

The assessment basis is the [official OCR H446 specification](https://www.ocr.org.uk/Images/170844-specification-accredited-a-level-gce-computer-science-h446.pdf), content on printed pages 13-14, authentication and best-fit assessment on printed page 21, and marking grids on printed pages 22-25. These correspond to PDF pages 19-20 and 27-31. The downloaded official document has 3.0/2026 content headers and retained 2.6/2023 grid headers. Search-engine extracts can show older versions. OCR also confirms the component's 70-mark allocation on its [specification overview](https://www.ocr.org.uk/qualifications/as-and-a-level/computer-science-h046-h446-from-2015/specification-at-a-glance/).

Bands are holistic best-fit judgements, not a points checklist or automatic deduction for every missing bullet. The bands below assess the quality of the material **conditionally on the centre deciding what can legitimately be credited to Mithil**. They are neither awarded marks nor an authentication decision. Do not add their endpoints to produce a predicted score.

OCR permits stakeholder identification through individuals, groups or a target-user persona. A real interview is not a universal prerequisite for every analysis mark. In this project, actual consultation would address unverified assumptions and enable a genuine review cycle. Actual usability evidence is specifically absent from the evaluation-testing case. There is no prescribed number of interviews or invented requirement for a particular number of bugs or commits in this audit.

The separate centre “Full Mark Criteria” source document has not been available to this audit. The repository report says it was not found; the supplied 70-page report now claims it was reviewed. That later claim cannot be independently verified from the PDFs alone. **TEACHER/CENTRE MUST CONFIRM** the actual checklist, additional instructions, permitted support, authentication requirements and acceptable further work. The report's own earlier audits are evidence locators, not substitutes for the official grids.

### Evidence inspected and preservation baseline

| Item | Current evidence and limits |
|---|---|
| Assessed report | Final DOCX SHA256 `661c721c119292dccfbf8bab155021b44054fed9086fcd95c103d4668c0fd81c`; final PDF SHA256 `95584b9eacf256746d16d35a578e0e1ab57c21a2235d9f2fd86b3356f0be2439`. |
| Repository | HEAD `ecf38296c5972ad4579848f2f42eb170709471de`; seven genuine same-day commits. Existing uncommitted changes predate this audit and are not changes made by this audit. |
| Implementation | All Python modules in `src/pitwall/`, relevant tests, test runner, capture and benchmark records. No application execution or new test run was needed for this documentary audit. |
| Evidence catalogue | All **214** rows in `report/evidence-index.csv` resolve and their SHA256 values match current files. A catalogue row can be a source file or blank form, not a completed experiment. |
| Latest suite | `evidence/test-runs/TEST-QUALITY-FINAL-20260908T224148466396Z/`: 87 JUnit cases, no failures/errors. Every recorded source/test hash matches current source/test files. This is a preserved assisted run, not a new candidate-run test. |
| Explicit SC05 check | `evidence/test-runs/TEST-SC05-20260908T224145702053Z/`: one passing absolute-tolerance test. It also appears as case 087 in the latest suite. |
| Development executions | Nineteen preserved run directories, including original 86-case final run, focused stage runs, two failing collection-type assertions and the 84-case retest. Repeated cases are not additional unique tests. |
| Visual output | First GUI capture plus eight completed advanced Windows Qt captures and associated search/Monte Carlo JSON. These are automated captures of the real application. |
| Performance | Original three-repeat benchmark and separate five-repeat comparison benchmark, with raw values. Recomputed minimum, maximum, mean and median agree with both JSON files. |
| Human evidence | Appendix F, `docs/stakeholder/`, `docs/usability/` and `docs/candidate/` contain plans, questions and incomplete forms. No completed participant session or candidate understanding record was found there. |
| Assistance | Appendix K, page 68, and `docs/assistance-log.md`, read in full. Both record broad assistance across documents, implementation and verification. |

A pre-write SHA256 inventory covered 621 existing project files, excluding Git internals, virtual environments and caches. Only this audit file is authorised for creation. No assessed text, factual evidence, assistance entry or application file is authorised for modification.

## Primary 70-page report and supporting pack review

Primary PDF SHA256: `efcb60beac04be946843881425a2ec2ce27c82586905f7745c7e37b01a20bad0`. Supporting pack SHA256: `8f31216af094a734902500ef5a120bf4d012159550e60fb95d735fee6818c628`. These files are separate from the repository report hashes below. The repository code, tests and raw outputs remain the implementation/evidence basis.

The supplied report adds reasoned provisional stakeholder needs on pages 6-7, stakeholder-specific runtime requirements on pages 10-11, more explicit statements that reviews/reflections were not recorded, and fuller provisional usability discussion on page 48. Those are real documentation improvements. They do not provide completed interviews, observed user outcomes, personal candidate explanations or new authenticated development. The six conditional bands below therefore remain the audit's strongest defensible judgements after reviewing this version. Analysis is strengthened by the added rationale, but authentication, actual research-informed decisions and substantiation still prevent a secure top-band conclusion.

The class tables on pages 14-15 retain the same 21 rows and the same generic enum/queue descriptions. The 87-case test inventory, SC judgements, numerical benchmark evidence and six-stage assistance declaration are materially unchanged. Appendix K is now on **page 70**. No completed human evidence appears in the separate pack: its answers, observations and reflections are blank. Its explanatory notes are not proof that Mithil has independently explained the program.

### Actual locations in the supplied report

| Category/material | Actual primary PDF pages |
|---|---|
| Analysis | 6-12; stakeholder rationale 6-7; runtime requirements 10-11; first criteria 11 and advanced criteria 12. |
| Design | 13-24; class inventory 14-15; structures 16; algorithms 16-21; validation 22; interface 23; iterative and final plans 24. |
| Development and its testing | 25-40; first desktop section 29; search section 34; persistence 35; robustness 37; failures 38-39; execution list 39-40. |
| Final testing | 41-45; benchmarks 42; manual oracle/usability plan 43-44; final verification 44-45. |
| Evaluation | 46-50; SC judgements 46-47; usability/stakeholder discussion 48-49; maintenance and limitations 49-50. |
| Bibliography | 51. |
| Appendices | A 52; B 53; C 55; D 56; E 58; F 59; G 64; H 64; I 66; J 67; K 70. |

All table numbers 1-39 and figure numbers 1-10 remain present and unique in the body. Their actual starting pages are:

- Tables: T1 6; T2 7; T3-4 8; T5 9; T6 10; T7 11; T8 12; T9 14; T10-14 15; T15-16 16; T17 18; T18 22; T19 24; T20 39; T21-22 41; T23 42; T24-25 43; T26-27 44; T28 46; T29 48; T30-31 49; T32 53; T33 60; T34 61; T35 62; T36 63; T37-38 64; T39 70.
- Figures: F1 14; F2 23; F3 30; F4 37; F5 52; F6 67; F7-8 68; F9-10 69. Their descriptions still correspond to the same actual captures/diagrams, with the class-diagram shorthand issue retained.

### Incorrect primary-report contents references

**46 of the 75 contents entries are stale.** The other 29 match their named heading's actual page. The table below lists every incorrect target, grouped only where old and new values match. Classification for every row: **REPORT FACTUAL CORRECTION NEEDED**. Correcting these would require a later permitted report export by Mithil; this audit does not update the PDF.

| Heading(s) | Contents says | Actual page |
|---|---:|---:|
| 1.5 Research into existing solutions | 6 | 7 |
| 1.10 Success criteria | 10 | 11 |
| 2.4 Data structures | 15 | 16 |
| 2.7 Validation design | 21 | 22 |
| 2.10 Iterative test plan | 23 | 24 |
| 3.2 Tyre degradation | 25 | 26 |
| 3.6 First desktop milestone | 28 | 29 |
| 3.9 Safety car | 31 | 32 |
| 3.12 Bounded optimisation | 33 | 34 |
| 3.13 JSON persistence | 34 | 35 |
| 3.15 Robustness and verification | 36 | 37 |
| 3.16 Genuine failures and remedial action | 37 | 38 |
| 3.17 Recorded test progression | 38 | 39 |
| 4 Post-development testing; 4.1 Functional testing; 4.2 Robustness testing | 40 | 41 |
| 4.3 Performance testing | 41 | 42 |
| 4.4 Manual verification; 4.5 Usability testing | 42 | 43 |
| 4.6 Final quality verification | 43 | 44 |
| 5 Evaluation; 5.1 Overall evaluation; 5.2 Evaluation against success criteria | 45 | 46 |
| 5.3 Functional correctness | 46 | 47 |
| 5.4 Evaluation of algorithms; 5.5 Performance; 5.6 Robustness; 5.7 Usability; 5.8 Stakeholder evaluation | 47 | 48 |
| 5.9 Maintenance; 5.10 Limitations | 48 | 49 |
| 5.11 Future improvements; 5.12 Final conclusion | 49 | 50 |
| 6 Bibliography | 50 | 51 |
| 7 Appendices; Appendix A Source and class relationships | 51 | 52 |
| Appendix B Automated test inventory | 52 | 53 |
| Appendix C Execution and failure evidence | 54 | 55 |
| Appendix D Full benchmark values | 55 | 56 |
| Appendix E Research materials | 57 | 58 |
| Appendix F Human evidence packs | 57 | 59 |
| Appendix G Git development summary; Appendix H Evidence catalogue and completeness audit | 62 | 64 |
| Appendix I JSON contract and example | 64 | 66 |
| Appendix J Additional application screenshots | 65 | 67 |
| Appendix K Development declaration | 68 | 70 |

### Primary-report correction crosswalk

Corrections C01-C18 below still apply substantively. Their primary-report locations are: C01 p14; C02-C04 p15; C05 pp14-15; C06 p15; C07 p52; C08 pp12, 27, 35 and historical plans p24; C09 p13, p24 and repeated extracts pp25-37; C10 p22; C11 p24 versus implemented behaviour p48; C12 p37 and oracle labels; C13 pp19-20; C14 pp20-21; C15 pp44 and 47; C16 pp46-47; C17 pp4-5 and the table pages listed above; C18 pp25-37. Exact wording may have additional spaces or changed line wraps. These locations, rather than repository page numbers, should be used when reviewing the supplied PDF.

### Additional factual corrections in the supplied documents

These entries extend **FACTUAL CORRECTIONS FOR MITHIL TO REVIEW** and must not be applied automatically.

| ID / classification | File/page | Current wording | Why inaccurate or unclear | Evidence reference | Factual point for Mithil to express in his own words |
|---|---|---|---|---|---|
| C19 / REPORT FACTUAL CORRECTION NEEDED | Primary report pp2-3 | Contents page values listed above | 46 targets no longer match the actual headings after reflow. | Actual primary PDF headings and complete mismatch table above. | Use the actual final export's heading pages, then recheck every contents target. |
| C20 / REPORT FACTUAL CORRECTION NEEDED | Primary report p65, T38 | “3.4.4(b) Presentation”, alongside “3.4.4(b) Further development” | The official content identifier is duplicated for different meanings. OCR 3.4.4(b) concerns further development; a centre presentation checklist is not that official content point. | Official specification printed p14; T38 p65. | Keep any centre-specific presentation requirement separately labelled and trace it to its actual checklist source. Do not present it as a second OCR 3.4.4(b). |
| C21 / TEACHER/CENTRE MUST CONFIRM | Primary report pp1, 65-66 | “cross-checks it against the centre checklist”; “The separate centre Full Mark Criteria checklist has now been reviewed”; page-count figures described as guidelines | This audit has the claim, not the underlying checklist or a dated review record. It cannot confirm that integration or interpret unseen page-count instructions. | Compare repository report p64 with primary pp65-66; actual centre checklist required. | Identify the checklist's actual title/version and review evidence, then confirm its requirements with the teacher. Do not infer completion merely from this sentence. |
| C22 / REPORT FACTUAL CORRECTION NEEDED | Supporting pack p1 | “At least one relevant person”; “at least two people” for usability | These are pack recommendations, not a numerical OCR minimum established by the marking grids reviewed. | Official stakeholder content and evaluation grids; supporting pack p1. | Distinguish a suggested session plan from a centre/OCR requirement. Confirm any centre-specific participant minimum. |
| C23 / REPORT FACTUAL CORRECTION NEEDED | Supporting pack pp1-2 | Questions “1. 1.” through “7. 7.” | Duplicate automatic/manual numbering creates a presentation defect, not additional questions. | Seven actual stakeholder questions in the pack. | Use one numbering sequence if the pack is later revised. |
| C24 / REPORT FACTUAL CORRECTION NEEDED | Supporting pack p4 | Race loop “stores a LapResult” | Broadly true by inheritance, but the concrete stored objects are EnvironmentalLapResult, including default dry runs. | `src/pitwall/engine.py:simulate`; `conditions.py:EnvironmentalLapResult`. | Explain the actual subclass and inherited core fields rather than treating the simplified class name as an exact construction call. |

The pack's other technical notes on linear wear, fuel, pit timing, event ties, weather, safety car, local seeded randomness, paired trials, statistics, bounded search, JSON and worker revision/cancellation agree with the reviewed implementation at their stated introductory level. Its blank explanations, reflection template and session forms remain **CANDIDATE MUST DO**, **HUMAN USER MUST DO** or **STAKEHOLDER MUST DO** items, not evidence already completed. Its commands to run sessions or fill reflections are not executed as part of this audit.

## Category-by-category gap assessment

The judgements apply to the supplied 70-page report as well as the repository evidence. Detailed source-report page citations below use repository pagination; use the primary-location tables above for the supplied PDF.

### Analysis: 10 marks

**Strongest defensible current content band: 6-8, conditional on authentication.** The material explains the computational problem and provides concrete requirements, but its justification of user suitability and research-led choices is not consistently strong enough to support 9-10.

**Exact current evidence:** pages 6-12, Tables 1-8; `docs/analysis/requirements.md`, `research.md`, `advanced-success-criteria.md` and `final-review-impact.md`. FR01-FR12 cover input, simulation, comparison, presentation, persistence, environmental events, trials and search. SC01-SC14 supply measurable computational conditions. Three existing-system reviews address TUM race simulation, FastF1 and F1 Manager. The report correctly dates those reviews after the prototype. Page 10 records actual machine/process information and explicitly says minimum end-user hardware is unmeasured. Model limitations include dry-only tyres, illustrative parameters, single-car behaviour and bounded search.

**What prevents a convincing next-band case:** several rationales are short feature-to-purpose associations rather than a sustained explanation of why this scope and these thresholds suit the identified audience. Proposed stakeholder involvement has no actual responses. Research reviews can support current scope evaluation, but cannot establish that those sources caused earlier choices. The report appropriately acknowledges this; it still leaves a gap in demonstrated research-informed decision making.

**What specifically prevents a full-mark case:** authenticated candidate reasoning that connects the problem, audience needs, alternatives, justified limits, deployment constraints and measurable criteria throughout. More pages or a retroactively written interview would not supply that evidence.

| Missing item or available evidence | Classification | Required factual outcome |
|---|---|---|
| Candidate rationale for scope, parameters, requirements and measurable thresholds | CANDIDATE MUST DO | Explain actual choices and assumptions, including why the simplified output is useful and what it cannot establish. |
| Confirmation of intended use and unmet needs from the proposed stakeholder | STAKEHOLDER MUST DO | Supply a genuine dated post-prototype response; it must remain labelled post-prototype. |
| Clear separation of earlier design intentions and later research findings | REPORT FACTUAL CORRECTION NEEDED | Review timing claims identified in correction C08. |
| Existing research, FR/SC definitions and hardware record | OBJECTIVE TECHNICAL EVIDENCE ALREADY EXISTS | Use the existing evidence without presenting it as participant feedback or candidate-originated work. |
| Centre-specific expectations and creditable authorship | TEACHER/CENTRE MUST CONFIRM | Determine what analysis can be assessed and what further candidate work is permitted. |

### Design: 15 marks

**Strongest defensible current content band: 9-12, conditional on authentication.** Detailed decomposition, algorithms, validation and test data are present. Accurate and consistently justified design, and the provenance of prospective decisions, remain less secure.

**Exact current evidence:** pages 13-24; Figure 1; Tables 9-19; Appendix A, page 51; the I01-I17 design records in `docs/design/`. A01-A14 identify the calculation and control algorithms. The report supplies hand-derived five-lap expectations, typical/boundary/erroneous inputs, immutable input structures, event ordering, worker snapshots, validation rules and post-development test plans. It explicitly labels the architecture diagram and class inventory as derived from completed source. No historical interface wireframe is claimed on page 23.

**What prevents a convincing next-band case:** generated class-table cells are inaccurate or uninformative; some algorithm prose conflates an earlier dry-only description with the current event-enabled program; usability choices are explained mainly from developer assumptions. Current-source architecture is useful documentation but does not itself prove prospective design. Seven commits and source hashes do not recover every earlier design state.

**What specifically prevents a full-mark case:** a fully accurate, justified, candidate-understood account of how the algorithms and structures form the complete solution, together with credible timing evidence for design decisions and justified usability/test choices. Corrections alone would improve accuracy, but not authenticate authorship or create a missing earlier design process.

| Missing item or available evidence | Classification | Required factual outcome |
|---|---|---|
| Class-table, diagram and algorithm-description corrections | REPORT FACTUAL CORRECTION NEEDED | Review C01-C07 and C10-C14 below; do not silently alter historical records. |
| Explanation of alternatives and complete algorithm interaction | CANDIDATE MUST DO | Demonstrate pit/event ordering, heap ties, paired randomness, search limits and validation boundaries using real inputs. |
| Prospective design for any later justified change | CANDIDATE MUST DO | Only if the centre permits further work: record the actual problem, design and expected tests before implementation. |
| Evidence that usability choices work for the intended audience | HUMAN USER MUST DO | Complete real tasks and report actual interpretation difficulties. |
| Existing design records, expected arithmetic and current-source structure | OBJECTIVE TECHNICAL EVIDENCE ALREADY EXISTS | Preserve provenance labels and distinguish design intention from implementation documentation. |

### Iterative development of coded solution: 15 marks

**Strongest defensible current content band: 9-12, conditional on authentication.** The modular implementation and staged records are substantial. The top-band case is weakened by incomplete personal review, coarse version checkpoints and retrospective extracts.

**Exact current evidence:** pages 25-39; `docs/iterations/`; source modules; Appendix G's seven commits. The stages cover models, tyre/fuel arithmetic, pit/race logic, comparison, first GUI, events, weather, safety car, randomness, Monte Carlo, search, persistence, advanced GUI and robustness. I04-I05 and I14-I16 are documented combined stages rather than unexplained missing numbers. Current extracts are labelled as current code, not exact historical snapshots. The real JSON defect and correction are retained. Modules separate pure computation from Qt; strict types, bounds, schema validation, cancellation and stale-result rejection are implemented.

**What prevents a convincing next-band case:** prototype versions are preserved at some checkpoints, but not independently recoverable for every described stage. Run hashes identify bytes, not the bytes themselves. Repeated “implementation and recorded review” framing is not a personal, stage-specific explanation of why choices were made. Appendix F's candidate understanding and reflection material remains incomplete. The assistance record explicitly attributes implementation authorship externally.

**What specifically prevents a full-mark case:** centre-authenticated evidence of Mithil's own contribution, reasoning and review at all relevant stages, with suitably evidenced prototype progression. A new small iteration can demonstrate new personal work if permitted; it cannot retrospectively make the existing modules independently authored.

| Missing item or available evidence | Classification | Required factual outcome |
|---|---|---|
| Personal understanding and actual contribution history | CANDIDATE MUST DO | Explain current code, identify real changes made personally, and distinguish present learning from past authorship. |
| A feedback-driven change with before/after evidence, where warranted | CANDIDATE MUST DO | After genuine feedback and centre guidance, perform one bounded prospective cycle; no feature is selected or implemented by this audit. |
| Source/version coverage at each recorded stage | OBJECTIVE TECHNICAL EVIDENCE ALREADY EXISTS | Existing commits, extracts and run records support some checkpoints. Missing snapshots must be acknowledged, never fabricated. |
| Whether existing assisted implementation can be credited | TEACHER/CENTRE MUST CONFIRM | Review the actual assistance scope before treating a content band as candidate attainment. |
| Stronger timing statements than preserved evidence supports | REPORT FACTUAL CORRECTION NEEDED | Qualify them using C08-C09. |

### Testing to inform development: 10 marks

**Strongest defensible current content band: 9-10, conditional on authentication.** This is the strongest documentary band case: stage-linked executed testing and a real defect/remedy sequence exist. There is no higher band. This is not an award of 10.

**Exact current evidence:** Table 20, pages 38-39; stage links on pages 25-36; nineteen `evidence/test-runs/` directories; `docs/testing/FAIL-I17-01.md` and `FAIL-I17-02.md`. Stage executions include I01, I02, I03, I05, I06, I07, I08, I09, I10, I11, I12, I13, I15 and I16, with combined stages identified in prose. `TEST-I17-ROBUSTNESS-20260908T212523289799Z` has five cases and two failures: replacing either `events` or `planned_stops` with `{}` failed to raise `ValueError`. The 84-case retest passes after explicit array validation. The report explains why checking members of an empty dictionary missed a container-type error and why explicit checks were selected. The capture-harness failure is separately identified as a tool issue with partial capture output and a factual transcript.

**What prevents unqualified top-band credit/full marks:** candidate execution and personal justification are not recorded; assistance explicitly covers writing/running tests and the fixes. Capture-harness evidence is not a preserved pytest failure and must retain that distinction. Any historical test/prototype state that cannot be recovered must remain a limitation. Neither passing counts nor an invented extra defect can replace the candidate's explanation of actual remedial action.

| Missing item or available evidence | Classification | Required factual outcome |
|---|---|---|
| Explanation of the real defect, chosen remedy and unchanged reproduction test | CANDIDATE MUST DO | Explain the difference between validating a collection and validating its elements, using the preserved failure. |
| Candidate-run tests in any permitted subsequent cycle | CANDIDATE MUST DO | Retain actual commands, inputs, outputs and honest failures/retests; do not relabel the existing assisted executions. |
| Stage tests and failure/retest chain | OBJECTIVE TECHNICAL EVIDENCE ALREADY EXISTS | This technical evidence need not be recreated merely to increase volume. |
| What authenticated testing evidence is creditable | TEACHER/CENTRE MUST CONFIRM | Resolve provenance and support boundaries. |
| Runner hash timing and test-independence wording | REPORT FACTUAL CORRECTION NEEDED | Review C09 and C12. |

### Testing to inform evaluation: 5 marks

**Strongest currently secure content descriptor: 2 marks, conditional on authentication.** Functional and robustness annotation is stronger than a basic functional demonstration, but there is no completed usability-testing evidence. A centre applying best fit could weigh that uneven profile differently; this audit does not impose an invented universal two-mark cap. It cannot substantiate the whole 3-4 descriptor or 5 from screenshots and blank forms.

**Exact current evidence:** pages 40-44, Tables 21-27; 87-case final suite; focused SC05 test; raw benchmarks; actual screenshots. Functional IDs F01-F08 map to real test cases. Post-development checks include maximum comparison, strict JSON container types, a small arithmetic search oracle, trial reconstruction, stale worker output and cancellation. Appendix F and Tables 25, 33-35 are unconducted human-task forms. Page 47 explicitly states that final usability evaluation is pending.

**What prevents a convincing next-band case:** no annotated real-user task outcomes, mistakes, help requirements or interpretation evidence. Automated Qt interaction verifies widget behaviour, not whether a user understands the application.

**What specifically prevents full marks:** completed and annotated evidence covering final function, robustness and usability, with candidate interpretation of what each result demonstrates. Existing functional/robustness evidence is substantial; missing usability evidence is not resolved by another automated screenshot.

| Missing item or available evidence | Classification | Required factual outcome |
|---|---|---|
| Genuine task performance and comments | HUMAN USER MUST DO | Use the application, interpret results, encounter any real difficulties and provide actual feedback. |
| Session conduct, recording and evidence annotation | CANDIDATE MUST DO | Record actual completion, errors, assistance given and timings only if measured; link observations to features and criteria. |
| Native-dialog use, keyboard/scaling and perceived cancellation behaviour | HUMAN USER MUST DO | Observe these on the real target setup; automated checks do not establish human responsiveness. |
| Existing final tests, tolerance output and raw performance values | OBJECTIVE TECHNICAL EVIDENCE ALREADY EXISTS | Reuse honestly as the existing assisted technical record. |
| Permitted participants, privacy arrangements and assessable support | TEACHER/CENTRE MUST CONFIRM | Apply the centre's process without inventing participant requirements. |

### Evaluation of solution: 15 marks

**Strongest defensible current content band: 9-12, conditional on authentication.** Criterion-linked technical evaluation, limitations and concrete maintenance considerations exist. Effective usability and candidate judgement remain unsupported.

**Exact current evidence:** pages 45-49, Tables 28-31. All fourteen criteria have judgements; SC04 and SC14 remain partial. SC05 is now supported by explicit absolute tolerance; SC13 by actual search/trial timings. The report limits its claims to an illustrative model and discusses event ordering, shared-noise cancellation, search-grid limits, schema changes, GUI growth and model calibration. Page 47 distinguishes empirical 88% trial frequency from a real-race probability. Usability and stakeholder evaluation remain explicitly pending.

**What prevents a convincing next-band case:** no participant evidence supports the effectiveness of usability features; no actual stakeholder judgement establishes suitability; repeated generic “Scope / reason” cells substitute for criterion-specific reasoning in places. Suggested improvements are technically plausible but have not been prioritised using real feedback or evaluated after a resulting change.

**What specifically prevents full marks:** an authenticated candidate evaluation explaining how each result supports its judgement, justified usability success/partial success/failure, and reasoned responses to actual limitations. Completing blank forms with hypothetical answers or accepting this audit as candidate prose would not meet that need.

| Missing item or available evidence | Classification | Required factual outcome |
|---|---|---|
| Personal interpretation of criterion and algorithm evidence | CANDIDATE MUST DO | Explain both support and limits; do not copy this audit into assessed evaluation. |
| Actual judgement of intended usefulness | STAKEHOLDER MUST DO | Review the real prototype and state what needs it meets or misses. |
| Observed usability success or failure | HUMAN USER MUST DO | Supply evidence through real task performance. |
| Evaluation of any genuine subsequent change | CANDIDATE MUST DO | Compare actual before/after evidence and obtain follow-up feedback, if such work is permitted. |
| Criterion-specific reasoning and SC13 description | REPORT FACTUAL CORRECTION NEEDED | Review C15-C16 without inflating current judgements. |
| Existing maintenance/limitation analysis and bounded computational results | OBJECTIVE TECHNICAL EVIDENCE ALREADY EXISTS | Retain these strengths with their model-specific qualifications. |

## Factual-quality audit

### Numbering, references and traceability

| Check | Finding |
|---|---|
| Contents | All **75** entries on pages 2-3 match the named heading on the stated PDF page. No stale contents-page target found. |
| Tables | All **39** tables are numbered once in the body; their list entries match. Continuation headers are not new tables. Repeated titles for Tables 2-4 and 33-35 are ambiguous presentation, not duplicated numbering. |
| Figures | All **10** numbered body figures have matching list entries. No missing or duplicated body figure number found. |
| Lists of tables/figures | Pages 4-5 list captions but omit page numbers. This is a navigation improvement opportunity, not a wrong page reference. |
| Appendices | A p51; B p52; C p54; D p55; E p57; F p57; G p62; H p62; I p64; J p65; K p68. Their contents targets exist. References to source/classes, tests, failures, benchmark values, research, human forms, Git, catalogue, JSON, screenshots and declaration point to the intended appendix. |
| Requirements | FR01-FR12 are unique. FR01-FR08 link to SC01-SC08; FR09 to SC09, FR10 to SC10, FR11 to SC11, FR12 to SC12; SC13 concerns FR11/FR12 and SC14 FR09-FR12. No dangling FR/SC identifier found. Table 5's “Separate iteration” for FR09-FR12 is a historical development-order label; Tables 8 and 28 carry the later links. |
| Algorithms | A01-A14 remain consistent with repository identifiers. Shared headings group related algorithms; they do not lose an ID. Detailed mapping appears below. |
| Final tests | All **87** Appendix B identifiers, names and PASS outcomes match the latest JUnit inventory exactly. Parameterised cases count separately; repeated runs do not. |
| Functional references | F01→015, F02→006, F03→031, F04→060, F05→011, F06→055, F07→027, F08→005 all resolve to the correct named cases. |
| Run IDs | All 19 listed execution directories exist. Table 20's counts agree with their XML: the sole failed suite has 2 failures out of 5 cases. Lexical listing order is not chronological ordering. |
| Evidence paths | All actual repository-relative paths extracted from current DOCX content resolve after removing sentence punctuation. “Worker tests/cancellation” is prose, not a missing `tests/cancellation` file. Abbreviated test-module names resolve within `tests/`. All 214 catalogue paths and hashes match. |
| Bibliography | R01, R02, R03, R03b and R04-R09 are distinct entries on page 50. Inline identifiers resolve. R03b is intentional, not a numbering error. Sources are attributed as post-prototype review or technical references, not original experimental data. This check verifies reference identity/context, not permanent future URL availability or the candidate's personal reading. |
| Terminology | Page 5 distinguishes SC as safety car from SC01-SC14. “Optimisation” is correctly bounded to the declared grid. “88%” is correctly an empirical simulated frequency. “Manual/independent oracle” still needs a clear distinction from independent human authorship; see C12. |
| Duplicated material | The five-lap oracle appears in design and final verification, appropriately serving different purposes. Criteria recur in evaluation for traceability. The two long “Implementation and recorded review” and “Extract provenance” introductions recur 15 times each; they are framing, not 15 independent reviews. Some generic explanations recur across distinct stages. |
| Template wording | Candidate/stakeholder placeholders, blank human forms and understanding rows are explicitly incomplete. They are missing evidence, not completed answers. No filled fabricated response was identified. Repeated generic class cells do require correction. |
| Timing/provenance | Pages 6-8, 13, 23, 50 and 62 correctly acknowledge post-prototype research, retrospective diagrams and coarse commits. Stronger “before implementation” statements elsewhere need qualification against that limitation. |

Table starting pages, for a complete numbering cross-check: T1 6; T2-3 7; T4 8; T5 9; T6-7 10; T8 11; T9 14; T10-15 15; T16 16; T17 18; T18 21; T19 23; T20 38; T21-22 40; T23 41; T24-25 42; T26-27 43; T28 45; T29 47; T30-31 48; T32 52; T33 58; T34-35 60; T36 61; T37-38 62; T39 68.

### Every class-table row checked against source

Tables 9-14 contain **21 classes**. Each row was compared with its actual class body, annotated fields, explicit methods, inheritance and relevant instance state. Type annotations alone do not enforce runtime validation. The Methods heading also conflates explicit methods, properties and record descriptions.

| Report row | Actual source reference | Verification and precise factual point |
|---|---|---|
| T9 Compound, p14 | `src/pitwall/models.py:25` | Enum members SOFT, MEDIUM, HARD, with string values. Neither queue state nor a dataclass. Both generic cells need correction. |
| T9 Circuit | `models.py:37` | All three fields and `__post_init__` match: name, base_lap_time, pit_lane_loss. Constructor checks names and numeric bounds. |
| T9 Driver | `models.py:49` | name and pace_delta match; `__post_init__` exists. Pace delta is non-negative in this implementation. |
| T9 TyreCompound | `models.py:59` | Four listed fields and validation method match. recommended_life is a positive reference input, not an engine-enforced maximum stint or degradation cliff. |
| T9 PitStopPlan | `models.py:73` | lap, compound, stationary_time and validation method match. Race-end legality is checked later against race length. |
| T9 Strategy | `models.py:85` | Three fields match. `__post_init__` validates ordered typed stops; `validate_for` enforces race-specific stop bounds. |
| T9 RaceConfig | `models.py:108` | Five fields and both listed methods match. Exactly three distinct compounds are required; `tyre` searches that tuple, as page 16 correctly explains. |
| T9 RaceState | `models.py:131` | Four fields and constructor validation match. It is a frozen state record, replaced as the engine advances. |
| T9 LapResult | `models.py:145` | All nine fields and `__post_init__` match. Per-record validation is not proof of all cross-lap relationships. |
| T9 StrategyResult | `models.py:172` | Two stored fields match. `total_time`, line 183, is a property returning the last cumulative value, not an ordinary callable method or an independently stored total. |
| T10 Weather, p15 | `src/pitwall/events.py:8` | Enum DRY, DAMP, WET. Generic queue wording and “Data record” are inaccurate. |
| T10 EventType | `events.py:14` | Enum WEATHER_CHANGE, SAFETY_CAR_START, SAFETY_CAR_END. Generic queue wording and “Data record” are inaccurate. |
| T10 RaceEvent | `events.py:21` | lap, kind, optional weather and `__post_init__` match. Weather payload is required only for a weather-change event and forbidden for safety-car commands. |
| T10 EventQueue | `events.py:37` | Methods match. Actual state is instance attribute `_heap`, a list of `(lap, input sequence, RaceEvent)` tuples. It is built then heapified. `at_lap` pops all events due at or before the supplied lap. No enum values and no public enqueue method. |
| T11 Conditions | `src/pitwall/conditions.py:9` | Eight fields and both methods match. Constructor checks settings and an event bound; actual race-specific validation also occurs elsewhere. |
| T11 EnvironmentalLapResult | `conditions.py:37` | Five listed fields are the added fields, not the complete attribute set. It inherits nine LapResult fields and calls its superclass validator. Inheritance is correctly mentioned in nearby prose; the row needs an explicit inherited-field label for completeness. |
| T12 Trial | `src/pitwall/monte_carlo.py:25` | Four fields match. Frozen dataclass with generated methods; no explicit `__post_init__`. “Data record” describes the kind of class, not a method. |
| T12 MonteCarloResult | `monte_carlo.py:33` | Five fields match. Frozen outer record but mutable statistics dictionaries, correctly qualified on page 14. No explicit validator. |
| T13 SearchSettings | `src/pitwall/optimiser.py:13` | Four fields and `__post_init__` match. max_stops is limited to 0-2; minimum_stint and pit_step are bounded positive integers. Race-specific feasibility is checked in candidate generation. |
| T13 CandidateScore | `optimiser.py:27` | strategy and total_time match. Frozen record with no explicit validator or custom method. |
| T14 Scenario | `src/pitwall/persistence.py:16` | Three fields and `__post_init__` match. Cross-validates race, conditions, strategy collection, names, event count/range and amplitude. |

Table 18, pages 21-22, repeats ten core rows. Every repeated row was also checked: Compound, Circuit, Driver, TyreCompound, PitStopPlan, Strategy, RaceConfig, RaceState, LapResult and StrategyResult all have accurate listed responsibilities/fields. Its “derived total_time” is more precise than Table 9's Methods column. Its following blanket validation paragraph needs qualification: signed random variation is permitted, and Trial/MonteCarloResult/CandidateScore have no constructor validation.

Three GUI classes are outside Tables 9-14: `MainWindow` (`gui.py:55`), `ExperimentWorker` (`advanced_gui.py:39`) and `AdvancedWindow` (`advanced_gui.py:57`). The nearby inheritance/ownership prose is consistent with code. The tables should be described as the model/computation inventory, not a complete inventory of every application class. A further table is not automatically required for marks; candidate explanation of GUI state, revision and worker interaction is the substantive need.

### Algorithm IDs, implementation and complexity

Let N be laps, E scheduled events, K compared strategies, C scored candidates, S stops per candidate, and R paired trials. Python container/number operations are treated at their usual fixed-size cost here; application limits remain explicit.

| ID | Report and source | Result |
|---|---|---|
| A01 lap time | p16-17; `physics.py:lap_time` | Base, driver, tyre pace, wear, fuel and pit loss match; environmental terms are added in engine. O(1) per lap. |
| A02 degradation | p17; `physics.py:degradation` | Rate multiplied by completed tyre age; O(1). No automatic recommended-life cliff. |
| A03 fuel | p16-17; `physics.py:fuel_effect` | Linear declining penalty with explicit one-lap zero case; O(1). |
| A04 validation | p17; `models.py:Strategy` and `RaceConfig` | Relevant checks exist. The broader pseudocode spans several validators, not only one Strategy method. Stop validation is O(S). |
| A05 race | p18, p21; `engine.py:simulate` | Historical dry-stage pseudocode is labelled. Current event-aware race cost O(N + S + E log E), simplified to O(N + E log E) because valid S is bounded by N-1. Space O(N + S + E), hence O(N+E). No per-lap cancellation callback. |
| A06 queue | p18-19, p21; `events.py:EventQueue` | Current build is O(E) heapify, all removals O(E log E); sequence breaks equal-lap ties. Page 21 correctly refines the older repeated-push design. |
| A07 weather | p19; `conditions.py`, `engine.py` | Before-lap state assignments and equal dry-tyre weather penalties match; constant extra work per lap after events. |
| A08 safety car | p19; `engine.py` | Adds configured delay and scales lane plus stationary loss while active. Assignment semantics, not stacked intervals. O(1) extra work per lap. |
| A09 comparison | p19-20; `comparison.py:compare`, `summary` | Stable sort of simulations exists; metrics are calculated separately by summary. Dry cost O(KN + K log K); current event-aware cost O(K(N + E log E) + K log K). Result space O(KN+E). |
| A10 generation | p20; `optimiser.py:candidates` | Increasing grid combinations, minimum-stint filtering and compound products match, including repeated compounds. Rejected stop combinations also take work. Under current S≤2, fixed three compounds and grid≤N, the broad O(CN) scoring bound can subsume generation; do not present a generator as constant-time per request. |
| A11 optimisation | p20-21; `optimiser.py:optimise` | Zero variation, full score list, limits and sorting match. Current scoring/sorting O(C(N + E log E) + C log C), plus generation. Space O(C(S+1)+N+E); no retained full lap history for every candidate. The `+1` accounts for zero-stop candidate records. |
| A12 Monte Carlo | p20-21; `monte_carlo.py:monte_carlo` | Paired trial conditions and seeds, generated SC commands and between-trial cancellation match. Overall O(R(N + E log E) + R log R), space O(R+N+E); at most two generated events per trial do not change this form. |
| A13 statistics | p21; `monte_carlo.py:describe` | Mean, median, population standard deviation and extrema use statistics functions. Median sorting adds O(R log R), acknowledged in current-code refinement. Probabilities are empirical counts; ties use absolute 1e-9 with zero relative tolerance. |
| A14 scenario | p21; `persistence.py` | Exact fields, arrays, enums, size/count limits, validation and atomic replacement match. Linear in file content and validated collections, including O(E) heap construction. It does not consume every event on load, so an E log E removal term is not automatically needed here. |

These are complexity analyses of source, not measured scaling laws. The later refinement resolves some earlier omissions, but a reader should not have to combine scattered dry-stage and current-stage formulae without clear scope labels.

### Independent tests, success claims, screenshots and benchmarks

**Independence:** the five-lap expected values are separate arithmetic expectations, not captured program output. The four-lap search oracle calculates totals without calling `simulate` or `candidates`, though it reuses model data/compound lookup. It compares sorted scores, not identity of every plan across every setting. `test_trial_reconstruction` calls the same production `simulate`; this proves replay consistency, not independently derived physical correctness. Zero-noise replay and maximum-size comparison are also not independent numerical oracles. All these tests remain recorded as externally authored/executed. No evidence establishes independent human testing.

| Criterion | Support and qualification |
|---|---|
| SC01-SC03 | Boundary/type tests, manual wear arithmetic and stop-transition cases support the computational claims for tested inputs. Configurable widgets are visible; real-world tyre realism is not established or claimed. |
| SC04 | Partial judgement is appropriately cautious. Parser/GUI recovery passes; no user has judged whether the error explanations are understandable. |
| SC05 | Explicit case 087 establishes absolute error ≤1e-9 for the recorded five-lap example and exact replay. Zero difference is between expected and actual Python floats, not unlimited real-number precision. The older approximate assertion alone was not sufficient for this specific tolerance. |
| SC06 | Lap-count, reset and total checks support the computational/visual judgement. “Equals” should be interpreted with the actual floating-point assertion, not a proof for arbitrary real arithmetic. |
| SC07-SC08 | Ranking/summary tests and actual 50-point graph captures support the limited model/rendering wording. SC08 explicitly leaves human usability pending. |
| SC09 | Typed scenario equality and malformed-container/schema checks support the tested-schema judgement. Not every file-system failure or native-dialog interaction is covered. |
| SC10 | Queue, weather and safety-car arithmetic support the specified simplified examples. There is no wet-tyre or traffic-model validation. |
| SC11 | Statistics oracle, 100 deterministic trials, additional seeded replay/tie checks and captured trials support the selected-uncertainty claim. No calibrated probability of real racing success follows. |
| SC12 | 21-plan tiny count, 182.2-second small optimum, separate four-lap score arithmetic and 1,056-candidate export support the constrained-grid wording. Not a proof of every possible strategy or unrestricted optimum. |
| SC13 | Original three-repeat default search and 1,000-paired-trial benchmarks meet the criterion as written. The new comparison measurements supplement performance coverage; they are not a missing element explicitly named by SC13. |
| SC14 | Partial remains appropriate for perceived responsiveness. Automated worker, stale-result, cancellation and representable-scenario round-trip tests exist; human observations and native-dialog behaviour remain incomplete. |

No blanket downgrade of correctly qualified computational judgements is warranted merely because human testing is absent. Conversely, those judgements cannot be promoted into full user acceptance or project-wide correctness.

Figure mapping was checked against the actual capture set and report images:

| Figure / page | Evidence | Caption/claim check |
|---|---|---|
| 1 / 14 | Current architecture diagram and module imports | Correctly retrospective, not an application screenshot or original wireframe. |
| 2 / 23 | `evidence/screenshots/FIG-I16-20260908T213427339706Z/01-comparison.png` | Actual two-strategy lap comparison with pit spikes; model output, not telemetry. |
| 3 / 30 | `evidence/screenshots/FIG-I07-20260908T210757444690Z/application.png` | First deterministic GUI milestone, not the later advanced interface. |
| 4 / 36 | Advanced capture `05-search-results.png` and `search-run.json` | Completed 1,056-candidate bounded search; the displayed best total is 4,674.175 s. Does not prove a global optimum outside the search bounds. |
| 5 / 51 | Core class-relationship diagram against source | Relationships broadly valid; shorthand field labels need C07. |
| 6 / 65 | Advanced capture `02-metrics.png` | Actual totals, stops, average, fastest/slowest, pit loss and stint lengths. |
| 7 / 66 | Advanced capture `03-laps.png` | Actual per-lap components. |
| 8 / 66 | Advanced capture `04-controls.png` | Actual scrolled environment/experiment controls; the need to scroll is acknowledged. |
| 9 / 67 | Advanced capture `07-monte-carlo-results.png` and `monte-carlo-run.json` | 100 recorded trials and A-win frequency 88%, not a prediction of real racing success. |
| 10 / 67 | Advanced capture `08-monte-carlo-chart.png` | Histogram of the same recorded trials, shared-bin plotting; not a separate experiment. |

No falsely described human session or fabricated screenshot was identified. Captures establish appearance/output at that state, not accessibility, comprehension or independent operation. Readability at a user's display scale still needs real observation.

Raw benchmark claims checked:

| Measurement | Mean seconds | Actual scope |
|---|---:|---|
| Single 50-lap race | 0.000522400 | Original BENCH-01, three repeats after one single-race warm-up. |
| 1,000 sequential races | 0.796303900 | Repeated races, not one 1,000-strategy comparison. |
| Complete 1,056-candidate search | 1.161633300 | Actual full default bounded search. All three runs below 10 s. |
| 1,000 paired Monte Carlo trials | 2.099057600 | Two simulations per trial. All three runs below 30 s. |
| 2 strategies × 50 laps | 0.001120600 | Separate BENCH-COMPARE, five repeats after a per-size warm-up. |
| 20 strategies × 50 laps | 0.011749560 | compare() computation and ranking only. |
| 20 strategies × 500 laps | 0.161278460 | Largest measured comparison dimensions, not worst-case events/stops or GUI workload. |

Paths: `evidence/benchmarks/BENCH-01-20260908T212651988284Z/timings.json` and `evidence/benchmarks/BENCH-COMPARE-20260908T224158666794Z/timings.json`. Tables 23, 26-27 and Appendix D agree with the recorded values at displayed precision. Candidate-prefix timings are correctly labelled as not full search. The comparison benchmark rotates starting compounds and gives each a halfway Hard stop; it is not the exact pair of default GUI strategies. Neither benchmark measures GUI drawing, a human's response time, other machines, native ARM Python performance, confidence intervals or real-world predictive accuracy. No unsupported raw numerical benchmark claim was found within the stated scope; the SC13 narrative needs C15.

## FACTUAL CORRECTIONS FOR MITHIL TO REVIEW

All entries below have classification **REPORT FACTUAL CORRECTION NEEDED**. These are factual review points, not replacement candidate prose. No correction has been applied. “File/page” means the final master DOCX/PDF unless another file is explicitly named. Related factual detail appears in the complete class/algorithm tables above.

| ID | File/page and current wording | Why inaccurate or unclear | Source-code/evidence reference | Suggested factual point Mithil should express in his own words |
|---|---|---|---|---|
| C01 | p14, T9 Compound: “Enum values or private queue state”; Methods “Data record” | Compound has enum members, no queue state, and is not a dataclass. | `src/pitwall/models.py:25` | Identify SOFT, MEDIUM, HARD and their string values; distinguish enum members from stored dataclass fields. |
| C02 | p15, T10 Weather: same generic attributes and “Data record” | Does not identify the actual states; queue wording is unrelated. | `src/pitwall/events.py:8` | Identify DRY, DAMP, WET as enum members; no custom methods are defined here. |
| C03 | p15, T10 EventType: same generic attributes and “Data record” | Does not describe the three event kinds; no queue state belongs to this enum. | `events.py:14` | Identify WEATHER_CHANGE, SAFETY_CAR_START and SAFETY_CAR_END. |
| C04 | p15, T10 EventQueue: “Enum values or private queue state” | A fallback description conceals the actual important data structure. | `events.py:37-50` | Explain `_heap` entries `(lap, sequence, event)`, O(E) construction, stable tie order and destructive retrieval of all due events. |
| C05 | p14 T9: “__post_init__; total_time” under Methods; p15 T12/T13: “Data record” under Methods | A property and a record-kind label are not ordinary methods. | `models.py:172-184`; `monte_carlo.py:25-39`; `optimiser.py:27-29` | Separate explicit methods, `total_time` property and generated dataclass behaviour. Trial, MonteCarloResult and CandidateScore have no explicit validator. |
| C06 | p15, T11 EnvironmentalLapResult lists only five environmental attributes | They are correct added fields, but not its complete state. Nearby inheritance prose helps; the row remains ambiguous. | `conditions.py:37-51`; `models.py:145-168` | Identify the five additions and nine inherited LapResult fields; explain superclass validation rather than implying an independent five-field record. |
| C07 | p51, Figure 5: Strategy “start”; Conditions “weather”; combined RaceEvent/EventQueue “payload” | These schematic labels are not the actual field names and merge record payload with queue state. | `models.py:85`; `conditions.py:9`; `events.py:21,37` | Use or explicitly map `starting_compound`, `initial_weather`, `RaceEvent.weather` and `EventQueue._heap`. The actual PitStopPlan label `stationary_time` is already correct. |
| C08 | p11: “recorded before implementation in I08..I17 designs”; p27: “combined before implementation”; p34: “as recorded before implementation”; prospective tense in historical plans, including p24 | The records describe that order, but their current existence and seven coarse commits do not prove every paragraph preceded each edit. Page 13 already states this limitation. | `docs/design/design-provenance.md`; Appendix G; Git history; linked design/iteration files | Distinguish recorded intention from independently evidenced timing. Cite a contemporaneous version if available; otherwise retain uncertainty. Do not rewrite a later record as an original plan. |
| C09 | p13 “source hashes at execution time”; repeated extract statements that metadata identifies hashes “used for each actual test run”; p24 runner wording | `run_tests.py` hashes files after the pytest subprocess returns. This is strong consistency evidence, not an immutable pre-execution snapshot. | `scripts/run_tests.py`, `subprocess.run` followed by hash comprehension; latest metadata hashes match current files | State when hashes are captured. Do not imply they alone prove pre-test source contents or design-before-code chronology. This does not invalidate observed test outputs. |
| C10 | p22: “Result/state objects validate types, bounds and finite times”; “Floats reject ... negative values” | True for many listed core fields, not all result records or all float fields. Environmental random variation can be negative. Some frozen result dataclasses have no validator. | `models.py`; `conditions.py:44`; `monte_carlo.py:25-39`; `optimiser.py:27-29` | Scope validation claims to their actual classes/fields. Distinguish non-negative penalties/amplitude from signed per-lap random variation and from unvalidated result containers. |
| C11 | p24: “Cancellation should return promptly between laps/candidates/trials” | It is a planned behaviour statement that exceeds the current implementation; p47 correctly states the implemented limit. | `engine.py:simulate`; `monte_carlo.py:58`; `optimiser.py:53`; `advanced_gui.py:248` | Record the plan/implementation difference: checks occur between candidates/trials, not during each lap. Do not claim measured prompt cancellation without actual timing evidence. |
| C12 | p36: “New independent checks cover JSON container types, full tiny search arithmetic, reconstructing Monte Carlo trials and maximum comparison”; “independent/manual” oracle labels elsewhere | The grouped phrase overstates independence: reconstruction reuses production simulate, and maximum comparison is a consistency/boundary check. Arithmetic independence is also different from independent authorship or human execution. | `tests/test_final_robustness.py:test_independent_search_oracle`, `test_trial_reconstruction`, `test_maximum_comparison`; assistance log | Identify which expectation is derived separately, which check is replay/regression, and who actually ran it. The four-lap oracle is separately calculated but shares model data and checks a restricted case. |
| C13 | p19-20 A09: “RETURN sorted results with summaries”; dry comparison complexity | `compare` returns sorted StrategyResult objects; `summary` is a separate call. Current comparisons can include events. Earlier dry-stage complexity is not the complete current bound. | `src/pitwall/comparison.py:10-32`; `gui.py:run` | Distinguish the conceptual comparison workflow from the function API. Identify dry versus event-enabled cost and where summaries are constructed. |
| C14 | p20 search: “Time O(C*N + C log C), memory O(C*S + N)”; p21 MC main formula followed later by median refinement | Search formula omits event work/storage and has a zero-stop ambiguity; MC's summary term is supplied separately. These are scope/clarity issues, not evidence that timings are false. | `optimiser.py:32-60`; `engine.py`; `monte_carlo.py:15-22,41`; p21 refinement | Give the current event-aware bound, include candidate records even at S=0, and include MC summary sorting. Explain fixed caps and generation work. Retain historical dry formulas as historical if needed. |
| C15 | p43: “SC05 and the missing SC13 computational evidence are now satisfied”; p46: “SC13 computational evidence is now complete” after discussing comparison | SC13 as written on p12 requires search and paired-trial thresholds, both already covered by BENCH-01. Comparison was a separate performance-coverage gap. | T8 SC13; both benchmark JSON files; `docs/testing/final-quality-results.md` | Distinguish satisfying SC13's actual definition from adding comparison evidence. Do not imply comparison measures GUI latency or the exact default GUI strategy pair. |
| C16 | p45-46, T28 repeated “Illustrative model; human acceptance pending” and generic candidate-review cells | Not false, but the same reason does not explain each distinct criterion judgement. SC05's narrative supplies specificity while several others remain terse. | Each criterion's named tests; full mapping above | Explain the specific asserted fact, tested boundary and remaining limitation for each judgement using personally understood evidence. Avoid implying every computational criterion requires identical human acceptance. |
| C17 | p4-5 caption lists lack page targets; T2-4 all “Existing solution comparison”; T33-35 all “Blank human evidence form” | No numbering error, but users cannot distinguish sources/forms from the lists without searching. | Actual table contents and verified page map above | If Mithil elects to improve navigation, distinguish each subject/purpose and use actual page references. This is lower impact than missing evidence. |
| C18 | pp25-36 repeat “Implementation and recorded review...” and “Extract provenance...” fifteen times, plus generic code explanations | Repeated framing is not stage-specific candidate review. Some repeated explanation concerns a general race workflow rather than the immediate extract. | DOCX paragraphs; actual module/test/iteration record at each stage | Retain necessary provenance while distinguishing factual record framing from Mithil's own dated review. Do not replace missing reviews with newly invented retrospective thoughts. |

### Points that do not need “correction” into stronger claims

- The report's blank stakeholder/usability/candidate responses must stay blank until those people actually provide the information.
- Appendix K must retain its complete assistance scope. “Limited assistance” or an unsupported percentage would contradict the present record.
- Current-source diagrams and late research must retain their retrospective labels.
- SC04 and SC14 must not be marked fully successful for usability on the strength of automated tests alone.
- The 86-case historical run remains correct for its date; 87 is the later final suite. Do not replace the old evidence.
- The capture failure remains distinct from the two actual pytest failures. A transcript is not the original raw traceback.
- Benchmarks remain local computational measurements. The low times do not establish user comprehension, real-race accuracy or performance on untested equipment.

## CANDIDATE HIGH-VALUE ACTIONS

Ranking reflects likely value to the assessment case, not guaranteed marks. No answers, reflections, feedback or assessed implementation are supplied here. Any further assessed work must follow centre guidance.

| Priority | Action | Responsible classification | Likely assessment value and completion evidence |
|---|---|---|---|
| 1 | Resolve authentication and permitted next steps with the complete record | TEACHER/CENTRE MUST CONFIRM | Affects whether any content can be credited. Review Appendix K, assistance log, report, source, tests and current candidate understanding. Determine acceptable work and declaration process; do not approve by assuming a small assistance share. |
| 2 | Demonstrate personal understanding and distinguish real contribution from assisted material | CANDIDATE MUST DO | Underpins all six categories. Explain the actual algorithms, validation, tests, limits and historical contribution. Use real code and inputs; record what was reviewed or changed and when. Present understanding does not rewrite authorship. |
| 3 | Conduct genuine usability testing with an appropriate real user | HUMAN USER MUST DO | Direct missing evidence for evaluation testing and usability evaluation. The person must actually operate the system and report their own experience. |
| 4 | Plan, observe and document that session factually | CANDIDATE MUST DO | Preserve task steps, actual outcomes, assistance, errors and direct comments; analyse their relationship to criteria. Do not estimate unmeasured timings or complete forms from expectation. |
| 5 | Obtain genuine stakeholder consultation about needs and the prototype | STAKEHOLDER MUST DO | Tests assumptions behind analysis and evaluation and identifies an actual priority. Record the real date and status as post-prototype consultation. A user and stakeholder may be the same person if that accurately describes their role. |
| 6 | Choose one justified feedback-driven iteration, if permitted and genuinely needed | CANDIDATE MUST DO | Can connect analysis, design, development, testing and evaluation. Choose the change from actual evidence; do not add features merely to make the project larger. |
| 7 | Record prospective design and expected tests before implementing that change | CANDIDATE MUST DO | Addresses the provenance gap with genuinely new evidence. Preserve the decision, alternatives, data/algorithm/UI implications, expected results and dated baseline before code exists. |
| 8 | Personally implement and run the permitted iteration's tests | CANDIDATE MUST DO | Demonstrates new candidate development and test reasoning. Keep real commands/results, unchanged reproduction cases where applicable, actual failures and retests. If nothing fails, record that honestly. This audit creates no code. |
| 9 | Obtain real follow-up use/review of the resulting change | HUMAN USER MUST DO | Supplies comparative usability evidence from actual operation, including unresolved problems. |
| 10 | Confirm whether the revised result meets the stakeholder's actual need | STAKEHOLDER MUST DO | Provides real acceptance or remaining concerns; it must not be inferred from a successful automated test. |
| 11 | Evaluate the resulting change and whole solution personally | CANDIDATE MUST DO | Connect actual before/after evidence to criteria and limitations. Justify outcomes rather than listing passed tests or copying prepared prose. |
| 12 | Review factual corrections, especially the class tables and independence claims | REPORT FACTUAL CORRECTION NEEDED | Improves accuracy and candidate explanation. Any later report edit belongs to Mithil's permitted process, not this audit. |
| 13 | Use existing technical evidence efficiently | OBJECTIVE TECHNICAL EVIDENCE ALREADY EXISTS | The raw tests, failure/retest, tolerance result, catalogue and benchmarks already exist. Extra execution is valuable only when it tests a real change, unresolved case or candidate activity. |
| 14 | Complete final authentication and submission checks after actual follow-up | TEACHER/CENTRE MUST CONFIRM | Confirm creditable evidence, required declarations, centre criteria, privacy and submission arrangements. A technical audit cannot authenticate candidate work. |

## AUTHENTICATION RISK

**The current record describes assistance across central assessed work, not a small isolated contribution.** Appendix K and `docs/assistance-log.md` agree on the six stages below. No percentage is recorded or defensibly calculable from lines, commits, test counts or document length. The record must not be minimised or disguised.

| Recorded date/stage | Exactly what the record attributes to external assistance | Affected scope | Candidate follow-up currently recorded |
|---|---|---|---|
| 2026-09-08, planning and records | Drafted requirements, designs, diagrams, development records, README and evaluation; reviewed three sources after the prototype | `docs/`, `README.md`, `report/` | Candidate supplied brief; subsequent review not recorded. |
| 2026-09-08, implementation | Authored simulation, comparison, GUI, environmental events, randomness, Monte Carlo, search and persistence modules | `src/pitwall/`, `main.py`, `launch.ps1` | Personal changes or explanation not recorded. |
| 2026-09-08, verification | Wrote/ran tests; fixed JSON validation and capture-harness issues; captured/inspected actual GUI output and ran benchmarks | `tests/`, `scripts/`, `evidence/` | Personal testing or review not recorded. |
| 2026-09-08, cleanup | Reorganised public documentation and consolidated attribution | Files identified in `report/documentation-cleanup.md` | Candidate requested cleanup; review of edits not recorded. |
| 2026-09-08, master report | Assembled and checked the evidence-based DOCX/PDF, diagrams and completeness audit | `report/`; SC05 evidence judgement in `docs/evaluation/review.md` | Candidate requested report; personal review and missing human evidence remain pending. |
| 2026-09-08, final quality pass | Added explicit tolerance verification and comparison benchmark; prepared blank human forms, final report and local release files | `tests/test_sc05_tolerance.py`, `scripts/benchmark_comparison.py`, `docs/`, `report/`, public packaging | Candidate requested quality pass; personal explanations, human sessions and centre approval remain pending. |

The recorded tool is **Codex**. The source-review note says there were no hands-on trials or copied source code/parameters in that source review. That note does not negate the separate record of externally authored implementation. The record also says execution records, captures and Git history remain intact.

**TEACHER/CENTRE MUST CONFIRM:** what parts can be authenticated and credited, what additional candidate work is permitted, which declaration/support records must accompany the submission, and whether the candidate can meet the centre's requirements. The official specification requires authentic, appropriately referenced work reflecting the learner's ability; it does not let this audit determine an individual malpractice outcome. Disclosure is necessary evidence for review, not automatic permission or authentication.

**CANDIDATE MUST DO:** report actual personal review, changes, tests and explanation only when they occur. Do not retrospectively claim writing the existing source, creating the prepared prose, running the existing assisted tests, receiving stakeholder input or experiencing particular development difficulties. Teacher questioning and present understanding can demonstrate current knowledge; they do not change the origin of earlier work.

This audit itself was produced with external assistance on 9 September 2026. It is an advisory gap review, not candidate-assessed prose, a completed reflection or a centre decision. The assistance log has deliberately not been edited because this task prohibits altering it. The centre can decide how this additional audit should be recorded through its own process.

## CURRENT STRONGEST AREAS

- Modular functioning implementation with explicit limits, pure computational modules and real GUI integration.
- Preserved stage testing, a genuine failed-test/remedy/retest chain and source-hash consistency.
- Separately derived small arithmetic expectations, an explicit SC05 tolerance check and bounded-search verification.
- Actual screenshots, complete run exports and raw benchmarks whose summaries reconcile.
- Honest model limitations and existing acknowledgement of missing human evidence.

## CURRENT WEAK AREAS

- Unresolved authentication across extensive assisted assessed material.
- No completed real-user usability or stakeholder-review evidence.
- Candidate understanding, personal testing and reflections remain unrecorded.
- Retrospective documentation cannot establish every prospective design decision or prototype stage.
- Generic class descriptions, broad independence wording and some scope/provenance inconsistencies reduce factual precision.

## CURRENT OCR GAPS

- A defensible, authenticated candidate contribution and reasoning trail.
- Stronger justification connecting audience needs, research, choices and acceptance criteria.
- Accurate class/algorithm documentation and credible evidence of design timing.
- Genuine usability testing and evidence-based evaluation of feature effectiveness.
- Candidate interpretation of technical outcomes, with any prospective feedback cycle documented honestly.
- Centre confirmation of creditable work and its own additional criteria. No claim of 70/70 is supported by this audit.

## WHAT MITHIL PERSONALLY MUST DO

Review the real source and evidence, demonstrate understanding, accurately identify personal contribution, conduct and document real sessions, and write only his own permitted analysis/evaluation of actual events. If further work is allowed and warranted, design before implementing one real feedback-driven change, run its tests and evaluate its result. Review the factual corrections himself. Do not use this audit as prewritten assessed prose.

## WHAT A REAL USER MUST DO

Actually use PITWALL for the planned tasks, interpret its graphs and probability output, try error recovery and relevant save/load/cancellation actions, and provide genuine outcomes and comments. Any follow-up observation must occur after the actual change being assessed.

## WHAT A REAL STAKEHOLDER MUST DO

Explain actual needs, priorities and constraints, review the current prototype, identify useful or unsuitable behaviour and give a real follow-up judgement where appropriate. Consultation now must be dated and described as occurring now, not as original pre-development research.

## WHAT THE TEACHER MUST CONFIRM

Review the full assistance declaration and authenticated candidate evidence; decide what can be credited and what further work is permitted; provide the missing centre criteria and declaration requirements; confirm participant/privacy and submission arrangements; and make the actual best-fit assessment. No tool-generated audit, passing suite or public portfolio description can replace that decision.

## Audit-only preservation statement

The intended and sole new output of this task is `report/FINAL_OCR_70_OUT_OF_70_GAP_AUDIT.md`. The assessed report, candidate prose, reflections, participant forms/results, assistance log, code, project features and existing evidence are left unchanged. No Git commit, reset, rebase, deletion or history rewrite is part of this task. The pre-existing working tree is preserved.
