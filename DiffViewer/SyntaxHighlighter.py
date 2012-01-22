#####################################################################################################

import bisect
import pygments

#####################################################################################################

class HighlightedItem(object):

    # How to subclass unicode ?

    ###############################################

    def __init__(self, token, text):

        self.token = token
        self.text = unicode(text)

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

    def __unicode__(self):

        return self.text

#####################################################################################################

class HighlightedLine(list):

    ###############################################

    def __init__(self):

        super(HighlightedLine, self).__init__()

        # _accumulated_lengths[i-1] gives the lower index of the item i
        self._accumulated_lengths = None

    ###############################################

    def __unicode__(self):

        return u''.join([unicode(x) for x in self])

    ###############################################

    def _init_bisect(self):

        # Fill _accumulated_lengths with
        #   [len(item_0), len(item_0 + item_1), ...]
        accumulator = 0
        self._accumulated_lengths = []
        for item in self:
            accumulator += len(item)
            self._accumulated_lengths.append(accumulator)

    ###############################################

    def _bisect(self, i):

        # Return the index j where i < _accumulated_lengths[j], since _accumulated_lengths[j]
        # corresponds to the lower index of the item j+1, thus j corresponds to the item that
        # include the location i.
        return bisect.bisect_right(self._accumulated_lengths, i)

    ###############################################

    def _item_lower_index(self, i):

        """ Return the item lower index.
        """

        if i:
            return self._accumulated_lengths[i -1]
        else:
            return 0

    ###############################################

    def get_line_slice(self, line_slice):

        """ Return the line subset corresponding to the line slice given by the parameter
        *line_slice*.
        """

        highlighted_line = HighlightedLine()
        if line_slice.start == line_slice.stop:
            return highlighted_line

        if self._accumulated_lengths is None:
            self._init_bisect()

        # Define line slice inclusive index
        lower_line_index = line_slice.start
        upper_line_slice_index = line_slice.stop -1

        # Define item slice inclusive index
        lower_item_index = self._bisect(lower_line_index)
        upper_item_index = self._bisect(upper_line_slice_index)

        # Define lower item start index
        lower_item_start = lower_line_index - self._item_lower_index(lower_item_index)
        # Define upper item stop index (+1 according to slice convention)
        upper_item_stop = upper_line_slice_index - self._item_lower_index(upper_item_index) +1

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

    self.newlines = ('\n', '\r', '\r\n')

    ###############################################

    def __init__(self, lexer, text_buffer):

        current_line = HighlightedLine()
        for token, text in pygments.lex(text_buffer, lexer):
            current_line.append(HighlightedItem(token, text))
            # \n \r \r\n
            if str(token) == 'Token.Text' and text in self.newlines:
                self.append(current_line)
                current_line = HighlightedLine()

#####################################################################################################
#
# End
#
#####################################################################################################
