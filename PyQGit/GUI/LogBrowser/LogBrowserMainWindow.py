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

####################################################################################################

import logging
import os
import subprocess

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

####################################################################################################

from PyQGit.GUI.Base.MainWindowBase import MainWindowBase
from PyQGit.GUI.Widgets.IconLoader import IconLoader
from PyQGit.GUI.Widgets.MessageBox import MessageBox

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class LogBrowserMainWindow(MainWindowBase):

    _logger = _module_logger.getChild('LogBrowserMainWindow')

    ##############################################

    def __init__(self, parent=None):

        super(LogBrowserMainWindow, self).__init__(title='PyQGit PDF Browser', parent=parent)

        self._current_path = None
        self._init_ui()

    ##############################################

    def _init_ui(self):

        self._central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._central_widget)
        

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

####################################################################################################
#
# End
#
####################################################################################################
