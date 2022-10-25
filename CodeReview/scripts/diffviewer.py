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

####################################################################################################

from CodeReview.Common.Logging import Logging
logger = Logging.setup_logging('pyqgit')

####################################################################################################

import argparse

####################################################################################################

from CodeReview.GUI.DiffViewer.DiffViewerApplication import DiffViewerApplication
from CodeReview.Common.ProgramOptions import PathAction

####################################################################################################

def main() -> None:

    argument_parser = argparse.ArgumentParser(description='Diff Viewer')

    argument_parser.add_argument(
        'file1', metavar='File1',
        help='First file',
    )

    argument_parser.add_argument(
        'file2', metavar='File2',
        help='Second File',
    )

    argument_parser.add_argument(
        '--show',
        action='store_true',
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

    application = DiffViewerApplication(args)
    application.exec_()
