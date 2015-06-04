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
import os
import subprocess

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

####################################################################################################

from CodeReview.GUI.Base.MainWindowBase import MainWindowBase
from CodeReview.GUI.Widgets.IconLoader import IconLoader
from CodeReview.GUI.Widgets.MessageBox import MessageBox

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class LogBrowserMainWindow(MainWindowBase):

    _logger = _module_logger.getChild('LogBrowserMainWindow')

    ##############################################

    def __init__(self, parent=None):

        super(LogBrowserMainWindow, self).__init__(title='CodeReview Log Browser', parent=parent)
        
        self._current_revision = None
        self._patches = []
        self._current_patch = None
        self._diff_window = None
        
        self._init_ui()

    ##############################################

    def _init_ui(self):

        self._central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._central_widget)
        
        self._vertical_layout = QtWidgets.QVBoxLayout(self._central_widget)
        self._message_box = MessageBox(self)
        splitter = QtWidgets.QSplitter()
        splitter.setOrientation(Qt.Vertical)
        self._log_table = QtWidgets.QTableView()
        self._commit_table = QtWidgets.QTableView()
        
        for widget in (self._message_box, splitter):
            self._vertical_layout.addWidget(widget)
        for widget in (self._log_table, self._commit_table):
            splitter.addWidget(widget)
        
        table = self._log_table
        table.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        # table.setSortingEnabled(True)
        table.clicked.connect(self._update_commit_table)
        
        table = self._commit_table
        table.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setSortingEnabled(True)
        table.clicked.connect(self._show_patch)
        
        # horizontal_header = table_view.horizontalHeader()
        # horizontal_header.setMovable(True)

    ##############################################

    def _create_actions(self):

        pass
        # icon_loader = IconLoader()

    ##############################################

    def _create_toolbar(self):

        pass

    ##############################################

    def init_menu(self):

        super(LogBrowserMainWindow, self).init_menu()

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

    ##############################################

    def _update_commit_table(self, index):

        index = index.row()
        if index:
            self._current_revision = index
            log_table_model = self._log_table.model()
            commit1 = log_table_model[index]
            try:
                commit2 = log_table_model[index +1]
                commit1, commit2 = commit2, commit1 # Fixme:
            except IndexError:
                commit2 = None
        else:
            self._current_revision = None
            print("\nStatus:")
            git_status = self._application._repository.status()
            for filepath, status in git_status.items():
                print(filepath, status)
            commit1 = commit2 = None

        commit_table_model = self._commit_table.model()
        commit_table_model.update(commit1, commit2, self._application.path_filter)
        self._commit_table.resizeColumnsToContents()
        
        self._patches = [patch for patch in commit_table_model] # Fixme:

    ##############################################

    def _show_patch(self, index):

        self._current_patch = index.row()
        self._show_current_patch()

    ##############################################

    def _object_text(self, oid):

        repository = self._application._repository
        try:
            return repository[oid].data.decode('utf-8')
        except KeyError:
            return None

    ##############################################

    def _on_diff_window_closed(self):

        self._diff_window = None

    ##############################################

    def _show_current_patch(self):

        if self._diff_window is None:
            from CodeReview.GUI.DiffViewer.DiffViewerMainWindow import DiffViewerMainWindow
            self._diff_window = DiffViewerMainWindow(self)
            self._diff_window.closed.connect(self._on_diff_window_closed)
            self._diff_window.showMaximized()
        
        patch = self._patches[self._current_patch]
        if not patch.is_binary:
            self._logger.info('revision {} '.format(self._current_revision) + patch.new_file_path)
            # print(patch.status, patch.similarity, patch.additions, patch.deletions, patch.is_binary)
            # for hunk in patch.hunks:
            #     print(hunk.old_start, hunk.old_lines, hunk.new_start, hunk.new_lines, hunk.lines)
            repository = self._application._repository
            if patch.status in ('M', 'R'):
                paths = (patch.old_file_path, patch.new_file_path)
            elif patch.status == 'A':
                paths = (None, patch.new_file_path)
            elif patch.status == 'D':
                paths = (patch.old_file_path, None)
            texts = [self._object_text(blob_id)
                     for blob_id in (patch.old_id, patch.new_id)]
            self._diff_window.diff_documents(paths, texts, workdir=repository.workdir)
        else:
            self._logger.info('revision {} Binary '.format(self._current_revision) + patch.new_file_path)
        # Fixme: show image pdf ...

    ##############################################

    def previous_patch(self):

        # Fixme: else notify
        if self._current_patch >= 1:
            self._current_patch -= 1
            self._show_current_patch()

    ##############################################

    def next_patch(self):

        if self._current_patch < (len(self._patches) -1):
            self._current_patch += 1
            self._show_current_patch()

####################################################################################################
#
# End
#
####################################################################################################
