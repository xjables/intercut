

def remove_last_word(string):
    """Return input string without the last word.
    
    Does not remove trailing whitespace character. A "word" is a collection of
    characters without spaces.

    Args:
        string (str): A string.
    """
    if " " not in string:
        return ""
    else:
        partition = string.rpartition(" ")
        return partition[0] + " "


class UnformattedText:
    """Hold and modify unformatted text for Text Inputs.

    This should be implemented as an attribute in subclasses of TextInput in
    which the insert_text function has been overridden to insert capitalized
    text in place (i.e. Scenes, Characters).  This class will hold a copy of 
    the text without the formatting associated with the insert_text override.

    For example, if you type "Int. House -- Night" into a Scene object, it will
    be displayed in all caps.  But via the UnformattedText object, we can
    preserve the user input as quoted above.

    This is useful because suppose the user is not paying attention and starts
    typing some action text into a Scene object.  Without this tool, when they
    try to copy and paste their text or convert the element into an Action 
    object, the text will be transferred over complete with capitalization.
    However, by holding onto this unformatted copy of the text, the user can 
    transfer the text they originally typed.

    Note:
        The actual tracking is not done for you. You need call the
        resolve_deletion method on your UnformattedText object every time text 
        is deleted. Testing needs to be done to determine whether this should
        be done in the on_text callback or the on_backspace callback.  It needs
        to be added to whichever one is called first.


    """

    def __init__(self, text=''):
        self.text = text

    # TODO: Add resolve_addition function or modify the resolve_deletion for
    # tracking additive_changes.

    def resolve_deletion(self, input_text):
        """Adjusts UnformattedText.text to follow deletions in TextInput.text

        Args:
            input_text: Text accessed from the TextInput.

        Returns:

        """

        input_len = len(input_text)
        unform_len = len(self.text)
        # cut_len is length of the word removed from the input
        assert unform_len >= input_len

        cut_len = unform_len - input_len

        # The text was not changed
        if cut_len == 0:
            return

        # All text removed
        if input_len == 0:
            self.text = ''
            return

        slice_to = input_len
        for i in range(input_len):
            if self.text[i].upper() != input_text[i]:
                slice_to = i
                break

        self.text = self.text[:slice_to] \
                    + self.text[(slice_to + cut_len):]
