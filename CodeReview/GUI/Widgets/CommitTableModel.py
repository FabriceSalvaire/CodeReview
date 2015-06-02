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

####################################################################################################

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

####################################################################################################

class CommitTableModel(QtCore.QAbstractTableModel):

    ##############################################

    def __init__(self, repository):

        super(CommitTableModel, self).__init__()

        self._column_names = (
            'Old Path',
            'New Path',
            'Modification',
        )

        self._repository = repository
        
        self._patch_datas = []
        self._number_of_patches = 0

    ##############################################

    def update(self, commit1=None, commit2=None):

        self._patch_datas = []
        self._number_of_patches = 0

        # GIT_DIFF_PATIENCE
        diff = self._repository.diff(commit1, commit2)
        diff.find_similar()
        # flags, rename_threshold, copy_threshold, rename_from_rewrite_threshold, break_rewrite_threshold, rename_limit
        for patch in diff:
            if patch.new_file_path != patch.old_file_path:
                new_file_path = patch.new_file_path + ' {} %'.format(patch.similarity)
            else:
                new_file_path = ''
            patch_data = (patch.old_file_path, new_file_path, patch.status, patch)
            self._patch_datas.append(patch_data)

        self._number_of_patches = len(diff)

        self.modelReset.emit()

    ##############################################

    def __getitem__(self, i):

        return self._patch_datas[i][-1]

    ##############################################

    def data(self, index, role=Qt.DisplayRole):

        if not index.isValid():
            return QtCore.QVariant()
        column = index.column()
        patch = self._patch_datas[index.row()]
        
        if role == Qt.DisplayRole:
            return QtCore.QVariant(patch[column])
        elif role == Qt.ForegroundRole and column == 0:
            modification = patch[2] # Fxme: enumerate
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
                column_name = self._column_names[section]
                return QtCore.QVariant(column_name)
        
        return QtCore.QVariant()

    ##############################################

    def columnCount(self, index=QtCore.QModelIndex()):

        return len(self._column_names)

    ##############################################

    def rowCount(self, index=QtCore.QModelIndex()):

        return self._number_of_patches

    ##############################################

    def sort(self, column, order):

       reverse = order == Qt.DescendingOrder
       self._patch_datas.sort(key=lambda x:x[column], reverse=reverse)
       self.modelReset.emit()

####################################################################################################
#
# End
#
####################################################################################################
