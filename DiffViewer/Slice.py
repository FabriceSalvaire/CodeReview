####################################################################################################

class Slice(object):

    # How to subclass slice ?

    ###############################################

    def __init__(self, start, stop):
        
        if stop < start:
            raise ValueError('stop < start')

        self._start = start
        self._stop = stop

    ###############################################

    def __repr__(self):

        return self.__class__.__name__ + ' [%u, %u]' % (self._start, self._stop)

    ###############################################

    def __len__(self):

        return self._stop - self._start

    ###############################################

    def __bool__(self):

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

        return Slice(start, stop)

    ###############################################

    def __idiv__(self, scale):

        self._start /= scale
        self._stop /= scale

        return self

    ###############################################

    def __div__(self, scale):

        return self.__class__(self._start / scale, self._stop / scale)

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
