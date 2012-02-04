#####################################################################################################

from bzrlib.patiencediff import unified_diff_files, PatienceSequenceMatcher

#####################################################################################################

class HunkAbc(object):

    ###############################################

    def __init__(self, hunk_slice):

        self.slice = hunk_slice
        self.length = hunk_slice.stop - hunk_slice.start

    ###############################################

    def __bool__(self):

        return self.length == 0

    ###############################################

    def __len__(self):

        return self.length

#####################################################################################################

class HunksAbc(list):

    ###############################################

    def __init__(self, diff_buffer):

        self.diff_buffer = diff_buffer

    ###############################################

    def add_hunk(self, hunk_slice):

        hunk = self.new_hunk(hunk_slice)
        self.append(hunk)

        return hunk

#####################################################################################################

class DiffBufferAbc(object):

    ###############################################

    def __init__(self, buffer_obj, name, hunks_class):

        self.buffer = buffer_obj
        self.name = name
        self.hunks = hunks_class(self)

    ###############################################

    def __getitem__(self, hunk):

        return self.buffer[hunk.slice]

    ###############################################

    def add_hunk(self, hunk_slice):

        return self.hunks.add_hunk(hunk_slice)

#####################################################################################################

class LinearHunk(HunkAbc):

    ###############################################

    def __init__(self, text, hunk_slice):

        super(LinearHunk, self).__init__(hunk_slice)

        self._text = text

    ###############################################

    def text(self):

        return self._text[self.slice]

#####################################################################################################

class LinearHunks(HunksAbc):

    ###############################################

    def new_hunk(self, hunk_slice):

        return LinearHunk(self.diff_buffer, hunk_slice)

#####################################################################################################

class LinearDiffBuffer(DiffBufferAbc):

    ###############################################

    def __init__(self, text, name):

        super(LinearDiffBuffer, self).__init__(text, name, LinearHunks)

#####################################################################################################

class LinearTwoWayHunk(object):

    ###############################################

    def __init__(self, slice_a, slice_b):

        self.slice_a, self.slice_b = slice_a, slice_b

#####################################################################################################

class LinearTwoWayHunkEqual(LinearTwoWayHunk):

    repr_string = 'equal'

#####################################################################################################

class LinearTwoWayHunkDelete(LinearTwoWayHunk):

    repr_string = 'delete'

#####################################################################################################

class LinearTwoWayHunkInsert(LinearTwoWayHunk):

    repr_string = 'insert'

#####################################################################################################

class LinearTwoWayHunkReplace(LinearTwoWayHunk):

    repr_string = 'replace'
        
#####################################################################################################

class Hunk(HunkAbc):

    ###############################################

    def __init__(self, diff_buffer, hunk_slice):

        super(Hunk, self).__init__(hunk_slice)

        self.diff_buffer = diff_buffer

    ###############################################

    def __repr__(self):

        if not self:
            return "Hunk %s empty\n" % (self.diff_buffer.name)

        string_template = 'Hunk %s [%u, %u]\n'

        s = string_template % (self.diff_buffer.name,
                               self.slice.start, self.slice.stop -1)
        s += '  '.join(self.lines())

        return s

    ###############################################

    def __str__(self):

        return ''.join(self.lines())

    ###############################################

    def lines(self):

        for line in self.diff_buffer[self]:
            yield line

#####################################################################################################

class Hunks(HunksAbc):

    ###############################################

    def __str__(self):

        return '\n'.join([str(x) for x in self])

    ###############################################

    def new_hunk(self, hunk_slice):

        return Hunk(self.diff_buffer, hunk_slice)

#####################################################################################################

class FileDiffBuffer(DiffBufferAbc):

    ###############################################

    def __init__(self, file_handler, name):

        super(FileDiffBuffer, self).__init__(file_handler, name, Hunks)

#####################################################################################################

