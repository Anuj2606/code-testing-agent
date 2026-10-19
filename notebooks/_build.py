"""Generates the Week 1 notebooks (run once: python notebooks/_build.py)."""
import json
from pathlib import Path


def nb(cells):
    out = []
    for kind, src in cells:
        c = {"cell_type": kind, "metadata": {}, "source": src.strip("\n").splitlines(keepends=True)}
        if kind == "code":
            c.update(execution_count=None, outputs=[])
        out.append(c)
    return {"cells": out, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                       "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}


SETUP = [
    ("markdown", "# 00 - Setup\nVerifies the Gemini API, the sandbox, and dependencies."),
    ("code", "import sys, os\nsys.path.insert(0, os.path.abspath('..'))\nfrom src.utils import config\nprint('model:', config.MODEL_NAME)\nprint('API key set:', bool(config.GEMINI_API_KEY))"),
    ("markdown", "## Gemini API"),
    ("code", "from src.tools.code_generator import generate_code\nprint(generate_code('Sort a list of integers in descending order'))"),
    ("markdown", "## Sandbox\nA good snippet passes; an unsafe import, an infinite loop and a syntax error are all blocked."),
    ("code", "from src.tools.code_executor import execute_code\ncode = 'def solution(xs):\\n    return sorted(xs)\\n'\ntests = 'def test_a():\\n    assert solution([2, 1]) == [1, 2]\\n'\nprint('good   :', execute_code(code, tests)['success'])\nprint('import :', execute_code('import os', '')['stderr'])\nprint('loop   :', execute_code('def solution():\\n    while True: pass', 'def test_a():\\n    solution()', timeout=2)['stderr'])\nprint('syntax :', execute_code('def f(:', '')['stderr'])"),
    ("markdown", "## Dependencies"),
    ("code", "import importlib\nfor m in ['google.genai', 'pytest', 'yaml', 'dotenv', 'RestrictedPython']:\n    try:\n        importlib.import_module(m); print('ok     ', m)\n    except ImportError:\n        print('MISSING', m)"),
]

ARCH = [
    ("markdown", "# 01 - Agent Architecture\nThe agent runs a ReAct loop: **THINK** (generate or fix?) -> **ACT** (call Gemini, run tests) -> **OBSERVE** (pass/fail) -> **DECIDE** (stop or iterate)."),
    ("code", "import sys, os\nsys.path.insert(0, os.path.abspath('..'))\nfrom src.agent.code_agent import CodeGenerationAgent"),
    ("markdown", "## Offline demo (no API)\nA fake generator returns a buggy first draft, then a fix, showing the self-repair loop."),
    ("code", "class FakeGen:\n    def generate_code(self, task, error_context='', previous_code=''):\n        return 'def solution(xs):\\n    return sorted(xs)\\n' if error_context else 'def solution(xs):\\n    return xs\\n'\n    def generate_tests(self, code, task):\n        return 'def test_a():\\n    assert solution([2, 1]) == [1, 2]\\n'\n\nr = CodeGenerationAgent(generator=FakeGen()).run('sort a list')\nprint(r['success'], 'iterations:', r['iterations'])"),
    ("markdown", "## Live run with Gemini"),
    ("code", "agent = CodeGenerationAgent()\nr = agent.run('Sort a list of dictionaries by their age field, handling missing age keys')\nprint('success:', r['success'], '| iterations:', r['iterations'])\nprint(r['code'])"),
    ("markdown", "## Per-iteration history"),
    ("code", "for h in agent.get_conversation_history():\n    print('iteration', h['iteration'], '->', 'PASS' if h['result'].get('success') else 'FAIL')\n    print(h['code'], '\\n')"),
]

TOOLS = [
    ("markdown", "# 02 - Tool Design\nThe four tools the agent composes: **generator** (LLM), **executor** (sandbox), **test runner** (pytest), **debugger** (error analysis)."),
    ("code", "import sys, os\nsys.path.insert(0, os.path.abspath('..'))"),
    ("markdown", "## 1. Code generator"),
    ("code", "from src.tools.code_generator import generate_code, generate_tests\ntask = 'Remove duplicates from a list preserving order'\ncode = generate_code(task)\ntests = generate_tests(code, task)\nprint(code); print(); print(tests)"),
    ("markdown", "## 2. Executor (sandbox)\nStatic screen (imports, `eval`/`open`...), then an isolated `python -I` subprocess with a timeout."),
    ("code", "from src.tools.code_executor import execute_code, screen_code\nprint(screen_code('import os'))\nprint(screen_code('x = eval(\"1\")'))\nprint(screen_code(code))"),
    ("markdown", "## 3. Test runner\nStructured pass/fail details from pytest output."),
    ("code", "from src.tools.test_runner import run_tests\nr = run_tests(code, tests)\nprint({k: r[k] for k in ('success', 'passed', 'failed', 'failed_tests')})"),
    ("markdown", "## 4. Debugger\nParses a failure and builds the repair context handed back to the generator."),
    ("code", "from src.tools.test_runner import run_tests\nfrom src.tools.debugger import analyze_error, generate_fix_prompt\nbad = 'def solution(xs):\\n    return xs[0] / 0\\n'\nr = run_tests(bad, 'def test_a():\\n    assert solution([1]) == 1\\n')\nprint(analyze_error(r['error'], bad)); print(); print(generate_fix_prompt(r['error'], bad))"),
    ("markdown", "## 5. Closing the loop\nThe debugger output feeds `generate_code(..., error_context=..., previous_code=...)`."),
    ("code", "fixed = generate_code('Return the first element divided by 1', generate_fix_prompt(r['error'], bad), bad)\nprint(fixed)"),
]

EVAL = [
    ("markdown", "# 03 - Evaluation\nReads the saved benchmark results (`results/benchmarks/`); makes **no** API calls."),
    ("code", "import sys, os, json\nsys.path.insert(0, os.path.abspath('..'))\nimport pandas as pd\nfrom IPython.display import Image, display\nfrom src.evaluation.metrics import generate_report\nrs = json.load(open('../results/benchmarks/raw_results.json'))\nrep = generate_report(rs, False)\npd.Series({k: v for k, v in rep.items() if not isinstance(v, (dict, list))})"),
    ("markdown", "## Per-task results"),
    ("code", "df = pd.DataFrame(rs)[['task_id', 'category', 'difficulty', 'success', 'verified', 'iterations', 'seconds']]\ndf"),
    ("markdown", "## By category"),
    ("code", "pd.DataFrame(rep['by_category']).T"),
    ("markdown", "## Plots"),
    ("code", "for p in ['success_rate_by_task', 'iterations_distribution', 'time_per_task']:\n    display(Image(f'../results/plots/{p}.png'))"),
    ("markdown", "## Reading the numbers\n- **52 tasks** (10 easy, 26 medium, 16 hard). All 52 pass the agent's own tests; **51/52 pass the hidden reference tests**.\n- **First-try 47/52 (95% CI 79-96%)**; the 5 that failed first (`sort_06`, `sort_07`, `data_07`, `search_07`, `search_10`) were all fixed autonomously: **5/5, but the 95% interval is only 57-100%**, so the 70% target is neither proven nor refuted. Hard tasks: 13/16 first-try.\n- `search_10` is the first live case of the test-repair path working end to end (`results/case_studies/task_4_test_repair_works.md`).\n- **Model confound**: the last 16 tasks ran mostly on `gemini-3.8-flash`, the first 36 mostly on `gemini-3.5-flash-lite`.\n- **`string_06` is the self-testing gap**: it passes the agent's own tests but fails the hidden ones (the solution splits on spaces and breaks on `3+2*2`; the agent's tests only used spaced input).\n- **Disclosure**: `search_07` and `string_06` were re-run once after tooling fixes (a hard-coding-detector false positive, a missing `import pytest`, a stricter test prompt). The earlier results are kept in `raw_results_run2_36tasks.json`. `search_04` was re-run after the anti-hard-coding changes; run 1 is in `raw_results_run1.json`.\n- Latency averages ~30 s (target <30 s), inflated by 503 'high demand' retries on the free tier.\n- Results mix several Gemini free-tier models, because the router rotates when one hits its daily quota."),
    ("markdown", "## Next\nGrow toward 100 tasks. The current model solves most tasks first time, so more failures need harder tasks (or a weaker model) to tighten the self-fix interval."),
]

here = Path(__file__).parent
for name, cells in [("03-evaluation.ipynb", EVAL),("00-setup.ipynb", SETUP), ("01-agent-architecture.ipynb", ARCH), ("02-tool-design.ipynb", TOOLS)]:
    if (here / name).exists() and "--force" not in __import__("sys").argv:
        continue  # keep already-executed notebooks (with outputs)
    (here / name).write_text(json.dumps(nb(cells), indent=1), encoding="utf-8")
    print("wrote", name)
