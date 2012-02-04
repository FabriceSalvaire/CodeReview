####################################################################################################

from Slice import FlatSlice, LineSlice

#####################################################################################################

def pairwise(iterable):

    """ Return a generator which generate a pair wise list from an iterable.
    s -> (s[0],s[1]), (s[1],s[2]), ... (s[N-1], s[N])
    """

    prev = iterable[0]
    for x in iterable[1:]:
        yield prev, x
        prev = x

####################################################################################################

class RawTextDocument(object):

    ##############################################

    def __init__(self, text_buffer):

        self._text_buffer = text_buffer

        self._split_lines()

    ###############################################

    def __getitem__(self, slice_):

        if isinstance(slice_, FlatSlice):
            flat_slice = slice_
        elif isinstance(slice_, LineSlice):
            flat_slice = self.line_to_flat_slice(slice_)
        else:
            raise IndexError

        return self._text_buffer[flat_slice()]

    ##############################################

    def _split_lines(self):
    
        line_start_locations = self._line_start_locations = [0]
        line_separators = self._line_separators = []
        i = 0
        buffer_length = len(self._text_buffer)
        while i < buffer_length:
            line_separator = 0
            c = self._text_buffer[i]
            if c == '\r':
                if self._text_buffer[i+1] == '\n':
                    line_separator = 2
                else:
                    line_separator = 1
            elif c == '\n':
                line_separator = 1
            if line_separator:
                new_line_location = i+line_separator 
                line_start_locations.append(new_line_location)
                line_separators.append(self._text_buffer[i:new_line_location])
                i = new_line_location
            else:    
                i += 1

        # Sentinel
        if line_start_locations[-1] < buffer_length:
            line_start_locations.append(buffer_length)
            line_separators.append('')

        # print buffer_length, line_start_locations, line_separators

    ##############################################

    def line_to_flat_slice(self, flat_slice):

        return FlatSlice(self._line_start_locations[flat_slice.lower],
                         self._line_start_locations[flat_slice.upper +1])

    ##############################################

    def complete_line_iterator(self):

        for start, end in pairwise(self._line_start_locations):
            yield self._text_buffer[start:end] 

    ##############################################

    def line_iterator(self):

        for i, start_end in enumerate(pairwise(self._line_start_locations)):
            start, end = start_end
            end -= len(self._line_separators[i])
            yield self._text_buffer[start:end] 

####################################################################################################
#
# End
#
####################################################################################################
