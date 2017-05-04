####################################################################################################

import unittest

####################################################################################################

from CodeReview.Tools.EnumFactory import EnumFactory, ExplicitEnumFactory

####################################################################################################

class TestEnumFactory(unittest.TestCase):

    def test(self):

        enum1 = EnumFactory('Enum1', ('cst1', 'cst2'))

        self.assertEqual(enum1.cst1, 0)
        self.assertEqual(repr(enum1.cst1), 'cst1')
        self.assertEqual(str(enum1.cst1), 'cst1')
        self.assertEqual(enum1.cst2, 1)
        self.assertEqual(repr(enum1.cst2), 'cst2')
        self.assertEqual(str(enum1.cst2), 'cst2')
        self.assertEqual(len(enum1), 2)

        enum2 = ExplicitEnumFactory('Enum2', {'cst1':1, 'cst2':3})

        self.assertEqual(enum2.cst1, 1)
        self.assertEqual(enum2.cst2, 3)

        self.assertTrue(enum2.cst2 in enum2)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
