"""Known-good solutions, used only to validate that each task's hidden tests are satisfiable."""

SOLUTIONS = {
    "sort_01": "def solution(items):\n    return sorted(items, key=lambda d: (1, 0) if 'age' not in d else (0, d['age']))\n",
    "sort_02": "def solution(words):\n    return sorted(words, key=lambda w: (len(w), w))\n",
    "sort_03": (
        "def solution(a, b):\n    i = j = 0\n    out = []\n"
        "    while i < len(a) and j < len(b):\n"
        "        if a[i] <= b[j]:\n            out.append(a[i]); i += 1\n"
        "        else:\n            out.append(b[j]); j += 1\n"
        "    return out + a[i:] + b[j:]\n"),
    "sort_04": "def solution(nums):\n    return sorted(set(nums), reverse=True)\n",
    "search_01": (
        "def solution(arr, target):\n    lo, hi = 0, len(arr) - 1\n"
        "    while lo <= hi:\n        mid = (lo + hi) // 2\n"
        "        if arr[mid] == target:\n            return mid\n"
        "        if arr[mid] < target:\n            lo = mid + 1\n"
        "        else:\n            hi = mid - 1\n    return -1\n"),
    "search_02": (
        "def solution(nums):\n    seen = set()\n    for n in nums:\n"
        "        if n in seen:\n            return n\n        seen.add(n)\n    return None\n"),
    "search_03": (
        "def solution(nums, target):\n    seen = {}\n    for j, n in enumerate(nums):\n"
        "        if target - n in seen:\n            return [seen[target - n], j]\n        seen[n] = j\n"),
    "search_04": "def solution(nums, k):\n    return sorted(nums, reverse=True)[k - 1]\n",
    "string_01": (
        "def solution(s):\n    t = [c.lower() for c in s if c.isalnum()]\n    return t == t[::-1]\n"),
    "string_02": (
        "import re\n\ndef solution(text):\n    out = {}\n"
        "    for w in re.findall(r'[A-Za-z]+', text):\n        out[w.lower()] = out.get(w.lower(), 0) + 1\n    return out\n"),
    "string_03": (
        "def solution(text, shift):\n    out = []\n    for c in text:\n"
        "        if c.isascii() and c.isalpha():\n"
        "            base = ord('A') if c.isupper() else ord('a')\n"
        "            out.append(chr((ord(c) - base + shift) % 26 + base))\n"
        "        else:\n            out.append(c)\n    return ''.join(out)\n"),
    "string_04": (
        "def solution(words):\n    groups = {}\n    for w in words:\n"
        "        groups.setdefault(''.join(sorted(w)), []).append(w)\n"
        "    return sorted(sorted(g) for g in groups.values())\n"),
    "api_01": (
        "def solution(qs):\n    qs = qs.lstrip('?')\n    if not qs:\n        return {}\n    out = {}\n"
        "    for part in qs.split('&'):\n        k, _, v = part.partition('=')\n        out[k] = v\n    return out\n"),
    "api_02": (
        "def solution(d, prefix=''):\n    out = {}\n    for k, v in d.items():\n"
        "        key = f'{prefix}.{k}' if prefix else k\n"
        "        if isinstance(v, dict):\n            out.update(solution(v, key))\n"
        "        else:\n            out[key] = v\n    return out\n"),
    "api_03": (
        "def solution(s):\n    if any(c.isspace() for c in s) or s.count('@') != 1:\n        return False\n"
        "    local, domain = s.split('@')\n"
        "    return bool(local) and '.' in domain and not domain.startswith('.') and not domain.endswith('.')\n"),
    "api_04": (
        "def solution(items, page, per_page):\n    total = -(-len(items) // per_page)\n"
        "    start = (page - 1) * per_page\n    return {'items': items[start:start + per_page], 'total_pages': total}\n"),
    "data_01": (
        "def solution(rows, key):\n    out = {}\n    for r in rows:\n        out.setdefault(r[key], []).append(r)\n    return out\n"),
    "data_02": (
        "def solution(nums, k):\n    return [sum(nums[i:i + k]) / k for i in range(len(nums) - k + 1)]\n"),
    "data_03": "def solution(items):\n    return list(dict.fromkeys(items))\n",
    "data_04": (
        "import csv, io\n\ndef solution(csv_text, column):\n    total = 0\n"
        "    for row in csv.DictReader(io.StringIO(csv_text)):\n"
        "        v = (row.get(column) or '').strip()\n        if v:\n            total += float(v)\n    return total\n"),
}


from src.data.reference_solutions_hard import HARD_SOLUTIONS  # noqa: E402

SOLUTIONS.update(HARD_SOLUTIONS)


from src.data.reference_solutions_hard2 import HARD2_SOLUTIONS  # noqa: E402

SOLUTIONS.update(HARD2_SOLUTIONS)
