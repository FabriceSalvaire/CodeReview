####################################################################################################

import unittest

####################################################################################################

from RawTextDocument import RawTextDocument
from RawTextDocumentDiff import TwoWayFileDiffFactory

####################################################################################################

class TestRawTextDocumentDiff(unittest.TestCase):

    ##############################################

    def test(self):

        with open('test_file1.txt') as f:
            text1 = f.read()

        with open('test_file2.txt') as f:
            text2 = f.read()

        raw_text_document1 = RawTextDocument(text1)
        raw_text_document2 = RawTextDocument(text2)
        
        two_way_file_diff_factory = TwoWayFileDiffFactory()
        file_diff = two_way_file_diff_factory.process(raw_text_document1, raw_text_document2)

        for group in file_diff:
            print '-'*25
            for chunk in group:
                print chunk

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
