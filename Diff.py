#####################################################################################################

from bzrlib.patiencediff import unified_diff_files, PatienceSequenceMatcher

#####################################################################################################

class Hunk(object):

    ###############################################

    def __init__(self, diff_file, hunk_slice):

        self.diff_file = diff_file
        self.slice = hunk_slice
        self.length = hunk_slice.stop - hunk_slice.start

    ###############################################

    def __bool__(self):

        return self.length == 0

    ###############################################

    def __len__(self):

        return self.length

    ###############################################

    def __repr__(self):

        if not self:
            return "Hunk %s empty\n" % (self.diff_file.name)

        string_template = 'Hunk %s [%u, %u]\n'

        s = string_template % (self.diff_file.name,
                               self.slice.start, self.slice.stop -1)
        s += '  '.join(self.lines())

        return s

    ###############################################

    def __str__(self):

        return ''.join(self.lines())

    ###############################################

    def lines(self):

        return self.diff_file[self]

#####################################################################################################

class Hunks(list):

    ###############################################

    def __str__(self):

        return '\n'.join([str(x) for x in self])

#####################################################################################################

class DiffFile(object):

    ###############################################

    def __init__(self, file_handler, name):

        self.file_handler = file_handler
        self.name = name
        self.hunks = Hunks()

    ###############################################

    def __getitem__(self, hunk):

        return self.file_handler[hunk.slice]

    ###############################################

    def add_hunk(self, hunk_slice):

        hunk = Hunk(self, hunk_slice)
        self.hunks.append(hunk)

        return hunk

#####################################################################################################

class Hunk2Way(object):

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

class Hunk2WayEqual(Hunk2Way):

    repr_string = 'Equal'

#####################################################################################################

class Hunk2WayDelete(Hunk2Way):

    repr_string = 'Delete'

#####################################################################################################

class Hunk2WayInsert(Hunk2Way):

    repr_string = 'Insert'

#####################################################################################################

class Hunk2WayReplace(Hunk2Way):

    repr_string = 'Replace'

    ###############################################

    def __init__(self, hunk_a, hunk_b):

        super(Hunk2WayReplace, self).__init__(hunk_a, hunk_b)

        sequence_matcher_class = PatienceSequenceMatcher

        sequence_matcher = sequence_matcher_class(None, str(hunk_a), str(hunk_b))

        self.hunks = list()
        for group in sequence_matcher.get_opcodes():
            for tag, lower_a, upper_a, lower_b, upper_b in group:
                hunk_a = diff_file_a.add_hunk(slice(lower_a, upper_a))
                hunk_b = diff_file_b.add_hunk(slice(lower_b, upper_b))
                if tag == 'equal':
                    hunk_diff = IntraHunkEqual(hunk_a, hunk_b)
                elif tag == 'delete':
                    hunk_diff = IntraHunkDelete(hunk_a, hunk_b)
                elif tag == 'insert':
                    hunk_diff = IntraHunkInsert(hunk_a, hunk_b)
                elif tag == 'replace':
                    hunk_diff = IntraHunkReplace(hunk_a, hunk_b)
                hunks.append(hunk_diff)

#####################################################################################################

class IntraHunk(object):

    ###############################################

    def __init__(self, slice_a, slice_b):

        self.slice_a, self.slice_b = slice_a, slice_b

#####################################################################################################

class IntraHunkEqual(IntraHunk):

    repr_string = 'Equal'

#####################################################################################################

class IntraHunkDelete(IntraHunk):

    repr_string = 'Delete'

#####################################################################################################

class IntraHunkInsert(IntraHunk):

    repr_string = 'Insert'

#####################################################################################################

class IntraHunkReplace(IntraHunk):

    repr_string = 'Replace'
        
#####################################################################################################

class Diff2Way(object):

    ###############################################

    def __init__(self, diff_file_a, diff_file_b):

        self.diff_file_a = diff_file_a
        self.diff_file_b = diff_file_b

        sequence_matcher_class = PatienceSequenceMatcher
        number_of_lines_of_context = 3

        # isjunk=None, a=file_a, b=file_b
        sequence_matcher = sequence_matcher_class(None,
                                                  diff_file_a.file_handler,
                                                  diff_file_b.file_handler)

        self.hunks = hunks = Hunks()
        for group in sequence_matcher.get_grouped_opcodes(number_of_lines_of_context):
            for tag, lower_a, upper_a, lower_b, upper_b in group:
                hunk_a = diff_file_a.add_hunk(slice(lower_a, upper_a))
                hunk_b = diff_file_b.add_hunk(slice(lower_b, upper_b))
                if tag == 'equal':
                    hunk_diff = Hunk2WayEqual(hunk_a, hunk_b)
                elif tag == 'delete':
                    hunk_diff = Hunk2WayDelete(hunk_a, hunk_b)
                elif tag == 'insert':
                    hunk_diff = Hunk2WayInsert(hunk_a, hunk_b)
                elif tag == 'replace':
                    hunk_diff = Hunk2WayReplace(hunk_a, hunk_b)
                hunks.append(hunk_diff)

#####################################################################################################
#
# End
#
#####################################################################################################
