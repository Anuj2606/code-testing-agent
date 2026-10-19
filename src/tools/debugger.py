"""Failure analysis: parse tracebacks and build repair context for the generator."""
import re

_E_LINE = re.compile(r"^E\s+(\w*(?:Error|Exception))\b:?\s*(.*)$", re.MULTILINE)
_PLAIN = re.compile(r"^(\w*(?:Error|Exception))\b:?\s*(.*)$", re.MULTILINE)
_LOC = re.compile(r'(?:^\S+\.py:(\d+): )|(?:line (\d+))', re.MULTILINE)


def extract_traceback(stderr: str) -> dict:
    """Last error type/message and line number from pytest or plain Python output."""
    errs = _E_LINE.findall(stderr) or _PLAIN.findall(stderr)
    locs = [a or b for a, b in _LOC.findall(stderr)]
    return {"line": int(locs[-1]) if locs else None,
            "error_type": errs[-1][0] if errs else "Unknown",
            "message": errs[-1][1] if errs else ""}


def classify_error(error: str) -> str:
    etype = extract_traceback(error)["error_type"]
    if "SyntaxError" in error:
        return "syntax_error"
    if "Timeout" in error:
        return "timeout"
    if "Restricted" in error:
        return "sandbox_violation"
    if etype == "AssertionError" or (etype == "Unknown" and "assert" in error):
        return "logic_error"
    return "runtime_error"


def looks_hardcoded(code: str, func: str = "solution") -> bool:
    """Heuristic: does `func` branch on an argument being equal to a literal collection/long string?

    Catches the test-gaming pattern `if nums == [3, 1, 4] and k == 3: return 6`. Plain checks such as
    `if k == 0` or `if s == ''` are not flagged.
    """
    import ast
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    for fn in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == func):
        args = {a.arg for a in fn.args.args}
        for node in ast.walk(fn):
            if not isinstance(node, ast.Compare):
                continue
            sides = [node.left, *node.comparators]
            has_arg = any(isinstance(s, ast.Name) and s.id in args for s in sides)

            def literal(s):  # only pure constants count; `(r, c) == end` is a tuple of variables
                try:
                    return ast.literal_eval(s)
                except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
                    return None

            big = False
            for s in sides:
                v = literal(s)
                if isinstance(v, (list, tuple, set, dict)) and len(v) >= 2:
                    big = True
                elif isinstance(v, str) and len(v) > 6:
                    big = True
            if has_arg and big:
                return True
    return False


def same_failure(prev: dict, cur: dict) -> bool:
    """True when two consecutive test results failed the same named tests."""
    a = sorted(t["name"] for t in prev.get("failed_tests", []))
    b = sorted(t["name"] for t in cur.get("failed_tests", []))
    return bool(a) and a == b


def analyze_error(error_message: str, code: str) -> dict:
    tb = extract_traceback(error_message)
    return {**tb, "category": classify_error(error_message)}


def generate_fix_prompt(error_message: str, code: str) -> str:
    info = analyze_error(error_message, code)
    return f"[{info['category']}] {info['error_type']} near line {info['line']}:\n{error_message[-1500:]}"
