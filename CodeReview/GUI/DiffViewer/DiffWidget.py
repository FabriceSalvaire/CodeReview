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

####################################################################################################

import logging

####################################################################################################

from PyQt5 import QtCore, QtGui, QtWidgets

####################################################################################################

from CodeReview.Diff.RawTextDocumentDiff import chunk_type
from CodeReview.Common.Math.Functions import number_of_digits, rint
from CodeReview.Common.IteratorTools import pairwise, iter_with_last_flag
from CodeReview.Common.StringTools import remove_trailing_newline
import CodeReview.GUI.DiffViewer.DiffWidgetConfig as DiffWidgetConfig
from .SyntaxHighlighterStyle import SyntaxHighlighterStyle

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

LEFT, RIGHT = list(range(2))

def side_iterator():
    return range(2)

####################################################################################################

class TextBlock:

    """This class stores the y top and bottom positions of a text block and the frame type."""

    ##############################################

    def __init__(self, y_top, y_bottom, frame_type):

        self.y_top, self.y_bottom = y_top, y_bottom
        self.frame_type = frame_type

    ##############################################

    def __repr__(self):

        return 'TextBlock [%u, %u] frame type: %s' % (self.y_top, self.y_bottom, str(self.frame_type))

####################################################################################################

class TextBlocks(list):

    """This class represents a list of text blocks."""

    ##############################################

    def add(self, y_top, y_bottom, frame_type):

        self.append(TextBlock(y_top, y_bottom, frame_type))

####################################################################################################

class DiffViewerCursor:

    ##############################################

    def __init__(self, cursor, text_blocks):

        self._cursor = cursor
        self._text_blocks = text_blocks
        self._insert = True

    ##############################################

    def y(self):

        """Return the top position of the current block."""

        return self._cursor.block().layout().position().y()

    ##############################################

    def begin_block(self, side, frame_type, aligned_mode=False):

        block_format = QtGui.QTextBlockFormat()
        if frame_type == chunk_type.header:
            block_format.setBottomMargin(20) # Fixme: font size
        else:
            block_format.setTopMargin(3)
            block_format.setBottomMargin(3)
        if self._insert:
            self._cursor.insertBlock(block_format)
        self._text_blocks.add(self.y(), 0, frame_type)
        if (not aligned_mode
            and ((side == LEFT and frame_type == chunk_type.insert) or
                 (side == RIGHT and frame_type == chunk_type.delete))):
            # Fixme: check
            # then it is an empty block, the inserted block will be used later
            self._insert = False
        else:
            self._insert = True

    ##############################################

    def insert_text(self, text, text_format=None, last_text_fragment=False):

        if text_format is None:
            text_format = QtGui.QTextCharFormat()
        if last_text_fragment:
            text = remove_trailing_newline(text)
        if text:
            self._cursor.insertText(text, text_format)

    ##############################################

    def end(self):

        """Insert a block and set the y positions."""

        self._cursor.insertBlock()
        self._text_blocks[-1].y_bottom = self.y()
        for text_block0, text_block1 in pairwise(self._text_blocks):
            text_block0.y_bottom = text_block1.y_top

####################################################################################################

class TextBrowser(QtWidgets.QTextBrowser):

    ##############################################

    def __init__(self, parent, text_blocks):

        # Fixme: text_blocks should not be passed like this

        super(TextBrowser, self).__init__(parent)

        self._text_blocks = text_blocks

        # Truncate long lines
        self.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

    ##############################################

    def paintEvent(self, event):

        width = self.width()

        y = self.verticalScrollBar().value()
        y_min = event.rect().top()
        y_max = event.rect().bottom()

        painter = QtGui.QPainter(self.viewport())
        painter.setClipRect(event.rect())

        for text_block in self._text_blocks:
            if text_block.frame_type is None or text_block.frame_type == chunk_type.equal:
                continue
            # Shift text block in the viewport
            # ensure type is int for painter.func
            y_top = rint(text_block.y_top - y)
            y_bottom = rint(text_block.y_bottom - y)
            if y_bottom < y_min:
                continue
            if y_top > y_max:
                break
            if text_block.frame_type == chunk_type.header:
                pen = QtGui.QPen(QtCore.Qt.black)
                pen_width = 3
                pen.setWidth(pen_width)
                painter.setPen(pen)
                yy = y_bottom - 2*pen_width
                painter.drawLine(0, yy, width, yy)
            else:
                y_top -= 1
                y_bottom += 1
                text_block_style = DiffWidgetConfig.text_block_styles[text_block.frame_type]
                # Paint the background
                painter.fillRect(0,  y_top, width, y_bottom - y_top, text_block_style.background_colour)
                # Paint horizontal lines
                pen = QtGui.QPen(text_block_style.line_colour)
                pen_width = 1
                pen.setWidth(pen_width)
                painter.setPen(pen)
                painter.drawLine(0, y_top, width, y_top)
                painter.drawLine(0, y_bottom, width, y_bottom)

        del painter

        # Paint text
        super(TextBrowser, self).paintEvent(event)

