#####################################################################################################

import bisect

#####################################################################################################

from pygments.lexers import get_lexer_for_filename
from pygments import lex

#####################################################################################################

class HighlightedItem(object):

    ###############################################

    def __init__(self, token, text):

        self.token = token
        self.text = text

    ###############################################

    def __getitem__(self, item_slice):

        return self.__class__(self.token, self.text[item_slice])

    ###############################################

    def __len__(self):

        return len(self.text)

    ###############################################

    def __repr__(self):

        return str((self.token, self.text))

    ###############################################

    def __str__(self):

        return self.text

#####################################################################################################

class HighlightedLine(list):

    ###############################################

    def __init__(self):

        super(HighlightedLine, self).__init__()

        self._accumulated_lengths = None

    ###############################################

    def __str__(self):

        return ''.join([str(x) for x in self])

    ###############################################

    def _init_bisect(self):

        accumulator = 0
        self._accumulated_lengths = []
        for item in self:
            accumulator += len(item)
            self._accumulated_lengths.append(accumulator)

    ###############################################

    def _bisect(self, i):

        return bisect.bisect(self._accumulated_lengths, i)

    ###############################################

    def _right_index(self, i):

        if i:
            return self._accumulated_lengths[i -1]
        else:
            return 0

    ###############################################

    def get_line_slice(self, line_slice):

        if self._accumulated_lengths is None:
            self._init_bisect()

        lower_line_slice_index = line_slice.start
        upper_line_slice_index = line_slice.stop -1

        lower_item_index = self._bisect(lower_line_slice_index)
        upper_item_index = self._bisect(upper_line_slice_index)

        lower_item_start = lower_line_slice_index - self._right_index(lower_item_index)
        upper_item_stop = upper_line_slice_index - self._right_index(upper_item_index) +1

        highlighted_line = HighlightedLine()

        print '>', [(i, repr(x)) for i, x in enumerate(self)]
        print '> bisect', self._accumulated_lengths
        print '> line slice', lower_line_slice_index, upper_line_slice_index
        print '> item index', lower_item_index, upper_item_index
        print '>', lower_item_start, upper_item_stop

        if lower_item_index == upper_item_index:
            item = self[lower_item_index]
            highlighted_line.append(item[lower_item_start:upper_item_stop])
        else:
            item = self[lower_item_index]
            highlighted_line.append(item[lower_item_start:])

            for item in self[lower_item_index +1:upper_item_index]:
                highlighted_line.append(item)

            item = self[upper_item_index]
            highlighted_line.append(item[:upper_item_stop])
        
        return highlighted_line

#####################################################################################################

class HighlightedText(list):

    ###############################################

    def __init__(self, lexer, text_buffer):

        current_line = HighlightedLine()
        for token, text in lex(text_buffer, lexer):
            current_line.append(HighlightedItem(token, text))
            if str(token) == 'Token.Text' and text == '\n':
                self.append(current_line)
                current_line = HighlightedLine()

#####################################################################################################
#
# End
#
#####################################################################################################
