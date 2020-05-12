####################################################################################################

def _getcpppointer(object):
    if hasattr(Qt, '_shiboken2'):
        return getattr(Qt, '_shiboken2').getCppPointer(object)[0]
    elif hasattr(Qt, '_sip'):
        return getattr(Qt, '_sip').unwrapinstance(object)
    raise AttributeError("'module' has no attribute 'getCppPointer'")

####################################################################################################

def _wrapinstance(ptr, base=None):
    '''Enable implicit cast of pointer to most suitable class

    This behaviour is available in sip per default.

    Based on http://nathanhorne.com/pyqtpyside-wrap-instance

    Usage:
        This mechanism kicks in under these circumstances.
        1. Qt.py is using PySide 1 or 2.
        2. A `base` argument is not provided.

        See :func:`QtCompat.wrapInstance()`

    Arguments:
        ptr (int): Pointer to QObject in memory
        base (QObject, optional): Base class to wrap with. Defaults to QObject,
            which should handle anything.

    '''

    assert isinstance(ptr, int), "Argument 'ptr' must be of type <int>"
    assert (base is None) or issubclass(base, Qt.QtCore.QObject), (
        "Argument 'base' must be of type <QObject>")

    if Qt.IsPyQt4 or Qt.IsPyQt5:
        func = getattr(Qt, '_sip').wrapinstance
    elif Qt.IsPySide2:
        func = getattr(Qt, '_shiboken2').wrapInstance
    elif Qt.IsPySide:
        func = getattr(Qt, '_shiboken').wrapInstance
    else:
        raise AttributeError("'module' has no attribute 'wrapInstance'")

    if base is None:
        q_object = func(int(ptr), Qt.QtCore.QObject)
        meta_object = q_object.metaObject()
        class_name = meta_object.className()
        super_class_name = meta_object.superClass().className()

        if hasattr(Qt.QtWidgets, class_name):
            base = getattr(Qt.QtWidgets, class_name)

        elif hasattr(Qt.QtWidgets, super_class_name):
            base = getattr(Qt.QtWidgets, super_class_name)

        else:
            base = Qt.QtCore.QObject

    return func(int(ptr), base)

####################################################################################################

def _translate(context, sourceText, *args):
    # In Qt4 bindings, translate can be passed 2 or 3 arguments
    # In Qt5 bindings, translate can be passed 2 arguments
    # The first argument is disambiguation[str]
    # The last argument is n[int]
    # The middle argument can be encoding[QtCore.QCoreApplication.Encoding]
    if len(args) == 3:
        disambiguation, encoding, n = args
    elif len(args) == 2:
        disambiguation, n = args
        encoding = None
    else:
        raise TypeError(
            'Expected 4 or 5 arguments, got {0}.'.format(len(args) + 2))

    if hasattr(Qt.QtCore, 'QCoreApplication'):
        app = getattr(Qt.QtCore, 'QCoreApplication')
    else:
        raise NotImplementedError(
            'Missing QCoreApplication implementation for {binding}'.format(
                binding=Qt.__binding__,
            )
        )
    if Qt.__binding__ in ('PySide2', 'PyQt5'):
        sanitized_args = [context, sourceText, disambiguation, n]
    else:
        sanitized_args = [
            context,
            sourceText,
            disambiguation,
            encoding or app.CodecForTr,
            n
        ]
    return app.translate(*sanitized_args)

####################################################################################################
####################################################################################################

def _none():
    '''Internal option (used in installer)'''

    Mock = type('Mock', (), {'__getattr__': lambda Qt, attr: None})

    Qt.__binding__ = 'None'
    Qt.__qt_version__ = '0.0.0'
    Qt.__binding_version__ = '0.0.0'
    Qt.QtCompat.loadUi = lambda uifile, baseinstance=None: None
    Qt.QtCompat.setSectionResizeMode = lambda *args, **kwargs: None

    for submodule in _common_members.keys():
        setattr(Qt, submodule, Mock())
        setattr(Qt, '_' + submodule, Mock())
