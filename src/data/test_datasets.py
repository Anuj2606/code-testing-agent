"""Benchmark tasks. Each has hidden `reference_tests` (pytest source using `solution`)
that the agent never sees; they verify correctness beyond the agent's own generated tests.
All tasks are pure/offline so they run inside the no-network sandbox."""


def _t(id, category, difficulty, description, reference_tests):
    return {"id": id, "category": category, "difficulty": difficulty,
            "description": description, "reference_tests": reference_tests}


TASKS = [
    # ---- sorting ----
    _t("sort_01", "sorting", "easy",
       "Write `solution(items)`: sort a list of dicts ascending by their 'age' key (stable). Dicts missing 'age' go last.",
       "def test_a():\n    r = solution([{'n':'a','age':3},{'n':'b'},{'n':'c','age':1}])\n    assert [x['n'] for x in r] == ['c','a','b']\n"
       "def test_empty():\n    assert solution([]) == []\n"
       "def test_stable():\n    r = solution([{'n':'x','age':2},{'n':'y','age':2}])\n    assert [d['n'] for d in r] == ['x','y']\n"),
    _t("sort_02", "sorting", "easy",
       "Write `solution(words)`: sort strings by length ascending, ties broken alphabetically.",
       "def test_a():\n    assert solution(['bb','a','ab','c']) == ['a','c','ab','bb']\n"
       "def test_empty():\n    assert solution([]) == []\n"),
    _t("sort_03", "sorting", "medium",
       "Write `solution(a, b)`: merge two already-sorted lists of numbers into one sorted list in O(n+m), without sorting the result.",
       "def test_a():\n    assert solution([1,3,5],[2,4,6]) == [1,2,3,4,5,6]\n"
       "def test_empty():\n    assert solution([],[1]) == [1] and solution([],[]) == []\n"
       "def test_dups():\n    assert solution([1,1],[1]) == [1,1,1]\n"),
    _t("sort_04", "sorting", "easy",
       "Write `solution(nums)`: return the unique values of a list of numbers sorted in descending order.",
       "def test_a():\n    assert solution([3,1,3,2,1]) == [3,2,1]\n"
       "def test_empty():\n    assert solution([]) == []\n"),
    # ---- searching ----
    _t("search_01", "searching", "easy",
       "Write `solution(arr, target)`: binary search a sorted list; return the index of target or -1.",
       "def test_a():\n    assert solution([1,3,5,7,9], 7) == 3\n"
       "def test_missing():\n    assert solution([1,3,5], 4) == -1\n"
       "def test_empty():\n    assert solution([], 1) == -1\n"
       "def test_ends():\n    assert solution([1,2,3], 1) == 0 and solution([1,2,3], 3) == 2\n"),
    _t("search_02", "searching", "easy",
       "Write `solution(nums)`: return the value whose second occurrence appears earliest in the list, or None if no duplicates.",
       "def test_a():\n    assert solution([2,1,3,1,2]) == 1\n"
       "def test_none():\n    assert solution([1,2,3]) is None\n"
       "def test_empty():\n    assert solution([]) is None\n"),
    _t("search_03", "searching", "medium",
       "Write `solution(nums, target)`: return [i, j] with i < j such that nums[i] + nums[j] == target. Exactly one solution exists.",
       "def test_a():\n    assert solution([2,7,11,15], 9) == [0,1]\n"
       "def test_b():\n    assert solution([3,2,4], 6) == [1,2]\n"
       "def test_c():\n    assert solution([3,3], 6) == [0,1]\n"),
    _t("search_04", "searching", "medium",
       "Write `solution(nums, k)`: return the k-th largest element (counting duplicates) of a list.",
       "def test_a():\n    assert solution([3,2,1,5,6,4], 2) == 5\n"
       "def test_b():\n    assert solution([3,2,3,1,2,4,5,5,6], 4) == 4\n"
       "def test_c():\n    assert solution([1], 1) == 1\n"),
    # ---- string manipulation ----
    _t("string_01", "string_manipulation", "easy",
       "Write `solution(s)`: return True if s is a palindrome considering only alphanumeric characters and ignoring case.",
       "def test_a():\n    assert solution('A man, a plan, a canal: Panama') is True\n"
       "def test_b():\n    assert solution('race a car') is False\n"
       "def test_empty():\n    assert solution('') is True\n"),
    _t("string_02", "string_manipulation", "easy",
       "Write `solution(text)`: return a dict of lowercase word counts, where a word is a maximal run of ASCII letters.",
       "def test_a():\n    assert solution('The cat, the hat.') == {'the':2,'cat':1,'hat':1}\n"
       "def test_empty():\n    assert solution('') == {}\n"
       "def test_punct():\n    assert solution('a-b a') == {'a':2,'b':1}\n"),
    _t("string_03", "string_manipulation", "medium",
       "Write `solution(text, shift)`: Caesar cipher. Shift letters by `shift` (may be negative or > 26), preserve case, leave other characters unchanged.",
       "def test_a():\n    assert solution('abc xyz!', 3) == 'def abc!'\n"
       "def test_neg():\n    assert solution('Abc', -1) == 'Zab'\n"
       "def test_big():\n    assert solution('abc', 29) == 'def'\n"),
    _t("string_04", "string_manipulation", "medium",
       "Write `solution(words)`: group anagrams. Return a list of groups; each group sorted alphabetically, groups sorted by their first element.",
       "def test_a():\n    assert solution(['eat','tea','tan','ate','nat','bat']) == [['ate','eat','tea'],['bat'],['nat','tan']]\n"
       "def test_empty():\n    assert solution([]) == []\n"),
    # ---- api / data (offline parsing & validation) ----
    _t("api_01", "api_calls", "easy",
       "Write `solution(qs)`: parse a URL query string into a dict of str->str. A leading '?' is ignored; a key with no value maps to ''; empty input gives {}.",
       "def test_a():\n    assert solution('a=1&b=2') == {'a':'1','b':'2'}\n"
       "def test_q():\n    assert solution('?x=hello') == {'x':'hello'}\n"
       "def test_empty():\n    assert solution('') == {}\n"
       "def test_novalue():\n    assert solution('a=&b=2') == {'a':'','b':'2'}\n"),
    _t("api_02", "api_calls", "medium",
       "Write `solution(d)`: flatten a nested dict into a single-level dict using '.'-joined keys.",
       "def test_a():\n    assert solution({'a':{'b':1,'c':{'d':2}},'e':3}) == {'a.b':1,'a.c.d':2,'e':3}\n"
       "def test_empty():\n    assert solution({}) == {}\n"),
    _t("api_03", "api_calls", "medium",
       "Write `solution(s)`: return True if s is a plausible email: exactly one '@', non-empty local part, domain contains a '.', "
       "domain does not start or end with '.', and no whitespace anywhere.",
       "def test_ok():\n    assert solution('a@b.com') is True\n"
       "def test_bad():\n    assert not solution('a@b') and not solution('@b.com') and not solution('a b@c.com')\n"
       "def test_dots():\n    assert not solution('a@.com') and not solution('a@b.') and not solution('a@@b.com')\n"),
    _t("api_04", "api_calls", "medium",
       "Write `solution(items, page, per_page)`: paginate a list (pages are 1-indexed). Return {'items': <slice>, 'total_pages': <int>}; "
       "a page past the end gives empty items; an empty list has 0 total pages.",
       "def test_a():\n    assert solution(list(range(1,11)), 2, 3) == {'items':[4,5,6],'total_pages':4}\n"
       "def test_past():\n    assert solution(list(range(1,11)), 5, 3) == {'items':[],'total_pages':4}\n"
       "def test_empty():\n    assert solution([], 1, 3) == {'items':[],'total_pages':0}\n"),
    # ---- data processing ----
    _t("data_01", "data_processing", "easy",
       "Write `solution(rows, key)`: group a list of dicts by the value of `key`; return a dict mapping value -> list of rows in original order.",
       "def test_a():\n    rows=[{'k':1,'v':'a'},{'k':2,'v':'b'},{'k':1,'v':'c'}]\n    assert solution(rows,'k') == {1:[rows[0],rows[2]],2:[rows[1]]}\n"
       "def test_empty():\n    assert solution([], 'k') == {}\n"),
    _t("data_02", "data_processing", "medium",
       "Write `solution(nums, k)`: return the list of averages of every contiguous window of size k; empty list if len(nums) < k.",
       "def test_a():\n    assert solution([1,2,3,4], 2) == [1.5,2.5,3.5]\n"
       "def test_short():\n    assert solution([1], 2) == []\n"
       "def test_full():\n    assert solution([2,4], 2) == [3]\n"),
    _t("data_03", "data_processing", "easy",
       "Write `solution(items)`: remove duplicates from a list while preserving first-occurrence order.",
       "def test_a():\n    assert solution([3,1,3,2,1]) == [3,1,2]\n"
       "def test_empty():\n    assert solution([]) == []\n"),
    _t("data_04", "data_processing", "medium",
       "Write `solution(csv_text, column)`: csv_text has a header row; return the numeric sum of the named column, skipping blank cells.",
       "def test_a():\n    assert solution('a,b\\n1,2\\n3,\\n', 'a') == 4\n"
       "def test_blank():\n    assert solution('a,b\\n1,2\\n3,\\n', 'b') == 2\n"
       "def test_float():\n    assert solution('x\\n1.5\\n2.5\\n', 'x') == 4.0\n"),
]


from src.data.test_datasets_hard import HARD_TASKS  # noqa: E402

TASKS += HARD_TASKS


from src.data.test_datasets_hard2 import HARD2_TASKS  # noqa: E402

TASKS += HARD2_TASKS
