# PITWALL provisional analysis

Candidate: Mithil Katkoria. Candidate number: 0460. Centre: 12709.

Source: user project brief supplied 2026-09-08. These are provisional candidate requirements, not stakeholder findings. The separate centre checklist has not been supplied. No marks are claimed.

Race strategy is a computational problem because tyre choice and pit timing interact over many laps. A faster fresh tyre can cost more time as it ages; stopping exchanges an immediate loss for later gains. Repeating arithmetic consistently allows controlled comparison. PITWALL abstracts a single car and a dry track, decomposes validation, lap calculation, simulation and presentation, iterates over laps and selects pit actions. Tables and graphs make changing pace visible.

## First milestone

| ID | Requirement | Source | Priority | Justification | Acceptance |
|---|---|---|---|---|---|
| FR01 | Configure race length and base pace | Brief | Must | Compare race scenarios | SC01 |
| FR02 | Configure Soft, Medium, Hard pace and degradation | Brief | Must | Model compound trade-offs | SC02 |
| FR03 | Create strategies with ordered pit stops | Brief | Must | Explore alternative stints | SC03 |
| FR04 | Reject invalid values with explanations | Brief | Must | Prevent misleading results | SC04 |
| FR05 | Simulate a deterministic dry race | Brief | Must | Establish correctness before uncertainty | SC05 |
| FR06 | Show per-lap and total results | Brief | Must | Make calculation inspectable | SC06 |
| FR07 | Compare at least two strategies under identical conditions | Brief | Must | Support strategy decisions | SC07 |
| FR08 | Plot actual simulated lap times in a desktop GUI | Brief | Must | Expose changes over race distance | SC08 |
| FR09 | Save and load a scenario as JSON | Brief | Later | Repeat comparisons | Separate iteration |
| FR10 | Process weather and safety-car events chronologically | Brief | Later | Explore changing conditions | Separate iteration |
| FR11 | Add seed-reproducible randomness and Monte Carlo statistics | Brief | Later | Quantify model uncertainty | Separate iteration |
| FR12 | Search constrained legal strategies and compare baselines | Brief | Later | Evaluate explainable algorithms | Separate iteration |

## Measurable success criteria

| ID | Criterion and measurement | Link | Justification |
|---|---|---|---|
| SC01 | Accept integer race lengths 1..500 and positive base lap time; reject 0, negative, fractional and oversized lengths | FR01 | Finite, useful interactive scope |
| SC02 | All three compounds have configurable non-negative pace penalties and linear degradation; age 3 at 0.2 s/lap gives 0.6 s | FR02 | Explainable arithmetic |
| SC03 | Ordered distinct stops after laps 1..N-1 change compound on the following lap and add pit loss exactly once | FR03 | Unambiguous lap indexing |
| SC04 | Automated typical, boundary and erroneous cases raise descriptive errors; GUI shows an error for malformed stops | FR04 | Actionable validation |
| SC05 | Two runs of identical inputs return equal results; five-lap manual oracle matches each lap within 1e-9 seconds | FR05 | Reproducibility and independent oracle |
| SC06 | Exactly N lap rows; total equals sum of lap times; tyre age resets after a stop | FR06 | Complete inspectable output |
| SC07 | At least two strategies produce ranked total, average, fastest, slowest, pit loss, stop count and stint lengths | FR07 | Useful direct comparison |
| SC08 | Real Qt application opens and renders a graph with N points per compared strategy; manual usability remains separately pending | FR08 | Viewable genuine output |

## Stakeholders and research pending

Potential real stakeholder categories: student motorsport enthusiasts learning trade-offs, a computer science teacher reviewing explainability, and a club racing participant assessing model limitations. No specific person has agreed to participate.

Interview questions: What strategy decisions do you want to explore? Which inputs can you explain? What output helps compare strategies? How should errors be presented? Which simplifications would make the result misleading? Can you interpret a pit-lap spike?

[GENUINE STAKEHOLDER RESPONSE REQUIRED]

Research of three existing solutions is pending. Do not treat the brief as external research or attribute requirements to unconsulted stakeholders.

## Assumptions and limitations

| Limitation | Explanation | Reason | Impact |
|---|---|---|---|
| Linear degradation | Loss grows with completed tyre laps | Transparent initial model | Does not capture thermal effects or cliffs |
| Single car | No traffic or overtaking | Manageable initial scope | Fastest model strategy may fail in a real race |
| Dry track | No events in first milestone | Establish correctness first | Cannot evaluate rain decisions |
| Illustrative parameters | Defaults are invented model inputs, not telemetry | No proprietary data | Results are conditional, not real race predictions |

Developer software: Python 3, PySide6 for desktop widgets, Matplotlib for plots, pytest for logic tests, Git for genuine history. Stakeholder software initially needs the same Python environment. Minimum hardware has not been measured; do not publish an untested specification. Initial development is on this Windows workspace.
