####################################################################################################
#
# PyQGit - A Python/Qt Git GUI
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

# Fixme: unicode support
#   - doc [] len ...
#   - englis 's

""" This module provides an enhancement over a basic array of characters, so called Text Buffer.  It
features an API to manipulate text buffer using a line indexing and slicing.

Definition of therms used in this document:

  Text Buffer
    A text buffer is an object that provide the characters and implements the method **__getitem__**
    to index or slice them and the method **__len__** to get the number of characters.

  Text Document
    A text document is a text buffer adapted by a :class:`RawTextDocument` class featuring the line
    indexing and slicing.

  Flat Slice
    A flat slice represents an interval of character indexes.  Only the sliced object know how to
    interpret the slice.

  Line Slice
    A line slice represents an interval of line indexes.  The only difference with a flat slice is
    semantic.

  Text Chunk or View
    A text chunk represents a sliced text buffer.

  Line
    A line represents either a slice, a view or the corresponding string of characters.

"""

####################################################################################################

import bisect

####################################################################################################

from PyQGit.Tools.Slice import FlatSlice, LineSlice
from PyQGit.Tools.IteratorTools import pairwise

####################################################################################################

class RawTextDocumentAbc(object):

    """ This class implements the basic function for a Text Chunk.

    To get the number of characters of the chunk use the function :func:`len` and to test if the
    slice is empty use a Boolean evaluation of the instance.

    To get the text buffer use the function :func:`unicode`.

    To get a view or light view if the light view mode is set, we can use::

      text_document[slice]

    The light view mode is set using the boolean attribute :attr:`light_view_mode`.

    """

    light_view_mode = False

    ###############################################

    def __init__(self, text_buffer, flat_slice, line_start_locations, line_separators):

        """ The parameter *text_buffer* specifies the text buffer.  It must implement the method
        **__getitem__** to index and slice the characters.

        The parameter *flat_slice* specifies the flat slice corresponding to the text chunk.

        The list *line_start_locations* contains the position of the new lines in the text chunk and
        the list *line_separators* contains the corresponding new line separators.  The standard
        separators (``\\\\r\\\\n``, ``\\\\r``, ``\\\\n``) are supported.  The list
        *line_start_locations* ends by a sentinel that corresponds to the number of characters in
        the text chunk and the list *line_separators* by an empty string.  This sentinel
        corresponds to a virtual line at the end of the text buffer.
        """

        self._text_buffer = text_buffer
        self._flat_slice = flat_slice
        self._line_start_locations = line_start_locations
        self._line_separators = line_separators

    ###############################################

    def __bool__(self):

        """ Test if the slice is empty. """

        return bool(self._flat_slice)

    ###############################################

    def __len__(self):

        """ Return the number of characters of the text chunk. """

        return len(self._flat_slice)

    ###############################################

    def __str__(self):

        """ Return the text buffer instance. """

        return self._text_buffer

    ###############################################

    def substring(self, slice_):

        """ Return the unicode sub-string corresponding to the slice. """

        return self._text_buffer[self.to_flat_slice(slice_)()]

    ###############################################

    def flat_slice(self):

        """ Return a copy of the flat slice corresponding to the text chunk. """

        # Fixme: copy? check consistency elsewhere.

        return FlatSlice(self._flat_slice)

    ###############################################

    def view(self, slice_):

        """ Return a :class:`RawTextDocumentView` instance for the corresponding slice.

        Not implemented.
        """

        raise NotImplementedError

    ###############################################

    def light_view(self, slice_):

        """ Return a :class:`RawTextDocumentLightView` instance for the corresponding slice.

        Not implemented.
        """

        # Fixme: light_view is abstract in a subclass

        raise NotImplementedError

    ###############################################

    def __getitem__(self, slice_):

        """ This method implements an array interface and return a light view or a view depending of
        the setup.
        """

        if self.light_view_mode:
            return self.light_view(slice_)
        else:
            return self.view(slice_)

    ##############################################

    def line_of(self, location):

        """ Return the line number for the location. """

        if location >= self._flat_slice.stop:
            raise IndexError

        # Return the index j where location < _line_start_locations[j]
        return bisect.bisect_right(self._line_start_locations, location) -1

    ##############################################

    def line_to_flat_slice(self, line_slice):

        """ Convert a line slice to a flat slice and return it. """

        return FlatSlice(self._line_start_locations[line_slice.start],
                         self._line_start_locations[line_slice.stop])

    ###############################################

    def to_flat_slice(self, slice_):

        """ Ensure *slice_* is a flat slice and return it. """

        if isinstance(slice_, FlatSlice):
            return slice_
        elif isinstance(slice_, LineSlice):
            return self.line_to_flat_slice(slice_)
        else:
            raise ValueError

    ##############################################

    def flat_to_line_slice(self, flat_slice):

        """ Convert a flat slice to a line slice and return it. """

        start_line = self.line_of(flat_slice.start)
        if flat_slice:
            upper_line = self.line_of(flat_slice.upper)
        else:
            upper_line= start_line

        return LineSlice(start_line, upper_line +1)

    ##############################################

    def line_slice_iterator(self, new_line_separator=True):

        """ Return an iterator on the line's flat slices.  If *new_line_separator* is set then the
        line separator is included.
        """

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

        """ Return an iterator on the string lines.  If *new_line_separator* is set then the line
        separator is included.
        """

        for flat_slice in self.line_slice_iterator(new_line_separator):
            yield self._text_buffer[flat_slice()]

    ##############################################

    def lines(self, new_line_separator=True):

        """ Return the list of string lines.  If *new_line_separator* is set then the line separator
        is included.
        """

        return list(self.line_iterator(new_line_separator))

