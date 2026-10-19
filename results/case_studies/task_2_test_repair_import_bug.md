# Case study 2: the test repair that broke the tests

**Task (`search_04`, re-run after the anti-hard-coding changes).**

## What happened

| Iter | Action | Result |
|---|---|---|
| 1 | Generate | FAIL: generated test says the 3rd largest of `[1,2,2,3,3,3]` is 2 (it is 3) |
| 2 | Fix | FAIL: same test, same reason |
| 3 | **Repair tests** (triggered because the same test failed twice) | FAIL: `ModuleNotFoundError: No module named 'solution'` |
| 4-5 | Fix | FAIL: same import error |

The new detection worked: the identical failure was spotted and the tests were regenerated. The regenerated
tests then began with `from solution import solution`. In the sandbox the solution and tests share one
module, so that import cannot succeed. Iterations 4 and 5 then tried to "fix" solution code that was already
correct; the final code did pass the hidden reference tests.

## Root cause

The test-repair prompt did not say "do not import the solution", unlike the original test prompt. The run
was a failure caused by the agent's own tooling.

## Fixes made

- The repair prompt now says the solution is already in scope.
- `sanitize_tests()` (`src/utils/helpers.py`) strips `from solution import ...` and similar lines from every
  generated test as a safety net.

A re-run of the task then passed on iteration 1, so this fix has **not** been exercised by a live repair; it is
covered by `tests/test_code_generator.py::test_self_imports_are_stripped_from_tests`.

## Takeaway

New recovery paths need their own tests. The repair step existed for one iteration before a live run found a
bug that unit tests had not.
