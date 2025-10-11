import pytest

from replit_stuff.string_algorithms import (
    DiffOp,
    diff_highlight,
    levenshtein_distance,
    longest_common_subsequence,
)


def test_levenshtein_distance_basic():
    assert levenshtein_distance("kitten", "sitting") == 3
    assert levenshtein_distance("", "") == 0
    assert levenshtein_distance("abc", "abc") == 0
    assert levenshtein_distance("flaw", "lawn") == 2


def test_levenshtein_distance_type_error():
    with pytest.raises(TypeError):
        levenshtein_distance(123, "abc")  # type: ignore[arg-type]


def test_longest_common_subsequence():
    assert longest_common_subsequence("abcde", "ace") == "ace"
    assert longest_common_subsequence("abc", "def") == ""
    assert longest_common_subsequence("aaaa", "aa") == "aa"
    # tie breaking
    assert longest_common_subsequence("zab", "zba") == "za"


def test_diff_highlight_equal():
    assert diff_highlight("hello", "hello") == [DiffOp("equal", "hello")]
    assert diff_highlight("", "") == []


def test_diff_highlight_insert_delete():
    ops = diff_highlight("cat", "cart")
    assert ops == [DiffOp("equal", "ca"), DiffOp("insert", "r"), DiffOp("equal", "t")]

    ops = diff_highlight("spore", "sore")
    assert ops == [DiffOp("equal", "s"), DiffOp("delete", "p"), DiffOp("equal", "ore")]


def test_diff_highlight_complex():
    ops = diff_highlight("abcd", "azced")
    assert ops == [
        DiffOp("equal", "a"),
        DiffOp("delete", "b"),
        DiffOp("insert", "z"),
        DiffOp("equal", "c"),
        DiffOp("insert", "e"),
        DiffOp("equal", "d"),
    ]


def test_diff_highlight_type_error():
    with pytest.raises(TypeError):
        diff_highlight(1, "abc")  # type: ignore[arg-type]


def test_diff_highlight_merge_adjacent():
    ops = diff_highlight("abc", "xyz")
    assert ops == [DiffOp("delete", "abc"), DiffOp("insert", "xyz")]
