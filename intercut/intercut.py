
from kivy.app import App

from screenplay import ScrollingScreenplay


class MyApp(App):

    def build(self):
        self.title = "InterXut"
        return ScrollingScreenplay()


if __name__ == '__main__':
    MyApp().run()
