####################################################################################################

#
# obj: TextView, link to pair
# replace TextFragment
#

####################################################################################################

import sys
import unittest

from pygments.lexers import get_lexer_for_filename

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
        print '\nHighlighted Document 1:'
        highlighted_document1 = self._highlight(raw_text_document1, document_model1)
        self._pretty_print(highlighted_document1)
        # print '\nDocument 2:'
        # self._pretty_print(document_model2)
                
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
                    next_highlighted_fragment = False
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
                if next_highlighted_fragment:
                    highlighted_fragment = highlighted_text_iterator.next()
                    highlighted_slice= highlighted_fragment.slice
                if next_text_fragment:
                    try:
                        text_fragment = text_block_iterator.next()
                        text_slice = text_fragment.text.flat_slice()
                    except StopIteration:
                        break

        return highlighted_document
                    
####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
