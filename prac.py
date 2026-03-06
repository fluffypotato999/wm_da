"""Convert an integer to its base-13 string representation."""

DIGITS = "0123456789ABC"


def _collect_digits(n: int) -> list[str]:
    """Recursively collect base-13 digits for a non-negative integer.

    Args:
        n: A non-negative integer.

    Returns:
        A list of base-13 digit characters, most significant first.
    """
    if n == 0:
        return []
    return _collect_digits(n // 13) + [DIGITS[n % 13]]


def to_base13(num: int) -> str:
    """Return the base-13 string representation of an integer.

    Uses digits 0-9 for values 0-9 and A, B, C for 10, 11, 12.

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
    digits = _collect_digits(abs(num))
    return sign + "".join(digits)


if __name__ == "__main__":
    test_cases = [0, 1, 12, 13, 14, 28, 169, -1, -13, -170]
    for n in test_cases:
        print(f"to_base13({n:>6}) = {to_base13(n)}")
