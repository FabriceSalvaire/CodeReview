####################################################################################################

class Slice(object):

    # How to subclass slice ?

    ###############################################

    def __init__(self, *args):
        
        start, stop = args[:2]

        if stop < start:
            raise ValueError('stop < start')

        self._start = start
        self._stop = stop

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
