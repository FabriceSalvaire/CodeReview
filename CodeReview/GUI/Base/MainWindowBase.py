####################################################################################################
#
# CodeReview - A Python/Qt Git GUI
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
#
#                                              Audit
#
# - 13/02/2013 Fabrice
#   - check close
#
####################################################################################################

####################################################################################################

import logging

from PyQt5 import QtWidgets, QtCore

####################################################################################################

class MainWindowBase(QtWidgets.QMainWindow):

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, title='', parent=None):

        super(MainWindowBase, self).__init__(parent)
        
        self.setWindowTitle(title)
        
        self._application = QtWidgets.QApplication.instance()
        self.init_menu()

    ##############################################

    @property
    def application(self):
        return self._application

    @property
    def menu_bar(self):
        return self.menuBar()

    @property
    def file_menu(self):
        return self._file_menu

    @property
    def help_menu(self):
        return self._help_menu

    ##############################################

    def init_menu(self):

        application = self._application
        
        self._file_menu = file_menu = self.menu_bar.addMenu('File')
        file_menu.addAction(application.exit_action) # Fixme: At the end
        
        self._help_menu = help_menu = self.menu_bar.addMenu('Help')
        help_menu.addAction(application.help_action)
        help_menu.addSeparator()
        help_menu.addAction(application.about_action)
        help_menu.addAction(application.show_system_information_action)
        help_menu.addAction(application.send_email_action)

    ##############################################

    def show_message(self, message=None, echo=False, timeout=0):

        """ Hides the normal status indications and displays the given message for the specified
        number of milli-seconds (timeout). If timeout is 0 (default), the message remains displayed
        until the clearMessage() slot is called or until the showMessage() slot is called again to
        change the message.

        Note that showMessage() is called to show temporary explanations of tool tip texts, so
        passing a timeout of 0 is not sufficient to display a permanent message.
        """

        status_bar = self.statusBar()
        if message is None:
            status_bar.clearMessage()
        else:
            status_bar.showMessage(message, timeout)
            if echo:
                self._logger.info(message)
        # self.application.processEvents()

    ##############################################

    def translate(self, text):

        return self._application.translate(self.__class__.__name__, text)

####################################################################################################
#
# End
#
####################################################################################################
