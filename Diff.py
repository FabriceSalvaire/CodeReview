#####################################################################################################

from bzrlib.patiencediff import unified_diff_files, PatienceSequenceMatcher

#####################################################################################################

class Hunk(object):

    ###############################################

    def __init__(self, diff_file, lower, upper):

        self.lower, self.upper = lower, upper
        self.length = upper - lower +1

    ###############################################

    def __len__(self):

        return self.length

    ###############################################

    def slice(self):

        return slice(self.lower, self.upper)

#####################################################################################################

class Hunks(list):
    pass

#####################################################################################################

class DiffFile(object):

    ###############################################

    def __init__(self, file_handler):

        self.file_handler = file_handler

    ###############################################

    def __getitem__(self, hunk):

        return self.file_handler[hunk.slice()]

#####################################################################################################

class Hunk2Way(object):

    ###############################################

    def __init__(self, hunk_a, hunk_b):

        self.hunk_a, self.hunk_b = hunk_a, hunk_b

#####################################################################################################

class Hunk2WayEqual(Hunk2Way):
    pass

#####################################################################################################

class Hunk2WayDelete(Hunk2Way):
    pass

#####################################################################################################

class Hunk2WayInsert(Hunk2Way):
    pass
#####################################################################################################

class Hunk2WayReplace(Hunk2Way):
    pass

#####################################################################################################

class Diff2Way(object):

    ###############################################

    def __init__(self, file_a, file_b):

        sequence_matcher_class = PatienceSequenceMatcher
        number_of_lines_of_context = 3

        # isjunk=None, a=file_a, b=file_b
        sequence_matcher = sequence_matcher_class(None, file_a, file_b)

        diff_file_a = DiffFile(file_a)
        diff_file_b = DiffFile(file_b)
        hunk_diffs = Hunks()

        for group in sequence_matcher.get_grouped_opcodes(number_of_lines_of_context):
            for tag, lower_a, upper_a, lower_b, upper_b in group:
                hunk_a = Hunk(diff_file_a, lower_a, upper_a)
                hunk_b = Hunk(diff_file_b, lower_b, upper_b)
                if tag == 'equal':
                    hunk_diff = Hunk2WayEqual(hunk_a, hunk_b)
                elif tag == 'delete':
                    hunk_diff = Hunk2WayDelete(hunk_a, hunk_b)
                elif tag == 'insert':
                    hunk_diff = Hunk2WayInsert(hunk_a, hunk_b)
                elif tag == 'replace':
                    hunk_diff = Hunk2WayReplace(hunk_a, hunk_b)
                hunk_diffs.append(hunk_diff)

#####################################################################################################
#
# End
#
#####################################################################################################
