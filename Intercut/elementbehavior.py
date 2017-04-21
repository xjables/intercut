# -*- encoding: utf-8 -*-

"""
Adds keyboard shortcut

Allows for a default text feature.
"""


from kivy.properties import StringProperty, NumericProperty


__all__ = ('ElementBehavior', )


class ElementBehavior(object):

    """For modifying the behavior of TextInput"""

    key_bindings = StringProperty('mods')


    def __init__(self, **kwargs):
        super(ElementBehavior, self).__init__(**kwargs)

        self.bindings = {
            # Registered shortcuts will take the form str(keycode): callback
            # inside one of the following sub dictionaries
            'ctrl': {},
            'alt': {},
            '': {},
        }

    def register_shortcut(self, keycode, callback, modifier=None, pass_signal=False):
        """Register a text input shortcut.

        Use register_shortcut in the class __init__.

        Note: If you register a shortcut in parent class and you want a child
            to overwrite it, make sure to reregister the shortcut in the child
            class __init__ AFTER you have called the parent initializer. To
            remove the parent class registration, use the revoke_shortcut
            method.

        Args:
            keycode (int): The ascii key code for the key to be captured.
            modifier (string): 'ctrl' or 'alt' or None.
            callback (function object): The function to run on key shortcut capture.
            pass_signal (bool): Bool indicating whether or not the key code
                should also be passed on to the TextInput widget to add its
                default behavior.
        """
        modifier = modifier if modifier else ''
        try:
            self.bindings[modifier][str(keycode)] = callback
        except KeyError as err:
            print("KeyError:", err)

    def print_bindings(self):
        print(self.bindings)


    # Keyboard Shortcut callbacks defined below
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # TODO: rewrite this to allow for callbacks with arguments
        key, key_str = keycode
        # Get modified or None
        mod = modifiers[0]
        is_mods_shortcut = False

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
            super(ElementBehavior, self).keyboard_on_key_down(window, keycode,
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
