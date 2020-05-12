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

####################################################################################################

def html_highlight_backtrace(backtrace_text):

    """Highlight a backtrace using HTML tags."""

    lines = [x for x in backtrace_text.split('\n') if x]

    backtrace_highlighted = '<h3>' + lines[0] + '</h3>'

    for line in lines[1:-1]:
        line = line.replace('<', '(')
        line = line.replace('>', ')')
        if 'File' in line:
            line = '<font color="blue"><h6>' + line + '</h6>'
        else:
            line = '<font color="black"><code>' + line + '</code>'
        backtrace_highlighted += line

    backtrace_highlighted += '<font color="blue"><h4>' + lines[-1] + '</h4>'

    return backtrace_highlighted
