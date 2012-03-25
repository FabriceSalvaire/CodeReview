####################################################################################################

from DiffViewer.RawTextDocumentDiff import chunk_type
from DiffViewer.Slice import LineSlice
from DiffViewer.TextDocumentModel import TextDocumentModel, TextBlock, TextFragment

####################################################################################################

class TextBlockDiff(TextBlock):

    ##############################################
    
    def __init__(self, line_slice, frame_type=None, other_side=None):

        super(TextBlockDiff, self).__init__(line_slice, frame_type)

        self.other_side = other_side

    ##############################################
    
    def clone(self):

        return self.__class__(self.line_slice, self.frame_type, self.other_side)
        
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

        def add_equal_contents(stop_line1, stop_line2):
            line_slice1 = LineSlice(current_line1, stop_line1)
            line_slice2 = LineSlice(current_line2, stop_line2)
            text_block1 = self._complete_one_side(document1, line_slice1, document_model1)
            text_block2 = self._complete_one_side(document2, line_slice2, document_model2)
            self._link(text_block1, text_block2)

        for group in file_diff:

            # Inter-group lines corresponds to equal contents
            if current_line1 < group.slice1.start or current_line2 < group.slice2.start:
                add_equal_contents(group.slice1.start, group.slice2.start)

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

        # Last group lines corresponds to equal contents
        if current_line1 < document1.line_slice.stop or current_line2 < document2().line_slice.stop:
            add_equal_contents(document1.line_slice.stop, document2.line_slice.stop)

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

def highlight_document(document_model, highlighted_text):

    raw_text_document = highlighted_text.raw_text_document
    
    highlighted_text_iterator = iter(highlighted_text)
    highlighted_fragment = highlighted_text_iterator.next()
    highlighted_slice= highlighted_fragment.slice
    
    highlighted_document = TextDocumentModel()
    for text_block in document_model:
        highlighted_text_block = text_block.clone()
        highlighted_document.append(highlighted_text_block)
        text_block_iterator = iter(text_block)
        text_fragment = text_block_iterator.next()
        text_slice = text_fragment.text.flat_slice()
        while True:
            # Fixme: add func in classes ?
            if highlighted_slice.is_included_in(text_slice):
                append_intersection = True
                next_highlighted_fragment = True
                next_text_fragment = False
            elif highlighted_slice.intersect(text_slice):
                append_intersection = True
                next_highlighted_fragment = highlighted_slice.stop == text_slice.stop
                next_text_fragment = True
            else:
                # highlighted_fragment is after text_fragment
                append_intersection = False
                next_highlighted_fragment = False
                next_text_fragment = True
            if append_intersection:
                text = raw_text_document[highlighted_slice & text_slice]
                highlighted_text_fragment = TextFragment(text,
                                                         frame_type=text_fragment.frame_type,
                                                         token_type=highlighted_fragment.token)
                highlighted_text_block.append(highlighted_text_fragment)
            try:
                if next_highlighted_fragment:
                    highlighted_fragment = highlighted_text_iterator.next()
                    highlighted_slice= highlighted_fragment.slice
                if next_text_fragment:
                    text_fragment = text_block_iterator.next()
                    text_slice = text_fragment.text.flat_slice()
            except StopIteration:
                break
    
    return highlighted_document

####################################################################################################
#
# End
#
####################################################################################################
