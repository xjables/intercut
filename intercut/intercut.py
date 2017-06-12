from kivy.core.window import Window
Window.clearcolor = (.2, .2, .2, 1)


from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder

from screenplay import Screenplay

Builder.load_file(r'intercut.kv')


class ViewManager(TabbedPanel):
    pass


class ScreenplayManager(TabbedPanel):
    pass


class InterXut(App):

    def build(self):
        self.title = "InterXut"
        spm = ScreenplayManager()
        spm._tab_strip.padding = [40,0,0,0]
        print(spm._tab_strip.padding)
        return spm


if __name__ == '__main__':
    InterXut().run()
