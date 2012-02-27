####################################################################################################

import bisect

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

class RawTextDocumentAbc(object):

    ###############################################

    def __init__(self, text_buffer, flat_slice, line_start_locations, line_separators):

        self._text_buffer = text_buffer
        self._flat_slice = flat_slice
        self._line_start_locations = line_start_locations
        self._line_separators = line_separators

    ###############################################

    def flat_slice(self):

        # Fixme: ?
        
        return FlatSlice(self._flat_slice)

    ###############################################

    def view(self, slice_):

        raise NotImplementedError

    ###############################################

    def __getitem__(self, slice_):
        
        return self.view(slice_)

    ##############################################

    def line_of(self, location):

        if location >= self._flat_slice.stop:
            raise IndexError

        # Return the index j where location < _line_start_locations[j]
        return bisect.bisect_right(self._line_start_locations, location) -1

    ##############################################

    def line_to_flat_slice(self, line_slice):

        return FlatSlice(self._line_start_locations[line_slice.start],
                         self._line_start_locations[line_slice.stop])

    ###############################################

    def to_flat_slice(self, slice_):

        if isinstance(slice_, FlatSlice):
            return slice_
        elif isinstance(slice_, LineSlice):
            return self.line_to_flat_slice(slice_)
        else:
            raise IndexError

    ##############################################

    def flat_to_line_slice(self, flat_slice):

        start_line = self.line_of(flat_slice.start)
        if flat_slice:
            stop_line = self.line_of(flat_slice.upper) +1
        else:
            stop_line= start_line +1
        
        return LineSlice(start_line, stop_line)

    ##############################################

    def line_slice_iterator(self, new_line_separator=True):

        if new_line_separator:
            for start, end in pairwise(self._line_start_locations):
                yield FlatSlice(start, end)
        else:
            for i, start_end in enumerate(pairwise(self._line_start_locations)):
                start, end = start_end
                end -= len(self._line_separators[i])
                yield FlatSlice(start, end)

    ##############################################

    def line_iterator(self, new_line_separator=True):

        for flat_slice in self.line_slice_iterator(new_line_separator):
            yield self._text_buffer[flat_slice()] 

    ##############################################

    def lines(self, new_line_separator=True):

        return list(self.line_iterator(new_line_separator))

####################################################################################################

class RawTextDocument(RawTextDocumentAbc):

    ##############################################

    def __init__(self, text_buffer):

        super(RawTextDocument, self). __init__(text_buffer,
                                               FlatSlice(0, len(text_buffer)),
                                               *self._split_lines(text_buffer))

    ##############################################

    def _append_sentinel(self, line_start_locations, line_separators, stop_location):

        if line_start_locations[-1] != stop_location:
            line_start_locations.append(stop_location)
            line_separators.append('')

    ##############################################

    def _split_lines(self, text_buffer):
 
        line_start_locations = [0]
        line_separators = []
        i = 0
        buffer_length = len(text_buffer)
        while i < buffer_length:
            line_separator = 0
            c = text_buffer[i]
            if c == '\r':
                if text_buffer[i+1] == '\n':
                    line_separator = 2
                else:
                    line_separator = 1
            elif c == '\n':
                line_separator = 1
            if line_separator:
                new_line_location = i+line_separator 
                line_start_locations.append(new_line_location)
                line_separators.append(text_buffer[i:new_line_location])
                i = new_line_location
            else:    
                i += 1

        self._append_sentinel(line_start_locations, line_separators, buffer_length)

        return line_start_locations, line_separators

    ###############################################

    def __len__(self):

        return len(self._text_buffer)

    ###############################################

    def __unicode__(self):

        return self._text_buffer

    ###############################################

    def substring(self, slice_):

        return self._text_buffer[self.to_flat_slice(slice_)()]

    ###############################################

    def view(self, slice_):

        flat_slice = self.to_flat_slice(slice_)
        if isinstance(slice_, LineSlice):
            line_slice = slice_
        else:
            line_slice = self.flat_to_line_slice(slice_)

        line_start_locations = [flat_slice.start]
        line_start_locations += self._line_start_locations[line_slice()][1:]
        line_separators = self._line_separators[line_slice()][:-1]

        self._append_sentinel(line_start_locations, line_separators, flat_slice.stop)

        return RawTextDocumentView(self,
                                   slice_,
                                   self._text_buffer,
                                   flat_slice,
                                   line_start_locations, line_separators)

####################################################################################################

class RawTextDocumentView(RawTextDocumentAbc):

    ##############################################

    def __init__(self, raw_text_document, slice_, *args):

        super(RawTextDocumentView, self).__init__(*args)

        self._raw_text_document = raw_text_document
        self.slice = slice_

    ###############################################

    def __nonzero__(self):

        return bool(self.slice)
    
    ###############################################

    def is_line_view(self):

        return isinstance(self.slice, LineSlice)

    ###############################################

    def to_document_flat_slice(self, slice_):

        return self._flat_slice.map(self.to_flat_slice(slice_))

    ###############################################

    def to_document_slice(self, slice_):

        if type(slice_) == type(self.slice):
            return self.slice.map(slice_)
        else:
            return self.to_document_flat_slice(slice_)

    ##############################################

    def __repr__(self):

        string_slice = str(self.slice)
        if isinstance(self.slice, LineSlice):
            string_slice += '/' + str(self._flat_slice)
        
        return self.__class__.__name__ + ' ' + string_slice

    ##############################################

    def __unicode__(self):

        return self._text_buffer[self._flat_slice()]

    ###############################################

    def substring(self, slice_):

        return self._text_buffer[self.to_document_flat_slice(slice_)()]

    ###############################################

    def view(self, slice_):

        return self._raw_text_document[self.to_document_slice(slice_)]

####################################################################################################
#
# End
#
####################################################################################################
