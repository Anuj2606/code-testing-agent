"""Runs generated tests and condenses pytest output into a structured result."""
import re

from src.tools.code_executor import execute_code


def run_tests(code: str, tests: str) -> dict:
    raw = execute_code(code, tests)
    return {**raw, **analyze_test_results(raw)}


def analyze_test_results(raw: dict) -> dict:
    out = raw["stdout"] + raw["stderr"]
    failed = re.findall(r"^FAILED\s+\S+::(\w+)(?:\s+-\s+(.*))?$", out, re.MULTILINE)
    summary = re.search(r"(\d+) passed", out)
    nfail = re.search(r"(\d+) failed", out)
    return {
        "passed": int(summary.group(1)) if summary else 0,
        "failed": int(nfail.group(1)) if nfail else 0,
        "failed_tests": [{"name": n, "message": m} for n, m in failed],
        "error": "" if raw["success"] else out.strip()[-3000:],
    }
