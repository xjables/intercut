"""Make layouts with background colors."""

from kivy.uix.boxlayout import BoxLayout

from kivy.lang import Builder

Builder.load_file(r'colorpad.kv')


class ColoredBoxLayout(BoxLayout):
    pass
