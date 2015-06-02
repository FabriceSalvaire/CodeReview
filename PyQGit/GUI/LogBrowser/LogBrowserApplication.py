####################################################################################################
#
# PyQGit - A Python/Qt Git GUI
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

###################################################################################################

import logging
import os

import pygit2 as git

from PyQt5 import QtCore, QtWidgets

####################################################################################################

from PyQGit.GUI.Base.GuiApplicationBase import GuiApplicationBase
from PyQGit.Application.ApplicationBase import ApplicationBase
from PyQGit.GUI.Widgets.LogTableModel import LogTableModel

####################################################################################################

class LogBrowserApplication(GuiApplicationBase, ApplicationBase):

    _logger = logging.getLogger(__name__)

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

        if self._args.path is None:
            path = os.getcwd()
        else:
            path = self._args.path
        try:
            repository_path = git.discover_repository(path)
            self._repository = git.Repository(repository_path)
            self._log_table_model = LogTableModel(self._repository)
            log_table = self._main_window._log_table
            log_table.setModel(self._log_table_model)
            log_table.resizeColumnsToContents()
        except KeyError:
            self.show_message("Any Git repository was found in path {}".format(path), warn=True)
            self._repository = None

####################################################################################################
#
# End
#
####################################################################################################
