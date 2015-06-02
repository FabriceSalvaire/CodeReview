####################################################################################################

import unittest

####################################################################################################

from DiffViewer.Tools.Slice import FlatSlice, LineSlice
from DiffViewer.RawTextDocument import RawTextDocument

####################################################################################################

class TestRawTextDocument(unittest.TestCase):

    ##############################################

    def _test_text(self, text_buffer, line_slice, sub_string):

        raw_text_document = RawTextDocument(text_buffer)
        lines = raw_text_document.lines(new_line_separator=False)
        self.assertEqual(len(lines), len(text_buffer.splitlines()))
        lines = raw_text_document.lines()
        self.assertEqual(len(text_buffer), sum([len(x) for x in lines]))
        self.assertEqual(raw_text_document.substring(FlatSlice(5, 10)), text_buffer[5:10])
        self.assertEqual(raw_text_document.substring(line_slice), sub_string)

    ##############################################

    def test_document(self):

        sub_string = 'qsdfg\r\nwxcvb\r'
        text_buffer = 'azerty\n' + sub_string + 'azerty\n'
        line_slice = LineSlice(1, 3)
        self._test_text(text_buffer, line_slice, sub_string)
        self._test_text(text_buffer + 'qsdfg', line_slice, sub_string)
        self._test_text(text_buffer[:-1] + '\r\n', line_slice, sub_string)

    ##############################################

    def test_line_of(self):

        text_buffer = "01\n34\n6"
        raw_text_document = RawTextDocument(text_buffer)
        self.assertEqual(raw_text_document.line_of(0), 0)
        self.assertEqual(raw_text_document.line_of(4), 1)
        self.assertEqual(raw_text_document.line_of(6), 2)

    ##############################################

    def test_view(self):

        text_buffer = ''
        for i in range(10):
            text_buffer += 'azerty' + str(i) + '\n'

        raw_text_document = RawTextDocument(text_buffer)
        view = raw_text_document[LineSlice(1, 3)]
        self.assertEqual(str(view).splitlines(), text_buffer.splitlines()[1:3])
        self.assertEqual(view.substring(FlatSlice(0,6)), 'azerty')

        text_buffer = "012\n45\n78\n01"
        raw_text_document = RawTextDocument(text_buffer)
        view = raw_text_document[FlatSlice(5, 11)]
        self.assertEqual(str(view).splitlines(), [x.strip() for x in view.lines()])

    ##############################################

    def test_light_view(self):

        text_buffer = 'azertyuiopqsdfghjklm'

        raw_text_document = RawTextDocument(text_buffer)
        raw_text_document.light_view_mode = True
        flat_slice = FlatSlice(5, 10)
        view = raw_text_document[flat_slice]
        self.assertEqual(str(view), text_buffer[flat_slice()])

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
