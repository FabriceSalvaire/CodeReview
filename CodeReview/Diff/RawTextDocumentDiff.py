####################################################################################################
#
# CodeReview - A Python/Qt Git GUI
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

####################################################################################################
#
#                                              Audit
#
# - 31/05/2012 Fabrice
#   languages:
#     two way chunk / chunk / view
#   equal_block vs equal
#
####################################################################################################

""" This module provides an API to compute and store the difference between two text documents.

The difference between two documents is computed in therms of line difference, thus documents are
split to a set of contiguous lines called *chunks*.  Chunks are implemented as document views.

There is three types of differences, some lines was removed, some lines was inserted and some lines
was replaced by something else.  A difference is located in the document using a number of context
lines, these lines are the same in both documents.  These context lines are useful to make patch.

The differences are grouped as ordered set of contiguous line differences (any combination of
removed, inserted and replaced chunk) and are delimited by two equal chunks to define the context.

Thus we have five types of chunks: *removed*, *inserted*, *replaced*, *equal* for the context lines
and *equal_block* for the equal contents that are out of the context lines.  This separation for
equal contents permits to keep at this level the structure computed by the difference algorithm.

For replaced contents, we can apply a similar logic and compute a difference in therms of flat
slices instead of line slices.

To sumarize, a document difference is an ordered list of group differences.  Each group is made of
any combination of *removed*, *inserted* and *replaced* chunk type and delimited by two *equal*
chunks.  And *replaced* chunks are made of any combination of *removed*, *inserted*, *replaced* and
*equal* sub-chunks.  Moreover we can complete the structure with *equal_block* chunks.
"""

####################################################################################################

from CodeReview.PatienceDiff import PatienceSequenceMatcher

####################################################################################################

from CodeReview.Tools.EnumFactory import EnumFactory
from CodeReview.Tools.Slice import FlatSlice, LineSlice

####################################################################################################

#: Defines the type of chunks
# Fixme: poorly formated by sphinx, name ?
chunk_type = EnumFactory('TwoWayChunkTypes', ('equal', 'insert', 'delete', 'replace',
                                              'equal_block'))

####################################################################################################

class TwoWayChunk(object):

    """ This class implements a two way chunk.

    Public attributes:

      :attr:`chunk1`
        view for document1

      :attr:`chunk2`
        view for document2

    """

    ##############################################

    def __init__(self, chunk1, chunk2):

        """ The parameters *chunk1* and *chunk2* are the corresponding document views for the
        chunk.
        """

        self.chunk1, self.chunk2 = chunk1, chunk2

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' (' + repr(self.chunk1) + ', ' + repr(self.chunk2) + ')'

####################################################################################################

class TwoWayChunkDelete(TwoWayChunk):
    """ This class implements a two way delete flat chunk. """
    chunk_type = chunk_type.delete

class TwoWayChunkEqual(TwoWayChunk):
    """ This class implements a two way equal flat chunk. """
    chunk_type = chunk_type.equal

class TwoWayChunkInsert(TwoWayChunk):
    """ This class implements a two way insert flat chunk. """
    chunk_type = chunk_type.insert

class TwoWayChunkReplace(TwoWayChunk):
    """ This class implements a two way replace flat chunk. """
    chunk_type = chunk_type.replace

####################################################################################################

class TwoWayLineChunkDelete(TwoWayChunk):
    """ This class implements a two way delete line chunk. """
    chunk_type = chunk_type.delete

class TwoWayLineChunkEqual(TwoWayChunk):
    """ This class implements a two way equal line chunk. """
    chunk_type = chunk_type.equal

class TwoWayLineChunkInsert(TwoWayChunk):
    """ This class implements a two way insert line chunk. """
    chunk_type = chunk_type.insert

####################################################################################################

