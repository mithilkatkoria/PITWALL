# Iteration 7 design: first usable GUI

Requirements FR01..FR08. PySide6 widgets, Matplotlib Qt canvas. No decorative imagery. Dark panels, high contrast text, labelled inputs with units, compound text plus colour, read-only output tables, explicit pending/invalid/result status. Keyboard-operable Qt controls.

Planned layout: title and model disclaimer; left race and tyre inputs; centre/right chart, ranked summary and lap table tabs; strategy editor below chart; run-selected and compare-all buttons. Changing inputs invalidates old output immediately so stale results cannot appear current. Strategy selection in output chooses whose lap rows are shown.

Data conversion: numeric widgets -> validated config; strategy rows -> Strategy. Stop entry syntax `15:Medium, 35:Hard` with a shared configurable stationary time. Blank means no stops. Parser accepts case-insensitive supported compound names, rejects missing separators, unknown compounds and invalid laps; model validates ordering and race boundary. No silent reordering. Names unique for comparisons.

```text
ON input change: clear old output and request new simulation
ON run:
    READ and VALIDATE configuration
    READ selected strategy or all strategies
    TRY simulation/comparison
    ON validation error: clear output and show explanatory status
    ON success: plot lap/time from returned records, populate ranking
        select first result and populate per-lap table
```

Synchronous execution is limited to 500 laps and 20 strategies. Later Monte Carlo/search must consider a worker and cancellation. GUI exposes only implemented actions.

Planned TEST-I07: parser typical/blank/erroneous cases; instantiate real window; compare defaults and assert 2 lines of 50 points; select single strategy and assert 50 lap rows; modify race length and ensure stale output clears; malformed stop -> visible error and no output; add/remove strategies; capture actual Qt widget output. This is automated integration/visual evidence, not a real stakeholder usability session.

Manual post-development plan: genuine user opens app, configures five laps, creates two strategies, runs, identifies faster total and pit spike, changes parameters, corrects a bad stop. Record completion, errors, help, comments only when performed by a user. Test keyboard navigation and display scaling on their machine. No responses yet.
