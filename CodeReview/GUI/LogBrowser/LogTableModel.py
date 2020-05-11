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

__all__ = ['LogTableFilterProxyModel', 'LogTableModel']

####################################################################################################

import datetime
fromtimestamp = datetime.datetime.fromtimestamp

####################################################################################################

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

####################################################################################################

from CodeReview.Tools.EnumFactory import EnumFactory

####################################################################################################

class LogTableFilterProxyModel(QtCore.QSortFilterProxyModel):

    ##############################################

    def __init__(self, parent=None):
        super().__init__(parent)

    ##############################################

    def __getitem__(self, row):
        # Fixme: don't work ???
        model = self.sourceModel()
        index = model.createIndex(row, 0)
        index = self.mapToSource(index)
        row = index.row()
        return model[row]

    ##############################################

    # def filterAcceptsRow(source_row, source_parent):

####################################################################################################

class LogTableModel(QtCore.QAbstractTableModel):

    COLUMN_ENUM = EnumFactory('LogColumnEnum', (
        'revision',
        'message',
        'sha',
        'date',
        'committer',
        ))

    _TITLES = (
        'Revision',
        'Message',
        'Id SH1',
        'Date',
        'Committer',
    )

    ##############################################

    def __init__(self, repository):

        super().__init__()

        self._tags = repository.tags
        commits = repository.commits
        self._number_of_rows = len(commits)
        self._rows = [('', 'Working directory changes', '', '', None)]
        for i, commit in enumerate(commits):
            row = self._commit_data(i, commit)
            self._rows.append(row)

    ##############################################

    def _match_tag(self, commit):

        for ref in self._tags:
            ref_commit = ref.peel()
            if commit.id == ref_commit.id:
                return ref
        return None

    ##############################################

    def _commit_data(self, i, commit):

        ref = self._match_tag(commit)
        if ref is not None:
            tag_name = ref.name
            tag_name = tag_name.replace('refs/tags/', '')
            tag_name = '[{}] '.format(tag_name)
        else:
            tag_name = ''

        author = commit.author
        committer = commit.committer

        return (
            self._number_of_rows - i -1,
            tag_name + commit.message.strip(),
            str(commit.hex),
            fromtimestamp(commit.commit_time).strftime('%Y-%m-%d %H:%M:%S'),
            '{} <{}>'.format(committer.name, committer.email),

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
                return QtCore.QVariant(self._TITLES[section])
            else:
                return QtCore.QVariant(self._number_of_rows - section)

        return QtCore.QVariant()

    ##############################################

    def columnCount(self, index=QtCore.QModelIndex()):
        return len(self._TITLES)

    ##############################################

    def rowCount(self, index=QtCore.QModelIndex()):
        return self._number_of_rows
