####################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2017 Fabrice Salvaire
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

from cffi import FFI

####################################################################################################

_ffi = FFI()

_ffi.cdef("""
  int levenshtein_distance(const char *, const char *);
""")

# Fixme: build/lib.linux-x86_64-3.5/CodeReview/TextDistance/levenshtein_distance_c.cpython-35m-x86_64-linux-gnu.so
_levenshtein_distance_lib = _ffi.dlopen('/home/fabrice/home/developpement/code-review/liblevenshtein_distance.so')
c_levenshtein_distance = _levenshtein_distance_lib.levenshtein_distance

def levenshtein_distance(string1, string2):
    return c_levenshtein_distance(string1.encode('utf8'), string2.encode('utf8'))
