# -*- coding: utf-8 -*-

####################################################################################################
#
# CodeReview - A Python/Qt Git GUI
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

import logging
import sys
import traceback

####################################################################################################

from CodeReview.Tools.Path import to_absolute_path
from CodeReview.Tools.Platform import Platform

####################################################################################################

class ApplicationBase(object):

    _logger = logging.getLogger(__name__)

    has_gui = False

    ##############################################

    def __init__(self, args, **kwargs):

        self._logger.debug(str(args) + ' ' + str(kwargs))

        sys.excepthook = self._exception_hook

        self._args = args
        self._platform = Platform()

    ##############################################

    @property
    def args(self):
        return self._args

    @property
    def platform(self):
        return self._platform

    ##############################################

    def _exception_hook(self, exception_type, exception_value, exception_traceback):

        traceback.print_exception(exception_type, exception_value, exception_traceback)

        # return sys.__excepthook__(exception_type, exception_value, exception_traceback)

    ##############################################

    def execute_given_user_script(self):

        if self._args.user_script is not None:
            self.execute_user_script(self._args.user_script)

    ##############################################

    def execute_user_script(self, file_name):

        """ Execute an user script provided by file *file_name* in a context where is defined a
        variable *application* that is a reference to the application instance.
        """

        file_name = to_absolute_path(file_name)
        self.show_message(message='Execute user script: ' + file_name, echo=True)
        source = open(file_name).read()
        bytecode = compile(source, file_name, 'exec')
        exec(bytecode, {'application':self})
        self.show_message(message='User script done', echo=True)

    ##############################################

    def exit(self):

        sys.exit(0)

    ##############################################

    def show_message(self, message=None, **kwargs):

        self._logger.info(message)

####################################################################################################
#
# End
#
####################################################################################################
