####################################################################################################
#
# CodeReview - A Python/Qt Git GUI
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

import os

####################################################################################################

class Path(object):

    config_directory = os.path.join(os.environ['HOME'], '.config', 'pyqgit')

    # data_directory = os.path.join(os.environ['HOME'], '.local', 'share', 'data', 'pyqgit')
    data_directory = os.path.join(os.environ['HOME'], '.local', 'pyqgit')

####################################################################################################

class Email(object):

    from_address = 'fabrice.salvaire@orange.fr'
    to_address = ['fabrice.salvaire@orange.fr',]

####################################################################################################

class Help(object):

    host = 'localhost'
    url_scheme = 'http'
    url_path_pattern = '/'

####################################################################################################

class Shortcut(object):

    pass

####################################################################################################
#
# End
#
####################################################################################################