####################################################################################################

class RawTextDocument(RawTextDocumentAbc):

    """ This class implements a Text Document. """

    ##############################################

    def __init__(self, text_buffer):

        """ The parameter *text_buffer* specifies the text buffer,
        cf. :class:`RawTextDocumentAbc` for explanations.
        """

        super(RawTextDocument, self). __init__(text_buffer,
                                               FlatSlice(0, len(text_buffer)),
                                               *self._split_lines(text_buffer))

        self.line_slice = self.flat_to_line_slice(self._flat_slice)

    ##############################################

    def _append_sentinel(self, line_start_locations, line_separators, stop_location):

        """ Append a sentinel to the lists: *line_start_locations* and *line_separators*.

        The parameter *stop_location* corresponds to the stop index of the text chunk.

        This method ensures the list *line_separators* end by *stop_location* and it appends an
        empty string to *line_separators* if it is not true.
        """

        if line_start_locations[-1] != stop_location:
            line_start_locations.append(stop_location)
            line_separators.append('')

    ##############################################

    def _split_lines(self, text_buffer):

        """ Split the lines and return the 2-tuple (*line_start_locations*, *line_separators*),
        cf. :class:`RawTextDocumentAbc` for their definitions.
        """

        line_start_locations = [0]
        line_separators = []
        buffer_length = len(text_buffer)
        i = 0
        while i < buffer_length:
            line_separator_length = 0
            char = text_buffer[i]
            if char == '\r':
                if text_buffer[i+1] == '\n':
                    line_separator_length = 2
                else:
                    line_separator_length = 1
            elif char == '\n':
                line_separator_length = 1
            if line_separator_length:
                new_line_location = i + line_separator_length 
                line_start_locations.append(new_line_location)
                line_separators.append(text_buffer[i:new_line_location])
                i = new_line_location
            else:
                i += 1

        self._append_sentinel(line_start_locations, line_separators, buffer_length)

        return line_start_locations, line_separators

    ###############################################

    def view(self, slice_):

        """ Return a :class:`RawTextDocumentView` instance for the corresponding slice. """

        flat_slice = self.to_flat_slice(slice_)
        if isinstance(slice_, LineSlice):
            line_slice = slice_
        else:
            line_slice = self.flat_to_line_slice(slice_)

        # line_start_locations ...
        line_start_locations = [flat_slice.start]
        line_start_locations += self._line_start_locations[line_slice()][1:]
        # line_separators is a subset
        line_separators = self._line_separators[line_slice()][:-1]
        self._append_sentinel(line_start_locations, line_separators, flat_slice.stop)

        return RawTextDocumentView(self,
                                   slice_,
                                   self._text_buffer,
                                   flat_slice,
                                   line_start_locations, line_separators)

    ###############################################

    def light_view(self, slice_):

        """ Return a :class:`RawTextDocumentLightView` instance for the corresponding slice. """

        flat_slice = self.to_flat_slice(slice_)

        return RawTextDocumentLightView(self, flat_slice)

