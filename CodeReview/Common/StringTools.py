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

"""This module provides string tools."""

####################################################################################################

def remove_trailing_newline(text):

    r"""Return the string *text* with only the last trailing newline (``\r\n``, ``\r``, ``\n``) removed.
    By contrast the standard function :func:`string.rstrip` removes all the trailing newlines.

    """

    if text.endswith('\r\n'):
        return text[:-2]
    elif text and text[-1] in ('\n', '\r'):
        return text[:-1]
    else:
        return text
