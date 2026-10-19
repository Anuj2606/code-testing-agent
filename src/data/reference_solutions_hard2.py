"""Known-good solutions for batch 3 (validates that the hidden tests are satisfiable and fair)."""

HARD2_SOLUTIONS = {
    "sort_08": r'''from collections import Counter

def solution(nums, k):
    c = Counter(nums)
    return [v for v, _ in sorted(c.items(), key=lambda x: (-x[1], x[0]))][:k]
''',
    "sort_09": r'''import re

def solution(strings):
    def key(s):
        return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', s.lower())]
    return sorted(strings, key=key)
''',
    "sort_10": r'''def solution(points, k):
    return sorted(points, key=lambda p: (p[0] ** 2 + p[1] ** 2, p[0], p[1]))[:k]
''',
    "search_08": r'''def solution(nums):
    s = set(nums)
    best = 0
    for n in s:
        if n - 1 not in s:
            m = n
            while m + 1 in s:
                m += 1
            best = max(best, m - n + 1)
    return best
''',
    "search_09": r'''from bisect import bisect_left, bisect_right

def solution(nums, target):
    lo = bisect_left(nums, target)
    if lo == len(nums) or nums[lo] != target:
        return [-1, -1]
    return [lo, bisect_right(nums, target) - 1]
''',
    "search_10": r'''def solution(s, words):
    idx = set()
    for w in words:
        if not w:
            continue
        i = s.find(w)
        while i != -1:
            idx.add(i)
            i = s.find(w, i + 1)
    return sorted(idx)
''',
    "string_08": r'''def solution(s):
    best_start, best_len = 0, 0
    for c in range(len(s)):
        for l, r in ((c, c), (c, c + 1)):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            st, ln = l + 1, r - l - 1
            if ln > best_len or (ln == best_len and st < best_start):
                best_start, best_len = st, ln
    return s[best_start:best_start + best_len]
''',
    "string_09": r'''def solution(s):
    stack = [['', 1]]
    num = 0
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c == '[':
            stack.append(['', num])
            num = 0
        elif c == ']':
            cur, k = stack.pop()
            stack[-1][0] += cur * k
        else:
            stack[-1][0] += c
    return stack[0][0]
''',
    "string_10": r'''def solution(roman):
    v = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for i, c in enumerate(roman):
        if i + 1 < len(roman) and v[c] < v[roman[i + 1]]:
            total -= v[c]
        else:
            total += v[c]
    return total
''',
    "api_08": r'''def solution(text):
    out, last = {}, None
    for ln in text.replace('\r\n', '\n').split('\n'):
        if not ln.strip():
            continue
        if ln[0] in ' \t' and last is not None:
            out[last] += ' ' + ln.strip()
            continue
        name, _, val = ln.partition(':')
        name, val = name.strip().lower(), val.strip()
        out[name] = out[name] + ', ' + val if name in out else val
        last = name
    return out
''',
    "api_09": r'''def solution(path):
    absolute = path.startswith('/')
    parts = []
    for p in path.split('/'):
        if p in ('', '.'):
            continue
        if p == '..':
            if parts and parts[-1] != '..':
                parts.pop()
            elif not absolute:
                parts.append('..')
        else:
            parts.append(p)
    res = '/'.join(parts)
    return '/' + res if absolute else (res or '.')
''',
    "api_10": r'''def solution(events, window):
    by = {}
    for u, t in sorted(events):
        by.setdefault(u, []).append(t)
    out = {}
    for u, ts in by.items():
        sessions = []
        start = prev = ts[0]
        n = 1
        for t in ts[1:]:
            if t - prev > window:
                sessions.append((start, prev, n))
                start, n = t, 1
            else:
                n += 1
            prev = t
        sessions.append((start, prev, n))
        out[u] = sessions
    return out
''',
    "data_09": r'''from collections import deque

def solution(nums, k):
    if k < 1 or k > len(nums):
        return []
    dq, out = deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
''',
    "data_10": r'''def solution(prices, fee):
    if not prices:
        return 0
    cash, hold = 0, -prices[0]
    for p in prices[1:]:
        cash = max(cash, hold + p - fee)
        hold = max(hold, cash - p)
    return cash
''',
    "data_11": r'''def solution(records):
    out = {}
    for r in records:
        region = r.get('region') or 'unknown'
        product = r.get('product')
        out.setdefault(region, {})
        out[region][product] = out[region].get(product, 0) + (r.get('sales') or 0)
    return out
''',
    "data_12": r'''import heapq

def solution(tasks):
    indeg = {t: len(set(d)) for t, d in tasks.items()}
    rev = {t: [] for t in tasks}
    for t, ds in tasks.items():
        for d in set(ds):
            rev[d].append(t)
    heap = [t for t, n in indeg.items() if n == 0]
    heapq.heapify(heap)
    out = []
    while heap:
        t = heapq.heappop(heap)
        out.append(t)
        for u in rev[t]:
            indeg[u] -= 1
            if indeg[u] == 0:
                heapq.heappush(heap, u)
    return out if len(out) == len(tasks) else None
''',
}
