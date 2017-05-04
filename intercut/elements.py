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
from tools import stringmanip
import time

Builder.load_file(r'elements.kv')


class Element(ElementBehavior, TextInput):

    """A base class for all of the individual elements."""

    # This will be used to track the elements location in the SP directly.
    element_index = NumericProperty()
    # TextInput.text is the displayed text. It will have formatting in it such
    # as capitalizations and wrapping newline characters. This text will remain
    # unformatted in the background.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.register_shortcut(  # 'ctrl' + backspace
            8, modifier='ctrl', callback=self.delete_word_left)
        self.register_shortcut(  # backspace
            8, callback=self.on_backspace)
        self.register_shortcut(  # 'ctrl' + delete
            127, modifier='ctrl', callback=self.delete_word_right)

    def insert_text(self, substring, from_undo=False):
        # TODO: Clip spaces at the beginning of lines post wrap.
        # TODO: Dynamically resize TextInput so it does not clip any of the
        #       inputted text from view. SEE: texture_size...
        unwrapped = self.text.replace('\n', '')
        to_wrap = unwrapped + substring
        wrapped_text = textwrap.fill(to_wrap, width=30, drop_whitespace=False)
        # The line below makes on_text be called. This is bad.
        self.text = wrapped_text

    def on_backspace(self):
        slice_to = self.cursor_index()
        focus_index = self.element_index
        screenplay = self.parent

        if self.text[:slice_to] == '':
            screenplay.remove_widget(self)
        screenplay.set_focus_by_index(focus_index)


    def get_length(self):
        return len(self.text)





class Action(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Scene(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unformatted = stringmanip.UnformattedText()

    def insert_text(self, substring, from_undo=False):
        """Capitalize scene heading."""
        self.unformatted.last_added = substring
        insert = substring.upper()
        super().insert_text(insert, from_undo)


class Character(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Dialogue(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



