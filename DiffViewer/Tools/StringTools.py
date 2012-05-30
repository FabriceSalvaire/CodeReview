####################################################################################################
# 
# DiffViewer - Diff Viewer 
# Copyright (C) Salvaire Fabrice 2012 
# 
####################################################################################################

""" This module provides string tools. """

####################################################################################################

def remove_trailing_newline(text):

    """ Return the string *text* with only the last trailing newline (``\\\\r\\\\n``, ``\\\\r``,
    ``\\\\n``) removed.  By contrast the standard function :func:`string.rstrip` removes all the
    trailing newlines.
    """
    
    if text.endswith('\r\n'):
        return text[:-2]
    elif text[-1] in ('\n', '\r'):
        return text[:-1]
    else:
        return text
    
####################################################################################################
#
# End
#
####################################################################################################
