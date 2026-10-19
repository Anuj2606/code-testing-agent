"""Generator tests with the LLM mocked: verify prompts are routed by role and code is extracted."""
from src.tools import code_generator


def _fake(reply, calls):
    def complete(prompt, role="generate"):
        calls.append((role, prompt))
        return reply
    return complete


def test_generate_extracts_block(monkeypatch):
    calls = []
    monkeypatch.setattr(code_generator, "complete", _fake("Sure!\n```python\ndef solution():\n    return 1\n```\nDone", calls))
    assert code_generator.generate_code("task") == "def solution():\n    return 1"
    assert calls[0][0] == "generate" and "task" in calls[0][1]


def test_fix_uses_fix_role_and_includes_error(monkeypatch):
    calls = []
    monkeypatch.setattr(code_generator, "complete", _fake("```python\ndef solution(): pass\n```", calls))
    code_generator.generate_code("task", "AssertionError: boom", "def solution(): return 0")
    role, prompt = calls[0]
    assert role == "fix" and "boom" in prompt and "return 0" in prompt


def test_tests_role(monkeypatch):
    calls = []
    monkeypatch.setattr(code_generator, "complete", _fake("def test_a():\n    assert True", calls))
    assert "test_a" in code_generator.generate_tests("def solution(): pass", "task")
    assert calls[0][0] == "tests"


def test_single_request_returns_code_and_tests(monkeypatch):
    calls = []
    reply = "```python\ndef solution(x):\n    return x\n```\n```python\ndef test_a():\n    assert solution(1) == 1\n```"
    monkeypatch.setattr(code_generator, "complete", _fake(reply, calls))
    code, tests = code_generator.generate_solution_and_tests("t")
    assert "def solution" in code and "def test_a" in tests and len(calls) == 1


def test_single_block_reply_falls_back_to_second_request(monkeypatch):
    calls = []
    monkeypatch.setattr(code_generator, "complete", _fake("```python\ndef solution(): pass\n```", calls))
    code_generator.generate_solution_and_tests("t")
    assert [r for r, _ in calls] == ["generate", "tests"]


def test_self_imports_are_stripped_from_tests(monkeypatch):
    from src.utils.helpers import sanitize_tests
    t = "from solution import solution\nimport pytest\n\ndef test_a():\n    assert solution(1) == 1\n"
    out = sanitize_tests(t)
    assert "from solution" not in out and "import pytest" in out and "def test_a" in out
    assert sanitize_tests("import solution\nx = 1\n") == "x = 1\n"
    monkeypatch.setattr(code_generator, "complete",
                        _fake("```python\nfrom solution import solution\ndef test_a():\n    pass\n```", []))
    assert "from solution" not in code_generator.repair_tests("t", "c", "tests", "err")


def test_unclosed_fence_is_tolerated(monkeypatch):
    monkeypatch.setattr(code_generator, "complete", _fake("```python\ndef solution():\n    return 2", []))
    assert code_generator.generate_code("t").endswith("return 2")
