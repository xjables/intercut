"""Defines the Screenplay container for holding elements.

A Screenplay is just a BoxLayout for carrying the actual Element widgets.

"""

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from elements import Action, Scene, Character, Dialogue

Builder.load_file(r'screenplay.kv')

class Screenplay(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.elements = []

    def add_action(self, index=0):
        # For some reason the focus functionality hangs when written as:
        # self.add_widget(Action(focus=True))
        action = Action()
        action.focus = True
        self.add_widget(action, index=index)

    def add_scene(self, index=0):
        scene = Scene()
        scene.focus = True
        self.add_widget(scene, index=index)

    def add_character(self, index=0):
        """Add Character element to screenplay.

        Args:
            index (int, optional): Default to 0.
        """
        character = Character()
        character.focus = True
        self.add_widget(character, index=index)

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
