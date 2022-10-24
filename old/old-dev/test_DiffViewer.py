#####################################################################################################

import io
import unittest

#####################################################################################################

from DiffBuffer import Slice

#####################################################################################################

class TestSyntaxHighlighter(unittest.TestCase):

    ###############################################

    def test_slice(self):

        a_slice = Slice(0, 10)
        self.assertEqual(len(a_slice), 10)
        self.assertTrue(bool(a_slice))
        self.assertEqual(a_slice.lower, 0)
        self.assertEqual(a_slice.upper, 9)

        a_slice = Slice(5, 5)
        self.assertEqual(len(a_slice), 0)
        self.assertFalse(bool(a_slice))
        self.assertIsNone(a_slice.lower)
        self.assertIsNone(a_slice.upper)

        text = 'azerty'
        a_slice = Slice(1, 2)
        self.assertEqual(text[a_slice()], 'z')

#####################################################################################################

if __name__ == '__main__':

    unittest.main()

#####################################################################################################
#
# End
#
#####################################################################################################
