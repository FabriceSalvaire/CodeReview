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
#
#  Translated from C++ to Python
#
#   https://github.com/mitchcurtis/slate/blob/master/lib/keysequenceeditor.cpp
#   https://github.com/mitchcurtis/slate/blob/master/lib/keysequenceeditor.h
#
#     Copyright 2016, Mitch Curtis
#
#     This file is part of Slate.
#
#     Slate is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Slate is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Slate. If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import logging

from PyQt5.QtCore import QMetaEnum
from PyQt5.QtGui import QKeyEvent, QKeySequence
from PyQt5.QtQuick import QQuickItem

from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
    Qt,
)

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class KeyHelper(QObject):
    def key_name(self, index):
        key_enum_index = self.staticQtMetaObject.indexOfEnumerator('Key')
        return self.staticQtMetaObject.enumerator(key_enum_index).valueToKey(index)

_key_helper = KeyHelper()

def _key_name(index):
    # return _key_helper.key_name(index) # Fixme: PyQt5 issue
    return index

####################################################################################################

class KeySequenceEditor(QQuickItem):

    _logger = _module_logger.getChild('KeySequenceEditor')

    ##############################################

    def __init__(self, parent):

        super().__init__(parent)

        self._default_sequence = QKeySequence() # default sequence
        self._edited_sequence = QKeySequence() # current/edited sequence
        self._new_sequence = QKeySequence() # customised sequence

        self._reset_pressed_keys()

    ##############################################

    def _reset_pressed_keys(self):
        self._logger.info('Clearing pressed keys')
        self._pressed_keys = []

    ##############################################

    default_sequence_changed = Signal()

    @Property(str, notify=default_sequence_changed)
    def default_sequence(self):
        return self._default_sequence.toString()

    ##############################################

    @default_sequence.setter
    def default_sequence(self, default_sequence):

        if default_sequence != self._default_sequence.toString():
            self._default_sequence = QKeySequence(default_sequence, QKeySequence.PortableText)
            self._set_edited_sequence('') # Fixme: why reset ???
            self.new_sequence = ''
            self.default_sequence_changed.emit()
            # This might not always be the case, I'm just lazy.
            self.is_customised_changed.emit()
            self.display_sequence_changed.emit()

    ##############################################

    new_sequence_changed = Signal()

    @Property(str, notify=new_sequence_changed)
    def new_sequence(self):
        return self._new_sequence.toString()

    @new_sequence.setter
    def new_sequence(self, new_sequence):

        if new_sequence != self._new_sequence.toString():
            self._new_sequence = QKeySequence(new_sequence, QKeySequence.PortableText)
            self._logger.info('Set new sequence to {}'.format(self._new_sequence.toString()))
            self.new_sequence_changed.emit()
            self.is_customised_changed.emit()
            self.display_sequence_changed.emit()

    ##############################################

    display_sequence_changed = Signal()

    @Property(str, notify=display_sequence_changed)
    def display_sequence(self):

        """Text to show in the sequence editor"""

        if self.hasActiveFocus():
            # we are editing the sequence
            sequence = self._edited_sequence
        elif self._new_sequence.isEmpty():
            # no new sequence
            sequence = self._default_sequence
        else:
            sequence = self._new_sequence

        return sequence.toString()

    ##############################################

    is_customised_changed = Signal()

    @Property(bool, notify=is_customised_changed)
    def is_customised(self):
        """Flag to indicate a new valid sequence is set"""
        return not self._new_sequence.isEmpty() and self._new_sequence != self._default_sequence

    ##############################################

    @Slot()
    def reset(self):
        """Reset the sequence to the default one"""
        self._set_edited_sequence(self.default_sequence)
        self.new_sequence = self.default_sequence
        self._reset_pressed_keys()

    ##############################################

    def _set_edited_sequence(self, edited_sequence=''):

        """Update the edited sequence.

        emit *is_customised* and *display_sequence*
        """

        if edited_sequence != self._edited_sequence.toString():
            self._edited_sequence = QKeySequence(edited_sequence, QKeySequence.PortableText)
            self._logger.info('Edited sequence changed to {}'.format(self._edited_sequence.toString()))
            self.is_customised_changed.emit()
            self.display_sequence_changed.emit()

    ##############################################

    def keyPressEvent(self, event):

        """Handler when a key is pressed.

        * use Escape to leave the control
        * use Enter to accept the sequence

        """

        if event.key() == Qt.Key_Escape:
            self.setFocus(False)

        elif event.key() == Qt.Key_Return:
            self._accept()

        elif not event.isAutoRepeat():
            modifiers = 0
            # event.modifiers().testFlag(...)
            if event.modifiers() & Qt.ControlModifier:
                modifiers |= Qt.CTRL
            if event.modifiers() & Qt.ShiftModifier:
                modifiers |= Qt.SHIFT
            if event.modifiers() & Qt.AltModifier:
                modifiers |= Qt.ALT
            if event.modifiers() & Qt.MetaModifier:
                modifiers |= Qt.META

            if Qt.Key_Shift <= event.key() <= Qt.Key_Meta:
                self._logger.info('Only modifiers were pressed ({} / {} / {} ignoring'.format(
                    event.text(),
                    _key_name(event.key()),
                    QKeySequence(event.key()).toString()
                ))

            else:
                self._pressed_keys.append(event.key() | modifiers)
                self._logger.info('Adding key {} / {} / {} with modifiers ({}) to pressed keys'.format(
                    event.text(),
                    _key_name(event.key()),
                    QKeySequence(event.key()).toString(),
                    # UnicodeEncodeError: 'utf-8' codec can't encode character '\udc21' in position 188: surrogates not allowed
                    QKeySequence(self._pressed_keys[-1]).toString(),
                ))

                sequence = QKeySequence(*self._pressed_keys) # up to 4 keys
                self._set_edited_sequence(sequence.toString())

                if len(self._pressed_keys) == 4:
                    # That was the last key out of four possible keys end it here.
                    self._accept()

        event.accept()

    ##############################################

    def keyReleaseEvent(self, event):
        event.accept()

    ##############################################

    def focusInEvent(self, event):
        event.accept()
        # The text displaying the shortcut should be cleared when editing begins.
        self.display_sequence_changed.emit()

    ##############################################

    def focusOutEvent(self, event):
        event.accept()
        self._cancel()

    ##############################################

    def _accept(self):

        """Update *new_sequence* if the input is valid."""

        self._logger.info('Attempting to accept input...')

        # If there hasn't been anything new successfully entered yet, check against the original
        # sequence, otherwise check against the latest successfully entered sequence.
        # Note: is_customised() assumes that an empty sequence isn't possible we might want to account
        # for this in the future.
        if ((self._edited_sequence != self._default_sequence) or
            (self.is_customised and self._edited_sequence != self._new_sequence)):
            if self._validate(self._edited_sequence):
                self._logger.info('Input valid')
                self.new_sequence = self._edited_sequence.toString()
            else:
                self._logger.info('Input invalid')
                self._cancel()
        else:
            self._logger.info('Nothing has changed in the input')
            # Nothing's changed.

        self._reset_pressed_keys()
        self.setFocus(False)

    ##############################################

    def _cancel(self):

        self._reset_pressed_keys()
        if self._edited_sequence.isEmpty():
            # If the edited sequence is empty, setting it to an empty string
            # obviously won't change anything, and it will return early.
            # We need the display sequence to update though, so call it here.
            self.display_sequence_changed.emit()
        else:
            self._set_edited_sequence('')

    ##############################################

    def _validate(self, sequence):

        """Method to validate the new sequence"""

        self._logger.info('Validating key sequence {} ...'.format(sequence.toString()))
        valid = True # False
        # do some checks
        return valid