class TwoWayLineChunkReplace(TwoWayChunk):

    """ This class implements the specific case of replace line chunk type.

    The class implements the *iter* and *getitem* protocol to access the sub-chunks.
    """

    chunk_type = chunk_type.replace

    ##############################################

    def __init__(self, chunk1, chunk2, chunks):

        super(TwoWayLineChunkReplace, self).__init__(chunk1, chunk2)
        
        self._chunks = chunks

    ##############################################

    def __repr__(self):

        return super(TwoWayLineChunkReplace, self).__repr__() + ': ' + repr(self._chunks)

    ##############################################

    def __iter__(self):

        """ Return an iterator over the sub-chunks. """

        return iter(self._chunks)

    ##############################################

    def __getitem__(self, slice_):

        """ Provide an array interface to the chunks. """

        return self._chunks[slice_]

####################################################################################################

class TwoWayGroup(object):

    """ This class implements a group of contiguous line changes between two files.

    The class implements the *iter* and *getitem* protocol to access the groups.

    Public attributes:

      :attr:`slice1`
        Line slice for document1

      :attr:`slice2`
        Line slice for document2
    """

    ##############################################

    def __init__(self):

        self._chunks = []
        self.slice1 = None
        self.slice2 = None

    ##############################################

    def __iter__(self):

        """ Return an iterator over the chunks. """

        return iter(self._chunks)

    ##############################################

    def __getitem__(self, slice_):

        """ Provide an array interface to the chunks. """

        return self._chunks[slice_]

    ##############################################

    def append(self, chunk):

        """ Append a chunk. """

        self._chunks.append(chunk)
        if self.slice1 is None:
            self.slice1 = LineSlice(chunk.chunk1.slice)
            self.slice2 = LineSlice(chunk.chunk2.slice)
        else:
            self.slice1 |= chunk.chunk1.slice
            self.slice2 |= chunk.chunk2.slice

####################################################################################################

class TwoWayFileDiff(object):

    """ This class stores the difference between two files. """

    ##############################################

    def __init__(self, document1, document2):

        """ The parameters *document1* and *document2* are two :class:`DiffViewer.RawTextDocument`
        documents.

        The class implements the *iter* and *getitem* protocol to access the groups.

        Public attributes:

          :attr:`document1`

          :attr:`document2`
        """

        self.document1, self.document2 = document1, document2
        self._groups = []

    ##############################################

    def __iter__(self):

        """ Return an iterator over the groups. """ 

        return iter(self._groups)

    ##############################################

    def __getitem__(self, slice_):

        """ Provides an array interface. """

        return self._groups[slice_]

    ##############################################

    def append(self, group):

        """ Append a group. """

        self._groups.append(group)

    ###############################################

    def pretty_print(self):

        """ Pretty-print the file differences. """

        def pretty_print_chunk(chunk, level=0):
            print(' '*level + chunk.__class__.__name__)
            for chunk_slice in chunk.chunk1, chunk.chunk2:
                print(' '*2*(level+1) + repr(chunk_slice))
        
        for group in self:
            print('='*80)
            print('@', group.slice1, group.slice2, '@')
            for chunk in group:
                pretty_print_chunk(chunk, level=0)
                if isinstance(chunk, TwoWayLineChunkReplace):
                    for sub_chunk in chunk:
                        pretty_print_chunk(sub_chunk, level=1)

    ###############################################

    def print_unidiff(self):

        """ Pretty-print the file differences using unidiff format. """

        def pretty_print_chunk_lines(chunk, prefix):
            print(prefix + prefix.join(chunk.lines()).rstrip())
        
        def pretty_print_chunk(chunk):
            if isinstance(chunk, TwoWayLineChunkEqual):
                pretty_print_chunk_lines(chunk.chunk1, prefix=' ')
            elif isinstance(chunk, TwoWayLineChunkDelete):
                pretty_print_chunk_lines(chunk.chunk1, prefix='-')
            elif isinstance(chunk, TwoWayLineChunkInsert):
                pretty_print_chunk_lines(chunk.chunk2, prefix='+')
            elif isinstance(chunk, TwoWayLineChunkReplace):
                pretty_print_chunk_lines(chunk.chunk1, prefix='-')
                pretty_print_chunk_lines(chunk.chunk2, prefix='+')
        
        for group in self:
            print('='*80)
            print('@', group.slice1, group.slice2, '@')
            for chunk in group:
                pretty_print_chunk(chunk)
                if isinstance(chunk, TwoWayLineChunkReplace):
                    for sub_chunk in chunk:
                        pretty_print_chunk(sub_chunk)

