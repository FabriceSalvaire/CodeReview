####################################################################################################

import os
import unittest

####################################################################################################

from CodeReview.Diff.RawTextDocument import RawTextDocument
from CodeReview.Diff.RawTextDocumentDiff import TwoWayFileDiffFactory

####################################################################################################

class TestRawTextDocumentDiff(unittest.TestCase):

    ##############################################

    @staticmethod
    def _join_data_path(filename):

        return os.path.join(os.path.dirname(__file__), 'data', filename)

    ##############################################

    @unittest.skip
    def test(self):

        with open(self._join_data_path('test_file1.py')) as f:
            text1 = f.read()

        with open(self._join_data_path('test_file2.py')) as f:
            text2 = f.read()

        raw_text_document1 = RawTextDocument(text1)
        raw_text_document2 = RawTextDocument(text2)

        two_way_file_diff_factory = TwoWayFileDiffFactory()
        file_diff = two_way_file_diff_factory.process(raw_text_document1, raw_text_document2)

        file_diff.pretty_print()
        file_diff.print_unidiff()

        print('='*10)
        replace_group = file_diff[1]
        print(replace_group)
        print(replace_group[1].chunk1)
        print(list(replace_group[1].chunk1.line_iterator()))
        print(list(replace_group[1].chunk2.line_iterator()))
        print(list(replace_group[1].chunk1.line_slice_iterator()))

    ##############################################

    def test_empty(self):

        text1 = ''

        with open(self._join_data_path('test_file2.py')) as f:
            text2 = f.read()

        raw_text_document1 = RawTextDocument(text1)
        raw_text_document2 = RawTextDocument(text2)

        two_way_file_diff_factory = TwoWayFileDiffFactory()
        file_diff = two_way_file_diff_factory.process(raw_text_document1, raw_text_document2)

        file_diff.pretty_print()
        file_diff.print_unidiff()

####################################################################################################

if __name__ == '__main__':

    unittest.main()
