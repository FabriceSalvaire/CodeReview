#! /usr/bin/env python3

####################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2017 Fabrice Salvaire
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

import sys

from setuptools import setup, Extension

####################################################################################################

if sys.version_info < (3,):
    print('CodeReview requires Python 3', file=sys.stderr)
    sys.exit(1)

####################################################################################################

from setup_data import setup_dict
setup(
    **setup_dict,
    # https://setuptools.pypa.io/en/latest/userguide/ext_modules.html
    # Add support for ext_modules in static setup.cfg
    #   https://github.com/pypa/setuptools/issues/2220
    ext_modules=[
        Extension(
            name='CodeReview.PatienceDiff._patiencediff_c',
            sources=['CodeReview/PatienceDiff/_patiencediff_c.c'],
        ),
        Extension(
            name='CodeReview.TextDistance.levenshtein_distance_c',
            sources=['CodeReview/TextDistance/levenshtein_distance.c'],
        )
    ],
)
