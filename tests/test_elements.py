import sys, os
tests_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, tests_path + '/../intercut')

import pytest

import elements


@pytest.fixture
def empty_action_element():
    '''Return an empty action element.'''
    print(type(elements.Action().on_enter()))
    return elements.Action()
    
    
def test_action_next_element(empty_action_element):
    assert isinstance(empty_action_element.on_enter(), elements.Action())

