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

import glob
import sys

from setuptools import setup, find_packages, Extension
setuptools_available = True

####################################################################################################

if sys.version_info < (3,):
    print('CodeReview requires Python 3', file=sys.stderr)
    sys.exit(1)

exec(compile(open('setup_data.py').read(), 'setup_data.py', 'exec'))

####################################################################################################

setup_dict.update(dict(
    # include_package_data=True, # Look in MANIFEST.in
    scripts=['bin/pyqgit', 'bin/diff-viewer'],
    console_scripts=['bin/pyqgit', 'bin/diff-viewer'],
    packages=find_packages(exclude=['unit-test']),
    ext_modules=[
        Extension('CodeReview.PatienceDiff._patiencediff_c',
                  ['CodeReview/PatienceDiff/_patiencediff_c.c']),
        Extension('CodeReview.TextDistance.levenshtein_distance_c',
                  ['CodeReview/TextDistance/levenshtein_distance.c'])
    ],
    package_data={
        'CodeReview.Config': ['logging.yml'],
    },
    data_files=[
        ('share/CodeReview/icons', glob.glob('share/icons/*.png')),
        ('share/CodeReview/icons/32x32', glob.glob('share/icons/32x32/*.png')),
        ('share/CodeReview/icons/48x48', glob.glob('share/icons/48x48/*.png')),
        ('share/CodeReview/icons/svg', glob.glob('share/icons/svg/*.svg')),
    ],

    platforms='any',
    zip_safe=False, # due to data files

    # cf. http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Topic :: Software Development :: Version Control",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
    ],

    install_requires=[
        'PyQt5',
        'PyYAML',
        'Pygments',
        'pygit2',
    ],
))

####################################################################################################

setup(**setup_dict)
