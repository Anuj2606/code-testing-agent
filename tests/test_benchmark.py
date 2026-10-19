"""Task data must be self-consistent: every task's hidden tests pass against a known-good solution,
and the metrics code works on synthetic records. No API key needed."""
from src.data.task_loader import load_coding_tasks
from src.evaluation.metrics import generate_report
from src.tools.code_executor import execute_code


def test_task_set_shape():
    tasks = load_coding_tasks()
    assert len(tasks) >= 20
    assert len({t["id"] for t in tasks}) == len(tasks)
    assert len({t["category"] for t in tasks}) >= 5


def test_reference_tests_are_valid_python_and_reject_stub():
    # A stub that returns None must fail every task's hidden tests (tests aren't vacuous).
    for t in load_coding_tasks():
        r = execute_code("def solution(*a, **k):\n    return None\n", t["reference_tests"])
        assert not r["success"], t["id"]
        assert "SyntaxError" not in r["stdout"] + r["stderr"], t["id"]


def test_every_task_has_a_reference_solution_that_passes_its_hidden_tests():
    from src.data.reference_solutions import SOLUTIONS
    tasks = load_coding_tasks()
    assert {t["id"] for t in tasks} == set(SOLUTIONS)
    for t in tasks:
        r = execute_code(SOLUTIONS[t["id"]], t["reference_tests"])
        assert r["success"], f"{t['id']}: {r['stdout'][-600:]}"


def test_plots(tmp_path):
    from src.evaluation.plots import generate_plots
    rs = [{"task_id": "a", "category": "x", "success": True, "verified": True, "iterations": 1,
           "first_try": True, "seconds": 1, "errors": []},
          {"task_id": "b", "category": "y", "success": False, "verified": False, "iterations": 5,
           "first_try": False, "seconds": 3, "errors": ["AssertionError"]}]
    paths = generate_plots(rs, tmp_path)
    assert len(paths) == 4 and all(p.exists() and p.stat().st_size > 0 for p in paths)


def test_wilson_interval():
    from src.evaluation.metrics import wilson_interval
    lo, hi = wilson_interval(5, 5)
    assert 0.55 < lo < 0.58 and hi == 1.0       # 5/5 is not "100%": the lower bound is about 57%
    assert wilson_interval(0, 0) == (0.0, 1.0)
    lo, hi = wilson_interval(50, 100)
    assert 0.40 < lo < 0.41 and 0.59 < hi < 0.60


def test_metrics():
    rs = [
        {"task_id": "a", "category": "x", "success": True, "verified": True, "iterations": 1, "first_try": True, "seconds": 1, "errors": []},
        {"task_id": "b", "category": "x", "success": True, "verified": False, "iterations": 3, "first_try": False, "seconds": 2, "errors": ["e"]},
        {"task_id": "c", "category": "y", "success": False, "verified": False, "iterations": 5, "first_try": False, "seconds": 3, "errors": ["AssertionError"]},
    ]
    rep = generate_report(rs, False)
    assert rep["success_rate"] == 0.6667 and rep["first_try_rate"] == 0.3333
    assert rep["self_fix_rate"] == 0.5 and rep["verified_rate"] == 0.3333
    assert rep["failure_modes"] == {"logic_error": 1}
