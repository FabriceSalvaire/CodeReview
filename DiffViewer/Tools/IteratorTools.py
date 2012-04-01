####################################################################################################

def pairwise(iterable):

    """ Return a generator which generate a pair wise list from an iterable.
    s -> (s[0],s[1]), (s[1],s[2]), ... (s[N-1], s[N])
    """

    prev = iterable[0]
    for x in iterable[1:]:
        yield prev, x
        prev = x

####################################################################################################

def iter_with_last_flag(iterable):

    last_index = len(iterable) -1
    for i, x in enumerate(iterable):
        yield x, i == last_index

####################################################################################################
#
# End
#
####################################################################################################
