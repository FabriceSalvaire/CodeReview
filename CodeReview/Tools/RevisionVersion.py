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

__ALL__ = ['RevisionVersion']

####################################################################################################

import re

####################################################################################################

class RevisionVersion(object):

    scale = 10**3 # 32 bits
    # scale = 10**6 # 64 bits

    ##############################################

    def __init__(self, version):

        if isinstance(version, str):
            match = re.match('v([0-9]+)\.([0-9]+)\.([0-9]+)(-.*)?', version)
            if match is not None:
                groups = match.groups()
                self.major, self.minor, self.revision = [int(x) for x in groups[:3]]
                self.suffix = groups[3]
            else:
                raise NameError('Bad version string %s' % (version))

        elif isinstance(version, tuple):
            self.major, self.minor, self.revision = version[:3]
            if len(version) == 4:
                self.suffix = version[3]
            else:
                self.suffix = None

        elif isinstance(version, dict):
            self.major, self.minor, self.revision = [version[key] for key in ('major', 'minor', 'revision')]
            if 'suffix' in version:
                self.suffix = version['suffix']
            else:
                self.suffix = None

        else:
            raise NameError('parameter must be a string or a tuple')

        # Check the scale
        for x in self.major, self.minor, self.revision:
            if x >= self.scale:
                raise NameError('Version %s must be less than %u' % (str(self), self.scale))

    ##############################################

    def __eq__(a, b):

        return a.major == b.major and a.minor == b.minor and a.revision == b.revision 

    ##############################################

    def __ge__(a, b):

        return int(a) >= int(b)

    ##############################################

    def __gt__(a, b):

        return int(a) > int(b)

    ##############################################

    def __le__(a, b):

        return int(a) <= int(b)

    ##############################################

    def __lt__(a, b):

        return int(a) < int(b)

    ##############################################

    def __int__(self):

        return (self.major * self.scale + self.minor) * self.scale + self.revision

    ##############################################

    def version_string(self):

        return 'v%u.%u.%u' % (self.major, self.minor, self.revision)

    ##############################################

    def __str__(self):

        version_string = self.version_string()
        if self.suffix is not None:
            version_string += self.suffix

        return version_string

    ##############################################

    def to_list(self):

        # Fixme: useful?

        return [self.major, self.minor, self.revision, self.suffix]
