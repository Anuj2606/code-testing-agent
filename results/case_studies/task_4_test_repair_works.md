# Case study 4: the test-repair path working, live

**Task (`search_10`):** `solution(s, words)` returns the sorted distinct start indices where any word occurs
in s (overlapping allowed).

## What happened

| Iter | Action | Result |
|---|---|---|
| 1 | Generate solution + tests | FAIL: test expects `[0, 9, 12]` for `("barfoothefoobarman", ["foo","bar"])` |
| 2 | Fix | FAIL: same test, same reason |
| 3 | **Repair tests** (same test failed twice) | PASS |

The solution was correct from iteration 1. It returns `[0, 3, 9, 12]`, which is right: "bar" at 0 and 9, "foo" at
3 and 12, and the hidden tests agree. The generated test expected `[0, 9, 12]`, the answer to a *different*, famous
puzzle (substring made of all the words concatenated). The model matched the string to the puzzle it knew
instead of reading the task.

The loop behaved as designed: after the same test failed on two consecutive iterations, the agent stopped editing
correct code, reverted to the last honest version, regenerated the tests, and passed.

## Why it matters

- It is the first live run where test repair worked end to end. Case studies 1 and 2 describe the bugs that
  stood in the way (a hard-coding "pass" and tests that imported the solution).
- It shows the failure the design was built for: a wrong self-written test that a frozen-test loop can never
  satisfy. Without repair, this task would have ended as a failure even though the code was right.
- It is also a reminder that "the test failed" and "the code is wrong" are different claims. The agent needed
  a rule for telling them apart: repeated identical failure after a fix points at the test.

## Caveat

One success is an anecdote, not a rate. Five tasks have now failed first and all five recovered, but the
95% interval on that is 57-100%.