####################################################################################################

class RawTextDocumentView(RawTextDocumentAbc):

    """ This class implements a view on a Text Document. """

    ##############################################

    def __init__(self, raw_text_document, slice_, *args):

        """ The parameter *raw_text_document* specifies the text document.

        The parameter *slice_* specifies the slice corresponding to the view, it can be either a
        flat ro a line slice.

        The remaining parameters are those of the :meth:`RawTextDocumentAbc.__init__` method.

        Public attributes:

          :attr:`slice`

            is a copy of the slice passed as argument.

        """

        # Fixme: raw_text_document has text_buffer

        super(RawTextDocumentView, self).__init__(*args)

        self._raw_text_document = raw_text_document
        self.slice = slice_

    ###############################################

    def is_line_view(self):

        """ Test if it is a line slice. """

        return isinstance(self.slice, LineSlice)

    ###############################################

    def to_document_flat_slice(self, slice_):

        """ Convert a slice into the view to a flat slice in the document space and return it. """

        return self._flat_slice.map(self.to_flat_slice(slice_))

    ###############################################

    def to_document_slice(self, slice_):

        """ Convert a slice into the view to a slice in the document space and return it.  This
        method tries to keep the type of slice.
        """

        # Fixme: if same type than original

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

    def __str__(self):

        """ Return the unicode string corresponding to the view. """

        return self._text_buffer[self._flat_slice()]

    ###############################################

    def substring(self, slice_):

        """ Return the sub-string corresponding to the local slice in the view. """

        return self._text_buffer[self.to_document_flat_slice(slice_)()]

    ###############################################

    def view(self, slice_):

        """ Return the view corresponding to the local slice in the view. """

        return self._raw_text_document[self.to_document_slice(slice_)]

####################################################################################################

class RawTextDocumentLightView(object):

    """ This class implements a light view on a Text Document.

    A light view doesn't feature line indexing and slicing.  The memory footprint is lighter than a
    standard view and thus well suited for many small chunks.

    To get the number of characters of the chunk use the function :func:`len` and to test if the
    slice is empty use a Boolean evaluation of the instance.

    To get the text buffer use the function :func:`unicode`.

    To get a light view, we can use::

      text_document[slice]

    Public attributes:

      :attr:`flat_slice`
    """

    __slots__ = ['_raw_text_document', 'flat_slice']

    ##############################################

    def __init__(self, raw_text_document, flat_slice):

        """ The parameter *raw_text_document* specifies the text document.

        The parameter *flat_slice* specifies the slice corresponding to the view.

        """

        self._raw_text_document = raw_text_document
        self.flat_slice = flat_slice

    ###############################################

    def __len__(self):

        """ Return the number of characters of the text chunk. """

        return len(self.flat_slice)

    ###############################################

    def __bool__(self):

        """ Test if the slice is empty. """

        return bool(self.flat_slice)

    ###############################################

    def to_document_flat_slice(self, flat_slice):

        """ Convert a flat slice into the view to a flat slice in the document space and return
        it.
        """

        return self.flat_slice.map(flat_slice)

    ##############################################

    def __repr__(self):

        string_slice = str(self.flat_slice)

        return self.__class__.__name__ + ' ' + string_slice

    ##############################################

    def __str__(self):

        """ Return the unicode string corresponding to the view. """

        return self._raw_text_document.substring(self.flat_slice)

    ###############################################

    def substring(self, flat_slice):

        """ Return the sub-string corresponding to the local slice in the view. """

        flat_slice = self.to_document_flat_slice(flat_slice)
        
        return self._raw_text_document.substring(flat_slice)

    ###############################################

    def view(self, flat_slice):

        """ Return the view corresponding to the local slice in the view. """

        return self._raw_text_document.light_view(flat_slice)

    ###############################################

    __getitem__  = view

####################################################################################################
#
# End
#
####################################################################################################
