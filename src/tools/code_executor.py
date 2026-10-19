"""Sandboxed execution.

RestrictedPython cannot host pytest (no imports, no introspection), so isolation is layered:
1. AST screen rejects restricted imports / dangerous builtins before anything runs.
2. Code runs in a separate `python -I` subprocess in a temp dir with a hard timeout.
"""
import ast
import subprocess
import sys
import tempfile
from pathlib import Path

from src.utils.config import RESTRICTED_IMPORTS, SANDBOX_TIMEOUT

_BANNED_CALLS = {"eval", "exec", "compile", "__import__", "open", "input"}


def validate_syntax(code: str) -> tuple[bool, str]:
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg} (line {e.lineno})"


def screen_code(code: str) -> tuple[bool, str]:
    """Static safety check. Returns (ok, reason)."""
    ok, msg = validate_syntax(code)
    if not ok:
        return False, msg
    for node in ast.walk(ast.parse(code)):
        mods = []
        if isinstance(node, ast.Import):
            mods = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods = [node.module]
        for m in mods:
            if m.split(".")[0] in RESTRICTED_IMPORTS:
                return False, f"Restricted import: {m}"
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in _BANNED_CALLS:
            return False, f"Restricted call: {node.func.id}()"
    return True, ""


def execute_code(code: str, test_code: str = "", timeout: int = SANDBOX_TIMEOUT) -> dict:
    """Run `code` (+ pytest `test_code`) in an isolated subprocess.

    Returns {success, stdout, stderr, exit_code, timed_out}.
    """
    ok, reason = screen_code(code + "\n" + test_code)
    if not ok:
        return {"success": False, "stdout": "", "stderr": reason, "exit_code": -1, "timed_out": False}

    with tempfile.TemporaryDirectory() as tmp:
        # Tests run in the same module namespace as the solution, so no import is needed.
        # `import pytest` is always provided: generated tests often use pytest.raises / approx unimported.
        Path(tmp, "test_solution.py").write_text(
            "import pytest\n" + code + "\n\n" + test_code + "\n", encoding="utf-8")
        cmd = [sys.executable, "-I", "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", "test_solution.py"]
        try:
            p = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {"success": False, "stdout": "", "stderr": f"Timeout after {timeout}s",
                    "exit_code": -1, "timed_out": True}
    return {"success": p.returncode == 0, "stdout": p.stdout, "stderr": p.stderr,
            "exit_code": p.returncode, "timed_out": False}
