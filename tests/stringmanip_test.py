import pytest

from intercut.Intercut.tools import stringmanip

def test_cut_basic_string():
    assert "the boy is " == stringmanip.remove_last_word("the boy is cool.")

def test_cut_empty_string():
    with pytest.raises(ValueError):
        stringmanip.remove_last_word("")
