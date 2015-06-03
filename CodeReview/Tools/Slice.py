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

"""This module implements interval arithmetic for flat [#f1]_ and line slice.

.. [#f1] Flat indexes address characters in a file.

"""

####################################################################################################

class Slice(object):

    """This class implements a generic slice.

    Like for a standard Python slice, a :class:`Slice` instance is built from two values or an
    indexable object providing the start and stop value.  This class implements an array interface
    (:func:`__getitem__` method) so as to pass a :class:`Slice` instance to the constructor.  Some
    examples to build a slice::

      slice1 = Slice(1, 2)
      slice2 = Slice((1, 2))
      slice2 = Slice([1, 2])
      slice3 = Slice(slice2)

    The interval limits of the slice can be accessed using the :attr:`start`, :attr:`stop`,
    :attr:`lower` and :attr:`upper` read-only attributes, *upper* is defined as *stop* -1.

    To cast an instance to a standard Python slice use the call::

      slice()

    To get the length of the slice defined by *stop* - *start* use the :func:`len` function.

    A slice is not empty if it verifies the predicate *stop* > *start*, this predicate can be tested
    using a Boolean evaluation of the instance.

    A slice can be scaled by a factor using::

      slice // 2
      slice //= 2

    The union and the intersection of two slices can be computed using::

      # union
      slice1 |= slice2
      slice = slice1 | slice2

      # intersection
      slice1 &= slice2
      slice = slice1 & slice2

    """

    # How to subclass slice ?

    ###############################################

    def __init__(self, *args):

        array = self._check_arguments(args)
        start = array[0]
        stop = array[1]
        
        if stop < start:
            raise ValueError('stop < start')
        
        self._start = start
        self._stop = stop

    ###############################################

    def _check_arguments(self, args):

        """Check the arguments provided to the constructor."""

        size = len(args)
        if size == 1:
            array = args[0]
        elif size == 2:
            array = args
        else:
            raise ValueError
        
        return array

    ###############################################

    def copy(self):

        # Clone ?

        """Return a copy of the slice."""

        return self.__class__(self._start, self._stop)

    ###############################################

    def __getitem__(self, i):

        """Provide an array interface to the slice."""

        if i == 0:
            return self._start
        elif i == 1:
            return self._stop
        else:
            raise IndexError

    ###############################################

    def __repr__(self):

        """Pretty-print a slice."""

        if bool(self):
            string_interval = '[%u, %u]' % (self.lower, self.upper)
        else:
            string_interval = '[]@%u' % (self.start)
        
        return self.__class__.__name__ + ' ' + string_interval

    ###############################################

    def __len__(self):

        """ Return the length of the slice defined by stop - start. """

        return self._stop - self._start

    ###############################################

    def __bool__(self):

        """ Test is the slice is not the empty. """

        # None > None = False

        return self._stop > self._start

    ###############################################

    def __call__(self):

        """ Return a standard Python slice. """

        return slice(self._start, self._stop)

    ###############################################

    @property
    def lower(self):

        """ Lower boundary. """

        if bool(self):
            return self._start
        else:
            return None

    ###############################################

    @property
    def upper(self):

        """ Upper boundary. """

        if bool(self):
            return self._stop -1
        else:
            return None

    ###############################################

    @property
    def start(self):

        """ Start boundary. """

        return self._start

    ###############################################

    @property
    def stop(self):

        """Stop boundary."""

        return self._stop

    ###############################################

    def map(self, sub_slice):

        """Map a sub-slice in the slice domain.

        Return a new slice shifted by *start*.

        """

        start = sub_slice.start + self._start
        stop = sub_slice.stop + self._start

        if stop > self._stop:
            raise IndexError
        
        return self.__class__(start, stop)

    ###############################################

    def __ifloordiv__(self, scale):

        """Divide start and stop by *scale*."""

        self._start //= scale
        self._stop //= scale
        
        return self

    ###############################################

    def __floordiv__(self, scale):

        """Return a new slice with start and stop divided by *scale*."""

        return self.__class__(self._start // scale, self._stop // scale)

    ###############################################

    @staticmethod
    def _intersection(i1, i2):

        """Compute the intersection of two slices."""

        if i1.intersect(i2):
            return (max((i1._start, i2._start)),
                    min((i1._stop, i2._stop)))
        else:
            return None, None

    def __and__(i1, i2):

        """Return the intersection of i1 and i2."""

        return i1.__class__(*i1._intersection(i1, i2))

    def __iand__(self, i2):

        """Update the interval with its intersection with i2."""

        self._start, self._stop = self._intersection(self, i2)
        return self

   ###############################################

    def intersect(i1, i2):

        """Test if the interval intersects with i2."""

        return ((i1._start < i2._stop and i2._start < i1._stop) or
                (i2._start < i1._stop and i1._start < i2._stop))

    ###############################################

    @staticmethod
    def _union(i1, i2):

        """Compute the union of two slices."""

        return (min((i1._start, i2._start)),
                max((i1._stop, i2._stop)))

    def __or__(i1, i2):

        """Return the union of i1 and i2."""

        return i1.__class__(*i1._union(i1, i2))

    def __ior__(self, i2):

        """Update the interval with its union with i2."""

        self._start, self._stop = self._union(self, i2)
        return self

    ###############################################

    def is_included_in(i1, i2):

        """Test if the interval is included in i2."""

        return i2._start <= i1._start and i1._stop <= i2._stop

####################################################################################################

class FlatSlice(Slice):
    """This class defines a flat slice."""
    pass

####################################################################################################

class LineSlice(Slice):
    """This class defines a line slice."""
    pass

####################################################################################################
#
# End
#
####################################################################################################
