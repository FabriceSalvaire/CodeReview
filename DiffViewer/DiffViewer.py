####################################################################################################

from PyQt4 import QtGui, QtCore

####################################################################################################

from SyntaxHighlighterStyle import SyntaxHighlighterStyle

####################################################################################################

class TextBrowser(QtGui.QTextBrowser):

    ##############################################
    
    def __init__(self, parent=None):

        super(TextBrowser, self).__init__(parent)

        # Truncate long lines
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)

    ##############################################
        
    def paintEvent(self, event):

        super(TextBrowser, self).paintEvent(event) 

####################################################################################################
        
class SplitterHandle(QtGui.QSplitterHandle):

    ##############################################
    
    def __init__(self, parent=None):

        super(SplitterHandle, self).__init__(QtCore.Qt.Horizontal, parent)
        
    ##############################################
    
    def paintEvent(self, event):

        pass

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
        self.browsers = (TextBrowser(self), TextBrowser(self))
        self.cursors = [QtGui.QTextCursor(document) for document in self.documents]
        
        for i, (browser, document, cursor) in enumerate(zip(self.browsers, self.documents, self.cursors)):
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
            cursor = self.cursors[i]
            for text_block in document_model:
                for text_fragment in text_block:
                    text_format = self.syntax_highlighter_style[text_fragment.token_type]
                    cursor.insertText(unicode(text_fragment), text_format)
            
####################################################################################################
#
# End
#
####################################################################################################