####################################################################################################

class SplitterHandle(QtWidgets.QSplitterHandle):

    ##############################################

    def __init__(self, parent):

        super(SplitterHandle, self).__init__(QtCore.Qt.Horizontal, parent)

        application_style = QtWidgets.QApplication.style()
        self._frame_width = application_style.pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)

    ##############################################

    def paintEvent(self, event):

        diff_view = self.parent()

        painter = QtGui.QPainter(self)
        painter.setClipRect(event.rect())

        width = self.width()
        height = self.height()

        y_correction = self._frame_width + 2 # Fixme: ?
        y_left, y_right = [browser.verticalScrollBar().value() - y_correction
                           for browser in diff_view._browsers]

        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        for text_block_left, text_block_right in zip(*diff_view._text_blocks):
            # print text_block_left, text_block_right

            if (text_block_left.frame_type is None
                or text_block_left.frame_type in (chunk_type.equal, chunk_type.header)):
                continue

            # ensure type is int for painter.func
            y_top_left = rint(text_block_left.y_top - y_left -1)
            y_bottom_left = rint(text_block_left.y_bottom - y_left +1)
            y_top_right = rint(text_block_right.y_top - y_right -1)
            y_bottom_right = rint(text_block_right.y_bottom - y_right +1)

            if y_top_left < 0 and y_bottom_right < 0:
                continue
            if y_top_left > height and y_top_right > height:
                break

            text_block_style = DiffWidgetConfig.text_block_styles[text_block_left.frame_type]

            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(text_block_style.background_colour)
            polygon = QtGui.QPolygon(4)
            polygon.setPoints(0, y_top_left, width, y_top_right, width, y_bottom_right, 0, y_bottom_left)
            painter.drawConvexPolygon(polygon)

            painter.setPen(text_block_style.line_colour)
            painter.setRenderHints(QtGui.QPainter.Antialiasing, y_top_left != y_top_right)
            painter.drawLine(0, y_top_left, width, y_top_right)
            painter.setRenderHints(QtGui.QPainter.Antialiasing, y_bottom_left != y_bottom_right)
            painter.drawLine(0, y_bottom_left, width, y_bottom_right)

        del painter

####################################################################################################

