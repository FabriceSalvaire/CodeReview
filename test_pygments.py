from pygments.lexers import get_lexer_for_filename
from pygments import lex

filename = 'test-bzr/file-2.py'

lexer = get_lexer_for_filename(filename, stripnl=False)
code = open(filename).read()

for token, text in lex(code, lexer):
    if text == '\n':
        print
    else:
        print (token, text)

 # End
