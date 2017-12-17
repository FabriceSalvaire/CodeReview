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
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

import pygit2 as git

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

        icon_loader = IconLoader()
        self.setWindowIcon(icon_loader['code-review@svg'])

        self._current_revision = None
        self._diff = None
        self._current_patch_index = None
        self._diff_window = None

        self._init_ui()
        self._create_actions()
        self._create_toolbar()

        self._application.directory_changed.connect(self._on_directory_changed)
        self._application.file_changed.connect(self._on_file_changed)

    ##############################################

    def _init_ui(self):

        # Table models are set in application

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
        table.clicked.connect(self._on_clicked_table)

        # horizontal_header = table_view.horizontalHeader()
        # horizontal_header.setMovable(True)

    ##############################################

    def finish_table_connections(self):

        self._log_table.selectionModel().currentRowChanged.connect(self._update_commit_table)
        self._commit_table.selectionModel().currentRowChanged.connect(self._on_clicked_table)

    ##############################################

    def _create_actions(self):

        icon_loader = IconLoader()

        self._stagged_mode_action = \
            QtWidgets.QAction('Stagged',
                              self,
                              toolTip='Stagged Mode',
                              shortcut='Ctrl+1',
                              checkable=True,
            )

        self._not_stagged_mode_action = \
            QtWidgets.QAction('Not Stagged',
                              self,
                              toolTip='Not Stagged Mode',
                              shortcut='Ctrl+2',
                              checkable=True,
            )

        self._all_change_mode_action = \
            QtWidgets.QAction('All',
                              self,
                              toolTip='All Mode',
                              shortcut='Ctrl+3',
                              checkable=True,
            )

        self._action_group = QtWidgets.QActionGroup(self)
        self._action_group.triggered.connect(self._update_working_tree_diff)
        for action in (self._all_change_mode_action,
                       self._stagged_mode_action,
                       self._not_stagged_mode_action,
                       ):
            self._action_group.addAction(action)
        self._all_change_mode_action.setChecked(True)

        self._reload_action = \
            QtWidgets.QAction(icon_loader['view-refresh@svg'],
                              'Refresh',
                              self,
                              toolTip='Refresh',
                              shortcut='Ctrl+R',
                              triggered=self._reload_repository,
            )

    ##############################################

    def _create_toolbar(self):

        self._tool_bar = self.addToolBar('Diff on Working Tree')
        for item in self._action_group.actions():
            self._tool_bar.addAction(item)
        for item in (self._reload_action,):
            self._tool_bar.addAction(item)

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

    def _on_directory_changed(self, path):

        self._logger.info(path)

        self._reload_repository()
        self._diff = self._application.repository.diff(**self._diff_kwargs)

        if self.number_of_patches:
            self._current_patch_index = 0
            self.reload_current_patch()
        elif self._diff_window is not None:
            self._diff_window.close()

    ##############################################

    def _on_file_changed(self, path):

        self._logger.info(path)

        repository = self._application.repository
        if path == repository.join_repository_path(repository.INDEX_PATH):
            self._diff = self._application.repository.diff(**self._diff_kwargs)
        else:
            message = 'File {} changed'.format(path)
            self.show_message(message)
            self.reload_current_patch()

    ##############################################

    def _reload_repository(self):

        self._logger.info('Reload signal')
        index = self._log_table.currentIndex()
        self._application.reload_repository()
        if index.row() != -1:
            self._logger.info("Index is {}".format(index.row()))
            self._log_table.setCurrentIndex(index)
            # Fixme: ???
            # self._update_working_tree_diff()
            self.show_working_tree_diff()
        else:
            self.show_working_tree_diff()

    ##############################################

    def show_working_tree_diff(self):

        self._logger.info('Show WT')
        log_model = self._log_table.model()
        if log_model.rowCount():
            top_index = log_model.index(0, 0)
            self._log_table.setCurrentIndex(top_index)
            self._update_working_tree_diff()

    ##############################################

    def _update_working_tree_diff(self):

        # Check log table is on working tree
        if self._log_table.currentIndex().row() == 0:
            self._update_commit_table()

    ##############################################

    def _update_commit_table(self, index=None):

        if index is not None:
            index = index.row()
        else:
            index = 0

        if index:
            self._current_revision = index
            log_table_model = self._log_table.model()
            commit1 = log_table_model[index]
            try:
                commit2 = log_table_model[index +1]
                kwargs = dict(a=commit2, b=commit1) # Fixme:
            except IndexError:
                kwargs = dict(a=commit1)
        else: # working directory
            self._current_revision = None
            if self._stagged_mode_action.isChecked():
                # Changes between the index and your last commit
                kwargs = dict(a='HEAD', cached=True)
            elif self._not_stagged_mode_action.isChecked():
                # Changes in the working tree not yet staged for the next commit
                kwargs = {}
            elif self._all_change_mode_action.isChecked():
                # Changes in the working tree since your last commit
                kwargs = dict(a='HEAD')

        self._diff_kwargs = kwargs
        self._diff = self._application.repository.diff(**kwargs)

        commit_table_model = self._commit_table.model()
        commit_table_model.update(self._diff)
        self._commit_table.resizeColumnsToContents()

    ##############################################

    def _on_clicked_table(self, index):

        # called when a commit row is clicked
        self._logger.info('')
        self._current_patch_index = index.row()
        self.reload_current_patch()

    ##############################################

    @property
    def current_patch_index(self):
        return self._current_patch_index

    ##############################################

    @property
    def number_of_patches(self):
        return len(self._diff)

    ##############################################

    def _create_diff_viewer_window(self):

        self._logger.info("Open Diff Viewer")

        from CodeReview.GUI.DiffViewer.DiffViewerMainWindow import DiffViewerMainWindow

        repository = self._application.repository
        self._diff_window = DiffViewerMainWindow(self, repository=repository)
        self._diff_window.closed.connect(self._on_diff_window_closed)
        self._diff_window.showMaximized()

    ##############################################

    def _on_diff_window_closed(self):

        self._application.unwatch_files() # Fixme: only current patch !
        self._diff_window = None
        self._logger.info("Diff Viewer closed")

    ##############################################

    def _show_patch(self, patch):

        self._logger.info("")

        self._application.unwatch_files()

        if self._diff_window is None:
            self._create_diff_viewer_window()

        delta = patch.delta
        old_path = delta.old_file.path
        new_path = delta.new_file.path
        if not delta.is_binary:
            self._logger.info('revision {} '.format(self._current_revision) + new_path)
            # print(delta.status, delta.similarity, delta.additions, delta.deletions, delta.is_binary)
            # for hunk in delta.hunks:
            #     print(hunk.old_start, hunk.old_lines, hunk.new_start, hunk.new_lines, hunk.lines)
            if delta.status in (git.GIT_DELTA_MODIFIED, git.GIT_DELTA_RENAMED):
                paths = (old_path, new_path)
            elif delta.status == git.GIT_DELTA_ADDED:
                paths = (None, new_path)
            elif delta.status == git.GIT_DELTA_DELETED:
                paths = (old_path, None)
            repository = self._application.repository
            texts = [repository.file_content(blob_id)
                     for blob_id in (delta.old_file.id, delta.new_file.id)]
            metadatas = [dict(path=old_path, document_type='file', last_modification_date=None),
                         dict(path=new_path, document_type='file', last_modification_date=None)]
            self._diff_window.diff_documents(paths, texts, metadatas, workdir=repository.workdir)
            self._application.watch(new_path)
        else:
            self._logger.info('revision {} Binary '.format(self._current_revision) + new_path)
        # Fixme: show image pdf ...

        # Monitor file change

    ##############################################

    @property
    def _last_path_index(self):

        return len(self._diff) -1

    ##############################################

    def _get_patch(self, forward):

        if forward:
            if self._current_patch_index < self._last_path_index:
                patch_index = self._current_patch_index + 1
            else:
                patch_index = 0
        else:
            if self._current_patch_index >= 1:
                patch_index = self._current_patch_index - 1
            else:
                patch_index = self._last_path_index

        return patch_index, self._diff[patch_index]

    ##############################################

    def _next_previous_patch(self, forward):

        try:
            patch_index, patch = self._get_patch(forward)
        except IndexError: # Fixme: still required ???
            self._logger.info('Patch index error {}'.format(patch_index))
            self._diff = self._application.repository.diff(**self._diff_kwargs)
            patch_index, patch = self._get_patch(forward)

        self._current_patch_index = patch_index
        self._show_patch(patch)

    ##############################################

    def previous_patch(self):
        self._next_previous_patch(forward=False)

    ##############################################

    def next_patch(self):
        self._next_previous_patch(forward=True)

    ##############################################

    def reload_current_patch(self):

        if self._current_patch_index is not None:
            patch = self._diff[self._current_patch_index]
            self._show_patch(patch)
