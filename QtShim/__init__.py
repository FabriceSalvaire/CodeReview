"""Minimal Python 3 shim around PyQt5 and Pyside2 Qt bindings for QML applications.

Forked from https://github.com/mottosso/Qt.py under MIT License.
Copyright (c) 2016 Marcus Ottosson

Changes

* Dropped Python2 and Qt4 support
* Focus on last Python 3 release
* Focus on last Qt API : QML

Requirements

* make use of lazy loading to speed up startup time !
"""

# Fixme: ressource file CodeReview/QtApplication/rcc/CodeReviewRessource.py

####################################################################################################

# Enable support for `from Qt import *`
__all__ = []

####################################################################################################

import importlib
import logging
import os
import sys
import types

from .QtConfig import _common_members, _misplaced_members, _compatibility_members

####################################################################################################

# _module_logger = logging.getLogger(__name__)

####################################################################################################

# Flags from environment variables
QT_VERBOSE = bool(os.getenv('QT_VERBOSE'))

QT_PREFERRED_BINDING = os.getenv('QT_PREFERRED_BINDING', '')
if QT_PREFERRED_BINDING:
    QT_PREFERRED_BINDING = list(x for x in QT_PREFERRED_BINDING.split(',') if x)
else:
    # on dec 2018, PySide2 is still not fully operational
    QT_PREFERRED_BINDING = ('PyQt5', 'PySide2')

####################################################################################################

def _new_module(name):
    return types.ModuleType(__name__ + '.' + name)

####################################################################################################

# Reference to Qt.py
Qt = sys.modules[__name__]
Qt.QtCompat = _new_module('QtCompat')

####################################################################################################

def _log(text):
    if QT_VERBOSE:
        # _logger print
        sys.stdout.write(text + '\n')

####################################################################################################

def _import_sub_module(module, name):
    """import a submodule"""
    _log('_import_sub_module {} {}'.format(module, name))
    module_name = module.__name__ + '.' + name # e.g. PyQt5.QtCore
    module = importlib.import_module(module_name)
    return module

####################################################################################################

def _setup(module, extras):
    """Install common submodules"""

    Qt.__binding__ = module.__name__

    for name in list(_common_members) + extras:
        try:
            submodule = _import_sub_module(module, name)
        except ImportError:
            try:
                # For extra modules like sip and shiboken that may not be
                # children of the binding.
                submodule = __import__(name)
            except ImportError:
                continue

        setattr(Qt, '_' + name, submodule)

        if name not in extras:
            # Store reference to original binding
            setattr(Qt, name, _new_module(name)) # Qt.QtCore = module(so module)

####################################################################################################

def _reassign_misplaced_members(binding):
    """Apply misplaced members from `binding` to Qt.py

    Arguments:
        binding (dict): Misplaced members

    """

    for src, dst in _misplaced_members[binding].items():
        # print()
        dst_value = None

        # Fixme: to func
        src_parts = src.split('.')
        src_module = src_parts[0]
        if len(src_parts):
            src_member = src_parts[1:]
        else:
            src_member = None

        if isinstance(dst, (list, tuple)):
            dst, dst_value = dst
        # print(src, '->', dst, dst_value)
        # print(src_module, src_member)

        dst_parts = dst.split('.')
        dst_module = dst_parts[0]
        if len(dst_parts):
            dst_member = dst_parts[1]
        else:
            dst_member = None
        # print(dst_module, dst_member)

        # Get the member we want to store in the namesapce.
        if not dst_value:
            try:
                _part = getattr(Qt, '_' + src_module)
                while src_member:
                    member = src_member.pop(0)
                    _part = getattr(_part, member)
                dst_value = _part
            except AttributeError:
                # If the member we want to store in the namespace does not
                # exist, there is no need to continue. This can happen if a
                # request was made to rename a member that didn't exist, for
                # example if QtWidgets isn't available on the target platform.
                _log('Misplaced member has no source: {0}'.format(src))
                continue
        # print(dst_value)

        try:
            # Fixme: src_object ???
            src_object = getattr(Qt, dst_module)
        except AttributeError:
            # print('Failed to get src_object')
            if dst_module not in _common_members:
                # Only create the Qt parent module if its listed in
                # _common_members. Without this check, if you remove QtCore
                # from _common_members, the default _misplaced_members will add
                # Qt.QtCore so it can add Signal, Slot, etc.
                msg = "Not creating missing member module '{m}' for '{c}'"
                _log(msg.format(m=dst_module, c=dst_member))
                continue
            # If the dst is valid but the Qt parent module does not exist
            # then go ahead and create a new module to contain the member.
            setattr(Qt, dst_module, _new_module(dst_module))
            src_object = getattr(Qt, dst_module)
            # Enable direct import of the new module
            sys.modules[__name__ + '.' + dst_module] = src_object

        if not dst_value:
            dst_value = getattr(Qt, '_' + src_module)
            if src_member:
                dst_value = getattr(dst_value, src_member)

        setattr(
            src_object,
            dst_member or dst_module,
            dst_value
        )

####################################################################################################

