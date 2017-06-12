from kivy.core.window import Window
Window.clearcolor = (.2, .2, .2, 1)


from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelContent
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.metrics import inch
from kivy.uix.label import Label

from screenplay import Screenplay

Builder.load_file(r'intercut.kv')


class MyTabbedPanel(TabbedPanel):
    pass


class ViewManager(MyTabbedPanel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # We are binding to Window.on_resize instead of using self.bind(size=self.sp_border_width) because the latter
        # does not catch maximize and minimize events for some reason, even though the content is resized.
        Window.bind(on_resize=self.sp_border_width)

    def sp_border_width(self, window, width, height):
        """Modify the Screenplay borders such that they only appear if the Screenplay doesn't fill the screen.

        Args:
            window: Instance of the application window
            width: Width of the window
            height: Height of the window
        """
        cont_w = self.content.width
        sp_w = inch(8.5)
        border_w = cont_w - sp_w

        # Find labels in default tab (Screenplay) and resize them
        for item in self.default_tab_content.children[:]:
            if isinstance(item, Label):
                if border_w > 0:
                    item.width = border_w/2
                else:
                    item.width = 0


class ScreenplayManager(MyTabbedPanel):
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
