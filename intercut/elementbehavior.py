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

        # Register special keys by setting modifier to None in
        # register_shortcut
        self.special_keys = {}

    def register_shortcut(self, keycode, callback, modifier=None, kill=True):
        """Register a text input shortcut.

        Use register_shortcut in the class __init__.

        Note: If you register a shortcut in parent class and you want a child
            to overwrite it, make sure to reregister the shortcut in the child
            class __init__ AFTER you have called the parent initializer. To
            remove the parent class registration, use the revoke_shortcut
            method.

        Args:
            keycode (int): The ascii key code for the key to be captured.
            modifier (string): 'ctrl' or 'alt' or None. If the modifier is
                None, the shortcut is tied to a particular key press without
                modifiers.
            callback (function object): The function to run on key shortcut
                capture.
            kill (bool): Kill the signal after use or pass it to TextInput.
        """
        if modifier:
            try:
                self.bindings[modifier][str(keycode)] = (callback, kill)
            except KeyError as err:
                raise err

        else:
            try:
                self.special_keys[str(keycode)] = (callback, kill)
            except KeyError as err:
                raise err

    def revoke_shortcut(self, keycode, modifier):
        """Remove shortcut from bindings.

        Args:
            keycode (int): The ascii key code for the key to be captured.
            modifier (string): 'ctrl' or 'alt' or None.
        """
        if modifier:
            try:
                del self.bindings[modifier][str(keycode)]
            except KeyError as err:
                print("KeyError:", err)

        else:
            try:
                del self.special_keys[str(keycode)]
            except KeyError as err:
                print("KeyError:", err)

    def print_bindings(self):
        print(self.bindings)

    def print_special(self):
        print(self.special_keys)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # TODO: This function needs to be refactored.
        # This function is called on key_down event. This is where control is
        # passed to the behavior.
        key, key_str = keycode
        is_special_key = (not modifiers) and (str(key) in self.special_keys)

        mod = modifiers[0] if modifiers else None
        if mod in ('alt', 'ctrl'):
            is_element_shortcut = str(key) in self.bindings[mod]
        else:
            is_element_shortcut = False

        # Only one of the blocks below should be triggers.
        if is_element_shortcut:
            assert not is_special_key

        if is_special_key:
            key_callback, kill = self.special_keys[str(key)]
            key_callback()
            if kill:
                return kill

        if is_element_shortcut:
            # Get callback from bindings and run it.
            shortcut_callback, kill = self.bindings[mod][str(key)]
            shortcut_callback()
            if kill:
                return kill
        else:
            # If no shortcut matches, pass control on to standard TextInput
            # to try to match shortcuts.
            super(ElementBehavior, self).keyboard_on_key_down(window, keycode,
                                                              text, modifiers)

    def delete_word_right(self):
        """Delete text right of the cursor to the end of the word."""
        if self._selection:
            self.delete_selection()
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
            self.delete_selection()
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
