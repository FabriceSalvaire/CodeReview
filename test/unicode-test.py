# -*- coding: utf-8 -*-

#####################################################################################################

text_ascii = u"Je suis allez a Paris"
text_with_accent = "Je suis allez à Paris"
text_unicode = u"Je suis allez à Paris"

print text_ascii, len(text_ascii) # len = 21
print text_with_accent, len(text_with_accent) # len = 21 +1
print text_unicode, len(text_unicode) # len = 21

text = u'|'.join(u'(%u)%s' % (i, x) for i, x in enumerate(text_unicode))
print text

char = text_unicode[14]
char_encoded = char.encode('UTF-8')
print char, len(char), repr(char_encoded), len(char_encoded)

s = u'abcé'.encode('utf_32-BE')
print len(s)
print [x for x in s]

#####################################################################################################
#
# End
#
#####################################################################################################

