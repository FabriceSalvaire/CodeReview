####################################################################################################

import unittest

####################################################################################################

from RawTextDocument import RawTextDocument
from RawTextDocumentDiff import TwoWayFileDiffFactory
from Slice import FlatSlice, LineSlice
from TextDocumentModel import TextDocumentModel, TextBlock, TextFragment
import RawTextDocumentDiff

####################################################################################################

class TestTextDocumentModel(unittest.TestCase):

    ##############################################

    def test(self):

        with open('test_file1.txt') as f:
            text1 = f.read()

        with open('test_file2.txt') as f:
            text2 = f.read()

        raw_text_document1 = RawTextDocument(text1)
        raw_text_document2 = RawTextDocument(text2)
        
        two_way_file_diff_factory = TwoWayFileDiffFactory()
        file_diff = two_way_file_diff_factory.process(raw_text_document1, raw_text_document2)
        
        text_document_model = TextDocumentModel()
        current_line1 = 0
        for group in file_diff:
            if current_line1 < group.slice1.start:
                print 'Complete: ', current_line1, group.slice1
                line_slice = LineSlice(current_line1, group.slice1.start)
                text_block = TextBlock(line_slice, RawTextDocumentDiff.EQUAL)
                flat_slice = raw_text_document1.to_flat_slice(line_slice)
                text_fragment = TextFragment(flat_slice)
                text_block.append(text_fragment)
                text_document_model.append(text_block)
            for chunk in group:
                frame_type = chunk.chunk_type
                text_block = TextBlock(chunk.chunk1.slice, frame_type)
                if frame_type == RawTextDocumentDiff.REPLACE:
                    for sub_chunk in chunk:
                        sub_frame_type = sub_chunk.chunk_type
                        text_fragment = TextFragment(sub_chunk.chunk1, sub_frame_type)
                        text_block.append(text_fragment)
                else:
                    text_fragment = TextFragment(chunk.chunk1)
                    text_block.append(text_fragment)
                text_document_model.append(text_block)
            current_line1 = group.slice1.stop

        for text_block in text_document_model:
            print text_block
            for text_fragment in text_block:
                print ' '*2 + repr(text_fragment)
            
####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
