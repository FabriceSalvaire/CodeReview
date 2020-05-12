####################################################################################################

def _qInstallMessageHandler(handler):
    '''Install a message handler that works in all bindings

    Args:
        handler: A function that takes 3 arguments, or None
    '''

    def messageOutputHandler(*args):
        # In Qt5 bindings, message handlers are passed 3 arguments
        # The first argument is a QtMsgType
        # The last argument is the message to be printed
        # The Middle argument (if passed) is a QMessageLogContext
        if len(args) == 3:
            msgType, logContext, msg = args
        elif len(args) == 2:
            msgType, msg = args
            logContext = None
        else:
            raise TypeError(
                'handler expected 2 or 3 arguments, got {0}'.format(len(args)))

        if isinstance(msg, bytes):
            # In python 3, some bindings pass a bytestring, which cannot be
            # used elsewhere. Decoding a python 2 or 3 bytestring object will
            # consistently return a unicode object.
            msg = msg.decode()

        handler(msgType, logContext, msg)

    if not handler:
        handler = messageOutputHandler
    return Qt._QtCore.qInstallMessageHandler(handler)