####################################################################################################

class TwoWayFileDiffFactory(object):

    """ This class implements a factory to compute file differences. """

    ###############################################

    def process(self, document1, document2, number_of_lines_of_context=3):

        """ Compute the difference between two :class:`RawTextDocument` documents and return a
        :class:`TwoWayFileDiff` instance.  The parameter *number_of_lines_of_context* provides the
        number of lines of context for the diff algorithm.
        """

        file_diff = TwoWayFileDiff(document1, document2)

        sequence_matcher = PatienceSequenceMatcher(None, document1.lines(), document2.lines())
        sequence_matcher_groups = sequence_matcher.get_grouped_opcodes(number_of_lines_of_context)

        for opcodes in sequence_matcher_groups:
            self._process_group(file_diff, opcodes)

        return file_diff

    ###############################################

    def _process_group(self, file_diff, opcodes):

        """ Process a group of contiguous line changes and append the group to the file diff. """

        group = TwoWayGroup()
        for tag, start_1, stop_1, start_2, stop_2 in opcodes:
            slice1 = LineSlice(start_1, stop_1)
            slice2 = LineSlice(start_2, stop_2)
            chunk1 = file_diff.document1[slice1]
            chunk2 = file_diff.document2[slice2]
            if tag == 'equal':
                chunk_diff = TwoWayLineChunkEqual(chunk1, chunk2)
            elif tag == 'delete':
                chunk_diff = TwoWayLineChunkDelete(chunk1, chunk2)
            elif tag == 'insert':
                chunk_diff = TwoWayLineChunkInsert(chunk1, chunk2)
            elif tag == 'replace':
                chunks = self._process_replace_chunk(chunk1, chunk2)
                chunk_diff = TwoWayLineChunkReplace(chunk1, chunk2, chunks)
            group.append(chunk_diff)
        file_diff.append(group)

    ###############################################

    def _process_replace_chunk(self, chunk1, chunk2):

        """ Process a replace chunk type and return the sub-chunks.

        The text is encoded in UTF-32 before to be passed to the diff algorithm in order to have
        fixed character boundaries.
        """

        sub_chunks = []
        text1, text2 = [str(chunk).encode('utf_32-BE') for chunk in (chunk1, chunk2)]
        line_sequence_matcher = PatienceSequenceMatcher(None, text1, text2)
        opcodes = line_sequence_matcher.get_opcodes()
        for tag, start_1, stop_1, start_2, stop_2 in opcodes:
            slice1 = FlatSlice(start_1, stop_1) //4 # 4-byte encoding
            slice2 = FlatSlice(start_2, stop_2) //4
            sub_chunk1 = chunk1[slice1]
            sub_chunk2 = chunk2[slice2]
            if tag == 'equal':
                sub_chunk_diff = TwoWayChunkEqual(sub_chunk1, sub_chunk2)
            elif tag == 'delete':
                sub_chunk_diff = TwoWayChunkDelete(sub_chunk1, sub_chunk2)
            elif tag == 'insert':
                sub_chunk_diff = TwoWayChunkInsert(sub_chunk1, sub_chunk2)
            elif tag == 'replace':
                sub_chunk_diff = TwoWayChunkReplace(sub_chunk1, sub_chunk2)
            sub_chunks.append(sub_chunk_diff)

        return sub_chunks

####################################################################################################
#
# End
#
####################################################################################################
