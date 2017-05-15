from kivy.uix.textinput import TextInput
from kivy.core.window import EventLoop

from tools import stringmanip

import textwrap

FL_IS_LINEBREAK = 0x01
FL_IS_WORDBREAK = 0x02
FL_IS_NEWLINE = FL_IS_LINEBREAK | FL_IS_WORDBREAK

class CoreInput(TextInput):



    def __init__(self, **kwargs):
        self.raw_text = stringmanip.RawText()
        self.wrap_length = 30
        super(CoreInput, self).__init__(**kwargs)

    def insert_text(self, substring, from_undo=False):
        '''Insert new text at the current cursor position. Override this
        function in order to pre-process text for input validation.
        '''
        if self.readonly or not substring or not self._lines:
            return

        if isinstance(substring, bytes):
            substring = substring.decode('utf8')

        if self.replace_crlf:
            substring = substring.replace(u'\r\n', u'\n')

        mode = self.input_filter
        if mode is not None:
            chr = type(substring)
            if chr is bytes:
                int_pat = self._insert_int_patb
            else:
                int_pat = self._insert_int_patu

            if mode == 'int':
                substring = re.sub(int_pat, chr(''), substring)
            elif mode == 'float':
                if '.' in self.text:
                    substring = re.sub(int_pat, chr(''), substring)
                else:
                    substring = '.'.join([re.sub(int_pat, chr(''), k) for k
                                          in substring.split(chr('.'), 1)])
            else:
                substring = mode(substring, from_undo)
            if not substring:
                return

        self._hide_handles(EventLoop.window)

        if not from_undo and self.multiline and self.auto_indent \
                and substring == u'\n':
            substring = self._auto_indent(substring)

        cc, cr = self.cursor
        sci = self.cursor_index
        ci = sci()
        text = self._lines[cr]
        len_str = len(substring)
        new_text = text[:cc] + substring + text[cc:]
        self._set_line_text(cr, new_text)

        start, finish, lines, \
            lineflags, len_lines = self._get_line_from_cursor(cr, new_text)
        # calling trigger here could lead to wrong cursor positioning
        # and repeating of text when keys are added rapidly in a automated
        # fashion. From Android Keyboard for example.
        self._refresh_text_from_property('insert', start, finish, lines,
                                             lineflags, len_lines)

        self.cursor = self.get_cursor_from_index(ci + len_str)
        # handle undo and redo
        self._set_unredo_insert(ci, ci + len_str, substring, from_undo)

    def _split_smart(self, text):
        # Do a "smart" split. If autowidth or autosize is set,
        # we are not doing smart split, just a split on line break.
        # Otherwise, we are trying to split as soon as possible, to prevent
        # overflow on the widget.

        # depend of the options, split the text on line, or word
        if not self.multiline:
            lines = text.split(u'\n')
            lines_flags = [0] + [FL_IS_LINEBREAK] * (len(lines) - 1)
            return lines, lines_flags

        # no autosize, do wordwrap.
        x = flags = 0
        line = []
        lines = []
        lines_flags = []
        _join = u''.join
        lines_append, lines_flags_append = lines.append, lines_flags.append
        width = self.wrap_length

        # try to add each word on current line.
        for word in self._tokenize(text):
            is_newline = (word == u'\n')
            w = len(word)
            # if we have more than the width, or if it's a newline,
            # push the current line, and create a new one
            if (x + w > width and line) or is_newline:
                lines_append(_join(line))
                lines_flags_append(flags)
                flags = 0
                line = []
                x = 0
            if is_newline:
                flags |= FL_IS_LINEBREAK
            elif w > width:
                while w > width:
                    split_width = split_pos = 0
                    # split the word
                    for c in word:
                        cw = len(c)
                        if split_width + cw > width:
                            break
                        split_width += cw
                        split_pos += 1
                    if split_width == split_pos == 0:
                        # can't fit the word in, give up
                        break
                    lines_append(word[:split_pos])
                    lines_flags_append(flags)
                    flags = FL_IS_WORDBREAK
                    word = word[split_pos:]
                    w -= split_width
                x = w
                line.append(word)
            else:
                x += w
                line.append(word)
        if line or flags & FL_IS_LINEBREAK:
            lines_append(_join(line))
            lines_flags_append(flags)
        return lines, lines_flags









