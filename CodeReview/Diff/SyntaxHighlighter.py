####################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If
# not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################
#
#                                              Audit
#
# - 04/06/2012 Fabrice
#   Check design: purpose of HighlightedText ? Merge code?
#
####################################################################################################

""" This modules provides a facility to syntax highlight a text document. """

####################################################################################################

import pygments

####################################################################################################

from CodeReview.Tools.Slice import FlatSlice
from CodeReview.Diff.TextDocumentModel import TextDocumentModel, TextBlock, TextFragment

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
        the parameter *lexer* is a Pygments lexer instance.
        """

        super(HighlightedText, self).__init__()

        self.raw_text_document = raw_text_document

        self._lex(lexer)

    ##############################################

    def _lex(self, lexer):

        """ Lex the document. """

        current_location = 0
        for token, text in pygments.lex(str(self.raw_text_document), lexer):
            stop_position = current_location + len(text)
            flat_slice = FlatSlice(current_location, stop_position)
            self.append(HighlightedTextFragment(flat_slice, token))
            current_location = stop_position

####################################################################################################

def highlight_text(raw_text_document, lexer):

    """ Highlight a text.

    The parameter *raw_text_document* is a :class:`DiffViewer.RawTextDocument` instance and the
    parameter *lexer* is a Pygments lexer instance.

    Return an :class:`DiffViewer.TextDocumentModel` instance.  The document has one text block that
    contains all the fragments.  Text fragments use light views.
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
