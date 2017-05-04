####################################################################################################

import os
import sys

####################################################################################################

import CodeReview.Tools.Path as PathTools # due to Path class

####################################################################################################

_this_file = PathTools.to_absolute_path(__file__)

class Path(object):

    CodeReview_module_directory = PathTools.parent_directory_of(_this_file, step=2)
    config_directory = os.path.dirname(_this_file)

    ##############################################

    @staticmethod
    def share_directory():

        path = os.path.dirname(Path.CodeReview_module_directory)
        if path.startswith(sys.exec_prefix):
            return os.path.join(sys.exec_prefix, 'share', 'CodeReview')
        else:
            return os.path.join(path, 'share')

####################################################################################################

class Logging(object):

    default_config_file = 'logging.yml'
    directories = (Path.config_directory,)

    ##############################################

    @staticmethod
    def find(config_file):

        return PathTools.find(config_file, Logging.directories)

####################################################################################################

class Icon(object):

    icon_directory = os.path.join(Path.share_directory(), 'icons')

    ##############################################

    @staticmethod
    def find(file_name, icon_size):

        if icon_size == 'svg':
            size_directory = icon_size
        else:
            size_directory = '{0}x{0}'.format(icon_size)

        icon_directory = os.path.join(Icon.icon_directory, size_directory)
        return PathTools.find(file_name, (icon_directory,))
