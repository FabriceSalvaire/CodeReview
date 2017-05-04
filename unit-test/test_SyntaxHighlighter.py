####################################################################################################

import os
import unittest

from pygments.lexers import get_lexer_for_filename

####################################################################################################

from CodeReview.Diff.RawTextDocument import RawTextDocument
from CodeReview.Diff.SyntaxHighlighter import HighlightedText

####################################################################################################

class TestSyntaxHighlighter(unittest.TestCase):

    ###############################################

    def test(self):

        test_file_path = os.path.join(os.path.dirname(__file__), 'data', 'test_file1.py')
        with open(test_file_path) as f:
            text = f.read()

        raw_text_document = RawTextDocument(text)

        lexer = get_lexer_for_filename(test_file_path, stripnl=False)
        highlighted_text = HighlightedText(raw_text_document, lexer)

        for fragment in highlighted_text:
            print(repr(fragment), '[' + raw_text_document.substring(fragment.slice) + ']')

####################################################################################################

if __name__ == '__main__':

    unittest.main()
