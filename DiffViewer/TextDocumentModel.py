####################################################################################################
#
# DiffViewer - Diff Viewer
# Copyright (C) Salvaire Fabrice 2012
#
####################################################################################################

# Fixme: english ...

""" This module implements a basic document model.

A document is made of text blocks that are made of text fragments.  A text block corresponds to a
chunck of lines and is decorated by a frame type.  A text fragment is a piece of text and is
decorated by a frame type and a token type used for the syntax highlighting.
"""

####################################################################################################

class TextBlock(list):

    """ This class implements a text block. """

    ##############################################

    def __init__(self, line_slice, frame_type=None):

        """ The parameter *line_slice* specifies the line slice corresponding to the text block and
        the parameter *frame_type* the type of frame.
        """

        super(TextBlock, self).__init__()

        self.line_slice = line_slice
        self.frame_type = frame_type

    ##############################################

    def __repr__(self):

        return 'Text Block: frame type=' + str(self.frame_type) + ', slice=' + repr(self.line_slice)

####################################################################################################

class TextFragment(object):

    """ This class implements a text fragment. """

    ##############################################

    def __init__(self, text, frame_type=None, token_type=None):

        """ The parameter *text* specifies the content, it must implement the Boolean
        evaluation and the unicode conversion.

        The parameter *frame_type* specifies the type of frame and the parameter *token_type* the
        type of token for the syntax highlighting.

        To test if an instance represents an non empty string use a Boolean evaluation like::

          bool(instance)

        To get the content string use::

          unicode(instance)
        """

        self.text = text
        self.frame_type = frame_type
        self.token_type = token_type

    ##############################################

    def __repr__(self):

        return 'Text Fragment: frame type=' + str(self.frame_type) \
            + ', token type=' + str(self.token_type) \
            + '\n' + ' '*2 + repr(self.text)

    ##############################################

    def __str__(self):

        """ Return the unicode text. """

        return str(self.text)

    ##############################################

    def __bool__(self):

        # Fixme: english whether

        """ Test if the text is an empty string. """

        return bool(self.text)

####################################################################################################

class TextDocumentModel(list):
    """ This class implements an ordered list of text blocks. """
    pass

####################################################################################################
#
# End
#
####################################################################################################
