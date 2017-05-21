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

###################################################################################################

import logging
import os

from PyQt5 import QtCore, QtWidgets

####################################################################################################

from .CommitTableModel import CommitTableModel
from .LogTableModel import LogTableModel
from CodeReview.Application.ApplicationBase import ApplicationBase
from CodeReview.GUI.Base.GuiApplicationBase import GuiApplicationBase
from CodeReview.Repository.Git import RepositoryNotFound, GitRepository

####################################################################################################

class LogBrowserApplication(GuiApplicationBase, ApplicationBase):

    _logger = logging.getLogger(__name__)

    file_system_changed = QtCore.pyqtSignal(str)

    ###############################################

    def __init__(self, args):

        super(LogBrowserApplication, self).__init__(args=args)
        self._logger.debug(str(args))

        from .LogBrowserMainWindow import LogBrowserMainWindow
        self._main_window = LogBrowserMainWindow()
        self._main_window.showMaximized()

        self.post_init()

    ##############################################

    def _init_actions(self):

        super(LogBrowserApplication, self)._init_actions()

    ##############################################

    def post_init(self):

        super(LogBrowserApplication, self).post_init()
        self._init_repository()
        self._init_file_system_watcher()
        self._main_window.show_working_tree_diff()

    ##############################################

    def show_message(self, message=None, timeout=0, warn=False):

        """ Hides the normal status indications and displays the given message for the specified
        number of milli-seconds (timeout). If timeout is 0 (default), the message remains displayed
        until the clearMessage() slot is called or until the showMessage() slot is called again to
        change the message.

        Note that showMessage() is called to show temporary explanations of tool tip texts, so
        passing a timeout of 0 is not sufficient to display a permanent message.
        """

        self._main_window.show_message(message, timeout, warn)

    ##############################################

    def _init_repository(self):

        self._logger.info('Init Repository')

        if self._args.path is None:
            path = os.getcwd()
        else:
            path = self._args.path
        try:
            self._repository = GitRepository(path)
        except RepositoryNotFound:
            self.show_message("Any Git repository was found in path {}".format(path), warn=True)
            self._repository = None
            return

        self._log_table_model = LogTableModel(self._repository)
        log_table = self._main_window._log_table
        log_table.setModel(self._log_table_model)
        # Set the column widths
        column_enum = self._log_table_model.column_enum
        width = 0
        for column in (
            column_enum.revision,
            # column_enum.message,
            column_enum.date,
            column_enum.comitter,
        ):
            log_table.resizeColumnToContents(int(column))
            width += log_table.columnWidth(int(column))
        width = log_table.width() - width
        width *= .9 # Fixme: subtract spaces ...
        log_table.setColumnWidth(int(column_enum.message), width)

        self._commit_table_model = CommitTableModel()
        commit_table = self._main_window._commit_table
        commit_table.setModel(self._commit_table_model)

        self._main_window.finish_table_connections()

    ##############################################

    def _init_file_system_watcher(self):

        self._file_system_watcher = QtCore.QFileSystemWatcher()
        self._setup_file_system_watcher()
        self._file_system_watcher.directoryChanged.connect(self.file_system_changed)
        self._file_system_watcher.fileChanged.connect(self.file_system_changed)
        self.file_system_changed.connect(self._setup_file_system_watcher)

    ##############################################

    def _setup_file_system_watcher(self):

        path = self._repository.workdir
        self._logger.info("Monitor {}".format(path))
        paths = []
        for root, dirs, files in os.walk(path):
            paths.append(root)
        directories = self._file_system_watcher.directories()
        if directories:
            self._file_system_watcher.removePaths(directories)
        self._file_system_watcher.addPaths(paths)

    ##############################################

    def reload_repository(self):

        self._init_repository()

    ##############################################

    @property
    def repository(self):
        return self._repository
