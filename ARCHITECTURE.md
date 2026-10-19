# Architecture

## The loop

```
task -> THINK -> ACT -> OBSERVE -> DECIDE -> (repeat, max 5)
        |        |        |
        |        |        +- pytest result (pass/fail, failing test names, error text)
        |        +- generate / fix code, or repair tests; then run tests in the sandbox
        +- chooses the action from the history (see below)
```

`src/agent/code_agent.py` owns the loop. Per-run state (code, tests, errors, every code version) lives in
`src/agent/state_manager.py`.

**THINK** picks one of three actions:

| Condition | Action |
|---|---|
| No code yet | `generate`: one request returning solution and tests together |
| Last failure differs from the one before | `fix`: debugger analysis + failing code go back to the model |
| The same named test failed on two consecutive iterations | `repair_tests`: revert to the last non-hard-coded code, regenerate the tests |

**OBSERVE** also applies a guard: a "passing" result whose code branches on an argument equalling a literal
(`looks_hardcoded`) is rewritten as a failure that inherits the previously failing tests, so the loop notices it
is stuck on the same test.

## Tools (`src/tools/`)

| Tool | Role |
|---|---|
| `code_generator.py` | Prompts the LLM for solution+tests, fixes, and test repairs; strips self-imports from tests |
| `code_executor.py` | Static screen, then an isolated `python -I` subprocess with a timeout; `pytest` always in scope |
| `test_runner.py` | Runs pytest in the sandbox and condenses the output |
| `debugger.py` | Traceback parsing, failure classification, `looks_hardcoded`, `same_failure` |
| `llm.py` | Model router: ordered Gemini pool with persisted per-model daily quota; optional Ollama |

## LLM router (`src/tools/llm.py`)

Free-tier quotas are per project and per model, so the router treats `gemini_models` as an ordered pool.

- Use the first model not marked exhausted today.
- `429 ... PerDay` -> mark that model exhausted until the next quota day (midnight Pacific, approximated as
  UTC-8) and move on.
- `429` per-minute -> wait the suggested delay, retry the same model.
- `503`/`500`/other -> fall through to the next model without marking it exhausted.
- `404` -> the model is retired; mark it exhausted.
- Every model spent -> raise `QuotaExhausted`. The agent reports an `api_error`, and the benchmark does not record
  the task, so infrastructure failures never count against the agent.

State is saved in `results/logs/llm_usage.json` (old-format files are ignored).

## Design decisions

- **Tests are generated once and held fixed**, so the agent cannot make a failure disappear by weakening the test.
  The cost is that a wrong test is unfixable, which is why the repair path and the hard-coding guard exist.
- **Hidden reference tests** (`src/data/test_datasets*.py`) are never shown to the agent. The benchmark reports
  *success* (own tests pass) and *verified* (hidden tests pass); the gap measures how far self-checking can be
  trusted. Every hidden suite is validated against a known-good solution in `src/data/reference_solutions*.py`.
- **Sandbox**: RestrictedPython cannot host pytest, so isolation is an AST screen (banned imports and calls) plus a
  subprocess with a hard timeout. It is not a security boundary; use a container for untrusted workloads.
- **API errors are not code failures.** Transient errors retry, permanent ones stop the run, and neither burns
  agent iterations.
- **One request for code and tests** on the first iteration, with a fallback to a second request if the reply
  has only one block. This roughly halves first-iteration usage.
- **Global agent state**: the agent keeps module-level state, so the API serialises runs with a lock.

## Metrics (`src/evaluation/`)

Success rate, clean success rate (excluding hard-coded solutions), verified rate, first-try rate, self-fix rate
(of tasks that failed iteration 1, the share eventually fixed), iterations to success, failure modes,
per-category breakdown, seconds per task. `run_batch` runs the next unfinished tasks and saves after each one.

## Lessons recorded in `results/case_studies/`

Each safeguard added to the loop (hard-coding detection, test repair) produced its own failure mode that only a
live run exposed: a detector false positive, tests importing the solution, tests using an unimported `pytest`.
Detectors and repair paths need regression tests built from real failures.
