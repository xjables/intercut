# -*- encoding: utf-8 -*-

"""
Adds keyboard shortcut

Allows for a default text feature.
"""


from kivy.properties import StringProperty, NumericProperty


__all__ = ('ModBehavior', )


class ModBehavior(object):

    """For modifying the behavior of TextInput"""

    key_bindings = StringProperty('mods')


    def __init__(self, **kwargs):
        super(ModBehavior, self).__init__(**kwargs)

        self.bindings = {
            'ctrl': {
                '8': self.delete_word_left,   # ctrl + backspace
                '127': self.delete_word_right,  # ctrl + del
            },
            'alt': {
                '97': self.transform,  # alt + 'a'
            },
        }

    # Keyboard Shortcut callbacks defined below
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # TODO: rewrite this to allow for callbacks with arguments
        key, key_str = keycode
        # Get modified or None
        mod = modifiers[0] if modifiers else None
        is_mods_shortcut = False

        if key == 8 and self.element_index == 'scene':
            if mod == 'ctrl':
                self.on_backspace(modifier=mod)
            else:
                self.on_backspace()


        if mod and key in range(256):
            is_mods_shortcut = ((mod == 'ctrl' and
                                  key in list(map(int,self.bindings['ctrl'].keys())))or
                                 (mod == 'alt' and
                                  str(key) in self.bindings['alt'].keys()))
        if is_mods_shortcut:
            # Look up mod and key
            mods_shortcut = self.bindings[mod][str(key)]
            mods_shortcut()
        else:
            # If no shortcut matche, pass control on to standard TextInput
            # to try to match shortcuts.
            super(ModBehavior, self).keyboard_on_key_down(window, keycode,
                                                            text, modifiers)

    def set_focus_index(self):
        self.last_focus_index = self.index
        print(last_focus_index)

    def delete_word_right(self):
        '''Delete text right of the cursor to the end of the word'''
        if self._selection:
            return
        start_index = self.cursor_index()
        start_cursor = self.cursor
        self.do_cursor_movement('cursor_right', control=True)
        end_index = self.cursor_index()
        if start_index != end_index:
            s = self.text[start_index:end_index]
            self._set_unredo_delsel(start_index, end_index, s, from_undo=False)
            self.text = self.text[:start_index] + self.text[end_index:]
            self._set_cursor(pos=start_cursor)

    def delete_word_left(self):
        '''Delete text left of the cursor to the beginning of word'''
        if self._selection:
            return
        start_index = self.cursor_index()
        self.do_cursor_movement('cursor_left', control=True)
        end_cursor = self.cursor
        end_index = self.cursor_index()
        if start_index != end_index:
            s = self.text[end_index:start_index]
            self._set_unredo_delsel(end_index, start_index, s, from_undo=False)
            self.text = self.text[:end_index] + self.text[start_index:]
            self._set_cursor(pos=end_cursor)
