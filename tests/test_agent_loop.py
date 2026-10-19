"""Agent loop with a fake generator (no API key needed): first draft is buggy, second is fixed."""
from src.agent.code_agent import CodeGenerationAgent


class FakeGen:
    def generate_code(self, task, error_context="", previous_code=""):
        return "def solution(xs):\n    return sorted(xs)\n" if error_context else "def solution(xs):\n    return xs\n"

    def generate_tests(self, code, task):
        return "def test_a():\n    assert solution([2, 1]) == [1, 2]\n"


class BrokenGen:
    def generate_code(self, *a, **k):
        raise RuntimeError("404 NOT_FOUND model gone")

    generate_tests = generate_code


def test_api_error_stops_without_burning_iterations():
    r = CodeGenerationAgent(generator=BrokenGen()).run("x")
    assert not r["success"] and r["iterations"] == 1


class GamingGen:
    """Test expects a wrong value (3rd largest of [3,1,2] is 1, test says 2). First solution is correct;
    the 'fix' hard-codes the input. The agent must reject that and repair the test instead."""
    def __init__(self):
        self.repaired = False

    def generate_code(self, task, error_context="", previous_code=""):
        if error_context and "Hard-coded" not in error_context:
            return "def solution(xs, k):\n    if xs == [3, 1, 2] and k == 3:\n        return 2\n    return sorted(xs, reverse=True)[k - 1]\n"
        return "def solution(xs, k):\n    return sorted(xs, reverse=True)[k - 1]\n"

    def generate_tests(self, code, task):
        return "def test_a():\n    assert solution([3, 1, 2], 3) == 2\n"

    def repair_tests(self, task, code, tests, error):
        self.repaired = True
        return "def test_a():\n    assert solution([3, 1, 2], 3) == 1\n"


def test_hardcoding_is_rejected_and_wrong_test_is_repaired():
    gen = GamingGen()
    r = CodeGenerationAgent(max_iterations=6, generator=gen).run("kth largest")
    assert r["success"] and gen.repaired
    assert "xs == [3, 1, 2]" not in r["code"]


def test_self_fix():
    r = CodeGenerationAgent(generator=FakeGen()).run("sort a list")
    assert r["success"] and r["iterations"] == 2
