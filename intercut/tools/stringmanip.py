

def remove_last_word(string):
    """Return input string without the last word.
    
    Does not remove trailing whitespace character. A "word" is a collection of
    characters without spaces.

    Args:
        string (str): A string.
    """
    # TODO: Below is hackey. Do it properly.
    return string[::-1].split(' ', 1)[1][::-1] + ' '
