import sys, os
tests_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, tests_path + '/../intercut')

import pytest

import elements


@pytest.fixture
def empty_action_element():
    '''Return an empty Action element.'''
    return elements.Action()


@pytest.fixture
def empty_character_element():
    '''Return and empty Character element.'''
    return elements.Character()

@pytest.fixture
def empty_dialogue_element():
    '''Return an empty Dialogue element.'''
    return elements.Dialogue()


@pytest.fixture
def empty_parenthetical_element():
    '''Return an empty Parenthetical element.'''
    return elements.Parenthetical()


@pytest.fixture
def empty_heading_element():
    '''Return an empty SceneHeading element.'''
    return elements.SceneHeading()


@pytest.mark.parametrize("current_element,next_elem", [
    (empty_action_element(), elements.Action),
    (empty_character_element(), elements.Dialogue),
    (empty_dialogue_element(), elements.Character),
    (empty_parenthetical_element(), elements.Dialogue),
    (empty_heading_element(), elements.Action),
])
def test_next_element(current_element, next_elem):
    assert isinstance(current_element.next_element(), next_elem)
