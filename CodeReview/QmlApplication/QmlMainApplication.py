####################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2019 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

__all__ = ['Application']

####################################################################################################

import logging

from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
    Qt, QTimer, QUrl
)

# Fixme: PYSIDE-574 qmlRegisterSingletonType and qmlRegisterUncreatableType missing in QtQml
from QtShim.QtQml import qmlRegisterUncreatableType

from . import QmlBaseApplication
from ..Common.ArgparseAction import PathAction
from .QmlRepository import (
    QmlBranch,
    QmlCommit,
    QmlCommitPool,
    QmlNote,
    QmlReference,
    QmlRepository,
)

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QmlApplication(QmlBaseApplication.QmlApplication):

    _logger = _module_logger.getChild('QmlApplication')

    ##############################################

    def __init__(self, application):

        super().__init__(application)

        self._repository = None

    ##############################################

    @Slot(str)
    def load_repository(self, path):

        self._logger.info(path)
        try:
            self._repository = QmlRepository(path)
        except NameError as exception:
            # self.show_message(, warn=True)
            self._repository = None
            pass
        self.repository_changed.emit()

    ##############################################

    repository_changed = Signal()

    @Property(QmlRepository, notify=repository_changed)
    def repository(self):
        return self._repository

####################################################################################################

class Application(QmlBaseApplication.Application):

    _logger = _module_logger.getChild('Application')

    QmlApplication_CLS = QmlApplication

    ##############################################

    def parse_arguments(self):

        super().parse_arguments()

        self.parser.add_argument(
            'path', metavar='PATH',
            action=PathAction,
            nargs='?', default='.',
            help='path',
        )

        self.parser.add_argument(
            '--diff-a',
            default=None,
            help='set a/old reference for diff a/b',
        )

        self.parser.add_argument(
            '--diff-b',
            default=None,
            help='set b/new reference for diff a/b',
        )

    ##############################################

    def register_qml_types(self):

        super().register_qml_types()

        qmlRegisterUncreatableType(QmlBranch, 'CodeReview', 1, 0, 'QmlBranch', 'Cannot create QmlBranch')
        qmlRegisterUncreatableType(QmlCommit, 'CodeReview', 1, 0, 'QmlCommit', 'Cannot create QmlCommit')
        qmlRegisterUncreatableType(QmlCommitPool, 'CodeReview', 1, 0, 'QmlCommitPool', 'Cannot create QmlCommitPool')
        qmlRegisterUncreatableType(QmlNote, 'CodeReview', 1, 0, 'QmlNote', 'Cannot create QmlNote')
        qmlRegisterUncreatableType(QmlReference, 'CodeReview', 1, 0, 'QmlReference', 'Cannot create QmlReference')
        qmlRegisterUncreatableType(QmlRepository, 'CodeReview', 1, 0, 'QmlRepository', 'Cannot create QmlRepository')

    ##############################################

    def post_init(self):
        self.qml_application.load_repository(self.args.path)
        super().post_init()
