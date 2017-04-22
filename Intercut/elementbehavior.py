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
        }

    def register_shortcut(self, keycode, callback, modifier):
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
        try:
            self.bindings[modifier][str(keycode)] = callback
        except KeyError as err:
            raise err

    def revoke_shortcut(self, keycode, modifier):
        """Remove shortcut from bindings.

        Args:
            keycode (int): The ascii key code for the key to be captured.
            modifier (string): 'ctrl' or 'alt' or None.
        """
        try:
            del self.bindings[modifier][str(keycode)]
        except KeyError as err:
            print("KeyError:", err)

    def print_bindings(self):
        print(self.bindings)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # This function is called on key_down event. This is where control is
        # passed to the behavior.
        key, key_str = keycode
        mod = modifiers[0] if modifiers else None
        is_element_shortcut = False

        # Once this is proven to work, you can remove the latter condition to
        # extend its use to all unicode character shortcuts
        if mod in ('alt', 'ctrl') and key in range(256):
            is_element_shortcut = str(key) in self.bindings[mod]

        if is_element_shortcut:
            # Get callback from bindings and run it.
            shortcut_callback = self.bindings[mod][str(key)]
            shortcut_callback()
        else:
            # If no shortcut matches, pass control on to standard TextInput
            # to try to match shortcuts.
            super(ElementBehavior, self).keyboard_on_key_down(window, keycode,
                                                              text, modifiers)

    def delete_word_right(self):
        """Delete text right of the cursor to the end of the word."""
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
        """Delete text left of the cursor to the beginning of word."""
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
