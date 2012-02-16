####################################################################################################

class Slice(object):

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

        return self.__class__(self._start, self._stop)

    ###############################################

    def __getitem__(self, i):

        if i == 0:
            return self._start
        elif i == 1:
            return self._stop
        else:
            raise IndexError

    ###############################################

    def __repr__(self):

        if bool(self):
            string_interval = '[%u, %u]' % (self.lower, self.upper)
        else:
            string_interval = '[%u]' % (self.start)
        
        return self.__class__.__name__ + ' ' + string_interval

    ###############################################

    def __len__(self):
        
        return self._stop - self._start

    ###############################################

    def __bool__(self):

        # None > None = False
        
        return self._stop > self._start

    ###############################################

    def __call__(self):

        return slice(self._start, self._stop)

    ###############################################

    def _get_lower(self):

        if bool(self):
            return self._start
        else:
            return None

    ###############################################

    def _get_upper(self):

        if bool(self):
            return self._stop -1
        else:
            return None

    ###############################################

    lower = property(_get_lower, None, None, 'Lower index')
    upper = property(_get_upper, None, None, 'Upper index')

    ###############################################

    def _get_start(self):

        return self._start

    ###############################################

    def _get_stop(self):

        return self._stop

    ###############################################

    start = property(_get_start, None, None, 'Start index')
    stop = property(_get_stop, None, None, 'Stop index')

    ###############################################

    def map(self, slice_):

        start = slice_.start + self._start
        stop = slice_.stop + self._start

        if stop > self._stop:
            raise IndexError

        return self.__class__(start, stop)

    ###############################################

    def __idiv__(self, scale):

        self._start /= scale
        self._stop /= scale

        return self

    ###############################################

    def __div__(self, scale):

        return self.__class__(self._start / scale, self._stop / scale)

    ###############################################

    @staticmethod
    def _intersection(i1, i2):

        if i1.intersect(i2):
            return (max((i1._start, i2._start)),
                    min((i1._stop, i2._stop)))
        else:
            return None, None

    def __and__(i1, i2):

        """ Return the intersection of i1 and i2
        """

        return i1.__class__(*i1._intersection(i1, i2))

    def __iand__(self, i2):

        """ Update the interval with its intersection with i2
        """

        self._start, self._stop = self._intersection(self, i2)
        return self

   ###############################################

    def intersect(i1, i2):

        """ Does the interval intersect with i2?
        """

        return ((i1._start < i2._stop and i2._start < i1._stop) or
                (i2._start < i1._stop and i1._start < i2._stop))

    ###############################################

    @staticmethod
    def _union(i1, i2):

        return (min((i1._start, i2._start)),
                max((i1._stop, i2._stop)))

    def __or__(i1, i2):

        """ Return the union of i1 and i2
        """

        return i1.__class__(*i1._union(i1, i2))

    def __ior__(self, i2):

        """ Update the interval with its union with i2
        """

        self._start, self._stop = self._union(self, i2)
        return self
    
    ###############################################

    def is_included_in(i1, i2):

        """ Is the interval included in i1?
        """
        
        return i2._start <= i1._start and i1._stop <= i2._stop
    
#####################################################################################################

class FlatSlice(Slice):
    pass

class LineSlice(Slice):
    pass

####################################################################################################
#
# End
#
####################################################################################################
