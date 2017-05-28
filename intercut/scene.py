"""Defines the Screenplay container for holding elements.

A Screenplay is just a BoxLayout for carrying the actual Element widgets.

"""

from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
from kivy.lang import Builder

from elements import SuggestiveElement, Parenthetical

Builder.load_file(r'scene.kv')


# TODO: Write a ScreenplayBehavior that captures keyboard shortcuts concerning
# TODO: the creation of elements, etc. ?Mixin with focus behavior?


class Scene(CompoundSelectionBehavior, GridLayout):
    """A collection of dialogue, action, and creative writing!

    A Screenplay object is simply a Kivy layout containing element objects.
    That's it. Take note of the separation of concerns here. Screenplay does
    not bother itself with the details of each element -- how they look, what
    they can do -- but rather handles the aspects of managing their logistics,
    (ie. position, creation)


    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scene_index = 0
        # Selection parameters
        self._select_from_index = 0
        self._select_to_index = 0
        self._select_to_input = None
        self._select_from_input = None

    def align_scene_indices(self):
        for e_index, element in enumerate(self.children):
            element.element_index = e_index

    def add_element(self, source_element, added_element):
        """Add an element to scene.

        Note: added_element is a class, not an instance of the class.

        Args:
            source_element: The element requesting that an element be added.
            added_element: The element object to be inserted.
        """
        # Adding the widget at source_element's location adds it in place
        self.add_widget(added_element, index=source_element.element_index)

        # Some element initialization steps cannot occur until the element knows
        # its place in the widget tree. If you need some of these steps,
        # override Element.integrate
        added_element.integrate()

        added_element.focus = True
        self.parent.parent.scroll_to(added_element)

    def transform_element(self, source_element, new_element):
        self.add_element(source_element, added_element=new_element)

        raw_source = source_element.raw_text

        if isinstance(new_element, SuggestiveElement):
            new_element.drop_down.dismiss()
            new_element.text = raw_source.upper()
        elif isinstance(new_element, Parenthetical):
            new_element.text = self.add_parentesis(raw_source)
            # TODO: Move the cursor to the left.
        else:
            new_element.text = raw_source

        new_element.raw_text = raw_source

        print('displayed:', new_element.text)
        print('raw:', new_element.raw_text)

        self.remove_element(source_element)
        new_element.focus = True
        if isinstance(new_element, Parenthetical):
            new_element.do_cursor_movement('cursor_left')
            ind = new_element.cursor_index()
            cur = new_element.get_cursor_from_index(ind - 1)
            new_element.cursor = cur
        self.parent.parent.scroll_to(new_element)

    def strip_parenthesis(self, string):
        if string.startswith('('):
            string = string[1:]
        if string.endswith(')'):
            string = string[:-1]
        return string

    def add_parentesis(self, string):
        return '(' + string + ')'

    def add_widget(self, widget, **kwargs):
        """Helper for Widget.add_widget() that updates element indices after
        adding new elements to the screenplay.
        """
        widget.bind(on_touch_move=self.left_click_move,
                    on_touch_down=self.left_click_down,
                    on_touch_up=self.left_click_up)
        super().add_widget(widget, **kwargs)
        self.align_scene_indices()

    def remove_element(self, element, **kwargs):
        """Helper function for removing elements from the screenplay.

        """
        new_index = element.element_index

        if isinstance(element, SuggestiveElement):
            element.drop_down.dismiss()

        super().remove_widget(element, **kwargs)
        self.align_scene_indices()
        f_element = self.get_element_by_index(new_index)
        f_element.focus = True

    def split_scene(self):
        """Split a scene at a particular element.
        
        This function splits a scene at the element given to it. That element
        is included in the new scene. Any subsequent elements in the scene are
        also transferred to the new scene.
        
        Args:
            element: The element that will become the first element of the new
                scene.

        Returns:

        """
        screenplay = self.parent
        new_scene = screenplay.add_scene()
        # self.children = self.children[:element.element_index]

    def get_element_by_index(self, element_index):
        return self.children[element_index]

    def left_click_move(self, element, touch):
        """Track final highlighting position across elements.

        The element argument is an instance of the element over which the user
        hovers while dragging their cursor across the screen. Both this and
        the touch object pass to this method update automatically.

        This method determines where to stop the selection by storing both the 
        cursor index and element object on which the touch is released. If the
        selection spans more than one element, <screenplay>.selection_span is
        called to handle highlighting the appropriate interstitial elements.

        Args:
            element: The element object the user is hovering over. Passed by
                event handler.
            touch: Touch object for given input event.
        """
        if element.collide_point(*touch.pos):
            cursor = element.get_cursor_from_xy(*touch.pos)
            self._select_to_index = element.cursor_index(cursor)
            self._select_to_input = element


            if element != self._select_from_input:
            # if element.element_index != self._select_from_input.element_index:
                self.selection_span(element, touch)

    def selection_span(self, element, touch):
        """Track selection across multiple elements.

        This method determines the range between the element initially selected
        and the current element. For each element internal to this range, all
        text is selected. The first and last elements are selected
        appropriately.

        For all of the selections mentioned, <TextInput>.select_text is used to
        select the text for each element.

        Args:
            element: The element object the user is hovering over.
            touch: Touch object for give input event.

        Returns:

        """
        # TODO: Edit this to handle selecting backwards properly.
        element.focus = True
        start = self._select_from_input.element_index
        end = self._select_to_input.element_index
        for element_index in range(end, start + 1):
            if element_index == start:
                self.children[start].select_text(
                    self._select_from_index,
                    self._select_from_input.get_length()
                )
            elif element_index == end:
                self.children[end].select_text(0, self._select_to_index)
            else:
                self.children[element_index].select_all()

    def left_click_down(self, element, touch):
        # All elements see this event, so this clears every element selection
        element.cancel_selection()
        if element.collide_point(*touch.pos):
            element.cancel_selection()
            cursor = element.get_cursor_from_xy(*touch.pos)
            self._select_from_index = element.cursor_index(cursor)
            self._select_from_input = element
            # print("Selecting from (", element.element_index, ",",
            #       self._select_from_index, ")", sep='')

    def left_click_up(self, element, touch):
        # FIXME: Why is this being called twice for certain elements?!!
        self._select_from_index = 0
        self._select_from_input = None

    def get_element_from_index(self, element_index):
        return self.children[element_index]

    def set_focus_by_index(self, element_index):
        element = self.get_element_by_index(element_index=element_index)
        element.focus = True
