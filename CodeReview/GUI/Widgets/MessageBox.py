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

import collections
import time

from PyQt5 import QtCore, QtGui, QtWidgets

####################################################################################################

from CodeReview.GUI.Widgets.IconLoader import IconLoader

####################################################################################################

class MessageBox(QtWidgets.QWidget):

    ##############################################

    def __init__(self, parent):

        super(MessageBox, self).__init__(parent)

        self._application = QtWidgets.QApplication.instance()
        self._message_queue = collections.deque()

        self.hide()
        self.setMaximumSize(QtCore.QSize(16777215, 50))
        self.setPalette(self._palette)
        self.setAutoFillBackground(True)

        icon_loader = IconLoader()
        self._icon_label = QtWidgets.QLabel(parent)
        warning_icon = icon_loader['dialog-warning@48']
        warning_pixmap = warning_icon.pixmap(warning_icon.availableSizes()[0])
        self._icon_label.setPixmap(warning_pixmap)

        self._message_text_browser = QtWidgets.QTextBrowser(self)
        self._message_text_browser.setFrameShadow(QtWidgets.QFrame.Plain)

        push_button = QtWidgets.QPushButton(self)
        push_button.setText('OK')
        push_button.clicked.connect(self._hide)

        horizontal_layout = QtWidgets.QHBoxLayout(self)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        for widget in self._icon_label, self._message_text_browser, push_button:
            horizontal_layout.addWidget(widget)

    ##############################################

    @property
    def _palette(self):

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 155, 155))
        brush.setStyle(QtCore.Qt.SolidPattern)
        for group in QtGui.QPalette.Disabled, QtGui.QPalette.Active,  QtGui.QPalette.Inactive:
            for role in QtGui.QPalette.Button, QtGui.QPalette.Base, QtGui.QPalette.Window:
                palette.setBrush(group, role, brush)

        return palette

    ##############################################

    def push_message(self, message):

        self._message_queue.appendleft(message)
        self._show_message()

    ##############################################

    def _show_message(self):

        # Show the last message
        message = self._message_queue[0]
        if self.isVisible():
            # Flash user
            self._message_text_browser.clear()
            self._icon_label.setVisible(False)
            self._application.processEvents()
            time.sleep(.25)
            self._icon_label.setVisible(True)
        self._message_text_browser.setHtml(message)
        self.setVisible(True)

    ##############################################

    def _hide(self):

        # The last message was seen
        self._message_queue.popleft()
        if self._message_queue:
            self._show_message()
        else:
            self.hide()
