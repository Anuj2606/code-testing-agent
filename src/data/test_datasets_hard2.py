"""Batch 3 of tasks (16), weighted toward hard edge cases and performance, to grow the number of first-try
failures available for measuring the self-fix rate. Hidden tests are raw strings (escapes stay literal)."""
from src.data.test_datasets import _t

HARD2_TASKS = [
    # ---- sorting ----
    _t("sort_08", "sorting", "medium",
       "Write `solution(nums, k)`: return the k most frequent values in nums, ordered by frequency descending and then by value "
       "ascending. If k exceeds the number of distinct values, return all of them.",
       r"""def test_a():
    assert solution([1,1,1,2,2,3], 2) == [1,2]
def test_tie_by_value():
    assert solution([4,4,5,5,6], 2) == [4,5]
    assert solution([9,8,9,8,7], 3) == [8,9,7]
def test_k_too_big_and_empty():
    assert solution([1,2], 5) == [1,2]
    assert solution([], 3) == []
"""),
    _t("sort_09", "sorting", "medium",
       "Write `solution(strings)`: natural sort. Compare strings case-insensitively, treating runs of digits as numbers "
       "(so 'file2' < 'file10'). Strings that compare equal keep their input order.",
       r"""def test_numbers():
    assert solution(['file10','file2','File1']) == ['File1','file2','file10']
def test_multiple_runs():
    assert solution(['x1y10','x1y2']) == ['x1y2','x1y10']
def test_prefix_and_letters():
    assert solution(['b','a','a1']) == ['a','a1','b']
def test_equal_numeric_value_is_stable():
    assert solution(['a01','a1']) == ['a01','a1']
    assert solution(['a1','a01']) == ['a1','a01']
def test_empty():
    assert solution([]) == []
"""),
    _t("sort_10", "sorting", "medium",
       "Write `solution(points, k)`: points is a list of (x, y) tuples. Return the k points closest to the origin as a list of tuples, "
       "ordered by squared distance, ties broken by x then y ascending.",
       r"""def test_a():
    assert solution([(1,3),(-2,2)], 1) == [(-2,2)]
def test_ties():
    assert solution([(1,0),(0,1),(-1,0)], 2) == [(-1,0),(0,1)]
def test_edges():
    assert solution([(1,1)], 0) == []
    assert solution([], 3) == []
    assert solution([(3,3),(1,1)], 5) == [(1,1),(3,3)]
"""),
    # ---- searching ----
    _t("search_08", "searching", "hard",
       "Write `solution(nums)`: return the length of the longest run of consecutive integers (e.g. 1,2,3,4) that appear anywhere in "
       "the unsorted list. Duplicates count once. It must run in O(n).",
       r"""def test_a():
    assert solution([100,4,200,1,3,2]) == 4
    assert solution([0,3,7,2,5,8,4,6,0,1]) == 9
def test_edges():
    assert solution([]) == 0
    assert solution([1,1,1]) == 1
    assert solution([-1,-2,0]) == 3
def test_large():
    import random
    xs = list(range(200000))
    random.Random(1).shuffle(xs)
    assert solution(xs) == 200000
"""),
    _t("search_09", "searching", "medium",
       "Write `solution(nums, target)`: nums is sorted ascending and may contain duplicates. Return [first_index, last_index] of target, "
       "or [-1, -1] if absent.",
       r"""def test_a():
    assert solution([5,7,7,8,8,10], 8) == [3,4]
    assert solution([5,7,7,8,8,10], 6) == [-1,-1]
def test_edges():
    assert solution([], 1) == [-1,-1]
    assert solution([1], 1) == [0,0]
    assert solution([2,2], 2) == [0,1]
    assert solution([1,2,3], 0) == [-1,-1] and solution([1,2,3], 9) == [-1,-1]
"""),
    _t("search_10", "searching", "medium",
       "Write `solution(s, words)`: return the sorted list of distinct start indices in s at which any word from `words` occurs "
       "(overlapping occurrences count). Empty words are ignored.",
       r"""def test_a():
    assert solution('abcabc', ['abc','bc']) == [0,1,3,4]
def test_overlap():
    assert solution('aaa', ['aa']) == [0,1]
def test_none_and_empty():
    assert solution('abc', ['x']) == []
    assert solution('abc', ['']) == []
    assert solution('', ['a']) == []
"""),
    # ---- string manipulation ----
    _t("string_08", "string_manipulation", "hard",
       "Write `solution(s)`: return the longest palindromic substring of s. If several have the maximum length, return the one that "
       "starts earliest. Return '' for an empty string.",
       r"""def test_a():
    assert solution('babad') == 'bab'
    assert solution('cbbd') == 'bb'
    assert solution('forgeeksskeegfor') == 'geeksskeeg'
def test_edges():
    assert solution('') == ''
    assert solution('a') == 'a'
    assert solution('abc') == 'a'
    assert solution('abacdfgdcaba') == 'aba'
"""),
    _t("string_09", "string_manipulation", "hard",
       "Write `solution(s)`: decode a string with repeat markers `k[...]`, where k is a positive integer (possibly several digits) and "
       "markers may be nested. Letters outside markers are copied. Example: '3[a2[c]]' -> 'accaccacc'.",
       r"""def test_basic():
    assert solution('2[ab]3[c]') == 'ababccc'
    assert solution('abc') == 'abc'
    assert solution('') == ''
def test_nested():
    assert solution('3[a2[c]]') == 'accaccacc'
    assert solution('2[a2[b]c]') == 'abbcabbc'
def test_multidigit_and_mixed():
    assert solution('10[a]') == 'a' * 10
    assert solution('x2[y]z') == 'xyyz'
"""),
    _t("string_10", "string_manipulation", "medium",
       "Write `solution(roman)`: convert a Roman numeral (I V X L C D M, with subtractive forms such as IV, IX, XL, XC, CD, CM) to an "
       "integer. An empty string gives 0.",
       r"""def test_simple():
    assert solution('III') == 3
    assert solution('LVIII') == 58
def test_subtractive():
    assert solution('IV') == 4
    assert solution('IX') == 9
    assert solution('MCMXCIV') == 1994
def test_edges():
    assert solution('') == 0
    assert solution('MMMCMXCIX') == 3999
"""),
    # ---- api / data ----
    _t("api_08", "api_calls", "hard",
       "Write `solution(text)`: parse a block of HTTP headers into a dict. Lines end in \\r\\n or \\n. Names are lowercased and stripped; "
       "values are stripped. Split each line at its FIRST colon only. A repeated header name has its values joined with ', '. "
       "A line starting with a space or tab continues the previous header's value (joined with a single space). Ignore blank lines.",
       r"""def test_basic_and_repeat():
    assert solution('Host: a.com\r\nAccept: x\r\nAccept: y\r\n') == {'host':'a.com','accept':'x, y'}
def test_folded_line():
    assert solution('X-A: 1\n  2\n') == {'x-a':'1 2'}
def test_colons_in_value():
    assert solution('Value:with:colons: ok') == {'value':'with:colons: ok'}
def test_empty_and_blank():
    assert solution('') == {}
    assert solution('\n\nA: 1\n\n') == {'a':'1'}
def test_case_and_spacing():
    assert solution('Content-Type :  text/html  ') == {'content-type':'text/html'}
"""),
    _t("api_09", "api_calls", "hard",
       "Write `solution(path)`: normalise a slash-separated path. Collapse repeated slashes, drop '.' parts, resolve '..' against the "
       "previous part. For an absolute path (starts with '/') a '..' above the root is ignored; for a relative path leading '..' parts "
       "are kept. No trailing slash except for the root '/'. An empty or fully-resolved relative path gives '.'.",
       r"""def test_absolute():
    assert solution('/a/./b/../c/') == '/a/c'
    assert solution('/../..') == '/'
    assert solution('/') == '/'
    assert solution('//a///b') == '/a/b'
def test_relative():
    assert solution('a//b/../../..') == '..'
    assert solution('../a/../b') == '../b'
    assert solution('./a') == 'a'
    assert solution('a/b/..') == 'a'
def test_dot_results():
    assert solution('') == '.'
    assert solution('a/..') == '.'
    assert solution('.') == '.'
"""),
    _t("api_10", "api_calls", "hard",
       "Write `solution(events, window)`: events is an unsorted list of (user, timestamp). Group each user's events into sessions: a new "
       "session starts when the gap to the previous event is GREATER than `window` (a gap equal to window stays in the session). "
       "Return a dict user -> list of (start, end, count) tuples ordered by start.",
       r"""def test_a():
    ev = [('a',1),('a',2),('a',10),('b',5)]
    assert solution(ev, 3) == {'a':[(1,2,2),(10,10,1)],'b':[(5,5,1)]}
def test_gap_equal_to_window_stays():
    assert solution([('a',1),('a',4)], 3) == {'a':[(1,4,2)]}
    assert solution([('a',1),('a',5)], 3) == {'a':[(1,1,1),(5,5,1)]}
def test_unsorted_and_duplicates():
    assert solution([('a',10),('a',1),('a',2),('a',2)], 3) == {'a':[(1,2,3),(10,10,1)]}
def test_empty():
    assert solution([], 3) == {}
"""),
    _t("data_09", "data_processing", "hard",
       "Write `solution(nums, k)`: return the maximum of every contiguous window of size k, in order. Return [] if k < 1 or k > len(nums). "
       "It must run in O(n); inputs can have 200000 elements with k = 5000.",
       r"""def test_a():
    assert solution([1,3,-1,-3,5,3,6,7], 3) == [3,3,5,5,6,7]
def test_edges():
    assert solution([1,2,3], 1) == [1,2,3]
    assert solution([1], 2) == []
    assert solution([5,4], 2) == [5]
    assert solution([1,2], 0) == []
def test_large():
    n, k = 200000, 5000
    assert solution(list(range(n)), k) == list(range(k - 1, n))
"""),
    _t("data_10", "data_processing", "hard",
       "Write `solution(prices, fee)`: prices[i] is a stock price on day i. You may buy and sell any number of times (hold at most one "
       "share) and pay `fee` on each completed sale. Return the maximum profit; 0 if the list is empty or no profit is possible.",
       r"""def test_a():
    assert solution([1,3,2,8,4,9], 2) == 8
    assert solution([1,3,7,5,10,3], 3) == 6
def test_edges():
    assert solution([], 2) == 0
    assert solution([5], 2) == 0
    assert solution([5,4,3], 1) == 0
    assert solution([1,10], 0) == 9
"""),
    _t("data_11", "data_processing", "medium",
       "Write `solution(records)`: records is a list of dicts with 'region', 'product' and 'sales'. Return a nested dict "
       "region -> product -> total sales. A missing or None region becomes 'unknown'; a None or missing sales counts as 0 "
       "(but the product still appears).",
       r"""def test_a():
    rs = [{'region':'N','product':'a','sales':5},{'region':'N','product':'a','sales':None},
          {'region':None,'product':'b','sales':2},{'product':'b','sales':3}]
    assert solution(rs) == {'N':{'a':5},'unknown':{'b':5}}
def test_zero_sales_still_listed():
    assert solution([{'region':'S','product':'c','sales':None}]) == {'S':{'c':0}}
def test_empty_and_multi():
    assert solution([]) == {}
    rs = [{'region':'N','product':'a','sales':1},{'region':'N','product':'b','sales':2},{'region':'S','product':'a','sales':3}]
    assert solution(rs) == {'N':{'a':1,'b':2},'S':{'a':3}}
"""),
    _t("data_12", "data_processing", "hard",
       "Write `solution(tasks)`: tasks maps a task name to the list of task names it depends on (all names appear as keys). Return an "
       "execution order as a list in which every task comes after its dependencies; among tasks that are ready, always pick the "
       "alphabetically smallest. Return None if there is a dependency cycle.",
       r"""def test_a():
    assert solution({'a':[], 'b':['a'], 'c':['a'], 'd':['b','c']}) == ['a','b','c','d']
def test_tiebreak():
    assert solution({'b':[], 'a':[]}) == ['a','b']
    assert solution({'c':['b'], 'b':['a'], 'a':[]}) == ['a','b','c']
    assert solution({'z':[], 'y':[], 'x':['z']}) == ['y','z','x']
def test_cycles():
    assert solution({'x':['y'], 'y':['x']}) is None
    assert solution({'a':['a']}) is None
def test_empty_and_duplicate_deps():
    assert solution({}) == []
    assert solution({'a':[], 'b':['a','a']}) == ['a','b']
"""),
]
