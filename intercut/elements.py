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
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.lang import Builder

from elementbehavior import ElementBehavior
from coreinput import CoreInput
from tools.stringmanip import RawText
import time

Builder.load_file(r'elements.kv')


class Element(ElementBehavior, CoreInput):

    """A base class for all of the individual elements."""

    element_index = NumericProperty()
    # TextInput.text is the displayed text. It will have formatting in it such
    # as capitalizations and wrapping newline characters. This text will remain
    # unformatted in the background.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # This will be used to track the elements location in the SP directly.
        self.element_index = 0
        self.raw_text = ''

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

    def get_location(self):
        """Retrieve the coordinates of this element.
        
        Returns:
            tuple: Tuple containing (scene_index, element_index)
        """
        scene = self.parent
        return scene.scene_index, self.element_index

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
            scene.remove_element(self)

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

    def raw_contraction(self):
        # TODO: Rework this a little (it is bount to on_text)
        len_txt = len(self.text)
        len_raw = len(self.raw_text)
        raw_text = self.raw_text

        if len_raw > len_txt:
            cut_len = len_raw - len_txt
            slice_to = 0
            try:
                for index, char in enumerate(self.raw_text):
                    if char.upper() != self.text[index]:
                        slice_to = index
                        break
            except IndexError:
                slice_to = len_txt
            self.raw_text = raw_text[:slice_to] + raw_text[slice_to + cut_len:]
            print(self.raw_text)


class SuggestiveElement(Element):
    """A special type of element that provides text completion DropDown.
    
    This class is designed for Character and SceneHeading elements with the
    intent that they will provide a DropDown list of already established
    characters and locations as the user types.
    """

    source = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drop_down = DropDown()
        dd = self.drop_down
        dd.bind(on_select=self.on_select)

    def on_source(self, instance, suggestions):
        """When drop_source changes, update DropDown options.
        
        Args:
            instance: 
                Catches another instance of self passed by the event handler.
            suggestions: 
                The actual list of established characters/locations
        """
        print('on_source')
        dd = self.drop_down
        dd.clear_widgets()
        for suggestion in suggestions:
            print('line_height', self.line_height)
            button = Button(text=suggestion, size_hint_y=None, height=30)
            button.bind(on_release=lambda btn: dd.select(btn.text))
            dd.add_widget(button)

    def on_select(self, instance, text):
        """Change Element text to selected text."""
        self.text = ''
        self.insert_text(substring=text, from_undo=False)

    def on_text(self, instance, value):
        text = self.text
        if not text:
            self.drop_down.dismiss()
        else:
            self.drop_down.open(self)

    def insert_text(self, substring, from_undo=False):
        raw_text = self.raw_text
        slice_to = self.cursor_index()
        self.raw_text = raw_text[:slice_to] + substring + raw_text[slice_to:]
        insert = substring.upper()
        super().insert_text(insert, from_undo=from_undo)


class Action(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def next_element(self):
        scene = self.parent
        scene.add_element(self, added_element=Dialogue)

    def tab_to(self):
        pass


class SceneHeading(SuggestiveElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def next_element(self):
        scene = self.parent
        scene.add_element(self, added_element=Action)
        self.drop_down.dismiss()

    def tab_to(self):
        pass


class Character(SuggestiveElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def next_element(self):
        scene = self.parent
        scene.add_element(self, added_element=Dialogue)
        self.drop_down.dismiss()

    def tab_to(self):
        pass


class Dialogue(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def insert_text(self, substring, from_undo=False):
        """Capitalize scene heading."""
        raw_text = self.raw_text
        slice_to = self.cursor_index()
        self.raw_text = raw_text[:slice_to] + substring + raw_text[slice_to:]
        print(self.raw_text)
        super().insert_text(substring, from_undo=from_undo)

    def next_element(self):
        scene = self.parent
        scene.add_element(self, added_element=Character)

    def tab_to(self):
        pass



