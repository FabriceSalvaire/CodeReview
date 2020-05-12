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

"""Module to implement argparse actions.

"""

####################################################################################################

__all__ = [
    'PathAction',
]

####################################################################################################

import argparse
from pathlib import Path

####################################################################################################

class PathAction(argparse.Action):

    """Class to implement argparse action for path."""

    ##############################################

    def __call__(self, parser, namespace, values, option_string=None):

        if values is not None:
            if isinstance(values, list):
                path = [Path(x) for x in values]
            else:
                path = Path(values)
        else:
            path = None
        setattr(namespace, self.dest, path)
