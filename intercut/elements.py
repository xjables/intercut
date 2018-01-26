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
from functools import partial
import os.path

from suggest import DropSuggestion, SuggestionButton
from kivy.properties import NumericProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.dropdown import DropDownException

from elementbehavior import ElementBehavior
from coreinput import CoreInput

from collections import OrderedDict

kivy_file = os.path.splitext(os.path.abspath(__file__))[0] + '.kv'
Builder.load_file(kivy_file)


class Element(ElementBehavior, CoreInput):

    """A base class for all of the individual elements."""

    element_index = NumericProperty()
    # TextInput.text is the displayed text. It will have formatting in it such
    # as capitalizations and wrapping newline characters. This text will remain
    # unformatted in the background.
    raw_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # This will be used to track the elements location in the SP directly.
        self.element_index = 0
        # Register Special Keys
        self.register_shortcut(  # enter
            13, callback=self.on_enter)
        self.register_shortcut(  # backspace
            8, callback=self.on_backspace, kill=False)
        self.register_shortcut(  # tab
            9, callback=self.tab_to)
        self.register_shortcut(  # tab + shift
            9, modifier='shift', callback=self.tab_inverse)
        self.register_shortcut(  # down
            274, callback=self.press_down, kill=False)
        self.register_shortcut(  # up
            273, callback=self.press_up, kill=False)

        self.register_shortcut(  # 'ctrl' + backspace
            8, modifier='ctrl', callback=self.delete_word_left)
        self.register_shortcut(  # 'ctrl' + delete
            127, modifier='ctrl', callback=self.delete_word_right)

        # Transformation shortcuts
        self.register_shortcut(  # 'alt' + a
            97, modifier='alt', callback=partial(self.morph, new_type=Action))
        self.register_shortcut(  # 'alt' + s
            115, modifier='alt', callback=partial(self.morph, new_type=SceneHeading))
        self.register_shortcut(  # 'alt' + c
            99, modifier='alt', callback=partial(self.morph, new_type=Character))
        self.register_shortcut(  # 'alt' + d
            100, modifier='alt', callback=partial(self.morph, new_type=Dialogue))
        self.register_shortcut(  # 'alt' + p
            112, modifier='alt', callback=partial(self.morph, new_type=Parenthetical)
        )

    def morph(self, new_type):
        """Change an element into another element.
        
        Args:
            new_type: The class to into which the element will change.
        """
        scene = self.parent
        new_element = new_type()
        scene.transform_element(source_element=self, new_element=new_element)

    def get_location(self):
        """Retrieve the coordinates of this element.
        
        Returns:
            tuple: Tuple containing (scene_index, element_index)
        """
        scene = self.parent
        return scene.scene_index, self.element_index

    def cursor_at_end(self):
        """Returns true if cursor position is at the end of an element."""
        return self.cursor_index() == len(self.raw_text)

    def on_enter(self):
        if self.cursor_at_end():
            scene = self.parent
            scene.next_element(self)
        else:
            start = self.cursor_index()
            end = len(self.raw_text)
            self.select_text(start, end)

    def press_down(self):
        c_row = self.cursor[1]
        rows = self.get_lines()
        scene = self.parent
        elem_index = self.element_index

        if rows == c_row + 1:
            # if element is at the bottom of the Scene
            if elem_index == 0:
                return True
            else:
                to_focus = scene.children[elem_index - 1]
                to_focus.focus = True
                return True

    def press_up(self):
        c_row = self.cursor[1]
        scene = self.parent
        elem_index = self.element_index

        # If we are not at the top line...
        if not c_row:
            try:
                to_focus = scene.children[elem_index + 1]
                to_focus.focus = True
                return True
            except IndexError:
                return False

    def on_backspace(self):
        """Handle special backspace cases.

        When backspace is pressed from the left-most position in the element,
        the element is deleted. The remaining text in the element is transformed
        into the format of the preceding element.
        """
        slice_to = self.cursor_index()
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
        # TODO: Rework this a little (it is bound to on_text)
        if isinstance(self, Parenthetical):
            text = self.cut_text_parenthesis()
        else:
            text = self.text

        len_txt = len(text)
        len_raw = len(self.raw_text)
        raw_text = self.raw_text

        if len_raw > len_txt:
            cut_len = len_raw - len_txt
            slice_to = 0
            try:
                for index, char in enumerate(self.raw_text):
                    if char.upper() != text[index].upper():
                        slice_to = index
                        break
            except IndexError:
                slice_to = len_txt
            self.raw_text = raw_text[:slice_to] + raw_text[slice_to + cut_len:]

    def insert_text(self, substring, from_undo=False):
        """Capitalize scene heading."""
        print('element.insert_text')
        raw_text = self.raw_text
        slice_to = self.cursor_index()
        self.raw_text = raw_text[:slice_to] + substring + raw_text[
                                                          slice_to:]
        super().insert_text(substring=substring, from_undo=from_undo)

    def core_insert(self, substring, from_undo=False):
        super().insert_text(substring=substring, from_undo=from_undo)

    def integrate(self):
        """Initialization steps that must occur after element is in widget tree.

        If you have initialization steps that require the element to know its
        location in the widget tree, override this function in that specific
        element subclass.
        
        The most common usage of this will be to gain access to the self.parent
        attribute provided by Kivy once an element has been added to the tree.
        
        For example, in the Character element, we want the element to know
        where a list of possible suggestions can be found. Rather than have
        each object hold its own list that we have to update, these lists are
        held in the Screenplay itself and referenced from each object. However,
        in the __init__ method for Character, we cannot reference self.parent
        before the object we are constructing is added to the Screenplay. So,
        instead, we override Character.integrate, which is called after the
        Character element is added to use self.parent.parent.characters to
        point the element to the list of previously entered characters.
        """
        pass

    def get_json(self):
        json_dict = OrderedDict()

        json_dict['type'] = self.__class__.__name__
        json_dict['raw_text'] = self.raw_text

        return json_dict


