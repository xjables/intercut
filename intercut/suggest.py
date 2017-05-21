from kivy.uix.dropdown import DropDown
from kivy.properties import BooleanProperty



class DropSuggestion(DropDown):

    is_open = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_dismiss(self):
        self.is_open = False

    def open(self, widget):
        super().open(widget)
        self.is_open = True