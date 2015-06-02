# -*- coding: utf-8 -*-

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
# - 25/05/2010 Fabrice
#   - exit button
#
####################################################################################################

####################################################################################################

import sys
import traceback

from PyQt5 import QtWidgets, QtCore

####################################################################################################

from .EmailBugForm import EmailBugForm
from CodeReview.Logging.ExceptionHook import format_exception
import CodeReview.Tools.BackTrace as BackTrace

####################################################################################################

from CodeReview.GUI.ui.critical_error_form_ui import Ui_critical_error_form

####################################################################################################

class CriticalErrorForm(QtWidgets.QDialog, Ui_critical_error_form):

    ###############################################

    def __init__(self, exception_type, exception_value, exception_backtrace):

        QtWidgets.QDialog.__init__(self)

        self.setupUi(self)

        self.expert_group_box.hide()

        self._exception_type = exception_type
        self._exception_value = exception_value
        self._exception_backtrace = exception_backtrace
        self._backtrace = format_exception(self._exception_type,
                                           self._exception_value,
                                           self._exception_backtrace)
        
        # Fixme: call critical exit
        self.exit_button.clicked.connect(lambda : sys.exit(1))
        self.show_backtrace_button.clicked.connect(self.show_backtrace)
        self.send_email_button.clicked.connect(self.send_email)

        title = str(exception_value)
        self.error_message_label.setText(title[:50])
        backtrace_text = ''.join(traceback.format_exception(exception_type,
                                                            exception_value,
                                                            exception_backtrace))

        self._trace_back_text_highlighted = BackTrace.html_highlight_backtrace(backtrace_text)

        self.back_trace_text_browser.clear()
        #!# self.back_trace_text_browser.hide()

    ###############################################

    def show_backtrace(self):

        # print trace_back_text_highlighted
        self.back_trace_text_browser.setHtml(self._trace_back_text_highlighted)

    ###############################################

    def send_email(self):

        dialog = EmailBugForm(self._backtrace)
        dialog.exec_()

####################################################################################################
#
# End
#
####################################################################################################
