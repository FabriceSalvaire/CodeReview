####################################################################################################
#
# PyQGit - A Python/Qt Git GUI
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

""" This modules provides iterator tools. """

####################################################################################################

def pairwise(iterable):

    """ Return a generator which generate a pair wise list from an iterable: s -> (s[0],s[1]),
    (s[1],s[2]), ... (s[N-1], s[N]).
    """

    prev = iterable[0]
    for x in iterable[1:]:
        yield prev, x
        prev = x

####################################################################################################

def iter_with_last_flag(iterable):
    
    """ Iterate over an iterable and yield a 2-tuple containing the current item and a Boolean
    indicating if it is the last item.
    """

    last_index = len(iterable) -1
    for i, x in enumerate(iterable):
        yield x, i == last_index

####################################################################################################
#
# End
#
####################################################################################################
