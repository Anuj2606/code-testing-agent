# Case study 3: what the harder tasks revealed

16 harder tasks were added (36 total). 12 passed first try. Four failed first and were fixed by the agent
(`sort_06` 2 iterations, `sort_07` 3, `data_07` 2, `search_07` 3). Two results taught more than the rest.

## `string_06`: passes its own tests, fails the real ones

Task: evaluate `+ - * /` expressions such as `3+2*2` (spaces optional).

The agent's solution starts with `expr.split()`, which assumes spaces between tokens. Input `3+2*2` becomes the
single token `'3+2*2'` and `int('3+2*2')` raises `ValueError`. The agent's own tests only used spaced input
(`3 + 2 * 2`), so they passed on iteration 1 and the run was recorded as a success.

- agent's own tests: **pass**; hidden tests: **fail** (3 of 4 tests).
- This is the gap `verified_rate` exists to expose: self-written tests can share the solution's blind spot.
- The test prompt now asks for every example and input format in the task text, exactly as written. A re-run
  did **not** change the outcome, so this is recorded as an open limitation, not a fix.

## `search_07`: two tooling bugs hid a correct solution

Task: shortest path in a grid. The agent's final code was correct (it passes the hidden tests), but the first
run was recorded as a failure after 5 iterations:

1. **Detector false positive.** `looks_hardcoded()` flagged `(r, c) == end`, a tuple of *variables* compared with
   an argument, as hard-coding. A legitimate solution was rejected and the loop continued. Fix: only count
   comparisons against pure literals (`ast.literal_eval`).
2. **Missing import.** After a test repair, the regenerated tests called `pytest.raises` without importing
   pytest, giving `NameError` on iterations 4 and 5. Fix: the sandbox always provides `import pytest`.

The agent's own test was also wrong (it expected 4 steps; the correct answer is 6), which is what triggered the
repair path, so this run is the first live exercise of test repair. After the fixes, `search_07` passed in 3
iterations with no false flag.

## Takeaways

- Every safety mechanism (hard-coding detection, test repair) produced its own failure modes in a live run.
  Detectors need regression tests built from real false positives.
- Success against the agent's own tests overstates correctness (36/36 vs 35/36 on hidden tests).
- Two tasks were re-run after tooling fixes; both runs are archived in `results/benchmarks/`.
