####################################################################################################

import io
import unittest

from pygments.lexers import get_lexer_for_filename

####################################################################################################

from DiffViewer.RawTextDocument import RawTextDocument
from DiffViewer.SyntaxHighlighter import HighlightedText

####################################################################################################

class TestSyntaxHighlighter(unittest.TestCase):

    ###############################################

    def test(self):

        with open('data/test_file1.py') as f:
            text = f.read()

        raw_text_document = RawTextDocument(text)
        
        lexer = get_lexer_for_filename('data/test_file1.py', stripnl=False)
        highlighted_text = HighlightedText(raw_text_document, lexer)

        for fragment in highlighted_text:
            print repr(fragment), '[' + raw_text_document.substring(fragment.slice) + ']'
        
####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
