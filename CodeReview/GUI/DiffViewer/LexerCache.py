####################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2017 Fabrice Salvaire
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
import os

import pygments.lexers as pygments_lexers

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class LexerCache:

    _logger = _module_logger.getChild('LexerCache')

    ##############################################

    def __init__(self):

        self._extension_cache = {}
        self._mode_cache = {}

    ##############################################

    @staticmethod
    def find_mode(text):

        start_pattern = '-*- mode:'
        start = text.find(start_pattern)
        if start != -1:
            stop = text.find('-*-', start)
            if stop != -1:
                return text[start + len(start_pattern):stop].strip()
        return None

    ##############################################

    def guess(self, filename, text):

        # This request is slow !
        # try:
        #     # get_lexer_for_filename(filename)
        #     return pygments_lexers.guess_lexer_for_filename(path, text, stripnl=False)
        # except pygments_lexers.ClassNotFound:
        #     try:
        #         return pygments_lexers.guess_lexer(text, stripnl=False)
        #     except pygments_lexers.ClassNotFound:
        #         return None

        extension = os.path.splitext(filename)[-1]
        if extension:
            # Try to find lexer from extension
            if extension in self._extension_cache:
                return self._extension_cache[extension]
            else:
                try:
                    lexer = pygments_lexers.get_lexer_for_filename(filename)
                    self._extension_cache[extension] = lexer
                    return lexer
                except pygments_lexers.ClassNotFound:
                    pass

        # Try to find lexer from -*- mode: MODE -*-
        mode = self.find_mode(text)
        if mode is not None:
            if mode in self._mode_cache:
                return self._mode_cache[mode]
            else:
                try:
                    lexer = pygments_lexers.get_lexer_by_name(mode)
                    self._mode_cache[mode] = lexer
                    return lexer
                except pygments_lexers.ClassNotFound:
                    pass

        self._logger.warn("Cannot found lexer for {}".format(filename))
        return None
