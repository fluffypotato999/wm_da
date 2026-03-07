"""Practice problems: base-13 conversion, duplicate detection, sliding window."""

import sys
from collections import defaultdict

DIGITS = "0123456789ABC"


def to_base13(num: int) -> str:
    """Return the base-13 string representation of an integer.

    Digits 0-9 represent values 0-9; A, B, C represent 10, 11, 12.
    Uses recursion: the most significant digits are resolved first by
    recursing on num // 13, then the current digit is appended.

    Args:
        num: The integer to convert.

    Returns:
        A string representing num in base 13.

    Examples:
        >>> to_base13(0)
        '0'
        >>> to_base13(13)
        '10'
        >>> to_base13(-14)
        '-11'
    """
    if num == 0:
        return "0"
    if num < 0:
        return "-" + to_base13(-num)
    if num < 13:
        return DIGITS[num]
    return to_base13(num // 13) + DIGITS[num % 13]


def run_tests() -> None:
    """Run test cases and report results."""
    # (input, expected_output)
    cases = [
        (0,        "0"),      # zero
        (1,        "1"),      # one
        (9,        "9"),      # last decimal-only digit
        (10,       "A"),      # first alpha digit
        (11,       "B"),
        (12,       "C"),      # last single digit
        (13,       "10"),     # base rollover
        (14,       "11"),
        (26,       "20"),
        (169,      "100"),    # 13^2
        (2026,     "BCB"),    # current year
        (1000000,  "290221"),
        (-1,       "-1"),     # negative
        (-13,      "-10"),
        (-170,     "-101"),
        (-2026,    "-BCB"),
    ]

    passed = failed = 0
    for num, expected in cases:
        result = to_base13(num)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            failed += 1
            print(f"  {status}  to_base13({num:>8}) = {result!r:>8}  (expected {expected!r})")
        else:
            passed += 1
            print(f"  {status}  to_base13({num:>8}) = {result!r}")

    print(f"\n{passed} passed, {failed} failed.")
    if failed:
        sys.exit(1)


def has_duplicate(input: list[int]) -> bool:
    """Return True if any value appears at least twice, False if all are distinct.

    Args:
        input: A list of integers.

    Returns:
        True if any duplicate exists, False otherwise.

    Examples:
        >>> has_duplicate([1, 2, 3, 1])
        True
        >>> has_duplicate([1, 2, 3, 4])
        False
    """
    return len(input) != len(set(input))


def run_duplicate_tests() -> None:
    """Run test cases for has_duplicate."""
    cases = [
        ([1, 2, 3, 1],      True),   # duplicate at start and end
        ([1, 2, 3, 4],      False),  # all distinct
        ([],                False),  # empty list
        ([1],               False),  # single element
        ([1, 1],            True),   # two identical elements
        ([1, 2, 3, 4, 2],  True),   # duplicate in middle
        ([-1, -2, -1],      True),   # negative duplicates
        ([0, 0],            True),   # zero duplicate
        ([1, 2, 3],         False),  # no duplicates
    ]

    passed = failed = 0
    for nums, expected in cases:
        result = has_duplicate(nums)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            failed += 1
            print(f"  {status}  has_duplicate({nums}) = {result}  (expected {expected})")
        else:
            passed += 1
            print(f"  {status}  has_duplicate({nums}) = {result}")

    print(f"\n{passed} passed, {failed} failed.")
    if failed:
        sys.exit(1)


def searching_challenge(s: str) -> str:
    """Find the longest substring with exactly k unique characters.

    The first character of s is the integer k. The search begins from
    the second character onward. Uses a sliding window approach.

    Args:
        s: A string whose first character is k (number of unique chars)
            and the remainder is the text to search.

    Returns:
        The longest substring containing exactly k unique characters.
        Returns an empty string if no such substring exists.

    Examples:
        >>> searching_challenge("2aabbacbaa")
        'aabba'
        >>> searching_challenge("3aabacbebebe")
        'cbebebe'
    """
    k = int(s[0])
    text = s[1:]

    if k == 0 or not text:
        return ""

    char_count = defaultdict(int)
    left = 0
    best_start = 0
    best_len = 0

    for right, char in enumerate(text):
        char_count[char] += 1

        while len(char_count) > k:
            char_count[text[left]] -= 1
            if char_count[text[left]] == 0:
                del char_count[text[left]]
            left += 1

        if len(char_count) == k and (right - left + 1) > best_len:
            best_len = right - left + 1
            best_start = left

    return text[best_start:best_start + best_len]


def run_searching_tests() -> None:
    """Run test cases for searching_challenge."""
    cases = [
        ("2aabbacbaa",    "aabba"),    # k=2, longest with 2 unique
        ("3aabacbebebe",  "cbebebe"),  # k=3, longest with 3 unique
        ("1aabbcc",       "aa"),       # k=1, only same chars
        ("2abcdef",       "ab"),       # k=2, no long run
        ("3aaaa",         ""),         # k=3, not enough unique chars
        ("2aabb",         "aabb"),     # k=2, whole string qualifies
    ]

    passed = failed = 0
    for s, expected in cases:
        result = searching_challenge(s)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            failed += 1
            print(f"  {status}  searching_challenge({s!r}) = {result!r}  (expected {expected!r})")
        else:
            passed += 1
            print(f"  {status}  searching_challenge({s!r}) = {result!r}")

    print(f"\n{passed} passed, {failed} failed.")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    print("=== Base-13 Tests ===")
    run_tests()
    print("\n=== Duplicate Detection Tests ===")
    run_duplicate_tests()
    print("\n=== Searching Challenge Tests ===")
    run_searching_tests()
