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

    def _slice_adaptator(self, slice_):

        if isinstance(slice_, FlatSlice):
            flat_slice = slice_
        elif isinstance(slice_, LineSlice):
            flat_slice = self.line_to_flat_slice(slice_)
        else:
            raise IndexError

        return flat_slice

    ###############################################

    def __getitem__(self, slice_):
        
        return self.view(slice_)

    ##############################################

    def _split_lines(self):

        if hasattr(self, '_line_start_locations'):
            return
 
        text_buffer = unicode(self)
   
        line_start_locations = self._line_start_locations = [0]
        line_separators = self._line_separators = []
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

        # Sentinel
        if line_start_locations[-1] < buffer_length:
            line_start_locations.append(buffer_length)
            line_separators.append('')

        # print buffer_length, line_start_locations, line_separators

    ##############################################

    def line_to_flat_slice(self, flat_slice):

        self._split_lines()

        return FlatSlice(self._line_start_locations[flat_slice.start],
                         self._line_start_locations[flat_slice.stop])

    ##############################################

    def line_iterator(self, new_line_separator=True):

        self._split_lines()

        if new_line_separator:
            for start, end in pairwise(self._line_start_locations):
                yield unicode(self)[start:end] 
        else:
            for i, start_end in enumerate(pairwise(self._line_start_locations)):
                start, end = start_end
                end -= len(self._line_separators[i])
                yield unicode(self)[start:end] 

    ##############################################

    def lines(self, new_line_separator=True):

        return list(self.line_iterator(new_line_separator))

####################################################################################################

class RawTextDocument(RawTextDocumentAbc):

    ##############################################

    def __init__(self, text_buffer):

        self._text_buffer = text_buffer

        self._split_lines()

    ###############################################

    def __unicode__(self):

        return self._text_buffer

    ###############################################

    def substring(self, slice_):

        return unicode(self)[self._slice_adaptator(slice_)()]

    ###############################################

    def view(self, slice_):

        return RawTextDocumentView(self, self._slice_adaptator(slice_))

####################################################################################################

class RawTextDocumentView(RawTextDocumentAbc):

    ##############################################

    def __init__(self, raw_text_document, flat_slice):

        self._raw_text_document = raw_text_document
        self._flat_slice = flat_slice

    ###############################################

    def _map_slice(self, slice_):

        return self._flat_slice.map(self._slice_adaptator(slice_))

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' ' + str(self._flat_slice)

    ##############################################

    def __unicode__(self):

        return unicode(self._raw_text_document)[self._flat_slice()]

    ###############################################

    def substring(self, slice_):

        return unicode(self._raw_text_document)[self._map_slice(slice_)()]

    ###############################################

    def view(self, slice_):

        return RawTextDocumentView(self, self._map_slice(slice_))

####################################################################################################
#
# End
#
####################################################################################################
