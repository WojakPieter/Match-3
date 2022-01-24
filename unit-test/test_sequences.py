from sequences import Sequence, NotQuadraticListError
import pytest


def test_invalid_list():
    list = [['a', 'b', 'c', 'd'],
            ['a', 'b', 'c', 'd']]
    with pytest.raises(NotQuadraticListError):
        seq = Sequence(list)


def test_find_sequences_vertical():
    list = [['a', 'b', 'c', 'd', 'e', 'f'],
            ['g', 'h', 'i', 'j', 'k', 'l'],
            ['m', 'n', 'J', 'o', 'p', 'r'],
            ['s', 't', 'J', 'u', 'w', 'x'],
            ['y', 'z', 'J', 'u', 'w', 'x'],
            ['a', 'b', 'c', 'd', 'e', 'f']]
    seq = Sequence(list).findSequences()
    assert (2, 2) in seq
    assert (3, 2) in seq
    assert (4, 2) in seq
    assert len(seq) == 3


def test_find_sequences_horizontal():
    list = [['a', 'b', 'c', 'd', 'e', 'f'],
            ['g', 'h', 'i', 'j', 'k', 'l'],
            ['m', 'n', 'J', 'J', 'J', 'r'],
            ['s', 't', 'o', 'u', 'w', 'x'],
            ['y', 'z', 'p', 'u', 'w', 'x'],
            ['a', 'b', 'c', 'd', 'e', 'f']]
    seq = Sequence(list).findSequences()
    assert (2, 2) in seq
    assert (2, 3) in seq
    assert (2, 4) in seq
    assert len(seq) == 3


def test_find_multiplied_sequences():
    list = [['a', 'b', 'c', 'J', 'e', 'f'],
            ['g', 'h', 'i', 'J', 'k', 'l'],
            ['m', 'n', 'J', 'J', 'J', 'r'],
            ['s', 't', 'o', 'u', 'w', 'x'],
            ['y', 'z', 'p', 'u', 'w', 'x'],
            ['a', 'b', 'c', 'd', 'e', 'f']]
    seq = Sequence(list).findSequences()
    assert (0, 3) in seq
    assert (1, 3) in seq
    assert (2, 3) in seq
    assert (2, 2) in seq
    assert (2, 4) in seq
    assert len(seq) == 5


def test_find_multiplied_sequences2():
    list = [['a', 'b', 'c', 'd', 'e', 'f'],
            ['g', 'h', 'i', 'j', 'k', 'l'],
            ['m', 'J', 'J', 'J', 't', 'r'],
            ['s', 'J', 'o', 'u', 'w', 'x'],
            ['y', 'J', 'p', 'u', 'w', 'x'],
            ['a', 'b', 'c', 'd', 'e', 'f']]
    seq = Sequence(list).findSequences()
    assert (2, 1) in seq
    assert (3, 1) in seq
    assert (4, 1) in seq
    assert (2, 2) in seq
    assert (2, 3) in seq
    assert (1, 3) not in seq
    assert len(seq) == 5


def test_find_multiplied_sequences_in_corner():
    list = [['J', 'J', 'J', 'd', 'e', 'f'],
            ['J', 'h', 'i', 'j', 'k', 'l'],
            ['J', 'n', 'j', 'k', 'j', 'r'],
            ['J', 't', 'o', 'u', 'w', 'x'],
            ['y', 'z', 'p', 'u', 'w', 'x'],
            ['a', 'b', 'c', 'd', 'e', 'f']]
    seq = Sequence(list).findSequences()
    assert (0, 0) in seq
    assert (0, 1) in seq
    assert (0, 2) in seq
    assert (1, 0) in seq
    assert (2, 0) in seq
    assert (3, 0) in seq
    assert len(seq) == 6


def test_find_possible_sequences_horizontal_separated():
    list = [['a', 'c', 'b', 'd', 'e', 'f'],
            ['b', 'h', 'i', 'J', 'k', 'l'],
            ['c', 'n', 'J', 'k', 'J', 'r'],
            ['d', 't', 'o', 'u', 'w', 'x'],
            ['y', 'z', 'p', 'u', 'w', 'x'],
            ['a', 'b', 'c', 'd', 'e', 'f']]
    seq = Sequence(list).findPossibleSequences()
    assert seq == [[(1, 3), (2, 3)]]


def test_find_possible_sequences_horizontal():
    list = [['a', 'J', 'c', 'd', 'J', 'f'],
            ['J', 'h', 'J', 'J', 'k', 'J'],
            ['d', 'J', 'x', 'k', 'J', 'r'],
            ['c', 't', 'o', 'u', 'w', 'x'],
            ['y', 'z', 'p', 'u', 'w', 'x'],
            ['a', 'b', 'c', 'd', 'e', 'f']]
    seq = Sequence(list).findPossibleSequences()
    assert [(1, 4), (2, 4)] in seq
    assert [(0, 4), (1, 4)] in seq
    assert [(1, 4), (1, 5)] in seq
    assert [(0, 1), (1, 1)] in seq
    assert [(1, 0), (1, 1)] in seq


def test_find_possible_sequences_vertical():
    list = [['a', 'a', 'J', 'd', 'J', 'f'],
            ['b', 'J', 'i', 'J', 'k', 'J'],
            ['d', 'a', 'J', 'k', 'J', 'r'],
            ['c', 't', 'J', 'u', 'w', 'x'],
            ['y', 'J', 'p', 'J', 'w', 'x'],
            ['a', 'b', 'J', 'd', 'e', 'f']]
    seq = Sequence(list).findPossibleSequences()
    assert [(1, 1), (1, 2)] in seq
    assert [(0, 2), (1, 2)] in seq
    assert [(1, 2), (1, 3)] in seq
    assert [(4, 1), (4, 2)] in seq
    assert [(4, 2), (4, 3)] in seq
    assert [(4, 2), (5, 2)] in seq


def test_find_possible_sequences_vertical_separated():
    list = [['a', 'a', 'J', 'd', 'J', 'f'],
            ['b', 'J', 'i', 'J', 'k', 'J'],
            ['d', 'a', 'J', 'k', 'J', 'r'],
            ['c', 't', 't', 'u', 'w', 'x'],
            ['y', 'J', 'p', 'J', 'w', 'x'],
            ['a', 'b', 'J', 'd', 'e', 'f']]
    seq = Sequence(list).findPossibleSequences()
    assert [(1, 1), (1, 2)] in seq
    assert [(1, 2), (1, 3)] in seq
