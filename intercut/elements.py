"""Define all of the Screenplay elements.

Scene:
    This element indicates the location of the following action.

Action:
    This element describes what happens.

Character:
    This element indicates who will be talking the following dialgue.

Dialogue:
    These are the talky parts.

Parenthetical:
    This is embedded in dialogue to indicate a non-verbal cue to the actors.
"""

import textwrap

from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.lang import Builder

from elementbehavior import ElementBehavior
from textinput import CoreInput
from tools import stringmanip
import time

Builder.load_file(r'elements.kv')


class Element(ElementBehavior, CoreInput):

    """A base class for all of the individual elements."""

    # This will be used to track the elements location in the SP directly.
    element_index = NumericProperty()
    # TextInput.text is the displayed text. It will have formatting in it such
    # as capitalizations and wrapping newline characters. This text will remain
    # unformatted in the background.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.register_shortcut(  # enter
            13, callback=self.next_element)
        self.register_shortcut(  # backspace
            8, callback=self.on_backspace, kill=False)
        self.register_shortcut(  # tab
             9, callback=self.tab_to)

        self.register_shortcut(  # 'ctrl' + backspace
            8, modifier='ctrl', callback=self.delete_word_left)
        self.register_shortcut(  # 'ctrl' + delete
            127, modifier='ctrl', callback=self.delete_word_right)

    def on_backspace(self):
        """Handle special backspace cases.

        When backspace is pressed from the left-most position in the element,
        the element is deleted. The remaining text in the element is transformed
        into the format of the preceding element.
        """
        slice_to = self.cursor_index()
        focus_index = self.element_index
        scene = self.parent

        if self.text[:slice_to] == '':
            leftover_text = self.text[slice_to:]
            scene.remove_widget(self)

            # preceding_element = scene.get_element_from_index(focus_index)
            # preceding_element.focus = True
            #
            # if leftover_text:
            #     preceding_element.insert_text(leftover_text)
            #     for char in range(len(leftover_text)):
            #         preceding_element.do_cursor_movement('cursor_left')
            #         print(preceding_element.cursor)

    def get_length(self):
        """Return the length of the text string for an element."""
        return len(self.text)


class Action(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def next_element(self):
        scene = self.parent
        scene.add_element(self, added_element=Dialogue)


class SceneHeading(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def insert_text(self, substring, from_undo=False):
        """Capitalize scene heading."""
        insert = substring.upper()
        super().insert_text(insert, from_undo=from_undo)

    def next_element(self):
        scene = self.parent
        scene.add_element(self, added_element=Action)

    def tab_to(self):
        pass


class Character(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def next_element(self):
        scene = self.parent
        scene.add_element(self, added_element=Dialogue)

    def tab_to(self):
        pass


class Dialogue(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def next_element(self):
        scene = self.parent
        scene.add_element(self, added_element=Character)

    def tab_to(self):
        pass



