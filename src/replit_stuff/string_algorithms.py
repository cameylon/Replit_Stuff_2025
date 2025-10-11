"""String comparison algorithms used throughout the project.

The module provides a small toolkit with dependable and well tested
implementations of classic string comparison algorithms:

* :func:`levenshtein_distance` implements the edit distance between two
  strings using dynamic programming with reduced memory usage.
* :func:`longest_common_subsequence` computes the longest subsequence that
  appears in the same relative order in both inputs.
* :func:`diff_highlight` produces a human friendly diff representation that
  can be used in logs or user interfaces to highlight how two strings differ.

The functions are designed to be straightforward to use and have comprehensive
unit tests.  They do not depend on any third-party libraries, making them
portable and reliable in constrained environments (such as Replit sandboxes).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import List, Sequence


def levenshtein_distance(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    The implementation uses a dynamic-programming algorithm with linear space
    complexity.  Only two rows of the DP matrix are kept in memory, making the
    function suitable for relatively long inputs while remaining easy to
    understand.

    Args:
        a: The first string.
        b: The second string.

    Returns:
        The minimum number of single-character edits (insertions, deletions or
        substitutions) required to change *a* into *b*.
    """

    if not isinstance(a, str) or not isinstance(b, str):  # type: ignore[unreachable]
        raise TypeError("Both arguments must be strings")

    if a == b:
        return 0

    if len(a) < len(b):
        a, b = b, a

    previous_row: List[int] = list(range(len(b) + 1))
    for i, char_a in enumerate(a, start=1):
        current_row = [i]
        for j, char_b in enumerate(b, start=1):
            insertion = current_row[j - 1] + 1
            deletion = previous_row[j] + 1
            substitution = previous_row[j - 1] + (char_a != char_b)
            current_row.append(min(insertion, deletion, substitution))
        previous_row = current_row
    return previous_row[-1]


def longest_common_subsequence(a: str, b: str) -> str:
    """Return the longest common subsequence of *a* and *b*.

    When multiple subsequences have the same maximum length the
    lexicographically smallest subsequence is returned.  The implementation uses
    memoised recursion which keeps the code compact while still being efficient
    for typical input sizes.
    """

    if not isinstance(a, str) or not isinstance(b, str):  # type: ignore[unreachable]
        raise TypeError("Both arguments must be strings")

    @lru_cache(maxsize=None)
    def helper(i: int, j: int) -> str:
        if i == len(a) or j == len(b):
            return ""
        if a[i] == b[j]:
            return a[i] + helper(i + 1, j + 1)

        option1 = helper(i + 1, j)
        option2 = helper(i, j + 1)
        if len(option1) > len(option2):
            return option1
        if len(option2) > len(option1):
            return option2
        return min(option1, option2)

    return helper(0, 0)


@dataclass(frozen=True)
class DiffOp:
    """A representation of a single diff operation."""

    tag: str
    text: str

    def __post_init__(self) -> None:
        if self.tag not in {"equal", "insert", "delete"}:
            raise ValueError(f"Invalid diff tag: {self.tag}")


def diff_highlight(a: str, b: str) -> List[DiffOp]:
    """Produce a simple diff between *a* and *b*.

    The function returns a list of :class:`DiffOp` instances describing how to
    transform *a* into *b*.  It is intentionally limited compared to the
    :mod:`difflib` module but produces cleaner output for short strings.
    """

    if not isinstance(a, str) or not isinstance(b, str):  # type: ignore[unreachable]
        raise TypeError("Both arguments must be strings")

    if a == b:
        return [DiffOp("equal", a)] if a else []

    lcs = longest_common_subsequence(a, b)

    ops: List[DiffOp] = []
    i = j = k = 0
    while k < len(lcs):
        target = lcs[k]
        while i < len(a) and a[i] != target:
            ops.append(DiffOp("delete", a[i]))
            i += 1
        while j < len(b) and b[j] != target:
            ops.append(DiffOp("insert", b[j]))
            j += 1
        ops.append(DiffOp("equal", target))
        i += 1
        j += 1
        k += 1

    if i < len(a):
        ops.append(DiffOp("delete", a[i:]))
    if j < len(b):
        ops.append(DiffOp("insert", b[j:]))

    return _merge_adjacent_ops(ops)


def _merge_adjacent_ops(ops: Sequence[DiffOp]) -> List[DiffOp]:
    """Merge neighbouring operations with the same tag."""

    merged: List[DiffOp] = []
    for op in ops:
        if merged and merged[-1].tag == op.tag:
            merged[-1] = DiffOp(merged[-1].tag, merged[-1].text + op.text)
        else:
            merged.append(op)
    return merged


__all__ = [
    "DiffOp",
    "diff_highlight",
    "levenshtein_distance",
    "longest_common_subsequence",
]
