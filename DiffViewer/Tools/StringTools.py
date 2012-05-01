####################################################################################################
# 
# DiffViewer - Diff Viewer 
# Copyright (C) Salvaire Fabrice 2012 
# 
####################################################################################################

""" This module provides string tools. """

####################################################################################################

def suppress_trailing_newline(text):

    """ Return *text* with the last trailing newline ('\\\\r\\\\n', '\\\\r', '\\\\n') removed
    (:func:`string.rstrip` removes all the trailing newlines).
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
