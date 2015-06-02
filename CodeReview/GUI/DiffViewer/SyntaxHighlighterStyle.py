####################################################################################################
#
# CodeReview - A Python/Qt Git GUI
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

""" This module defines styles for syntax highlighting. """

####################################################################################################

from PyQt5 import QtGui
from pygments.styles import get_style_by_name

####################################################################################################

def to_brush(colour):
    """ Convert a Pygments colour rrggbb to a Qt brush compatible object. """
    return QtGui.QColor("#" + colour)

####################################################################################################

class SyntaxHighlighterStyle(dict):

    """ This class defines a QTextCharFormat for each type of tokens defined by Pygments.

    This class has a dictionnary interface and return a copy of the QTextCharFormat instance.
    """

    ##############################################

    def __init__(self, style='default'):

        """ The parameter *style* select the Pygments style.

        Pygments style attributes are:

        * bgcolor,
        * bold,
        * border,
        * color,
        * italic,
        * mono,
        * roman,
        * sans,
        * underline.

        """

        pygments_style = get_style_by_name(style)
        for token, style_attributes in pygments_style.list_styles():
            text_format = QtGui.QTextCharFormat()
            if style_attributes['bgcolor']:
                text_format.setBackground(to_brush(style_attributes['bgcolor']))
            if style_attributes['color']:
                text_format.setForeground(to_brush(style_attributes['color']))
            if style_attributes['bold']:
                text_format.setFontWeight(QtGui.QFont.Bold)
            if style_attributes['italic']:
                text_format.setFontItalic(True)
            self[token] = text_format

    ##############################################

    def __getitem__(self, key):

        """ Return a copy of the QTextCharFormat for the corresponding key. """

        text_char_format = super(SyntaxHighlighterStyle, self).__getitem__(key)

        return QtGui.QTextCharFormat(text_char_format)

####################################################################################################
#
# End
#
####################################################################################################
