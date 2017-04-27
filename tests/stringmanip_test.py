import pytest

from intercut.intercut.tools import stringmanip


def test_cut_basic_string():
    assert "the boy is " == stringmanip.remove_last_word("the boy is cool.")


def test_cut_empty_string():
    with pytest.raises(ValueError):
        stringmanip.remove_last_word("")


def test_cut_no_spaces():
    assert "" == stringmanip.remove_last_word("NoSpacesInString")
