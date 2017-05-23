from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
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

    def move_highlight(self, increment=None):

        options = self.container.children

        if not (self.is_open and options):
            return

        if increment is None:
            self.set_highlight()
            return

        for index, option in enumerate(options):
            if option.highlighted:
                try:
                    # Because kivy widget tree is reverse indexed, a minus.
                    self.set_highlight(options[index - increment])
                    return
                except IndexError:
                    self.set_highlight(button=option)
                    return

    def set_highlight(self, button=None):
        """Highlight button and clear highlight from all other buttons.
        
        If no button is passed, the top button will be highlighted.
        """
        options = self.container.children

        if not (self.is_open and options):
            return

        if button is None:
            button = options[-1]

        for option in options:
            if button is option:
                option.highlighted = True
            else:
                option.highlighted = False

    def get_selection_text(self):
        options = self.container.children

        for option in options:
            if option.highlighted:
                return option.text
        return ''


class SuggestionButton(Button):

    highlighted = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # TODO: Move these args to a .kv file
        # self.background_normal = ''
        self.size_hint_y = None
        self.height = 30

        self.focus_color = [1, 0, 0, 1]
        self.unfocus_color = [1, 1, 1, 1]

    def on_highlighted(self, instance, value):
        """Change the button color appropriately when highlighting changes."""
        if value:
            self.background_color = self.focus_color
        else:
            self.background_color = self.unfocus_color
