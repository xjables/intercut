"""Defines the Screenplay container for holding elements.

A Screenplay is just a BoxLayout for carrying the actual Element widgets.

"""

from kivy.uix.gridlayout import GridLayout
from colorpad import ColoredBoxLayout
from kivy.lang import Builder

from elements import Action, Scene, Character, Dialogue

Builder.load_file(r'screenplay.kv')

class Screenplay(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_move(self, touch):
        """Return False to pass moving touch directly to children (Elements)"""
        return False

    def add_element(self, source_element, added_element=Action):
        """Add an element to screenplay.

        Note: added_element is a class, not an instance of the class.

        Args:
            source_element: The element requesting that an element be added.
            added_element: The element object to be inserted.
        """
        element = added_element()
        element.focus = True
        # Adding the widget at source_element's location adds it in place
        self.add_widget(element, index=source_element.element_index)
        self.parent.scroll_to(element)

    def add_widget(self, widget, **kwargs):
        """Wrapper for Widget.add_widget() that updates element indicies after
        adding new elements to the screenplay.
        """
        super().add_widget(widget, **kwargs)
        self._align_indicies()

    def _align_indicies(self):
        """Align the indicies of the Screenplay.children and the their own
        element_index property.

        This should be called anytime the ordering of the Screeplay elements
        changes.
        """
        for i, child in enumerate(self.children):
            child.element_index = i
