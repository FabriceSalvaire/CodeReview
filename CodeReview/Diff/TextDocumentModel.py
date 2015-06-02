####################################################################################################
#
# CodeReview - A Python/Qt Git GUI
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

# Fixme: english ...

"""This module implements a basic document model.

A document is made of text blocks that are themselves made of text fragments.  A text block
corresponds to a chunck of lines and is decorated by a frame type.  A text fragment is a piece of
text and is decorated by a frame type and a token type used for the syntax highlighting.

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

          str(instance)
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
