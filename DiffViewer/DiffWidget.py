####################################################################################################

from PyQt4 import QtGui, QtCore

####################################################################################################

from DiffViewer.DiffWidgetConfig import text_block_styles
from DiffViewer.RawTextDocumentDiff import chunk_type
from DiffViewer.SyntaxHighlighterStyle import SyntaxHighlighterStyle

####################################################################################################

def get_monospaced_font():

    # Get the defaul font size
    size = QtGui.QApplication.font().pointSize()
    
    font = QtGui.QFont('', size)
    font.setFixedPitch(True)
    font.setStyleHint(QtGui.QFont.TypeWriter)

    print 'Monospaced Font familly is', QtGui.QFontInfo(font).family()
    
    return font

####################################################################################################

class TextBlock(object):

    ##############################################

    def __init__(self, y_top, y_bottom, frame_type):

        self.y_top, self.y_bottom = y_top, y_bottom
        self.frame_type = frame_type

    ##############################################

    def __repr__(self):

        return 'TextBlock [%u, %u] frame type: %s' % (self.y_top, self.y_bottom, str(self.frame_type))
        
####################################################################################################
        
class TextBlocks(list):

    ##############################################

    def add(self, y_top, y_bottom, frame_type):

        self.append(TextBlock(y_top, y_bottom, frame_type))

####################################################################################################

class DiffViewerCursor(object):

    ##############################################

    def __init__(self, cursor, text_blocks):

        self.cursor = cursor
        self.text_blocks = text_blocks

        self.begin_y = None
        self.frame_type = None
        
    ##############################################

    def y(self):

        return self.cursor.block().layout().position().y()

    ##############################################

    def begin_block(self, frame_type, i):

        self.begin_y = self.y()
        self.frame_type = frame_type
        text_block_format = QtGui.QTextBlockFormat()
        if i & 1 == 0:
            text_block_format.setBackground(QtGui.QColor(220, 220, 220))
        else:
            text_block_format.setBackground(QtGui.QColor(240, 240, 240))
        if i > 0:
            self.cursor.insertBlock(text_block_format)

    ##############################################

    def insert_text(self, text, text_format):

        self.cursor.insertText(text, text_format)
        
    ##############################################

    def end_block(self):

        end_y = self.y()
        self.text_blocks.add(self.begin_y -1, end_y +1, self.frame_type)
    
####################################################################################################

class TextBrowser(QtGui.QTextBrowser):

    ##############################################
    
    def __init__(self, parent, text_blocks):

        super(TextBrowser, self).__init__(parent)

        self.text_blocks = text_blocks
        
        # Truncate long lines
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)

    ##############################################
        
    def paintEvent(self, event):

        width = self.width()

        y = self.verticalScrollBar().value()
        y_min = event.rect().top()
        y_max = event.rect().bottom()

        print 'y, y_min, y_max:', y, y_min, y_max
        
        painter = QtGui.QPainter(self.viewport())
        painter.setClipRect(event.rect())

        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(1)
        painter.setPen(pen)
        
        for text_block in self.text_blocks:

            print text_block

            if text_block.frame_type is None or text_block.frame_type == chunk_type.equal:
                continue

            # Shift text block in the viewport
            y_top = text_block.y_top - y
            y_bottom = text_block.y_bottom - y
            if y_bottom < y_min:
                continue
            if y_top > y_max:
                break
            text_block_style = text_block_styles[text_block.frame_type]
            # Paint the background
            ### painter.fillRect(0,  y_top, width, y_bottom - y_top, text_block_style.background_colour)
            # Paint horizontal lines
            painter.setPen(text_block_style.line_colour)
            painter.drawLine(0, y_top, width, y_top)
            painter.drawLine(0, y_bottom - 1, width, y_bottom - 1)

        del painter

        # Paint text
        super(TextBrowser, self).paintEvent(event) 
        
####################################################################################################
        
