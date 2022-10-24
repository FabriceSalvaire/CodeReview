#####################################################################################################

import bisect

#####################################################################################################

#####################################################################################################

# FileTextContent

class TextContent(object):

    ###############################################

    def __init__(self, text_buffer):
    
        self.text_buffer = text_buffer
        self.text_lines = text_buffer.splitlines()
        self._init_line_bisect()

    ###############################################

    def __getitem__(self, text_slice):

        slice_obj = text_slice.to_slice()
        if isinstance(text_slice, FlatSlice):
            return self.text_buffer[slice_obj]
        elif isinstance(text_slice, LineSlice):
            return self.text_lines[slice_obj]
        else:
            raise IndexError

    ###############################################

    def flat_iterator(self):

        return iter(self.text_buffer)

    ###############################################

    def line_iterator(self):

        return iter(self.text_lines)

    ###############################################

    def _init_line_bisect(self):

        # Fill _accumulated_lengths with
        #   [len(line_0), len(line_0 + line_1), ...]
        accumulator = 0
        self._accumulated_lengths = []
        for line in self.line_iterator():
            accumulator += len(line)
            self._accumulated_lengths.append(accumulator)

    ###############################################

    def flat_to_line_index(self, i):

        # Return the index j where i < _accumulated_lengths[j], since _accumulated_lengths[j]
        # corresponds to the lower index of the line j+1, thus j corresponds to the line that
        # include the location i.
        return bisect.bisect_right(self._accumulated_lengths, i)

    ###############################################

    def line_to_lower_flat_index(self, i):

        """ Return the line lower index.
        """

        if i:
            return self._accumulated_lengths[i -1]
        else:
            return 0

    ###############################################

    def line_to_flat_slice(self, line_slice):

        if hasattr(line_slice, '__index__'):
            i = line_slice.__index__
            start, stop = i, i+1
        elif isinstance(line_slice, LineSlice):
            start, stop = line_slice.start, line_slice.stop
        else:
            raise ValueError
    
        return FlatSlice(self.line_lower_index(start), self.line_lower_index(stop))

#####################################################################################################

class TextChunk(object):

    ###############################################

    def __init__(self, text_content, text_slice):

        self.text_content = text_content
        self.text_slice = text_slice

#####################################################################################################
#
# End
#
#####################################################################################################
