from src.tools.code_executor import execute_code, screen_code, validate_syntax
from src.tools.debugger import classify_error

CODE = "def solution(xs):\n    return sorted(xs)\n"
TESTS = "def test_a():\n    assert solution([2, 1]) == [1, 2]\n"


def test_pass():
    assert execute_code(CODE, TESTS)["success"]


def test_fail():
    r = execute_code(CODE, "def test_a():\n    assert solution([2, 1]) == [2, 1]\n")
    assert not r["success"] and classify_error(r["stdout"]) == "logic_error"


def test_pytest_is_available_without_import():
    t = "def test_a():\n    with pytest.raises(ZeroDivisionError):\n        1 / 0\n"
    assert execute_code(CODE, t)["success"]


def test_syntax():
    assert not validate_syntax("def f(:")[0]


def test_restricted_import():
    assert not screen_code("import os")[0]


def test_timeout():
    r = execute_code("def solution():\n    while True: pass\n", "def test_a():\n    solution()\n", timeout=2)
    assert r["timed_out"]
