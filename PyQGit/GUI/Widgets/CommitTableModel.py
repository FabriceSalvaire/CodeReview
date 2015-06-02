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

from PyQt5 import QtCore, QtGui, QtWidgets

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
        
        self._patches = []
        self._patche_datas = []
        self._number_of_patches = 0

    ##############################################

    def update(self, commit1=None, commit2=None):

        self._patches = []
        self._patche_datas = []
        self._number_of_patches = 0

        # GIT_DIFF_PATIENCE
        diff = self._repository.diff(commit1, commit2)
        diff.find_similar()
        # flags, rename_threshold, copy_threshold, rename_from_rewrite_threshold, break_rewrite_threshold, rename_limit
        for patch in diff:
            self._patches.append(patch)
            if patch.new_file_path != patch.old_file_path:
                new_file_path = patch.new_file_path + ' {} %'.format(patch.similarity)
            else:
                new_file_path = ''
            patch_data = (patch.old_file_path, new_file_path, patch.status)
            self._patche_datas.append(patch_data)

        self._number_of_patches = len(self._patches) # len(diff)

        self.modelReset.emit()

    ##############################################

    def __getitem__(self, i):

        return self._patches[i]

    ##############################################

    def data(self, index, role=QtCore.Qt.DisplayRole):

        if not index.isValid():
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            patch = self._patche_datas[index.row()]
            column = index.column()
            return QtCore.QVariant(patch[column])

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
        
        return QtCore.QVariant()

    ##############################################

    def columnCount(self, index=QtCore.QModelIndex()):

        return len(self._column_names)

    ##############################################

    def rowCount(self, index=QtCore.QModelIndex()):

        return self._number_of_patches

####################################################################################################
#
# End
#
####################################################################################################
