

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
