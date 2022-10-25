####################################################################################################

from pathlib import Path as plPath
import sys

####################################################################################################

import CodeReview.Common.Path as PathTools   # due to Path class

####################################################################################################

class OsFactory:

    ##############################################

    def __init__(self) -> None:
        if sys.platform.startswith('linux'):
            self._name = 'linux'
        elif sys.platform.startswith('win'):
            self._name = 'windows'
        elif sys.platform.startswith('darwin'):
            self._name = 'osx'

    ##############################################

    @property
    def name(self) -> str:
        return self._name

    @property
    def on_linux(self) -> bool:
        return self._name == 'linux'

    @property
    def on_windows(self) -> bool:
        return self._name == 'windows'

    @property
    def on_osx(self) -> bool:
        return self._name == 'osx'

OS = OsFactory()

####################################################################################################

_this_file = plPath(__file__).absolute()

class Path:

    CodeReview_module_directory = _this_file.parents[1]
    config_directory = _this_file.parent

    ##############################################

    @staticmethod
    def share_directory() -> plPath:
        return Path.CodeReview_module_directory.joinpath('share')

####################################################################################################

class Logging:

    default_config_file = 'logging.yml'
    directories = (Path.config_directory,)

    ##############################################

    @staticmethod
    def find(config_file: str) -> plPath:
        return PathTools.find(config_file, Logging.directories)

####################################################################################################

class Icon:

    icon_directory = Path.share_directory().joinpath('icons')

    ##############################################

    @staticmethod
    def find(file_name: str, icon_size: int) -> plPath:
        if icon_size == 'svg':
            size_directory = icon_size
        else:
            size_directory = f'{icon_size}x{icon_size}'
        icon_directory = Icon.icon_directory.joinpath(size_directory)
        return PathTools.find(file_name, (icon_directory,))