class SplitterHandle(QtGui.QSplitterHandle):

    ##############################################
    
    def __init__(self, parent):

        super(SplitterHandle, self).__init__(QtCore.Qt.Horizontal, parent)

        self.frame_width = QtGui.QApplication.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        
    ##############################################
    
    def paintEvent(self, event):

        diff_view = self.parent()

        painter = QtGui.QPainter(self)
        painter.setClipRect(event.rect())

        width = self.width()
        height = self.height()

        y_left, y_right = [browser.verticalScrollBar().value() - self.frame_width
                           for browser in diff_view.browsers]
        
        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        print 'Paint Handle:'
        for text_block_left, text_block_right in zip(* diff_view.text_blocks):
            print text_block_left, text_block_right

            if text_block_left.frame_type is None or text_block_left.frame_type == chunk_type.equal:
                continue

            y_top_left = text_block_left.y_top - y_left
            y_bottom_left = text_block_left.y_bottom - y_left -1
            y_top_right = text_block_right.y_top - y_right
            y_bottom_right = text_block_right.y_bottom - y_right + 1
            
            if y_top_left < 0 and y_bottom_right < 0:
                continue
            if y_top_left > height and y_top_right > height:
                break
 
            text_block_style = text_block_styles[text_block_left.frame_type]

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

class DiffView(QtGui.QSplitter):

    """ Widget to show differences in side-by-side format.
    """

    ##############################################
    
    def __init__(self, parent=None):

        super(DiffView, self).__init__(QtCore.Qt.Horizontal, parent)
    
        self.setHandleWidth(30)

        self.monospaced_font = get_monospaced_font()
        self.syntax_highlighter_style = SyntaxHighlighterStyle()
        
        self.documents = (QtGui.QTextDocument(), QtGui.QTextDocument())
        self.text_blocks = (TextBlocks(), TextBlocks())
        self.browsers = [TextBrowser(self, text_block) for text_block in self.text_blocks]
        self.cursors = [QtGui.QTextCursor(document) for document in self.documents]

        for i, (browser, document) in enumerate(zip(self.browsers, self.documents)):
            document.setUndoRedoEnabled(False)
            document.setDefaultFont(self.monospaced_font)
            self.setCollapsible(i, False)
            browser.setDocument(document)
            self.addWidget(browser)

        self.ignore_scroll_bar_update_signal = False
        for browser in self.browsers:
            for scroll_bar in browser.horizontalScrollBar(), browser.verticalScrollBar():
                callback = lambda value, scroll_bar=scroll_bar: self.update_scroll_bar(scroll_bar, value)
                scroll_bar.valueChanged.connect(callback)

    ##############################################

    def createHandle(self):

        return SplitterHandle(self)

    ##############################################

    def update_scroll_bar(self, scroll_bar, value):

        if self.ignore_scroll_bar_update_signal:
            return
        
        if scroll_bar.orientation() == QtCore.Qt.Horizontal:
            method = TextBrowser.horizontalScrollBar
        else:
            method = TextBrowser.verticalScrollBar
        scroll_bar1, scroll_bar2 = [method(browser) for browser in self.browsers]
        if scroll_bar is scroll_bar2:
            scroll_bar1, scroll_bar2 = scroll_bar2, scroll_bar1
        
        maximum1 = scroll_bar1.maximum()
        if maximum1:
            value = scroll_bar2.minimum() + scroll_bar2.maximum() * (value - scroll_bar1.minimum()) / maximum1
            self.ignore_scroll_bar_update_signal = True
            scroll_bar2.setValue(value)
            self.ignore_scroll_bar_update_signal = False
        self.handle(1).update()
            
    ##############################################
    
    def set_document_models(self, document_models):

        for i, document_model in enumerate(document_models):
            print '\nDocument', i
            cursor = DiffViewerCursor(self.cursors[i], self.text_blocks[i])
            for k, text_block in enumerate(document_model):
                print '  Block', repr(text_block)
                cursor.begin_block(text_block.frame_type, k)
                last_fragment_index = len(text_block) -1
                for j, text_fragment in enumerate(text_block):
                    # print '    Fragment', repr(text_fragment).replace('\n', '\n      ')
                    text_format = self.syntax_highlighter_style[text_fragment.token_type]
                    text = unicode(text_fragment)
                    if j == last_fragment_index:
                        if text.endswith('\r\n'):
                            text = text[:-2]
                        elif text[-1] in ('\n', '\r'):
                            text = text[:-1]
                    print i, k, j, '[' + text + ']'
                    cursor.insert_text(text, text_format)
                cursor.end_block()
        
####################################################################################################
#
# End
#
####################################################################################################
