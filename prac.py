"""Convert an integer to its base-13 string representation."""

import sys

DIGITS = "0123456789ABC"


def _digit_stream(n: int):
    """Generate base-13 digits for a positive integer, least significant first.

    Args:
        n: A positive integer.

    Yields:
        Single base-13 digit characters from least to most significant.
    """
    while n:
        yield DIGITS[n % 13]
        n //= 13


def to_base13(num: int) -> str:
    """Return the base-13 string representation of an integer.

    Digits 0-9 represent values 0-9; A, B, C represent 10, 11, 12.

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
    sign = "-" if num < 0 else ""
    return sign + "".join(reversed(list(_digit_stream(abs(num)))))


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


if __name__ == "__main__":
    run_tests()
