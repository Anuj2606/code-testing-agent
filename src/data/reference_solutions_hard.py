"""Known-good solutions for the hard tasks (validates that their hidden tests are satisfiable)."""

HARD_SOLUTIONS = {
    "sort_05": (
        "def solution(intervals):\n    out = []\n    for s, e in sorted(intervals):\n"
        "        if out and s <= out[-1][1]:\n            out[-1][1] = max(out[-1][1], e)\n"
        "        else:\n            out.append([s, e])\n    return out\n"),
    "sort_06": (
        "def solution(versions):\n    def key(v):\n        parts = [int(p) for p in v.split('.')]\n"
        "        while parts and parts[-1] == 0:\n            parts.pop()\n        return parts\n"
        "    return sorted(versions, key=key)\n"),
    "sort_07": (
        "def solution(nums):\n    def sort(a):\n        if len(a) <= 1:\n            return a, 0\n"
        "        m = len(a) // 2\n        l, x = sort(a[:m])\n        r, y = sort(a[m:])\n"
        "        out, i, j, c = [], 0, 0, x + y\n"
        "        while i < len(l) and j < len(r):\n"
        "            if l[i] <= r[j]:\n                out.append(l[i]); i += 1\n"
        "            else:\n                out.append(r[j]); j += 1; c += len(l) - i\n"
        "        return out + l[i:] + r[j:], c\n    return sort(list(nums))[1]\n"),
    "search_05": (
        "def solution(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo <= hi:\n"
        "        mid = (lo + hi) // 2\n        if nums[mid] == target:\n            return mid\n"
        "        if nums[lo] <= nums[mid]:\n"
        "            if nums[lo] <= target < nums[mid]:\n                hi = mid - 1\n"
        "            else:\n                lo = mid + 1\n"
        "        else:\n"
        "            if nums[mid] < target <= nums[hi]:\n                lo = mid + 1\n"
        "            else:\n                hi = mid - 1\n    return -1\n"),
    "search_06": (
        "def solution(s):\n    last, start, best = {}, 0, 0\n    for i, c in enumerate(s):\n"
        "        if c in last and last[c] >= start:\n            start = last[c] + 1\n"
        "        last[c] = i\n        best = max(best, i - start + 1)\n    return best\n"),
    "search_07": (
        "from collections import deque\n\ndef solution(grid, start, end):\n"
        "    R, C = len(grid), len(grid[0])\n"
        "    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:\n        return -1\n"
        "    seen = {start}\n    q = deque([(start, 0)])\n    while q:\n        (r, c), d = q.popleft()\n"
        "        if (r, c) == end:\n            return d\n"
        "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
        "            nr, nc = r + dr, c + dc\n"
        "            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and (nr, nc) not in seen:\n"
        "                seen.add((nr, nc)); q.append(((nr, nc), d + 1))\n    return -1\n"),
    "string_05": (
        "def solution(s):\n    pairs = {')': '(', ']': '[', '}': '{'}\n    st = []\n    for c in s:\n"
        "        if c in '([{':\n            st.append(c)\n"
        "        elif c in pairs:\n            if not st or st.pop() != pairs[c]:\n                return False\n"
        "    return not st\n"),
    "string_06": (
        "def solution(expr):\n    s = expr.replace(' ', '') + '+'\n    stack, num, op = [], 0, '+'\n"
        "    for c in s:\n        if c.isdigit():\n            num = num * 10 + int(c)\n            continue\n"
        "        if op == '+':\n            stack.append(num)\n        elif op == '-':\n            stack.append(-num)\n"
        "        elif op == '*':\n            stack.append(stack.pop() * num)\n"
        "        else:\n            a = stack.pop()\n            q = abs(a) // num\n            stack.append(q if a >= 0 else -q)\n"
        "        op, num = c, 0\n    return sum(stack)\n"),
    "string_07": (
        "def solution(text, width):\n    lines, cur = [], ''\n    for w in text.split():\n"
        "        if not cur:\n            cur = w\n"
        "        elif len(cur) + 1 + len(w) <= width:\n            cur += ' ' + w\n"
        "        else:\n            lines.append(cur)\n            cur = w\n"
        "    if cur:\n        lines.append(cur)\n    return lines\n"),
    "api_05": (
        "import copy\n\ndef solution(a, b):\n    out = copy.deepcopy(a)\n    for k, v in b.items():\n"
        "        if k in out and isinstance(out[k], dict) and isinstance(v, dict):\n            out[k] = solution(out[k], v)\n"
        "        else:\n            out[k] = copy.deepcopy(v)\n    return out\n"),
    "api_06": (
        "from urllib.parse import urlsplit, parse_qs\n\ndef solution(url):\n    u = urlsplit(url)\n"
        "    return {'scheme': u.scheme, 'host': u.hostname, 'port': u.port, 'path': u.path or '/',\n"
        "            'query': parse_qs(u.query, keep_blank_values=True)}\n"),
    "api_07": (
        "def solution(timestamps, limit, window):\n    allowed, out = [], []\n    for t in timestamps:\n"
        "        recent = sum(1 for a in allowed if a > t - window)\n"
        "        if recent < limit:\n            allowed.append(t)\n            out.append(True)\n"
        "        else:\n            out.append(False)\n    return out\n"),
    "data_05": (
        "def solution(records):\n    recs = sorted(records, key=lambda r: (-r[1], r[0]))\n    out, prev, rank = [], None, 0\n"
        "    for i, (n, s) in enumerate(recs, 1):\n        if s != prev:\n            rank, prev = i, s\n"
        "        out.append((rank, n))\n    return out\n"),
    "data_06": "def solution(matrix):\n    return [list(r) for r in zip(*matrix[::-1])]\n",
    "data_07": (
        "def solution(text):\n    rows, row, field, i, inq, n = [], [], '', 0, False, len(text)\n"
        "    while i < n:\n        c = text[i]\n        if inq:\n"
        "            if c == '\"':\n"
        "                if i + 1 < n and text[i + 1] == '\"':\n                    field += '\"'; i += 1\n"
        "                else:\n                    inq = False\n"
        "            else:\n                field += c\n"
        "        else:\n"
        "            if c == '\"':\n                inq = True\n"
        "            elif c == ',':\n                row.append(field); field = ''\n"
        "            elif c == '\\n':\n                row.append(field); rows.append(row); row, field = [], ''\n"
        "            else:\n                field += c\n"
        "        i += 1\n    if field or row:\n        row.append(field); rows.append(row)\n    return rows\n"),
    "data_08": (
        "from collections import OrderedDict\n\ndef solution(capacity, ops):\n    c, out = OrderedDict(), []\n"
        "    for op in ops:\n        if op[0] == 'put':\n            _, k, v = op\n"
        "            if k in c:\n                c.move_to_end(k)\n            c[k] = v\n"
        "            if len(c) > capacity:\n                c.popitem(last=False)\n"
        "        else:\n            k = op[1]\n"
        "            if k in c:\n                c.move_to_end(k)\n                out.append(c[k])\n"
        "            else:\n                out.append(-1)\n    return out\n"),
}
