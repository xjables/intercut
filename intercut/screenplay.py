"""Defines the Screenplay container for holding elements.

A Screenplay is just a BoxLayout for carrying the actual Element widgets.

"""
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
from kivy.lang import Builder

from scene import Scene
from elements import Character, SceneHeading

import json
from collections import OrderedDict

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
        self.characters = []
        self.locations = []
        self.title = 'Untitled'
        self.author = 'Anonymous'
        self.phone = ''
        self.email = ''
        self.version = ''
        self.save_to = ''
        super().__init__(**kwargs)

    def add_scene(self):
        """Add an element to screenplay.

        Note: added_element is a class, not an instance of the class.

        Args:
            calling_scene: The scene in which a new scene heading was created.
        """
        new_scene = Scene()
        self.add_widget(new_scene)

        return new_scene

    def add_widget(self, widget, **kwargs):
        """Helper for Widget.add_widget() that updates element indices after
        adding new elements to the screenplay.
        """
        super().add_widget(widget, **kwargs)
        # self.align_all_indices()

    def remove_widget(self, widget, **kwargs):
        # FIXME: It probably shouldn't be possible to delete an entire scene.
        """Helper function for removing elements from the screenplay.
        
        """
        super().remove_widget(widget, **kwargs)
        # self.align_all_indices()

    def align_all_indices(self):
        """Align the indices of the Screenplay.children and the their own
        element_index property.

        This should be called anytime the ordering of the Screenplay elements
        changes.
        """
        for s_index, scene in enumerate(self.children):
            scene.scene_index = s_index
            scene.align_scene_indices()

    def update_characters(self, new_character):
        if new_character:
            character = new_character.strip()
            lower_character = character.lower()
            lower_characters = [char.lower() for char in self.characters]
            if lower_character in lower_characters:
                return
            else:
                self.characters.append(character)

    def update_locations(self, new_location):
        if new_location:
            location = new_location.strip()
            lower_loc = location.lower()
            lower_locs = [scn.lower() for scn in self.locations]
            if lower_loc in lower_locs:
                return
            else:
                self.locations.append(location)
            print(self.locations)

    def get_json(self):
        json_dict = OrderedDict()
        json_dict['title'] = self.title
        json_dict['author'] = self.author
        json_dict['phone'] = self.phone
        json_dict['email'] = self.email
        json_dict['locations'] = self.locations
        json_dict['characters'] = self.characters
        json_dict['version'] = self.version
        json_dict['save_to'] = self.save_to

        json_dict['scenes'] = []

        for scene in self.children[:]:
            json_dict['scenes'].append(scene.get_json())

        return json.dumps(json_dict, indent=4)



class ScrollingScreenplay(ScrollView):
    pass
