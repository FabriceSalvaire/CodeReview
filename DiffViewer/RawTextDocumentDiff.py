#####################################################################################################

from bzrlib.patiencediff import unified_diff_files, PatienceSequenceMatcher

####################################################################################################

from Slice import FlatSlice, LineSlice
from RawTextDocument import RawTextDocument

####################################################################################################

class TwoWayChunk(object):

    ##############################################

    def __init__(self, chunk1, chunk2):

        self.chunk1, self.chunk2 = chunk1, chunk2

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' (' + repr(self.chunk1) + ', ' + repr(self.chunk2) + ')'

####################################################################################################

class TwoWayChunkDelete(TwoWayChunk):
    pass

class TwoWayChunkEqual(TwoWayChunk):
    pass

class TwoWayChunkInsert(TwoWayChunk):
    pass

class TwoWayChunkReplace(TwoWayChunk):
    pass

####################################################################################################

class TwoWayLineChunkDelete(TwoWayChunk):
    pass

class TwoWayLineChunkEqual(TwoWayChunk):
    pass

class TwoWayLineChunkInsert(TwoWayChunk):
    pass

####################################################################################################

class TwoWayLineChunkReplace(TwoWayChunk):

    ##############################################

    def __init__(self, chunk1, chunk2, chunks):

        super(TwoWayLineChunkReplace, self).__init__(chunk1, chunk2)
        
        self._chunks = chunks

    ##############################################

    def __repr__(self):

        return super(TwoWayLineChunkReplace, self).__repr__() + ': ' + repr(self._chunks)

    ##############################################

    def __iter__(self):

        return iter(self._chunks)

    ##############################################

    def __getitem__(self, slice_):

        return self._chunks[slice_]

####################################################################################################

class TwoWayGroup(list):
    pass

####################################################################################################

class TwoWayFileDiff(object):

    ##############################################

    def __init__(self, document1, document2):

        self.document1, self.document2 = document1, document2
        self._groups = []

    ##############################################

    def __iter__(self):

        return iter(self._groups)

    ##############################################

    def __getitem__(self, slice_):

        return self._groups[slice_]

    ##############################################

    def append(self, group):

        self._groups.append(group)

####################################################################################################

class TwoWayFileDiffFactory(object):

    ###############################################

    def _process_group(self, file_diff, opcodes):

        """ Process a group of contiguous line changes. """

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

        sub_chunks = []
        text1, text2 = [unicode(chunk).encode('utf_32-BE') for chunk in chunk1, chunk2]
        line_sequence_matcher = PatienceSequenceMatcher(None, text1, text2)
        opcodes = line_sequence_matcher.get_opcodes()
        for tag, start_1, stop_1, start_2, stop_2 in opcodes:
            slice1 = FlatSlice(start_1, stop_1) /4 # 4-byte encoding
            slice2 = FlatSlice(start_2, stop_2) /4
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
  
    ###############################################

    def process(self, document1, document2, number_of_lines_of_context=3):

        file_diff = TwoWayFileDiff(document1, document2)

        sequence_matcher = PatienceSequenceMatcher(None, document1.lines(), document2.lines())
        sequence_matcher_groups = sequence_matcher.get_grouped_opcodes(number_of_lines_of_context)

        for opcodes in sequence_matcher_groups:
            self._process_group(file_diff, opcodes)

        return file_diff

####################################################################################################
#
# End
#
####################################################################################################
