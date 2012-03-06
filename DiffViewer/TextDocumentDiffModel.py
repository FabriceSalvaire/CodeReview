####################################################################################################

from RawTextDocumentDiff import chunk_type
from Slice import LineSlice
from TextDocumentModel import TextDocumentModel, TextBlock, TextFragment

####################################################################################################

class TextBlockDiff(TextBlock):

    ##############################################

    def link_other_side(self, other_side):

        self.other_side = other_side
        
####################################################################################################

class TextDocumentDiffModelFactory(object):

    ###############################################

    def process(self, file_diff):

        document1 = file_diff.document1
        document2 = file_diff.document2
        
        document_model1 = TextDocumentModel()
        document_model2 = TextDocumentModel()
        current_line1 = 0
        current_line2 = 0
        for group in file_diff:

            # Inter-group lines corresponds to equal contents
            if current_line1 < group.slice1.start or current_line2 < group.slice2.start:
                line_slice1 = LineSlice(current_line1, group.slice1.start)
                text_block1 = self._complete_one_side(document1, line_slice1, document_model1)
                line_slice2 = LineSlice(current_line2, group.slice2.start)
                text_block2 = self._complete_one_side(document2, line_slice2, document_model2)
                self._link(text_block1, text_block2)

            for chunk in group:
                frame_type = chunk.chunk_type
                text_block1 = TextBlockDiff(chunk.chunk1.slice, frame_type)
                text_block2 = TextBlockDiff(chunk.chunk2.slice, frame_type)
                self._link(text_block1, text_block2)
                
                if frame_type == chunk_type.replace:
                    self._append_sub_chunk(chunk, text_block1, text_block2)
                else:
                    text_block1.append(TextFragment(chunk.chunk1))
                    text_block2.append(TextFragment(chunk.chunk2))
                    
                document_model1.append(text_block1)
                document_model2.append(text_block2)

            current_line1 = group.slice1.stop
            current_line2 = group.slice2.stop

        return document_model1, document_model2

    ###############################################

    def _link(self, text_block1, text_block2):

        text_block1.link_other_side(text_block2)
        text_block2.link_other_side(text_block1)
    
    ###############################################

    def _complete_one_side(self, document, line_slice, document_model):

        text_block = TextBlockDiff(line_slice, chunk_type.equal_block)
        document_model.append(text_block)
        
        if bool(line_slice):
            flat_slice = document.to_flat_slice(line_slice)
            chunk = document[flat_slice]
            text_fragment = TextFragment(chunk)
            text_block.append(text_fragment)
            
        return text_block
             
    ###############################################

    def _append_sub_chunk(self, chunk, text_block1, text_block2):

        for sub_chunk in chunk:
            sub_frame_type = sub_chunk.chunk_type
            if bool(sub_chunk.chunk1):
                text_block1.append(TextFragment(sub_chunk.chunk1, sub_frame_type))
            if bool(sub_chunk.chunk2):
                text_block2.append(TextFragment(sub_chunk.chunk2, sub_frame_type))
        
####################################################################################################
#
# End
#
####################################################################################################
