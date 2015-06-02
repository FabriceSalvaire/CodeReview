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

import datetime

import pygit2 as git

####################################################################################################

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

####################################################################################################

class LogTableModel(QtCore.QAbstractTableModel):

    ##############################################

    def __init__(self, repository):

        super(LogTableModel, self).__init__()

        self._column_names = (
            # 'Hex',
            'Revision',
            'Message',
            'Date',
            # 'Author',
            'Comitter',
        )

        self._commits = [None]
        self._commit_datas = [None]

        head = repository.head
        head_commit = repository[head.target]
        fromtimestamp = datetime.datetime.fromtimestamp
        for commit in repository.walk(head_commit.id, git.GIT_SORT_TIME):
            self._commits.append(commit)
        self._number_of_commits = len(self._commits)
        for i, commit in enumerate(self._commits[1:]):
            commit_data = (
                # commit.hex,
                self._number_of_commits - i -1,
                commit.message,
                fromtimestamp(commit.commit_time).strftime('%Y-%m-%d %H:%M:%S'),
                # commit.author.name,
                commit.committer.name,
            )
            self._commit_datas.append(commit_data)

    ##############################################

    def __getitem__(self, i):

        return self._commits[i]

    ##############################################

    def data(self, index, role=Qt.DisplayRole):

        if not index.isValid(): # or not(0 <= index.row() < self._number_of_commits):
            return QtCore.QVariant()

        if role == Qt.DisplayRole:
            commit = self._commit_datas[index.row()]
            if commit is not None:
                column = index.column()
                return QtCore.QVariant(commit[column])
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
                column_name = self._column_names[section]
                return QtCore.QVariant(column_name)
            else:
                return QtCore.QVariant(self._number_of_commits - section)
        
        return QtCore.QVariant()

    ##############################################

    def columnCount(self, index=QtCore.QModelIndex()):

        return len(self._column_names)

    ##############################################

    def rowCount(self, index=QtCore.QModelIndex()):

        return self._number_of_commits

####################################################################################################
#
# End
#
####################################################################################################
