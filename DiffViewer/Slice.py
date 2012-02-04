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
