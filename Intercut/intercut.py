

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from screenplay import Screenplay
from colorpad import ColoredBoxLayout

Builder.load_string('''
<ColoredBoxLayout>:
    Screenplay:
''')

class MyApp(App):

    def build(self):
        box = BoxLayout(orientation='vertical')
        box.add_widget(ColoredBoxLayout())
        return box


if __name__ == '__main__':
    MyApp().run()
