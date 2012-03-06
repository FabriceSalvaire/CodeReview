####################################################################################################

__all__ = ['EnumFactory', 'ExplicitEnumFactory']

####################################################################################################

class ReadOnlyMetaClass(type):

    ###############################################

    def __setattr__(self, name, value):

        raise NotImplementedError

####################################################################################################

class EnumMetaClass(ReadOnlyMetaClass):

    ###############################################

    def __len__(self):

        return self._size

####################################################################################################

class ExplicitEnumMetaClass(ReadOnlyMetaClass):

    ###############################################

    def __contains__(self, item):

        return item in self.constants

####################################################################################################

class EnumConstant(object):

    ##############################################
    
    def __init__(self, name, value):

        self._name = name
        self._value = value

    ##############################################
    
    def __eq__(self, other):

        return self._value == int(other)
        
    ##############################################
    
    def __int__(self):

        return self._value

    ##############################################
    
    def __repr__(self):

        return self._name
    
####################################################################################################

def EnumFactory(enum_name, enum_tuple):

    obj_dict = {}
    obj_dict['_size'] = len(enum_tuple)
    for value, name in enumerate(enum_tuple):
        obj_dict[name] = EnumConstant(name, value)

    return EnumMetaClass(enum_name, (), obj_dict)

####################################################################################################

def ExplicitEnumFactory(enum_name, enum_dict):

    obj_dict = {}
    obj_dict['constants'] = enum_dict.values()
    for name, value in enum_dict.items():
        obj_dict[name] = EnumConstant(name, value)

    return ExplicitEnumMetaClass(enum_name, (), obj_dict)

####################################################################################################
#
# End
#
####################################################################################################
