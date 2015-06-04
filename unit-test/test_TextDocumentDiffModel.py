####################################################################################################

#
# obj: TextView, link to pair
# replace TextFragment
#

####################################################################################################

import os
import unittest

from pygments.lexers import get_lexer_for_filename

####################################################################################################

from CodeReview.Diff.RawTextDocument import RawTextDocument
from CodeReview.Diff.RawTextDocumentDiff import TwoWayFileDiffFactory
from CodeReview.Diff.SyntaxHighlighter import HighlightedText
from CodeReview.Diff.TextDocumentDiffModel import TextDocumentDiffModelFactory, highlight_document

####################################################################################################

class TestTextDocumentModel(unittest.TestCase):

    ##############################################

    @staticmethod
    def _join_data_path(filename):

        return os.path.join(os.path.dirname(__file__), 'data', filename)

    ##############################################

    def test(self):

        with open(self._join_data_path('test_file1.py')) as f:
            text1 = f.read()

        with open(self._join_data_path('test_file2.py')) as f:
            text2 = f.read()

        lexer = get_lexer_for_filename('data/test_file1.py', stripnl=False)
        
        raw_text_document1 = RawTextDocument(text1)
        raw_text_document2 = RawTextDocument(text2)
        file_diff = TwoWayFileDiffFactory().process(raw_text_document1, raw_text_document2)
        document_model1, document_model2 = TextDocumentDiffModelFactory().process(file_diff)

        highlighted_text1 = HighlightedText(raw_text_document1, lexer)
        
        print('Document 1:')
        self._pretty_print(document_model1)
        print('\nHighlighted Document 1:')
        highlighted_document1 = highlight_document(document_model1, highlighted_text1)
        self._pretty_print(highlighted_document1)
        # print '\nDocument 2:'
        # self._pretty_print(document_model2)
                
    ##############################################

    def _pretty_print(self, document_model):
        
        for text_block in document_model:
            print('='*100)
            print(text_block)
            for text_fragment in text_block:
                margin = ' '*2
                print(margin + '-'*48)
                print(margin + ('\n' + margin).join(repr(text_fragment).splitlines()))
                if bool(text_fragment):
                    line = '#'*100
                    print(line)
                    print(str(text_fragment).rstrip())
                    print(line)

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
