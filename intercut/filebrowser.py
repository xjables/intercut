from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty, OptionProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder

import os

Builder.load_file(r'filebrowser.kv')


class DialogPopup(Popup):

    def load(self):
        print('load the damn thing')

    def cancel(self):
        self.dismiss()


class SaveDialog(DialogPopup):

    default_path = StringProperty('')
    default_thing = ObjectProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_selection')
        super().__init__(**kwargs)

    def save(self, path, filename):
        self.dispatch('on_selection', path, filename)
        self.dismiss()

    def on_selection(self, path, filename):
        pass


class LoadDialog(DialogPopup):
    pass
