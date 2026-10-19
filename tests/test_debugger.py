from src.tools.debugger import analyze_error, classify_error, extract_traceback, generate_fix_prompt
from src.tools.test_runner import run_tests

TB = """Traceback (most recent call last):
  File "x.py", line 7, in solution
    return a / b
ZeroDivisionError: division by zero"""


def test_extract_traceback():
    tb = extract_traceback(TB)
    assert tb["line"] == 7 and tb["error_type"] == "ZeroDivisionError" and "zero" in tb["message"]


def test_classify():
    assert classify_error("SyntaxError: bad") == "syntax_error"
    assert classify_error("Timeout after 10s") == "timeout"
    assert classify_error("Restricted import: os") == "sandbox_violation"
    assert classify_error("AssertionError") == "logic_error"
    assert classify_error(TB) == "runtime_error"


PYTEST_OUT = """    def test_a():
>       assert solution([1]) == 1
    def solution(xs):
>       return xs[0] / 0
E       ZeroDivisionError: division by zero

test_solution.py:2: ZeroDivisionError
FAILED test_solution.py::test_a - ZeroDivisionError: division by zero"""


def test_pytest_runtime_error_not_misclassified_as_logic():
    assert classify_error(PYTEST_OUT) == "runtime_error"
    tb = extract_traceback(PYTEST_OUT)
    assert tb["line"] == 2 and tb["error_type"] == "ZeroDivisionError"


def test_pytest_assertion_is_logic():
    out = "E       AssertionError: assert [2, 1] == [1, 2]\n\ntest_solution.py:3: AssertionError"
    assert classify_error(out) == "logic_error"


def test_hardcode_detector_flags_test_gaming():
    from src.tools.debugger import looks_hardcoded
    bad = ("def solution(nums, k):\n    if nums == [3, 1, 4, 1, 5, 9, 2, 6] and k == 3:\n        return 6\n"
           "    return sorted(nums, reverse=True)[k - 1]\n")
    assert looks_hardcoded(bad)


def test_hardcode_detector_ignores_tuple_of_variables():
    # Regression: BFS code comparing `(r, c) == end` was wrongly rejected as hard-coded.
    from src.tools.debugger import looks_hardcoded
    bfs = ("def solution(grid, start, end):\n    q = [(start[0], start[1], 0)]\n    while q:\n"
           "        r, c, d = q.pop(0)\n        if (r, c) == end:\n            return d\n    return -1\n")
    assert not looks_hardcoded(bfs)
    assert looks_hardcoded("def solution(grid, end):\n    if end == (2, 0):\n        return 6\n    return 0\n")


def test_hardcode_detector_ignores_normal_code():
    from src.tools.debugger import looks_hardcoded
    ok = ("def solution(xs, k):\n    if k == 0 or xs == []:\n        return None\n"
          "    if xs == [1]:\n        return 1\n    return sorted(xs)[k]\n")
    assert not looks_hardcoded(ok)
    assert not looks_hardcoded("def solution(s):\n    return s.lower() == 'yes'\n")


def test_fix_prompt_contains_category_and_error():
    p = generate_fix_prompt(TB, "code")
    assert "runtime_error" in p and "ZeroDivisionError" in p
    assert analyze_error(TB, "code")["category"] == "runtime_error"


def test_run_tests_reports_failed_tests():
    r = run_tests("def solution(x):\n    return x\n",
                  "def test_ok():\n    assert solution(1) == 1\ndef test_bad():\n    assert solution(1) == 2\n")
    assert not r["success"] and r["passed"] == 1 and r["failed"] == 1
    assert r["failed_tests"][0]["name"] == "test_bad"
