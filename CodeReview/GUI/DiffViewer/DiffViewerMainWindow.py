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

####################################################################################################

import logging

from pygments.lexers import get_lexer_for_filename

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

####################################################################################################

from CodeReview.Diff.RawTextDocument import RawTextDocument
from CodeReview.Diff.RawTextDocumentDiff import TwoWayFileDiffFactory
from CodeReview.Diff.SyntaxHighlighter import HighlightedText, highlight_text
from CodeReview.Diff.TextDocumentDiffModel import TextDocumentDiffModelFactory, highlight_document
from CodeReview.GUI.Base.MainWindowBase import MainWindowBase
from CodeReview.GUI.DiffViewer.DiffWidget import DiffView
from CodeReview.GUI.Widgets.MessageBox import MessageBox

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class DiffViewerMainWindow(MainWindowBase):

    _logger = _module_logger.getChild('DiffViewerMainWindow')

    ##############################################

    def __init__(self, parent=None):

        super(DiffViewerMainWindow, self).__init__(title='CodeReview Diff Viewer', parent=parent)

        self._current_path = None
        self._init_ui()

    ##############################################

    def _init_ui(self):

        self._central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._vertical_layout = QtWidgets.QVBoxLayout(self._central_widget)
        
        self._message_box = MessageBox(self)
        self._vertical_layout.addWidget(self._message_box)
        
        self._diff_view = DiffView()
        self._vertical_layout.addWidget(self._diff_view)
        
        self._horizontal_layout = QtWidgets.QHBoxLayout()
        self._vertical_layout.addLayout(self._horizontal_layout)
        self._complete_checkbox = QtWidgets.QCheckBox(self._central_widget)
        self._complete_checkbox.setText("Complete")
        # QtWidgets.QApplication.translate("main_window", , None, QtWidgets.QApplication.UnicodeUTF8))
        self._horizontal_layout.addWidget(self._complete_checkbox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._horizontal_layout.addItem(spacerItem)
        self._refresh_button = QtWidgets.QPushButton(self._central_widget)
        self._refresh_button.setText("Refresh")
        # QtWidgets.QApplication.translate("main_window", "Refresh", None, QtWidgets.QApplication.UnicodeUTF8)
        self._horizontal_layout.addWidget(self._refresh_button)
        
        self._complete_checkbox.stateChanged.connect(self._set_document_models)

    ##############################################

    def _create_actions(self):

        pass
        # icon_loader = IconLoader()

    ##############################################

    def _create_toolbar(self):

        pass

    ##############################################

    def init_menu(self):

        super(DiffViewerMainWindow, self).init_menu()

    ##############################################

    def show_message(self, message=None, timeout=0, warn=False):

        """ Hides the normal status indications and displays the given message for the specified
        number of milli-seconds (timeout). If timeout is 0 (default), the message remains displayed
        until the clearMessage() slot is called or until the showMessage() slot is called again to
        change the message.

        Note that showMessage() is called to show temporary explanations of tool tip texts, so
        passing a timeout of 0 is not sufficient to display a permanent message.
        """

        if warn:
            self._message_box.push_message(message)
        else:
            status_bar = self.statusBar()
            if message is None:
                status_bar.clearMessage()
            else:
                status_bar.showMessage(message, timeout)

    ################################################

    def open_files(self, file1, file2, show=False):

        paths = (file1, file2)
        texts = []
        for file_name in paths:
            with open(file_name) as f:
                texts.append(f.read())
        self.diff_documents(texts, paths, show)

    ##############################################

    def diff_documents(self, texts, paths, show=False):

        self._paths = paths
        self._raw_text_documents = []
        self._lexers = []
        for text, path in zip(texts, self._paths):
            raw_text_document = RawTextDocument(text)
            self._raw_text_documents.append(raw_text_document)
            lexer = get_lexer_for_filename(path, stripnl=False)
            self._lexers.append(lexer)
            
        self._highlighted_documents = []
        if not show:
            file_diff = TwoWayFileDiffFactory().process(* self._raw_text_documents)
            self._document_models = TextDocumentDiffModelFactory().process(file_diff)
            self._highlighted_texts = []
            for raw_text_document, lexer in zip(self._raw_text_documents, self._lexers):
                highlighted_text = HighlightedText(raw_text_document, lexer)
                self._highlighted_texts.append(highlighted_text)
            for document_model, highlighted_text in zip(self._document_models, self._highlighted_texts):
                highlighted_document = highlight_document(document_model, highlighted_text)
                self._highlighted_documents.append(highlighted_document)
        else: # Only show the document
            # Fixme: broken, chunk_type is ???
            # self._diff_view.set_document_models(self._highlighted_documents, complete_mode)
            # File "/home/gv/fabrice/unison-osiris/git-python/DiffViewer/DiffWidget.py", line 333, in set_document_models
            # cursor.begin_block(side, text_block.frame_type)
            # File "/home/gv/fabrice/unison-osiris/git-python/DiffViewer/DiffWidget.py", line 99, in begin_block
            # if ((side == LEFT and frame_type == chunk_type.insert) or
            # File "/home/gv/fabrice/unison-osiris/git-python/DiffViewer/Tools/EnumFactory.py", line 107, in __eq__
            # return self._value == int(other)
            # TypeError: int() argument must be a string or a number, not 'NoneType'
            for raw_text_document, lexer in zip(self._raw_text_documents, self._lexers):
                highlighted_document = highlight_text(raw_text_document, lexer)
                self._highlighted_documents.append(highlighted_document)
        
        self._set_document_models()

    ################################################

    def _set_document_models(self):

        complete_mode = self._complete_checkbox.checkState() == QtCore.Qt.Checked
        self._diff_view.set_document_models(self._highlighted_documents, complete_mode)

####################################################################################################
#
# End
#
####################################################################################################
