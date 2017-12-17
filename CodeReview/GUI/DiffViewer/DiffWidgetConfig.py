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

"""This modules defines colour styles used by the Diff Viewer for text blocks."""

####################################################################################################

from PyQt5 import QtGui

####################################################################################################

from CodeReview.Diff.RawTextDocumentDiff import chunk_type

####################################################################################################

class TextBlockStyle:

    """This class defines colour style for a text block.

    Public attributes:

      :attr:`background_colour`
        background colour of the text block

      :attr:`line_colour`
        top and bottom line colour of the text block

    """

    ##############################################

    def __init__(self, background_colour, line_colour):

        self.background_colour = background_colour
        self.line_colour = line_colour

####################################################################################################

class TextBlockStyles(dict):

    """This class implements a dictionary of Text Block Styles indexed by the frame type."""

    ##############################################

    def add(self, frame_type, background_colour, line_colour):

        # API ?

        self[frame_type] = TextBlockStyle(background_colour, line_colour)

####################################################################################################

#: Defines the default text block styles
text_block_styles = TextBlockStyles()
for style in (
    {'frame_type':chunk_type.equal,
     'background_colour':QtGui.QColor(255, 255, 255),
     'line_colour':QtGui.QColor(0, 0, 0)},

    {'frame_type':chunk_type.insert,
     'background_colour':QtGui.QColor(180, 255, 180),
     'line_colour':QtGui.QColor(80, 210, 80)},

    {'frame_type':chunk_type.delete,
     'background_colour':QtGui.QColor(255, 160, 180),
     'line_colour':QtGui.QColor(200, 60, 90)},

    {'frame_type':chunk_type.replace,
     'background_colour':QtGui.QColor(206, 226, 250),
     'line_colour':QtGui.QColor(90, 130, 180)},

    {'frame_type':chunk_type.equal_block,
     'background_colour':QtGui.QColor(240, 240, 240),
     'line_colour':QtGui.QColor(171, 171, 171)},

    ):
    text_block_styles.add(**style)

#: Defines the background colour for intra-difference
intra_difference_background_colour = QtGui.QColor(180, 210, 250)