def _build_compatibility_members(binding, decorators=None):
    """Apply `binding` to QtCompat

    Arguments:
        binding (str): Top level binding in _compatibility_members.
        decorators (dict, optional): Provides the ability to decorate the
            original Qt methods when needed by a binding. This can be used
            to change the returned value to a standard value. The key should
            be the classname, the value is a dict where the keys are the
            target method names, and the values are the decorator functions.

    """

    decorators = decorators or dict()

    # Allow optional site-level customization of the compatibility members.
    # This method does not need to be implemented in QtSiteConfig.
    try:
        import QtSiteConfig
    except ImportError:
        pass
    else:
        if hasattr(QtSiteConfig, 'update_compatibility_decorators'):
            QtSiteConfig.update_compatibility_decorators(binding, decorators)

    _QtCompat = type('QtCompat', (object,), {})

    for classname, bindings in _compatibility_members[binding].items():
        attrs = {}
        for target, binding in bindings.items():
            namespaces = binding.split('.')
            try:
                src_object = getattr(Qt, '_' + namespaces[0])
            except AttributeError as e:
                _log('QtCompat: AttributeError: %s' % e)
                # Skip reassignment of non-existing members.
                # This can happen if a request was made to
                # rename a member that didn't exist, for example
                # if QtWidgets isn't available on the target platform.
                continue

            # Walk down any remaining namespace getting the object assuming
            # that if the first namespace exists the rest will exist.
            for namespace in namespaces[1:]:
                src_object = getattr(src_object, namespace)

            # decorate the Qt method if a decorator was provided.
            if target in decorators.get(classname, []):
                # staticmethod must be called on the decorated method to
                # prevent a TypeError being raised when the decorated method
                # is called.
                src_object = staticmethod(
                    decorators[classname][target](src_object))

            attrs[target] = src_object

        # Create the QtCompat class and install it into the namespace
        compat_class = type(classname, (_QtCompat,), attrs)
        setattr(Qt.QtCompat, classname, compat_class)

####################################################################################################

def _pyside2():
    """Initialise PySide2

    These functions serve to test the existence of a binding
    along with set it up in such a way that it aligns with
    the final step; adding members from the original binding
    to Qt.py

    """

    import PySide2 as module
    extras = []
    # try:
    #     from PySide2 import shiboken2
    #     extras.append('shiboken2')
    # except ImportError:
    #     pass

    _setup(module, extras)
    Qt.__binding_version__ = module.__version__

    # if hasattr(Qt, '_shiboken2'):
    #     Qt.QtCompat.wrapInstance = _wrapinstance
    #     Qt.QtCompat.getCppPointer = _getcpppointer
    #     Qt.QtCompat.delete = shiboken2.delete

    if hasattr(Qt, '_QtCore'):
        Qt.__qt_version__ = Qt._QtCore.qVersion()

    # if hasattr(Qt, '_QtWidgets'):
    #     Qt.QtCompat.setSectionResizeMode = \
    #         Qt._QtWidgets.QHeaderView.setSectionResizeMode

    _reassign_misplaced_members('PySide2')
    # _build_compatibility_members('PySide2')

####################################################################################################

def _pyqt5():
    """Initialise PyQt5"""

    import PyQt5 as module
    extras = []
    # try:
    #     import sip
    #     extras.append(sip.__name__)
    # except ImportError:
    #     sip = None

    _setup(module, extras)
    # if hasattr(Qt, '_sip'):
    #     Qt.QtCompat.wrapInstance = _wrapinstance
    #     Qt.QtCompat.getCppPointer = _getcpppointer
    #     Qt.QtCompat.delete = sip.delete

    if hasattr(Qt, '_QtCore'):
        Qt.__binding_version__ = Qt._QtCore.PYQT_VERSION_STR
        Qt.__qt_version__ = Qt._QtCore.QT_VERSION_STR

    # if hasattr(Qt, '_QtWidgets'):
    #     Qt.QtCompat.setSectionResizeMode = \
    #         Qt._QtWidgets.QHeaderView.setSectionResizeMode

    _reassign_misplaced_members('PyQt5')
    # _build_compatibility_members('PyQt5')

####################################################################################################

def _install():

    # Default order (customise order and content via QT_PREFERRED_BINDING)
    order = QT_PREFERRED_BINDING

    available = {
        'PySide2': _pyside2,
        'PyQt5': _pyqt5,
    }

    _log("Order: {}".format(' '.join(order)))

    found_binding = False
    for name in order:
        _log('Trying %s' % name)

        try:
            available[name]()
            found_binding = True
            break

        except ImportError as e:
            _log('ImportError: %s' % e)

        except KeyError:
            _log("ImportError: Preferred binding '%s' not found." % name)

    if not found_binding:
        # If not binding were found, throw this error
        raise ImportError('No Qt binding were found.')

    # Install individual members
    for name, members in _common_members.items():
        try:
            their_submodule = getattr(Qt, '_' + name)
        except AttributeError:
            continue

        our_submodule = getattr(Qt, name)

        # Enable import *
        __all__.append(name)

        # Enable direct import of submodule,
        # e.g. import Qt.QtCore
        sys.modules[__name__ + '.' + name] = our_submodule

        for member in members:
            # Accept that a submodule may miss certain members.
            try:
                their_member = getattr(their_submodule, member)
            except AttributeError:
                _log("'%s.%s' was missing." % (name, member))
                continue
            setattr(our_submodule, member, their_member)

    # Enable direct import of QtCompat
    sys.modules['Qt.QtCompat'] = Qt.QtCompat

####################################################################################################

_install()

####################################################################################################

# Fixme: Python 3.7
# def __getattr__(name):
#     print('__getattr__', name)

####################################################################################################

# Setup Binding Enum states
Qt.IsPySide2 = Qt.__binding__ == 'PySide2'
Qt.IsPyQt5 = not Qt.IsPySide2
