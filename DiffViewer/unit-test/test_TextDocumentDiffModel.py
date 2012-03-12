####################################################################################################

#
# obj: TextView, link to pair
# replace TextFragment
#

####################################################################################################

import sys
import unittest

####################################################################################################

from RawTextDocument import RawTextDocument
from RawTextDocumentDiff import TwoWayFileDiffFactory
from SyntaxHighlighter import HighlightedText
from TextDocumentModel import TextDocumentModel, TextFragment
from TextDocumentDiffModel import TextDocumentDiffModelFactory, TextBlockDiff

####################################################################################################

class TestTextDocumentModel(unittest.TestCase):

    ##############################################

    def test(self):

        with open('data/test_file1.py') as f:
            text1 = f.read()

        with open('data/test_file2.py') as f:
            text2 = f.read()

        raw_text_document1 = RawTextDocument(text1)
        raw_text_document2 = RawTextDocument(text2)
        file_diff = TwoWayFileDiffFactory().process(raw_text_document1, raw_text_document2)
        document_model1, document_model2 = TextDocumentDiffModelFactory().process(file_diff)

        print 'Document 1:'
        self._pretty_print(document_model1)
        print '\nDocument 2:'
        self._pretty_print(document_model2)
        
    ##############################################

    def _pretty_print(self, document_model):
        
        for text_block in document_model:
            print '='*100
            print text_block
            for text_fragment in text_block:
                margin = ' '*2
                print margin + '-'*48
                print margin + ('\n' + margin).join(repr(text_fragment).splitlines())
                if bool(text_fragment):
                    line = '#'*100
                    print line
                    print unicode(text_fragment).rstrip()
                    print line

    ##############################################

    def _highlight(self, raw_text_document, document_model):
                
        lexer = get_lexer_for_filename('data/test_file1.py', stripnl=False)
        highlighted_text = HighlightedText(raw_text_document, lexer)

        highlighted_text_iterator = iter(highlighted_text)
        highlighted_fragment = highlighted_text_iterator.next()

        highlighted_document = DocumentModel()
        for text_block in document_model:
            highlighted_text_block = text_block.clone()
            highlighted_document.append(highlighted_text_block)
            text_block_iterator = iter(text_block)
            text_fragment = text_block_iterator.next()
            while True:
                # highlighted_fragment is included in text_fragment
                #   - append intersection
                #   - get next highlighted_fragment and loop
                #
                # highlighted_fragment intersect with text_fragment
                #   - append intersection
                #   - get next text_fragment and loop
                #
                # highlighted_fragment is after text_fragment
                #   - get next text_fragment and loop
                #
                
                #intersection = text_fragment.split(highlighted_fragment)
                #if intersection:
                #    highlighted_text_block.append(intersection)
                #    highlighted_fragment = highlighted_text_iterator.next()
                #    else:
                #        break
                        
####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
