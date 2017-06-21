from kivy.core.window import Window
Window.clearcolor = (.2, .2, .2, 1)

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.metrics import inch
from kivy.uix.label import Label
from kivy.core.window import Window

import os
import json

from screenplay import Screenplay, ScrollingScreenplay
from filebrowser import SaveDialog, LoadDialog
from elementbehavior import ElementBehavior

Builder.load_file(r'intercut.kv')


class MyTabbedPanel(TabbedPanel):
    pass


class ViewManager(MyTabbedPanel):

    def sp_border_width(self, border_w):
        """Modify the Screenplay borders such that they only appear if the Screenplay doesn't fill the screen.

        Args:
            border_w:
                Width to be applied to each screenplay border.
        """

        for item in self.default_tab_content.children[:]:
            if isinstance(item, Label):
                if border_w > 0:
                    item.width = border_w/2
                else:
                    item.width = 0

    def get_screenplay(self):
        layout = self.default_tab_content
        for item in layout.children[:]:
            if isinstance(item, ScrollingScreenplay):
                return item.children[0]


class ScreenplayManager(ElementBehavior, MyTabbedPanel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # We are binding to Window.on_resize instead of using
        # self.bind(size=self.sp_border_width) because the latter does not
        #  catch maximize and minimize events for some reason, even though
        # the content is resized.
        Window.bind(on_resize=self.adjust_sp_widths, on_key_down=self.on_key_down)

    def adjust_sp_widths(self, window, width, height):
        """Adjust the Screenplay borders for ALL open screenplays.

        The current window is used to calculate borders for all screenplays because when a screenplay tab is not open,
        it's content size is not adjusted with window, so we cannot use its values for calculation.

        Args:
            window: Instance of the application Window.
            width: Width of the window.
            height: Height of the window.
        """
        current_view = self.current_tab.content
        cont_w = current_view.content.width
        sp_w = inch(8.5)
        border_w = cont_w - sp_w

        screenplay_tabs = self.tab_list

        for tab in screenplay_tabs:
            view_manager = tab.content
            view_manager.sp_border_width(border_w=border_w)

    def save_screenplay(self, location=None):
        screenplay = self.get_screenplay()
        json_string = screenplay.get_json()
        save_to = screenplay.save_to
        save_path = os.path.dirname(save_to)

        if screenplay.save_to and (os.path.isfile(save_to) or os.path.isdir(save_path)):
            with open(save_to, 'w') as sp_file:
                print('writing:\n', json_string)
                sp_file.write(json_string)
        else:
            file_dialog = SaveDialog(on_selection=self.update_save_location,
                                     default_path=os.path.expanduser('~'))

            file_dialog.open()

    def update_save_location(self, instance, path, filename):
        """Update screenplay save location and write to file.

        Note: This is automatically called when SaveDialog is completed.

        Args:
            instance:
            path: (str) Path to selected in file dialog.
            filename: File name selected in file dialog.
        """
        screenplay = self.get_screenplay()
        screenplay.save_to = os.path.join(path, filename)
        self.save_screenplay()

    def get_screenplay(self):
        current_view = self.current_tab.content
        return current_view.get_screenplay()

    def new_screenplay(self):
        sp_view = ViewManager()
        screenplay = sp_view.get_screenplay()
        tab_header = TabbedPanelHeader(text=screenplay.title)
        tab_header.content = sp_view
        self.add_widget(tab_header)
        self.switch_to(header=tab_header)
        return screenplay

    def load_from_file(self):
        file_dialog = LoadDialog(on_selection=self.fill_screenplay,
                                 default_path=os.path.expanduser('~'))
        file_dialog.open()

    def fill_screenplay(self, instance, path, filename):
        screenplay = self.new_screenplay()
        screenplay.clear_widgets()
        print('children', screenplay.children[:])
        open_file = os.path.join(path, filename)
        with open(open_file, 'r') as stream:
            json_string = stream.read()
        json_dict = json.loads(json_string)
        print('children', screenplay.children[:])
        screenplay.load_from_json(json_dict=json_dict)
        print('children', screenplay.children[:])

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if len(modifiers) == 1:
            if modifiers[0] == 'ctrl':
                if key == 115:  # 'ctrl' + s
                    self.save_screenplay()
                if key == 110:  # 'ctrl' + n
                    self.new_screenplay()
                if key == 111:  # 'ctrl' + o
                    self.load_from_file()


class InterXut(App):

    def build(self):
        self.title = "InterXut"
        spm = ScreenplayManager()
        spm._tab_strip.padding = [40, 0, 0, 0]
        print(spm._tab_strip.padding)
        return spm


if __name__ == '__main__':
    InterXut().run()
