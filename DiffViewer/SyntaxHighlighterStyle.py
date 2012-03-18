####################################################################################################
# 
# - 
# Copyright (C) 2012 
# 
####################################################################################################

####################################################################################################

from pygments.styles import get_style_by_name

from PyQt4 import QtGui, QtCore

####################################################################################################

class SyntaxHighlighterStyle(dict):

    ##############################################
    
    def __init__(self, style='default'):

        pygments_style = get_style_by_name(style)
        for token, style_attributes in pygments_style.list_styles():
            # style attributes: bgcolor, bold, border, color, italic, mono, roman, sans, underline
            text_format = QtGui.QTextCharFormat()
            def to_brush(colour):
                return QtGui.QBrush(QtGui.QColor("#" + colour))
            if style_attributes['bgcolor']:
                text_format.setBackground(to_brush(style_attributes['bgcolor']))
            if style_attributes['color']:
                text_format.setForeground(to_brush(style_attributes['color']))
            if style_attributes['bold']:
                text_format.setFontWeight(QtGui.QFont.Bold)
            if style_attributes['italic']:
                text_format.setFontItalic(True)
            self[token] = text_format
            
####################################################################################################
# 
# End
# 
####################################################################################################