class DiffView(QtWidgets.QSplitter):

    """Widget to show differences in side-by-side format."""

    _logger = _module_logger.getChild('DiffView')

    ##############################################

    def __init__(self, parent=None):

        super(DiffView, self).__init__(QtCore.Qt.Horizontal, parent)

        self.setHandleWidth(30)

        self._syntax_highlighter_style = SyntaxHighlighterStyle()

        self._documents = (QtGui.QTextDocument(), QtGui.QTextDocument())
        self._text_blocks = (TextBlocks(), TextBlocks())
        self._browsers = [TextBrowser(self, text_block) for text_block in self._text_blocks]
        cursors = [QtGui.QTextCursor(document) for document in self._documents]
        self._cursors = [DiffViewerCursor(cursors[side], self._text_blocks[side])
                         for side in side_iterator()]

        for i, (browser, document) in enumerate(zip(self._browsers, self._documents)):
            document.setUndoRedoEnabled(False)
            self.setCollapsible(i, False)
            browser.setDocument(document)
            self.addWidget(browser)
        self.set_font()

        self._ignore_scroll_bar_update_signal = False
        for browser in self._browsers:
            for scroll_bar in browser.horizontalScrollBar(), browser.verticalScrollBar():
                callback = lambda value, scroll_bar=scroll_bar: self.update_scroll_bar(scroll_bar, value)
                scroll_bar.valueChanged.connect(callback)

    ##############################################

    def set_font(self, font_size=None):

        if font_size is None:
            # Get the defaul font size
            font_size = QtWidgets.QApplication.font().pointSize()

        font = QtGui.QFont('', font_size)
        font.setFixedPitch(True)
        font.setStyleHint(QtGui.QFont.TypeWriter)

        self._logger.info('Monospaced Font familly is ' + QtGui.QFontInfo(font).family())

        for browser, document in zip(self._browsers, self._documents):
            document.setDefaultFont(font)

    ##############################################

    def createHandle(self):

        return SplitterHandle(self)

    ##############################################

    def update_scroll_bar(self, scroll_bar, value):

        if self._ignore_scroll_bar_update_signal:
            return

        if scroll_bar.orientation() == QtCore.Qt.Horizontal:
            method = TextBrowser.horizontalScrollBar
        else:
            method = TextBrowser.verticalScrollBar
        scroll_bar1, scroll_bar2 = [method(browser) for browser in self._browsers]
        if scroll_bar is scroll_bar2:
            scroll_bar1, scroll_bar2 = scroll_bar2, scroll_bar1

        maximum1 = scroll_bar1.maximum()
        if maximum1:
            value = rint(scroll_bar2.minimum() + scroll_bar2.maximum() * (value - scroll_bar1.minimum()) / maximum1)
            # cannot use blockSignals
            self._ignore_scroll_bar_update_signal = True
            scroll_bar2.setValue(value)
            self._ignore_scroll_bar_update_signal = False
        self.handle(1).update()

    ##############################################

    def clear(self):

        for i in range(2):
            self._browsers[i].clear()
            self._documents[i].clear()
            self._text_blocks[i].clear()
        self.update()

    ##############################################

    def _insert_metadata(self, cursor, document_model):

        metadata = document_model.metadata
        bold_text_format = QtGui.QTextCharFormat()
        # Fixme: font looks bad
        # bold_text_format.setFontWeight(QtGui.QFont.Bold)
        # Fixme: metadata.path
        cursor.insert_text(metadata['path'], bold_text_format, chunk_type.header)

    ##############################################

    def _append_document_on_side(self, side, document_model,
                                 aligned_mode,
                                 complete_mode,
                                 line_number_mode,
                                ):

        cursor = self._cursors[side]

        if line_number_mode:
            previous_line_number = -1
            last_line_number = document_model[-1].line_slice.upper
            line_number_pattern = '{:' + str(number_of_digits(last_line_number)) + '} | '

        if document_model.metadata is not None:
            cursor.begin_block(side, chunk_type.header)
            self._insert_metadata(cursor, document_model)

        for text_block in document_model:
            cursor.begin_block(side, text_block.frame_type, aligned_mode)
            if text_block.frame_type != chunk_type.equal_block or complete_mode:
                for text_fragment, last_text_fragment in iter_with_last_flag(text_block):
                    text_format = self._syntax_highlighter_style[text_fragment.token_type]
                    if (text_block.frame_type == chunk_type.replace and
                        text_fragment.frame_type != chunk_type.equal):
                        text_format.setBackground(DiffWidgetConfig.intra_difference_background_colour)
                    if line_number_mode:
                        line_slice = text_block.line_slice
                        line_number = line_slice.start
                        for line in text_fragment.text.line_iterator():
                            if line_number > previous_line_number:
                                cursor.insert_text(line_number_pattern.format(line_number +1))
                            cursor.insert_text(str(line), text_format, line_number == line_slice.upper)
                            previous_line_number = line_number
                            line_number += 1
                    else:
                        cursor.insert_text(str(text_fragment), text_format, last_text_fragment)
                if aligned_mode:
                    delta = text_block.alignment_padding()
                    if delta:
                        padding = '\n'*delta # same as last_text_fragment=True
                        cursor.insert_text(padding)

    ##############################################

    def append_document_models(self, document_models,
                               aligned_mode=True,
                               complete_mode=True,
                               line_number_mode=True,
                              ):

        for side, document_model in enumerate(document_models):
            self._append_document_on_side(side, document_model,
                                          aligned_mode, complete_mode, line_number_mode)

    ##############################################

    def set_document_models(self, document_models,
                            aligned_mode=True,
                            complete_mode=True,
                            line_number_mode=True,
                           ):

        self.clear()
        self.append_document_models(document_models, aligned_mode, complete_mode, line_number_mode)
        for cursor in self._cursors:
            cursor.end()
