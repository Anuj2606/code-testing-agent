import re

_BLOCK = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL)
_OPEN_BLOCK = re.compile(r"```(?:python)?\s*\n(.*)", re.DOTALL)


def extract_code_block(text: str) -> str:
    """Return the first fenced code block (tolerating a missing closing fence), else the raw text."""
    m = _BLOCK.search(text) or _OPEN_BLOCK.search(text)
    return (m.group(1) if m else text).strip()


def extract_code_blocks(text: str) -> list[str]:
    """All fenced code blocks, in order; a trailing unclosed fence counts as a block."""
    blocks = [b.strip() for b in _BLOCK.findall(text)]
    tail = text.rsplit("```", 1)[-1] if text.count("```") % 2 == 1 else ""
    if tail.strip():
        blocks.append(re.sub(r"^python\s*\n", "", tail.lstrip()).strip())
    return blocks or ([text.strip()] if text.strip() else [])


_SELF_IMPORT = re.compile(
    r"^[ \t]*(?:from\s+(?:solution|code|main|test_solution)\s+import\s+.*|import\s+(?:solution|code|main|test_solution)\b.*)\n?",
    re.MULTILINE)


def sanitize_tests(tests: str) -> str:
    """Drop imports of the solution module: tests share a namespace with the solution in the sandbox."""
    return _SELF_IMPORT.sub("", tests)


def compare_outputs(actual, expected) -> bool:
    return actual == expected
