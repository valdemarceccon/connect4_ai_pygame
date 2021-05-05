import game


def test_is_sublist():
    assert game.is_sublist([1, 2, 3, 4, 5], [2, 3, 4]) is True
    assert game.is_sublist([1, 2, 3, 4, 5], [3, 2, 4]) is False
    assert game.is_sublist([1, 2, 3, 4, 5], [1, 2]) is True
    assert game.is_sublist([1, 2, 3, 4, 5], [1]) is True
    assert game.is_sublist([1, 2, 3, 4, 5], []) is True
