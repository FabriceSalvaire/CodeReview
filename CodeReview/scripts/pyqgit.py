#! /usr/bin/env python3

####################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2015 Fabrice Salvaire
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

import CodeReview.Common.Logging.Logging as Logging
logger = Logging.setup_logging('pyqgit')

####################################################################################################

import argparse

from CodeReview.GUI.LogBrowser.LogBrowserApplication import LogBrowserApplication
from CodeReview.Common.ProgramOptions import PathAction

####################################################################################################

def main():
    argument_parser = argparse.ArgumentParser(description='Log Browser')

    argument_parser.add_argument(
        'path', metavar='PATH',
        action=PathAction,
        nargs='?', default='.',
        help='path',
    )

    argument_parser.add_argument(
        '--diff-a',
        default=None,
        help='set a/old reference for diff a/b',
    )

    argument_parser.add_argument(
        '--diff-b',
        default=None,
        help='set b/new reference for diff a/b',
    )

    argument_parser.add_argument(
        '--user-script',
        action=PathAction,
        default=None,
        help='user script to execute',
    )

    argument_parser.add_argument(
        '--user-script-args',
        default='',
        help="user script args (don't forget to quote)",
    )

    args = argument_parser.parse_args()

    application = LogBrowserApplication(args)
    application.exec_()
