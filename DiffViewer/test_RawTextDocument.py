####################################################################################################

import unittest

####################################################################################################

from Slice import FlatSlice, LineSlice
from RawTextDocument import RawTextDocument

####################################################################################################

class TestRawTextDocument(unittest.TestCase):

    ##############################################

    def _test_text(self, text_buffer, sub_string):

        raw_text_document = RawTextDocument(text_buffer)
        lines = list(raw_text_document.line_iterator())
        self.assertEqual(len(lines), len(text_buffer.splitlines()))
        complete_lines = list(raw_text_document.complete_line_iterator())
        self.assertEqual(len(text_buffer), sum([len(x) for x in complete_lines]))
        self.assertEqual(raw_text_document[FlatSlice(5,10)], text_buffer[5:10])
        self.assertEqual(raw_text_document[LineSlice(1,3)], sub_string)

    ##############################################

    def test(self):

        sub_string = 'qsdfg\r\nwxcvb\r'
        text_buffer = 'azerty\n' + sub_string + 'azerty\n'
        self._test_text(text_buffer, sub_string)
        self._test_text(text_buffer + 'qsdfg', sub_string)
        self._test_text(text_buffer[:-1] + '\r\n', sub_string)

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
