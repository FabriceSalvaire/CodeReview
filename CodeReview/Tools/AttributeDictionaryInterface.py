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

class ExtendedDictionaryInterface(dict):

    # Fixme: This class don't work as expected

    """ This class implements an extended dictionary interface.

    Example::

      extended_dictionary = ExtendedDictionaryInterface()

      extended_dictionary['key1'] = 1
      print extended_dictionary['key1']
      print extended_dictionary.key1

      # Unusal use case
      extended_dictionary.key2 = 1
      print extended_dictionary.key2
      # print extended_dictionary['key2'] # Not Implemented

    """

    ##############################################

    def __setitem__(self, key, value):

        if key not in self and key not in self.__dict__:
            dict.__setitem__(self, key, value)
            setattr(self, key, value)
        else:
            raise KeyError

####################################################################################################

class ReadOnlyAttributeDictionaryInterface(object):

    """ This class implements a read-only attribute and dictionary interface.

    Example::

      attribute_dictionary = ReadOnlyAttributeDictionaryInterface()

      attribute_dictionary._dictionary['a'] = 1
      attribute_dictionary._dictionary['b'] = 2

      print attribute_dictionary['a']
      print attribute_dictionary.b

      'a' in attribute_dictionary
      list(attribute_dictionary)
      # will return [1, 2]

    """

    ##############################################

    def __init__(self):

        object.__setattr__(self, '_dictionary', dict())

    ##############################################

    def __getattr__(self, name):

        """ Get the value from its name. """

        return self._dictionary[name]

    ##############################################

    __getitem__ = __getattr__

    ##############################################

    def __iter__(self):

        """ Iterate over the dictionary. """

        return self.keys()

    ##############################################

    def items(self):

        return self._dictionary.items()

    ##############################################

    def keys(self):

        return self._dictionary.keys()

    ##############################################

    def values(self):

        return self._dictionary.values()

    ##############################################

    def __contains__(self, name):

        """ Test if *name* is in the dictionary. """

        return name in self._dictionary

    ##############################################

    def __setattr__(self, name, value):

        raise NotImplementedError

    ##############################################

    __setitem__ = __setattr__

####################################################################################################

class AttributeDictionaryInterface(ReadOnlyAttributeDictionaryInterface):

    """ This class implements an attribute and dictionary interface.

    Example::

      attribute_dictionary = AttributeDictionaryInterface()

      attribute_dictionary['a'] = 1
      print attribute_dictionary['a']

      attribute_dictionary.b = 2
      print attribute_dictionary.b

      'a' in attribute_dictionary
      list(attribute_dictionary)
      # will return [1, 2]

    """

    ##############################################

    def __setattr__(self, name, value):

        """ Set the value from its name. """

        self._dictionary[name] = value

    ##############################################

    __setitem__ = __setattr__

####################################################################################################

class AttributeDictionaryInterfaceDescriptor(AttributeDictionaryInterface):

    """ This class implements an attribute and dictionary interface using Descriptor.

    Example::

      class DescriptorExample(object):
          def __init__(self, value):
              self.value = value
          def get(self):
              return self.value
          def set(self, value):
              self.value = value

      attribute_dictionary = AttributeDictionaryInterfaceDescriptor()
      attribute_dictionary._dictionary['attribute1'] = DescriptorExample(1)

      attribute_dictionary['attribute1'] = 2
      print attribute_dictionary['attribute1']

      attribute_dictionary.attribute1 = 3
      print attribute_dictionary.attribute1

    """

    ##############################################

    def _get_descriptor(self, name):

        return self._dictionary[name]

    ##############################################

    def __getattr__(self, name):

        return self._get_descriptor(name).get()

    ##############################################

    def __setattr__(self, name, value):

        return self._get_descriptor(name).set(value)

    ##############################################

    __getitem__ = __getattr__
    __setitem__ = __setattr__
