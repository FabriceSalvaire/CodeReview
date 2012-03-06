#####################################################################################################

import io
import unittest

from pygments.lexers import get_lexer_for_filename

#####################################################################################################

from SyntaxHighlighter import HighlightedText

#####################################################################################################

class TestSyntaxHighlighter(unittest.TestCase):

    ###############################################

    def test(self):

        code = u'''def distance(self, x, y):
    return x**2 + y**2
'''
        
        text_buffer = io.StringIO(code)

        lexer = get_lexer_for_filename('foo.py', stripnl=False)
        highlighted_text = HighlightedText(lexer, text_buffer.read())

        text_buffer.seek(0)
        code_lines = text_buffer.readlines()

        self.assertEqual(len(highlighted_text), len(code_lines))

        rule = '-'*50

        print rule
        print 'Text:'
        print rule
        for highlighted_line in highlighted_text:
            print unicode(highlighted_line).rstrip()
        print rule

        for i in xrange(len(code_lines)):
            code_line = code_lines[i]
            highlighted_line = highlighted_text[i]
            self.assertEqual(code_line, unicode(highlighted_line))
            for j in xrange(len(code_line)):
                for k in xrange(j, len(code_line)):
                    line_slice = slice(j, k)
                    highlighted_line_slice = highlighted_line.get_line_slice(line_slice)
                    self.assertEqual(code_line[line_slice], unicode(highlighted_line_slice))

#####################################################################################################

if __name__ == '__main__':

    unittest.main()

#####################################################################################################
#
# End
#
#####################################################################################################
