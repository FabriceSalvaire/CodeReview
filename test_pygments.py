#####################################################################################################

from pygments.lexers import get_lexer_for_filename

from SyntaxHighlighter import HighlightedText

#####################################################################################################

filename = 'test-bzr/file-2.py'

lexer = get_lexer_for_filename(filename, stripnl=False)
code = open(filename).read()

highlighted_text = HighlightedText(lexer, code)

print 'Text:'
for highlighted_line in highlighted_text:
    print str(highlighted_line).rstrip()

print
print 'line 0:'
line = highlighted_text[0]
print line
print 'line 0 [0]:'
line_slice = slice(0,1)
print '|%s|' % str(line)[line_slice]
print '|%s|' % line.get_line_slice(line_slice)

print
print 'line 3:'
line = highlighted_text[3]
print line
print 'line 3 [2:10]:'
line_slice = slice(2,10)
print '|%s|' % str(line)[line_slice]
print '|%s|' % line.get_line_slice(line_slice)

print
print 'line 4:'
line = highlighted_text[4]
print line
print 'line 4 [1:3]:'
line_slice = slice(1,3)
print '|%s|' % str(line)[line_slice]
print '|%s|' % line.get_line_slice(line_slice)

#####################################################################################################
#
# End
#
#####################################################################################################
