####################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If
# not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import unittest

####################################################################################################

from CodeReview.Tools.AttributeDictionaryInterface import (
    ExtendedDictionaryInterface,
    ReadOnlyAttributeDictionaryInterface,
    AttributeDictionaryInterface,
    AttributeDictionaryInterfaceDescriptor)

####################################################################################################

class TestExtendedDictionaryInterface(unittest.TestCase):

    ##############################################

    def test(self):

        extended_dictionary = ExtendedDictionaryInterface()

        extended_dictionary['key1'] = 1
        self.assertEqual(extended_dictionary['key1'], 1)
        self.assertEqual(extended_dictionary.key1, 1)

        extended_dictionary.key2 = 1
        # self.assertEqual(extended_dictionary['key2'], 1) # Fixme: ?
        self.assertEqual(extended_dictionary.key2, 1)

####################################################################################################

class ReadOnlyAttributeDictionaryInterfaceExample(ReadOnlyAttributeDictionaryInterface):

    ##############################################

    def __init__(self):

        super(ReadOnlyAttributeDictionaryInterfaceExample, self).__init__()

        for i in (1, 2):
            self._dictionary['attribute' + str(i)] = int(i)

####################################################################################################

class AttributeDictionaryInterfaceExample(AttributeDictionaryInterface):

    ##############################################

    def __init__(self):

        super(AttributeDictionaryInterfaceExample, self).__init__()

        for i in (1, 2):
            self._dictionary['attribute' + str(i)] = int(i)

####################################################################################################

class DescriptorExample(object):

    ##############################################

    def __init__(self, value):

        self.value = value

    ##############################################

    def get(self):

        return self.value

    ##############################################

    def set(self, value):

        self.value = value

####################################################################################################

class AttributeDictionaryInterfaceDescriptorExample(AttributeDictionaryInterfaceDescriptor):

    ##############################################

    def __init__(self):

        super(AttributeDictionaryInterfaceDescriptorExample, self).__init__()

        for i in (1, 2):
            self._dictionary['attribute' + str(i)] = DescriptorExample(i)


####################################################################################################

class TestReadOnlyBase(object):

    ##############################################

    def test_base(self):

        self.assertTrue('attribute1' in self.obj)
        self.assertEqual(self.obj.attribute1, 1)
        self.assertEqual(self.obj['attribute1'], 1)
        self.assertEqual(self.obj.attribute2, 2)
        with self.assertRaises(NotImplementedError):
            self.obj.attribute2 = 22

####################################################################################################

class TestReadOnlyAttributeDictionaryInterface(unittest.TestCase, TestReadOnlyBase):

    ##############################################

    def setUp(self):

        self.obj = ReadOnlyAttributeDictionaryInterfaceExample()

    ##############################################

    def test_iter(self):

        # self.assertListEqual(sorted(list(iter(self.obj))), [1, 2])
        self.assertListEqual(sorted(list(iter(self.obj))), ['attribute1', 'attribute2'])

####################################################################################################

class TestBase(object):

    ##############################################

    def test_base(self):

        self.assertTrue('attribute1' in self.obj)
        self.assertEqual(self.obj.attribute1, 1)
        self.assertEqual(self.obj['attribute1'], 1)
        self.assertEqual(self.obj.attribute2, 2)
        self.obj.attribute2 = 22
        self.assertEqual(self.obj.attribute2, 22)
        #self.obj.attribute3 = 3
        #self.assertEqual(self.obj.attribute3, 3)

####################################################################################################

class TestAttributeDictionaryInterface(unittest.TestCase, TestBase):

    ##############################################

    def setUp(self):

        self.obj = AttributeDictionaryInterfaceExample()

    ##############################################

    def test_iter(self):

        # self.assertListEqual(sorted(list(iter(self.obj))), [1, 2])
        self.assertListEqual(sorted(list(iter(self.obj))), ['attribute1', 'attribute2'])

####################################################################################################

class TestAttributeDictionaryInterfaceDescriptor(unittest.TestCase, TestBase):

    ##############################################

    def setUp(self):

        self.obj = AttributeDictionaryInterfaceDescriptorExample()

    ##############################################

    def test_iter(self):

        # self.assertListEqual(sorted([x.get() for x in iter(self.obj)]), [1, 2])
        self.assertListEqual(sorted(list(iter(self.obj))), ['attribute1', 'attribute2'])

####################################################################################################

if __name__ == '__main__':

    unittest.main()
