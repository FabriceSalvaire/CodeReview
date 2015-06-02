# -*- coding: utf-8 -*-

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

###################################################################################################
#
# If an exception is raise before application.exec then application exit.
#
####################################################################################################

####################################################################################################

import logging
import sys
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets

####################################################################################################

from CodeReview.Application.ApplicationBase import ApplicationBase
from CodeReview.GUI.Forms.CriticalErrorForm import CriticalErrorForm
from CodeReview.GUI.Forms.EmailBugForm import EmailBugForm
import CodeReview.Config.Config as Config
import CodeReview.Config.Messages as Messages
import CodeReview.Version as Version

# Load RC
#import CodeReview.gui.ui.pyqgit_rc

####################################################################################################

class GuiApplicationBase(ApplicationBase, QtWidgets.QApplication):

    _logger = logging.getLogger(__name__)

    has_gui = True

    ##############################################

    def __init__(self, args, **kwargs):

        super(GuiApplicationBase, self).__init__(args=args, **kwargs)
        # Fixme: Why ?
        self._logger.debug("QtWidgets.QApplication " + str(sys.argv))
        QtWidgets.QApplication.__init__(self, sys.argv)
        self._logger.debug('GuiApplicationBase ' + str(args) + ' ' + str(kwargs))
        
        self._display_splash_screen()
        
        self._main_window = None
        self._init_actions()

    ##############################################

    @property
    def main_window(self):
        return self._main_window

    ##############################################

    def _exception_hook(self, exception_type, exception_value, exception_traceback):

        traceback.print_exception(exception_type, exception_value, exception_traceback)
        dialog = CriticalErrorForm(exception_type, exception_value, exception_traceback)
        dialog.exec_()

        # return sys.__excepthook__(exception_type, exception_value, exception_traceback)

    ##############################################

    def _display_splash_screen(self):

        pixmap = QtGui.QPixmap(':/splash screen/images/splash_screen.png')
        self._splash = QtWidgets.QSplashScreen(pixmap)
        self._splash.show()
        self._splash.showMessage('<h2>CodeReview %(version)s</h2>' % {'version':str(Version.pyqgit)})
        self.processEvents()

    ##############################################

    def _init_actions(self):

        self.about_action = \
            QtWidgets.QAction('About CodeReview',
                          self,
                          triggered=self.about)
        
        self.exit_action = \
            QtWidgets.QAction('Exit',
                          self,
                          triggered=self.exit)
        
        self.help_action = \
            QtWidgets.QAction('Help',
                          self,
                          triggered=self.open_help)
        
        self.show_system_information_action = \
            QtWidgets.QAction('System Information',
                          self,
                          triggered=self.show_system_information)
        
        self.send_email_action = \
            QtWidgets.QAction('Send Email',
                          self,
                          triggered=self.send_email)

    ##############################################

    def post_init(self):

        self._splash.finish(self._main_window)
        self.processEvents()
        del self._splash
        
        QtCore.QTimer.singleShot(0, self.execute_given_user_script)

        self.show_message('Welcome to CodeReview')

        # return to main and then enter to event loop

    ##############################################

    def show_message(self, message=None, echo=False, timeout=0):

        # Fixme: cf. LogBrowserApplication
        if self._main_window is not None:
            self._main_window.show_message(message, echo, timeout)

    ##############################################

    # Fixme: CriticalErrorForm vs critical_error

    def critical_error(self, title='CodeReview Critical Error', message=''):

        QtWidgets.QMessageBox.critical(None, title, message)
        
        # Fixme: qt close?
        sys.exit(1)

    ##############################################

    def open_help(self):

        url = QtCore.QUrl()
        url.setScheme(Config.Help.url_scheme)
        url.setHost(Config.Help.host)
        url.setPath(Config.Help.url_path_pattern) # % str(Version.pyqgit))
        # X.QDesktopServices.openUrl(url) # Fixme

    ##############################################

    def about(self):

        message = Messages.about_pyqgit % {'version':str(Version.pyqgit)}
        QtWidgets.QMessageBox.about(self.main_window, 'About CodeReview', message)

    ##############################################

    def show_system_information(self):

        fields = dict(self._platform.__dict__)
        fields.update({
                'pyqgit_version': str(Version.pyqgit),
                })
        message = Messages.system_information_message_pattern % fields
        QtWidgets.QMessageBox.about(self.main_window, 'System Information', message)

    ###############################################

    def send_email(self):

        dialog = EmailBugForm()
        dialog.exec_()

####################################################################################################
#
# End
#
####################################################################################################