class TwoWayHunk(object):

    ###############################################

    def __init__(self, hunk_a, hunk_b):

        self.hunk_a, self.hunk_b = hunk_a, hunk_b

    ###############################################

    def __str__(self):

        s = '-'*50 + '\n' + self.repr_string + '\n'
        for hunk in self.hunk_a, self.hunk_b:
            s += repr(hunk)

        return s

#####################################################################################################

class TwoWayHunkEqual(TwoWayHunk):

    repr_string = 'equal'

#####################################################################################################

class TwoWayHunkDelete(TwoWayHunk):

    repr_string = 'delete'

#####################################################################################################

class TwoWayHunkInsert(TwoWayHunk):

    repr_string = 'insert'

#####################################################################################################

class TwoWayHunkReplace(TwoWayHunk):

    repr_string = 'replace'

    ###############################################

    def __init__(self, hunk_a, hunk_b):

        super(TwoWayHunkReplace, self).__init__(hunk_a, hunk_b)

        self.diff_buffer_a = LinearDiffBuffer(str(hunk_a), 'A')
        self.diff_buffer_b = LinearDiffBuffer(str(hunk_b), 'B')
        
        sequence_matcher_class = PatienceSequenceMatcher
        sequence_matcher = sequence_matcher_class(None,
                                                  self.diff_buffer_a.buffer,
                                                  self.diff_buffer_b.buffer)
        
        sequence_matcher_groups = sequence_matcher.get_opcodes()
        
        self.hunks = hunks = TwoWayHunks()
        for tag, lower_a, upper_a, lower_b, upper_b in sequence_matcher_groups:
            hunk_a = self.diff_buffer_a.add_hunk(slice(lower_a, upper_a))
            hunk_b = self.diff_buffer_b.add_hunk(slice(lower_b, upper_b))
            if tag == 'equal':
                hunk_diff = LinearTwoWayHunkEqual(hunk_a, hunk_b)
            elif tag == 'delete':
                hunk_diff = LinearTwoWayHunkDelete(hunk_a, hunk_b)
            elif tag == 'insert':
                hunk_diff = LinearTwoWayHunkInsert(hunk_a, hunk_b)
            elif tag == 'replace':
                hunk_diff = LinearTwoWayHunkReplace(hunk_a, hunk_b)
            hunks.append(hunk_diff)

    ###############################################

    def __str__(self):

        s = super(TwoWayHunkReplace, self).__str__()

        s += str(self.hunks)

        return s
        
#####################################################################################################

class TwoWayHunks(list):

    ###############################################

    def __str__(self):

        return '\n'.join([str(x) for x in self])

#####################################################################################################

class Diff2Way(object):

    ###############################################

    def __init__(self, diff_buffer_a, diff_buffer_b):

        self.diff_buffer_a = diff_buffer_a
        self.diff_buffer_b = diff_buffer_b

        sequence_matcher_class = PatienceSequenceMatcher
        sequence_matcher = sequence_matcher_class(None,
                                                  self.diff_buffer_a.buffer,
                                                  self.diff_buffer_b.buffer)

        number_of_lines_of_context = 3

        sequence_matcher_groups = sequence_matcher.get_grouped_opcodes(number_of_lines_of_context)

        self.hunks = hunks = TwoWayHunks()
        for group in sequence_matcher_groups:
            for tag, lower_a, upper_a, lower_b, upper_b in group:
                hunk_a = self.diff_buffer_a.add_hunk(slice(lower_a, upper_a))
                hunk_b = self.diff_buffer_b.add_hunk(slice(lower_b, upper_b))
                if tag == 'equal':
                    hunk_diff = TwoWayHunkEqual(hunk_a, hunk_b)
                elif tag == 'delete':
                    hunk_diff = TwoWayHunkDelete(hunk_a, hunk_b)
                elif tag == 'insert':
                    hunk_diff = TwoWayHunkInsert(hunk_a, hunk_b)
                elif tag == 'replace':
                    hunk_diff = TwoWayHunkReplace(hunk_a, hunk_b)
                hunks.append(hunk_diff)

#####################################################################################################
#
# End
#
#####################################################################################################
