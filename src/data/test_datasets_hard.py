"""Harder tasks (edge cases, performance) meant to make first drafts fail so the self-fix loop is exercised.
Hidden tests are raw strings so '\\n' stays an escape inside the test source."""
from src.data.test_datasets import _t

HARD_TASKS = [
    # ---- sorting ----
    _t("sort_05", "sorting", "medium",
       "Write `solution(intervals)`: merge overlapping intervals. Input is an unsorted list of [start, end] pairs; "
       "intervals that touch (e.g. [1,4] and [4,5]) also merge. Return a list of [start, end] lists sorted by start.",
       r"""def test_a():
    assert solution([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
def test_touching():
    assert solution([[1,4],[4,5]]) == [[1,5]]
def test_unsorted_and_contained():
    assert solution([[5,6],[1,2]]) == [[1,2],[5,6]]
    assert solution([[1,10],[2,3]]) == [[1,10]]
def test_empty():
    assert solution([]) == []
"""),
    _t("sort_06", "sorting", "medium",
       "Write `solution(versions)`: sort version strings like '1.10.2' ascending by numeric components "
       "(so '1.2' < '1.10'). Missing trailing components count as 0, so '1.0' and '1.0.0' are equal and keep their input order.",
       r"""def test_numeric():
    assert solution(['1.10','1.2','1.2.1']) == ['1.2','1.2.1','1.10']
def test_equal_stable():
    assert solution(['1.0','1.0.0']) == ['1.0','1.0.0']
    assert solution(['1.0.0','1.0']) == ['1.0.0','1.0']
def test_mixed_lengths():
    assert solution(['2','1.9.9']) == ['1.9.9','2']
def test_empty():
    assert solution([]) == []
"""),
    _t("sort_07", "sorting", "hard",
       "Write `solution(nums)`: count inversions, i.e. pairs i < j with nums[i] > nums[j]. "
       "It must run in O(n log n); inputs can have 20000 elements.",
       r"""def test_small():
    assert solution([2,4,1,3,5]) == 3
    assert solution([5,4,3,2,1]) == 10
    assert solution([1,1,1]) == 0
    assert solution([]) == 0
def test_large_reversed():
    n = 20000
    assert solution(list(range(n, 0, -1))) == n * (n - 1) // 2
"""),
    # ---- searching ----
    _t("search_05", "searching", "hard",
       "Write `solution(nums, target)`: nums is a sorted list of distinct integers that was rotated at an unknown pivot "
       "(e.g. [4,5,6,7,0,1,2]). Return the index of target or -1, in O(log n).",
       r"""def test_a():
    assert solution([4,5,6,7,0,1,2], 0) == 4
    assert solution([4,5,6,7,0,1,2], 5) == 1
def test_missing():
    assert solution([4,5,6,7,0,1,2], 3) == -1
def test_small():
    assert solution([1], 1) == 0 and solution([1], 0) == -1 and solution([], 1) == -1
    assert solution([3,1], 1) == 1 and solution([3,1], 3) == 0
def test_not_rotated():
    assert solution([1,2,3,4], 4) == 3
"""),
    _t("search_06", "searching", "medium",
       "Write `solution(s)`: return the length of the longest substring of s without repeating characters.",
       r"""def test_a():
    assert solution('abcabcbb') == 3
    assert solution('bbbbb') == 1
    assert solution('pwwkew') == 3
def test_edges():
    assert solution('') == 0
    assert solution('abba') == 2
    assert solution('dvdf') == 3
"""),
    _t("search_07", "searching", "hard",
       "Write `solution(grid, start, end)`: grid is a list of lists of 0 (open) / 1 (wall); start and end are (row, col) tuples. "
       "Return the minimum number of 4-directional steps from start to end, or -1 if unreachable. "
       "If the start or end cell is a wall return -1 (even when start == end); if start == end and open return 0.",
       r"""def test_path():
    g = [[0,0,0],[1,1,0],[0,0,0]]
    assert solution(g, (0,0), (2,0)) == 6
def test_blocked():
    assert solution([[0,1],[1,0]], (0,0), (1,1)) == -1
def test_same_cell():
    assert solution([[0]], (0,0), (0,0)) == 0
def test_wall_endpoints():
    assert solution([[1,0],[0,0]], (0,0), (1,1)) == -1
    assert solution([[0,0],[0,1]], (0,0), (1,1)) == -1
    assert solution([[1]], (0,0), (0,0)) == -1
def test_open_grid():
    assert solution([[0]*5 for _ in range(5)], (0,0), (4,4)) == 8
"""),
    # ---- string manipulation ----
    _t("string_05", "string_manipulation", "medium",
       "Write `solution(s)`: return True if the brackets in s are balanced and correctly nested. "
       "Bracket types are (), [] and {}; ignore all other characters.",
       r"""def test_ok():
    assert solution('([]{})') is True
    assert solution('') is True
    assert solution('a(b)c[d]') is True
def test_bad():
    assert solution('(]') is False
    assert solution('(') is False
    assert solution(']') is False
    assert solution('([)]') is False
"""),
    _t("string_06", "string_manipulation", "hard",
       "Write `solution(expr)`: evaluate an arithmetic expression of non-negative integers with + - * / and spaces "
       "(no parentheses). * and / bind tighter than + and -, and are evaluated left to right. "
       "Division truncates toward zero. Return an int.",
       r"""def test_precedence():
    assert solution('3+2*2') == 7
    assert solution('2*3-4*5') == -14
def test_division():
    assert solution(' 3/2 ') == 1
    assert solution(' 3+5 / 2 ') == 5
    assert solution('14-3/2') == 13
    assert solution('10/3*3') == 9
def test_negative_results():
    assert solution('0-7/2') == -3
    assert solution('1-1-1') == -1
def test_single():
    assert solution('42') == 42
    assert solution('  7  ') == 7
"""),
    _t("string_07", "string_manipulation", "medium",
       "Write `solution(text, width)`: greedy word wrap. Split text on whitespace and pack words into lines of at most `width` "
       "characters separated by single spaces. A word longer than width gets its own line, unbroken. Return a list of lines "
       "(empty list for no words).",
       r"""def test_a():
    assert solution('the quick brown fox', 10) == ['the quick', 'brown fox']
def test_edges():
    assert solution('a', 5) == ['a']
    assert solution('', 5) == []
    assert solution('   ', 5) == []
def test_long_word():
    assert solution('supercalifragilistic is', 5) == ['supercalifragilistic', 'is']
def test_collapses_spaces():
    assert solution('a  b   c', 3) == ['a b', 'c']
"""),
    # ---- api / data ----
    _t("api_05", "api_calls", "medium",
       "Write `solution(a, b)`: deep-merge two dicts into a NEW dict. Values from b win; when both values are dicts they are "
       "merged recursively; any other value (including lists) is replaced. Neither input may be modified, and the result must "
       "not share nested dicts with the inputs.",
       r"""def test_merge():
    assert solution({'a':{'x':1,'y':2},'b':[1]}, {'a':{'y':3},'b':[2],'c':1}) == {'a':{'x':1,'y':3},'b':[2],'c':1}
def test_type_override():
    assert solution({'a':{'x':1}}, {'a':5}) == {'a':5}
    assert solution({'a':5}, {'a':{'x':1}}) == {'a':{'x':1}}
def test_no_mutation_or_sharing():
    a = {'a':{'x':1}}
    b = {'a':{'y':2}, 'n':{'z':1}}
    r = solution(a, b)
    assert a == {'a':{'x':1}} and b == {'a':{'y':2}, 'n':{'z':1}}
    r['a']['x'] = 99
    r['n']['z'] = 99
    assert a['a']['x'] == 1 and b['n']['z'] == 1
def test_empty():
    assert solution({}, {}) == {}
"""),
    _t("api_06", "api_calls", "medium",
       "Write `solution(url)`: parse a URL into {'scheme': str, 'host': str, 'port': int or None, 'path': str, 'query': dict}. "
       "The path defaults to '/'. The query maps each key to a LIST of its values (repeated keys give several values; "
       "a key with an empty value gives ['']).",
       r"""def test_full():
    assert solution('https://example.com:8080/a/b?x=1&x=2&y=3') == {
        'scheme':'https','host':'example.com','port':8080,'path':'/a/b','query':{'x':['1','2'],'y':['3']}}
def test_minimal():
    assert solution('http://example.com') == {
        'scheme':'http','host':'example.com','port':None,'path':'/','query':{}}
def test_blank_value():
    assert solution('http://example.com/p?flag=')['query'] == {'flag':['']}
"""),
    _t("api_07", "api_calls", "hard",
       "Write `solution(timestamps, limit, window)`: sliding-window rate limiter. timestamps is a non-decreasing list of request times. "
       "Return a list of booleans: a request at time t is allowed if fewer than `limit` previously ALLOWED requests have a time in "
       "(t - window, t] (strictly greater than t - window). Denied requests do not count toward the limit.",
       r"""def test_a():
    assert solution([1,2,3,4,5], 2, 3) == [True, True, False, True, True]
def test_same_time():
    assert solution([10,10,10], 2, 5) == [True, True, False]
def test_boundary():
    assert solution([0,5,5,10], 1, 5) == [True, True, False, True]
def test_empty():
    assert solution([], 2, 3) == []
"""),
    _t("data_05", "data_processing", "medium",
       "Write `solution(records)`: records is a list of (name, score) tuples. Return a list of (rank, name) tuples using competition "
       "ranking (ties share a rank and the next rank is skipped: 1, 2, 2, 4), ordered by score descending, then name ascending.",
       r"""def test_ties():
    assert solution([('a',90),('b',80),('c',80),('d',70)]) == [(1,'a'),(2,'b'),(2,'c'),(4,'d')]
def test_name_tiebreak():
    assert solution([('z',5),('a',5)]) == [(1,'a'),(1,'z')]
def test_empty():
    assert solution([]) == []
"""),
    _t("data_06", "data_processing", "medium",
       "Write `solution(matrix)`: return a NEW matrix (list of lists) that is the input rotated 90 degrees clockwise. "
       "The input may be non-square or empty and must not be modified.",
       r"""def test_rect():
    assert solution([[1,2,3],[4,5,6]]) == [[4,1],[5,2],[6,3]]
def test_square():
    assert solution([[1,2],[3,4]]) == [[3,1],[4,2]]
def test_edges():
    assert solution([]) == []
    assert solution([[1]]) == [[1]]
def test_no_mutation():
    m = [[1,2],[3,4]]
    solution(m)
    assert m == [[1,2],[3,4]]
"""),
    _t("data_07", "data_processing", "hard",
       "Write `solution(text)`: parse CSV text into a list of rows (lists of strings). Fields may be quoted with double quotes; a quoted "
       "field may contain commas and newlines, and a doubled quote \"\" inside it is a literal quote. Rows end at newline; "
       "a trailing newline does not create an extra row; empty input gives [].",
       r'''def test_basic():
    assert solution('a,b\n"x,y",z\n') == [['a','b'],['x,y','z']]
def test_escaped_quotes():
    assert solution('"he said ""hi""",1') == [['he said "hi"','1']]
def test_empty_fields():
    assert solution('a,,c') == [['a','','c']]
    assert solution('a,\n') == [['a','']]
def test_quoted_newline():
    assert solution('"a\nb",c') == [['a\nb','c']]
def test_empty():
    assert solution('') == []
'''),
    _t("data_08", "data_processing", "hard",
       "Write `solution(capacity, ops)`: simulate an LRU cache. ops is a list of ('put', key, value) and ('get', key) tuples. "
       "A get returns the value (or -1 if absent) and marks the key most recently used; a put inserts or updates the key, "
       "marks it most recently used, and evicts the least recently used key if over capacity. Return the list of get results.",
       r"""def test_classic():
    ops = [('put',1,1),('put',2,2),('get',1),('put',3,3),('get',2),('put',4,4),('get',1),('get',3),('get',4)]
    assert solution(2, ops) == [1,-1,-1,3,4]
def test_update_refreshes():
    ops = [('put',1,1),('put',2,2),('put',1,10),('put',3,3),('get',1),('get',2)]
    assert solution(2, ops) == [10,-1]
def test_empty():
    assert solution(1, []) == []
    assert solution(1, [('get',5)]) == [-1]
"""),
]
