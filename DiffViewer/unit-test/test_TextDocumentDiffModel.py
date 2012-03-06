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
from TextDocumentDiffModel import TextDocumentDiffModelFactory

####################################################################################################

class TestTextDocumentModel(unittest.TestCase):

    ##############################################

    def test(self):

        with open('data/test_file1.txt') as f:
            text1 = f.read()

        with open('data/test_file2.txt') as f:
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
                                
####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
