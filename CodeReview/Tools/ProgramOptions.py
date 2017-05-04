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

import argparse

####################################################################################################

from CodeReview.Tools.Path import to_absolute_path

####################################################################################################

class PathAction(argparse.Action):

    ##############################################

    def __call__(self, parser, namespace, values, option_string=None):

        if values is not None:
            if isinstance(values, list):
                absolute_path = [to_absolute_path(x) for x in values]
            else:
                absolute_path = to_absolute_path(values)
        else:
            absolute_path = None
        setattr(namespace, self.dest, absolute_path)
