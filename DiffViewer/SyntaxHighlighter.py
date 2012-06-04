####################################################################################################
# 
# DiffViewer - Diff Viewer 
# Copyright (C) Salvaire Fabrice 2012 
# 
####################################################################################################

####################################################################################################
#
#                                              Audit
#
# - 02/04/2012 Fabrice
#   Check design: purpose of HighlightedText ? Merge code?
#
####################################################################################################

""" This modules provides facility to syntax highlight a text document. """

####################################################################################################

import pygments

####################################################################################################

from DiffViewer.Tools.Slice import FlatSlice
from DiffViewer.TextDocumentModel import TextDocumentModel, TextBlock, TextFragment

####################################################################################################

class HighlightedTextFragment(object):

    """ This class implements an highlighted text fragment. """

    ##############################################

    def __init__(self, flat_slice, token):

        """ The parameter *token* specifies the Pygments token type.

        Public Attributes:

          :attr:`slice`

          :attr:`token`          
        """

        self.slice = flat_slice
        self.token = token

    ##############################################

    def __repr__(self):

        return repr(self.slice) + ' ' + str(self.token)
        
####################################################################################################

class HighlightedText(list):

    """ This class implements an highlighted text. """

    ##############################################

    def __init__(self, raw_text_document, lexer):

        """ The parameter *raw_text_document* is a :class:`DiffViewer.RawTextDocument` instance and
        the parameter *lexer* is Pygments lexer instance.
        """

        super(HighlightedText, self).__init__()

        self.raw_text_document = raw_text_document

        self._lex(lexer)

    ##############################################
    
    def _lex(self, lexer):

        """ Lex the document. """

        current_location = 0
        for token, text in pygments.lex(unicode(self.raw_text_document), lexer):
            stop_position = current_location + len(text)
            flat_slice = FlatSlice(current_location, stop_position)
            self.append(HighlightedTextFragment(flat_slice, token))
            current_location = stop_position

####################################################################################################

def highlight_text(raw_text_document, lexer):

    """ Highlight a text.

    The parameter *raw_text_document* is a :class:`DiffViewer.RawTextDocument` instance and the
    parameter *lexer* is Pygments lexer instance.

    Return an :class:`TextDocumentModel` instance.  The document has one text block that contains
    all the fragments.  Text fragments use light views.
    """

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
