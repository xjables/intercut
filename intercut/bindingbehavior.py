# -*- encoding: utf-8 -*-

"""
Adds keyboard shortcut

Allows for a default text feature.
"""


from kivy.properties import StringProperty, NumericProperty


__all__ = ('BindingBehavior',)


class BindingBehavior(object):

    """For modifying the behavior of TextInput"""

    key_bindings = StringProperty('mods')

    def __init__(self, **kwargs):
        super(BindingBehavior, self).__init__(**kwargs)

        self.bindings = {
            # Registered shortcuts will take the form str(keycode): callback
            # inside one of the following sub dictionaries
            'ctrl': {},
            'alt': {},
        }

        # Register special keys by setting modifier to None in
        # register_shortcut
        self.special_keys = {}

    def register_shortcut(self, keycode, callback, modifier=None):
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
        """
        if modifier:
            try:
                self.bindings[modifier][str(keycode)] = callback
            except KeyError as err:
                raise err

        else:
            try:
                self.special_keys[str(keycode)] = callback
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
            key_callback = self.special_keys[str(key)]
            key_callback()
            super(BindingBehavior, self).keyboard_on_key_down(window, keycode,
                                                              text, modifiers)
            return True

        if is_element_shortcut:
            # Get callback from bindings and run it.
            shortcut_callback = self.bindings[mod][str(key)]
            shortcut_callback()
            return True
        else:
            # If no shortcut matches, pass control on to standard TextInput
            # to try to match shortcuts.
            super(BindingBehavior, self).keyboard_on_key_down(window, keycode,
                                                              text, modifiers)
