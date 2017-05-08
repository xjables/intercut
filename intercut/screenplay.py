"""Defines the Screenplay container for holding elements.

A Screenplay is just a BoxLayout for carrying the actual Element widgets.

"""

from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
from kivy.lang import Builder

from scene import Scene

Builder.load_file(r'screenplay.kv')

# TODO: Write a ScreenplayBehavior that captures keyboard shortcuts concerning
# TODO: the creation of elements, etc. ?Mixin with focus behavior?


class Screenplay(CompoundSelectionBehavior, GridLayout):

    """A collection of dialogue, action, and creative writing!
    
    A Screenplay object is simply a Kivy layout containing element objects.
    That's it. Take note of the separation of concerns here. Screenplay does
    not bother itself with the details of each element -- how they look, what
    they can do -- but rather handles the aspects of managing their logistics,
    (ie. position, creation)
    
    
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_scene(self, source_element):
        """Add an element to screenplay.

        Note: added_element is a class, not an instance of the class.

        Args:
            source_element: The element requesting that an be added.
        """
        new_scene = Scene()
        # Adding the widget at source_element's location adds it in place
        self.add_widget(new_scene, index=source_element.parent.scene_index)

    def add_widget(self, widget, **kwargs):
        """Helper for Widget.add_widget() that updates element indices after
        adding new elements to the screenplay.
        """
        # widget.bind(on_touch_move=self.left_click_move,
        #             on_touch_down=self.left_click_down,
        #             on_touch_up=self.left_click_up)
        super().add_widget(widget, **kwargs)
        # self._align_indices()

    def remove_widget(self, widget, **kwargs):
        # FIXME: It probably shouldn't be possible to delete an entire scene.
        """Helper function for removing elements from the screenplay.
        
        """
        super().remove_widget(widget, **kwargs)
        # self._align_indices()

    def _align_indices(self):
        """Align the indices of the Screenplay.children and the their own
        element_index property.

        This should be called anytime the ordering of the Screenplay elements
        changes.
        """
        absolute_index = 0
        for scene in self.children:
            for element in scene.children:
                element.element_index = absolute_index
                absolute_index += 1