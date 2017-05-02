

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView

from screenplay import Screenplay
from colorpad import ColoredBoxLayout

Builder.load_string('''
<ScrollableLabel>:
    bar_width: 10
    # scroll_timeout being 0 prevents touch scrolling and sends touch controls
    # directly to the children
    scroll_timeout: 0
    Screenplay:
''')

class ScrollableLabel(ScrollView):
    pass



class MyApp(App):

    def build(self):
        return ScrollableLabel()


if __name__ == '__main__':
    MyApp().run()
