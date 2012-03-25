####################################################################################################

from PyQt4 import QtGui

####################################################################################################

from DiffViewer.RawTextDocumentDiff import chunk_type

####################################################################################################

class TextBlockStyle(object):

    ##############################################

    def __init__(self, background_colour, line_colour):

        self.background_colour = background_colour
        self.line_colour = line_colour

####################################################################################################

class TextBlockStyles(dict):

    ##############################################

    def add(self, frame_type, background_colour, line_colour):

        self[frame_type] = TextBlockStyle(background_colour, line_colour)

####################################################################################################

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

####################################################################################################
# 
# End
# 
####################################################################################################
