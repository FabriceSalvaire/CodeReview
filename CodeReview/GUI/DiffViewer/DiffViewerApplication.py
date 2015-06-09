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

from PyQt5 import QtCore

####################################################################################################

from CodeReview.GUI.Base.GuiApplicationBase import GuiApplicationBase
from CodeReview.Application.ApplicationBase import ApplicationBase

####################################################################################################

class DiffViewerApplication(GuiApplicationBase, ApplicationBase):

    _logger = logging.getLogger(__name__)

    ###############################################

    def __init__(self, args):

        super(DiffViewerApplication, self).__init__(args=args)
        self._logger.debug(str(args))
        
        from .DiffViewerMainWindow import DiffViewerMainWindow
        self._main_window = DiffViewerMainWindow()
        self._main_window.showMaximized()
        
        self.post_init()

    ##############################################

    def _init_actions(self):

        super(DiffViewerApplication, self)._init_actions()

    ##############################################

    def post_init(self):

        super(DiffViewerApplication, self).post_init()
        self._main_window.open_files(self._args.file1, self._args.file2, self._args.show)

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

####################################################################################################
#
# End
#
####################################################################################################
