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

import datetime

import pygit2 as git

####################################################################################################

from PyQt5 import QtCore, QtGui, QtWidgets

####################################################################################################

class LogTableModel(QtCore.QAbstractTableModel):

    ##############################################

    def __init__(self, repository):

        super(LogTableModel, self).__init__()

        self._column_names = (
            # 'Hex',
            'Message',
            'Date',
            # 'Author',
            'Comitter',
        )

        self._commits = []

        head = repository.head
        head_commit = repository[head.target]
        fromtimestamp = datetime.datetime.fromtimestamp
        for commit in repository.walk(head_commit.id, git.GIT_SORT_TIME):
            commit_data = (
                # commit.hex,
                commit.message,
                fromtimestamp(commit.commit_time).strftime('%Y-%m-%d %H:%M:%S'),
                # commit.author.name,
                commit.committer.name,
            )
            self._commits.append(commit_data)
        self._number_of_commits = len(self._commits)

    ##############################################

    def data(self, index, role=QtCore.Qt.DisplayRole):

        if not index.isValid(): # or not(0 <= index.row() < self._number_of_commits):
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            commit = self._commits[index.row()]
            column = index.column()
            return QtCore.QVariant(commit[column])

        return QtCore.QVariant()

    ##############################################

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):

        if role == QtCore.Qt.TextAlignmentRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QVariant(int(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
            else:
                return QtCore.QVariant(int(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter))
        
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
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
