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

from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

from kivy.lang import Builder

from elementbehavior import ElementBehavior

import textwrap

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
        self.register_shortcut(8, modifier='ctrl', callback=self.delete_word_left) # 'ctrl' + backspace
        self.register_shortcut(127, modifier='ctrl', callback=self.delete_word_right) # 'ctrl' + delete

    def insert_text(self, substring, from_undo=False):
        # TODO: Clip spaces at the beginning of lines post wrap.
        # TODO: Dynamically resize TextInput so it does not clip any of the
        #       inputted text from view. SEE: texture_size...
        unwrapped = self.text.replace('\n', '')
        to_wrap = unwrapped + substring
        wrapped_text = textwrap.fill(to_wrap, width=30, drop_whitespace=False)
        self.text = ''
        super().insert_text(wrapped_text, from_undo=from_undo)


class Action(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Scene(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unaltered_text = ''

    def insert_text(self, substring, from_undo=False):
        '''Capitalize scene heading.'''
        self.unaltered_text += substring
        print(self.unaltered_text)
        insert = substring.upper()
        super().insert_text(insert, from_undo)

    def on_backspace(self, modifier=None):
        """Track unaltered text on backspace"""
        if self.unaltered_text:
            if modifier == 'ctrl':
                # Slice off trailing word
                # TODO: Below is hackey. Do it properly.
                self.unaltered_text = self.unaltered_text[::-1].split(' ', 1)[1][::-1] + ' '
            else:
                self.unaltered_text = self.unaltered_text[:-1]


class Character(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Dialogue(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
