####################################################################################################

import pygments

####################################################################################################

from Slice import FlatSlice
from TextDocumentModel import TextDocumentModel, TextBlock, TextFragment

####################################################################################################

class HighlightedTextFragment(object):

    ##############################################

    def __init__(self, flat_slice, token):

        self.slice = flat_slice
        self.token = token

    ##############################################

    def __repr__(self):

        return repr(self.slice) + ' ' + str(self.token)
        
####################################################################################################

class HighlightedText(list):

    ##############################################

    def __init__(self, raw_text_document, lexer):

        super(HighlightedText, self).__init__()

        self.raw_text_document = raw_text_document

        self._lex(lexer)

    ##############################################
    
    def _lex(self, lexer):

        current_location = 0
        for token, text in pygments.lex(unicode(self.raw_text_document), lexer):
            stop_position = current_location + len(text)
            flat_slice = FlatSlice(current_location, stop_position)
            self.append(HighlightedTextFragment(flat_slice, token))
            current_location = stop_position

####################################################################################################

def highlight_text(raw_text_document, lexer):

    highlighted_text = HighlightedText(raw_text_document, lexer)

    document = TextDocumentModel()
    text_block = TextBlock(raw_text_document.line_slice)
    document.append(text_block)
    for highlighted_fragment in highlighted_text:
        text_fragment = TextFragment(raw_text_document.light_view(highlighted_fragment.slice),
                                     token_type=highlighted_fragment.token)
        text_block.append(text_fragment)

    return document
        
####################################################################################################
#
# End
#
####################################################################################################
