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

"""Module to implement a application settings.

"""

####################################################################################################

__all__ = [
    'ApplicationSettings',
    'Shortcut',
]

####################################################################################################

import logging

# Fixme:
from PyQt5.QtCore import QSettings
from PyQt5.QtQml import QQmlListProperty
from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
    # QUrl,
)

from . import DefaultSettings
from .DefaultSettings import Shortcuts

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Shortcut(QObject):

    _logger = _module_logger.getChild('Shortcut')

    ##############################################

    def __init__(self, settings, name, display_name, sequence):

        super().__init__()

        self._settings = settings
        self._name = name
        self._display_name = display_name
        self._default_sequence = sequence
        self._sequence = sequence

    ##############################################

    @Property(str, constant=True)
    def name(self):
        return self._name

    @Property(str, constant=True)
    def display_name(self):
        return self._display_name

    @Property(str, constant=True)
    def default_sequence(self):
        return self._default_sequence

    ##############################################

    sequence_changed = Signal()

    @Property(str, notify=sequence_changed)
    def sequence(self):
        self._logger.info('get sequence {} = {}'.format(self._name, self._sequence))
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        if self._sequence != value:
            self._logger.info('Shortcut {} = {}'.format(self._name, value))
            self._sequence = value
            self._settings.set_shortcut(self)
            self.sequence_changed.emit()

####################################################################################################

class ApplicationSettings(QSettings):

    """Class to implement application settings."""

    _logger = _module_logger.getChild('ApplicationSettings')

    ##############################################

    def __init__(self):

        super().__init__()
        self._logger.info('Loading settings from {}'.format(self.fileName()))

        self._shortcut_map = {
            name: Shortcut(self, name, self._shortcut_display_name(name), self._get_shortcut(name))
            for name in self._shortcut_names
        }
        self._shortcuts = list(self._shortcut_map.values())

    ##############################################

    @property
    def _shortcut_names(self):
        return [name for name in dir(Shortcuts) if not name.startswith('_')]

    def _shortcut_display_name(self, name):
        return getattr(Shortcuts, name)[0]

    def _default_shortcut(self, name):
        return getattr(Shortcuts, name)[1]

    ##############################################

    def _shortcut_path(self, name):
        return 'shortcut/{}'.format(name)

    ##############################################

    def _get_shortcut(self, name):
        path = self._shortcut_path(name)
        if self.contains(path):
            return self.value(path)
        else:
            return self._default_shortcut(name)

    ##############################################

    def set_shortcut(self, shortcut):
        path = self._shortcut_path(shortcut.name)
        self.setValue(path, shortcut.sequence)

    ##############################################

    @Property(QQmlListProperty, constant=True)
    def shortcuts(self):
        return QQmlListProperty(Shortcut, self, self._shortcuts)

    ##############################################

    @Slot(str, result=Shortcut)
    def shortcut(self, name):
        return self._shortcut_map.get(name, None)

    ##############################################

    # @Slot(str, result=str)
    # def shortcut_sequence(self, name):
    #     shortcut = self._shortcut_map.get(name, None)
    #     if shortcut is not None:
    #         return shortcut.sequence
    #     else:
    #         return None
