# Iteration 11 design: seeded variation

FR11. Conditions adds seed integer 0..2^32-1 and variation amplitude seconds (default 0). Use a private `random.Random(seed)` per simulation, never global state. Draw uniform [-amplitude,+amplitude] once each lap and record the exact draw. Uniform bounded noise is simpler than normal noise and cannot create arbitrarily extreme negative times. Reject amplitude >= circuit base time, ensuring positivity since all other terms are non-negative.

```text
rng = new generator(seed)
FOR each lap:
    noise = uniform(-amplitude, amplitude) if amplitude > 0 else 0
    ADD noise and RECORD it
```

O(1) per lap. Same inputs/seed reproduce on the recorded Python environment. Compared strategies use the same draw per lap to hold common driving disturbances constant. This also means additive noise alone cannot change relative ranking; Monte Carlo must explain that fact.

Planned TEST-I11: seed repeat exact; different seeds change noisy output; zero noise matches dry totals; each draw bounded; global random state unchanged; invalid seed and excessive amplitude rejected.