class SuggestiveElement(Element):
    """A special type of element that provides a text completion DropDown.
    
    This class is designed for Character and SceneHeading elements with the
    intent that they will provide a DropDown list of already established
    characters and locations as the user types.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drop_down = DropSuggestion()
        self.init_drop_down()
        self.source = []  # Reassign in subclasses

        self.register_shortcut(
            273, self.on_arrow_up
        )
        self.register_shortcut(
            274, self.on_arrow_down
        )
        # TODO: Register up and down arrow shortcuts (38 and 40, respectively)
        # TODO: To navigate through buttons

    def on_arrow_down(self):
        if self.drop_down.is_open:
            self.drop_down.move_highlight(increment=1)
        else:
            self.press_down()

    def on_arrow_up(self):
        if self.drop_down.is_open:
            self.drop_down.move_highlight(increment=-1)
        else:
            self.press_up()

    def init_drop_down(self):
        """Handle binding for drop down menu."""
        dd = self.drop_down
        dd.bind(on_select=self.on_select)

    def update_options(self):
        """When drop_source changes, update DropDown options.
        
        Args:
            instance: 
                Catches another instance of self passed by the event handler.
            suggestions: 
                The actual list of established characters/locations
        """
        suggestions = self.filtered_options()
        dd = self.drop_down
        dd.clear_widgets()
        for suggestion in suggestions:
            button = SuggestionButton(text=suggestion)
            button.bind(on_release=lambda btn: dd.select(btn.text))
            dd.add_widget(button)

    def filtered_options(self):
        """Filter the list of possible options based on entered text."""
        options = self.source
        lower_text = (self.text).lower()
        filtered = []
        for option in options:
            lower_option = option.lower()
            if lower_option.startswith(lower_text):
                filtered.append(option)
        return filtered

    def on_select(self, instance, text):
        """Change Element text to selected text."""
        self.text = ''
        self.insert_text(substring=text, from_undo=False)
        super().on_enter()

    def on_text(self, instance, value):
        """Live update the drop down during typing."""
        text = self.text
        if text:
            self.update_options()
            try:
                self.drop_down.open(self)
                self.drop_down.set_highlight()
            except DropDownException:
                self.drop_down.dismiss()
        else:
            self.drop_down.dismiss()

    def on_enter(self):
        """Enter the top level option into the element."""
        dd = self.drop_down
        suggestions = dd.container.children
        if dd.is_open and suggestions:
            text = self.drop_down.get_selection_text()
            dd.select(text)
        else:
            super().on_enter()

    def insert_text(self, substring, from_undo=False):
        raw_text = self.raw_text
        slice_to = self.cursor_index()
        self.raw_text = raw_text[:slice_to] + substring + raw_text[slice_to:]
        insert = substring.upper()
        super().core_insert(substring=insert, from_undo=from_undo)
        return


class Action(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def next_element(self):
        return Action()

    def tab_to(self):
        self.morph(new_type=Character)

    def tab_inverse(self):
        self.morph(new_type=SceneHeading)


class SceneHeading(SuggestiveElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def integrate(self):
        screenplay = self.parent.parent
        self.source = screenplay.locations

    def update_selections(self):
        '''Update the list of SceneHeadings in use.'''
        location = self.raw_text
        scene = self.parent
        screenplay = scene.parent
        screenplay.update_locations(new_location=location)

    def next_element(self):
        self.drop_down.dismiss()
        return Action()

    def tab_to(self):
        self.morph(new_type=Action)

    def tab_inverse(self):
        scene_i, elem_i = self.get_location()
        print("<scene, element> = <{scene}, {elem}>".format(scene=scene_i, elem=elem_i))


class Character(SuggestiveElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def integrate(self):
        """Initialization for after Character is added to the widget tree."""
        screenplay = self.parent.parent
        self.source = screenplay.characters

    def update_selections(self):
        character = self.raw_text
        scene = self.parent
        screenplay = scene.parent
        screenplay.update_characters(new_character=character)

    def next_element(self):
        self.drop_down.dismiss()
        return Dialogue()

    def tab_to(self):
        pass

    def tab_inverse(self):
        self.morph(new_type=Action)


class Dialogue(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def next_element(self):
        return Character()

    def tab_to(self):
        self.morph(new_type=Parenthetical)

    def tab_inverse(self):
        self.morph(new_type=Character)


class Parenthetical(Element):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.register_shortcut(  # del
            127, callback=self.on_delete, kill=False)

    def insert_text(self, substring, from_undo=False):
        c_index = self.cursor_index()
        text_len = len(self.text)
        if 0 < c_index < text_len:
            super().insert_text(substring=substring, from_undo=from_undo)
        else:
            return True

    def on_delete(self):
        c_index = self.cursor_index()
        text_len = len(self.text)
        if 0 < c_index < (text_len - 1):
            return False
        else:
            # prevent 'del' from being passed to TextInput
            return True

    def on_backspace(self):
        c_index = self.cursor_index()
        text_len = len(self.text)
        if text_len == 2:
            scene = self.parent
            scene.remove_element(self)

        if 1 < c_index < text_len:
            super().on_backspace()
        else:
            return True

    def next_element(self):
        return Dialogue()

    def tab_to(self):
        pass

    def tab_inverse(self):
        self.morph(new_type=Dialogue)

    def insert_text(self, substring, from_undo=False):
        """Capitalize scene heading."""
        raw_text = self.raw_text
        # The -1 offsets the fact that an opening parenthesis leads
        slice_to = self.cursor_index() - 1
        self.raw_text = raw_text[:slice_to] + substring + raw_text[
                                                          slice_to:]
        # Skip over Element.insert_text
        super(Element, self).insert_text(substring, from_undo=from_undo)

    def cut_text_parenthesis(self):
        return self.text[1: -1]
