from kivy.uix.textinput import TextInput
from kivy.core.window import EventLoop

from tools import stringmanip

import textwrap


class CoreInput(TextInput):

    def __init__(self, **kwargs):
        self.raw_text = stringmanip.RawText()
        self.wrap_length = 30
        super(CoreInput, self).__init__(**kwargs)

    def insert_text(self, substring, from_undo=False):
        """
        
        Args:
            substring: 
            from_undo: 

        Returns:

        """
        cc, cr = self.cursor
        sci = self.cursor_index()
        text = self.unwrap(self.text)
        new_text = text[:sci] + substring + text[sci:]
        wrapped = self.get_wrapped(new_text)

        self.text = wrapped
        # super().insert_text(wrapped, from_undo=from_undo)

    def get_wrapped(self, text):
        tmp = textwrap.fill(text, width=self.wrap_length, drop_whitespace=False)
        return textwrap.dedent(tmp)

    def unwrap(self, text):
        return text.replace(' \n', ' ')
