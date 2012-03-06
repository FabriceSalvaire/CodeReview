####################################################################################################

import pygments

####################################################################################################

from Slice import FlatSlice

####################################################################################################

class HighlightedTextFragment(object):

    ##############################################

    def __init__(self, flat_slice, token):

        self.slice = flat_slice
        self.token = token

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
#
# End
#
####################################################################################################
