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

import yaml
import logging
import logging.config

####################################################################################################

from CodeReview.Logging.ExceptionHook import DispatcherExceptionHook, StderrExceptionHook
from CodeReview.Tools.Singleton import singleton
import CodeReview.Config.ConfigInstall as ConfigInstall

####################################################################################################

@singleton
class ExceptionHookInitialiser(object):

    ##############################################

    def __init__(self, context, stderr=True):

        self._context = context
        self._dispatcher_exception_hook = DispatcherExceptionHook()

        if stderr:
            stderr_exception_hook = StderrExceptionHook()
            self._dispatcher_exception_hook.register_observer(stderr_exception_hook)

####################################################################################################

def setup_logging(application_name, config_file=ConfigInstall.Logging.default_config_file):

    logging_config_file_name = ConfigInstall.Logging.find(config_file)
    logging_config = yaml.load(open(logging_config_file_name, 'r'))

    # Fixme: \033 is not interpreted in YAML
    formatter_config = logging_config['formatters']['ansi']['format']
    logging_config['formatters']['ansi']['format'] = formatter_config.replace('<ESC>', '\033')
    logging.config.dictConfig(logging_config)

    logger = logging.getLogger(application_name)
    logger.info('Start %s' % (application_name))

    return logger

####################################################################################################
#
# End
#
####################################################################################################
