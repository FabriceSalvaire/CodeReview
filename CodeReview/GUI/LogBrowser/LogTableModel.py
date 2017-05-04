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

import datetime
fromtimestamp = datetime.datetime.fromtimestamp

####################################################################################################

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

####################################################################################################

from CodeReview.Tools.EnumFactory import EnumFactory

####################################################################################################

class LogTableModel(QtCore.QAbstractTableModel):

    column_enum = EnumFactory('LogColumnEnum', (
        'revision',
        'message',
        'date',
        'comitter',
        ))

    __titles__ = (
        # 'Hex',
        'Revision',
        'Message',
        'Date',
        # 'Author',
        'Comitter',
    )

    ##############################################

    def __init__(self, repository):

        super(LogTableModel, self).__init__()

        commits = repository.commits()
        self._number_of_rows = len(commits)
        self._rows = [('', 'Working directory changes', '', '', None)]
        self._rows.extend([self._commit_data(i, commit)
                           for i, commit in enumerate(commits)])

    ##############################################

    def _commit_data(self, i, commit):

        return (
            # commit.hex,
            self._number_of_rows - i -1,
            commit.message,
            fromtimestamp(commit.commit_time).strftime('%Y-%m-%d %H:%M:%S'),
            # commit.author.name,
            commit.committer.name,
            commit,
        )

    ##############################################

    def __getitem__(self, i):

        return self._rows[i][-1]

    ##############################################

    def data(self, index, role=Qt.DisplayRole):

        if not index.isValid(): # or not(0 <= index.row() < self._number_of_rows):
            return QtCore.QVariant()

        if role == Qt.DisplayRole:
            row = self._rows[index.row()]
            column = index.column()
            return QtCore.QVariant(row[column])

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
                return QtCore.QVariant(self.__titles__[section])
            else:
                return QtCore.QVariant(self._number_of_rows - section)

        return QtCore.QVariant()

    ##############################################

    def columnCount(self, index=QtCore.QModelIndex()):

        return len(self.__titles__)

    ##############################################

    def rowCount(self, index=QtCore.QModelIndex()):

        return self._number_of_rows
