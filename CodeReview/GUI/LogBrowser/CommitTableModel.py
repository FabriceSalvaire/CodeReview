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

import pygit2 as git

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

####################################################################################################

from CodeReview.Common.EnumFactory import EnumFactory

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class CommitTableModel(QtCore.QAbstractTableModel):

    _logger = _module_logger.getChild('CommitTableModel')

    column_enum = EnumFactory('CommitColumnEnum', (
        'modification',
        'old_path',
        'new_path',
        'similarity',
        ))

    _TITLES = (
        'Modification',
        'Old Path',
        'New Path',
        'Similarity',
    )

    _STATUS_TO_LETTER = {
        git.GIT_DELTA_DELETED: 'D',
        git.GIT_DELTA_MODIFIED: 'M',
        git.GIT_DELTA_ADDED: 'A',
        git.GIT_DELTA_RENAMED: 'R',
    }

    ##############################################

    def __init__(self):

        super(CommitTableModel, self).__init__()

        self._rows = []
        self._number_of_rows = 0

    ##############################################

    def update(self, diff):

        self._rows = []
        self._number_of_rows = 0

        for patch in diff:
            delta = patch.delta
            if delta.new_file.path != delta.old_file.path:
                new_file_path = delta.new_file.path
                similarity = ' {} %'.format(delta.similarity)
            else:
                new_file_path = ''
                similarity = ''
            status = self._STATUS_TO_LETTER[delta.status]
            row = (status, delta.old_file.path, new_file_path, similarity, patch)
            self._rows.append(row)

        self._number_of_rows = len(self._rows)

        self.modelReset.emit()

    ##############################################

    def __iter__(self):
        for row in self._rows:
            yield row[-1]

    ##############################################

    def __getitem__(self, i):
        return self._rows[i][-1]

    ##############################################

    def data(self, index, role=Qt.DisplayRole):

        if not index.isValid():
            return QtCore.QVariant()
        column = index.column()
        row = self._rows[index.row()]

        if role == Qt.DisplayRole:
            return QtCore.QVariant(row[column])
        elif role == Qt.ForegroundRole and column == self.column_enum.old_path:
            modification = row[int(self.column_enum.modification)]
            if modification == 'D':
                return QtGui.QColor(Qt.red)
            elif modification == 'M':
                return QtGui.QColor(Qt.black)
            elif modification == 'A':
                return QtGui.QColor(Qt.green)
            elif modification == 'R':
                return QtGui.QColor(Qt.black)
            else:
                return QtCore.QVariant()

        return QtCore.QVariant()

    ##############################################

    def headerData(self, section, orientation, role=Qt.DisplayRole):

        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QtCore.QVariant(int(Qt.AlignHCenter|Qt.AlignVCenter))
            else:
                return QtCore.QVariant(int(Qt.AlignRight|Qt.AlignVCenter))

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return QtCore.QVariant(self._TITLES[section])

        return QtCore.QVariant()

    ##############################################

    def columnCount(self, index=QtCore.QModelIndex()):
        return len(self._TITLES)

    ##############################################

    def rowCount(self, index=QtCore.QModelIndex()):
        return self._number_of_rows

    ##############################################

    def sort(self, column, order):
       reverse = order == Qt.DescendingOrder
       self._rows.sort(key=lambda x:x[column], reverse=reverse)
       self.modelReset.emit()
