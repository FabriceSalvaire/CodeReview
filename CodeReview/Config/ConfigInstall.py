####################################################################################################

from pathlib import Path
import os
import sys

####################################################################################################

import CodeReview.Common.Path as PathTools   # due to Path class

####################################################################################################

_this_file = Path(__file__).absolute()

class Path:

    CodeReview_module_directory = _this_file.parents[1]
    config_directory = _this_file.parent

    ##############################################

    @staticmethod
    def share_directory():
        return Path.CodeReview_module_directory.joinpath('share')

####################################################################################################

class Logging:

    default_config_file = 'logging.yml'
    directories = (Path.config_directory,)

    ##############################################

    @staticmethod
    def find(config_file):
        return PathTools.find(config_file, Logging.directories)

####################################################################################################

class Icon:

    icon_directory = Path.share_directory().joinpath('icons')

    ##############################################

    @staticmethod
    def find(file_name, icon_size):
        if icon_size == 'svg':
            size_directory = icon_size
        else:
            size_directory = f'{icon_size}x{icon_size}'
        icon_directory = Icon.icon_directory.joinpath(size_directory)
        return PathTools.find(file_name, (icon_directory,))
