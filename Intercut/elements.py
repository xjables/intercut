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

from elementbehavior import ModBehavior

Builder.load_file(r'elements.kv')


class Element(ModBehavior, TextInput):

    """A base class for all of the individual elements."""

    # This will be used to track the elements location in the SP directly.
    element_index = NumericProperty()

    def __init__(self, **kwargs):
        # Every object can be referenced by a lowercase version of its name
        super().__init__(**kwargs)


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
