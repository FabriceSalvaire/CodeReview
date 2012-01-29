======
 Diff
======

 * document slice
  * flat index
  * line index

 * diff structure:
  * input is split into chunks
  * a chunk is defined by:
   * input A slice
   * input B slice
   * chunk type:
    * equal: content is same in A and B
    * insert: content is inserted into B
    * delete: content is deleted from A
    * replace: content from A is replaced in B
  
 * input is a byte flow:
  * thus Unicode multi-byte is not taken into account
  * it is not a problem for line segmentation since new line separator is part of ASCII
  * it appears for inline diff:
   * diff -> list of byte-slices

=======
 UTF-8
=======

* U-00000000 - U-0000007F  7-bit 0xxx xxxx
* U-00000080 - U-000007FF 11-bit 110x xxxx 10xx xxxx
* U-00000800 - U-0000FFFF 16-bit 1110 xxxx 10xx xxxx 10xx xxxx
* U-00010000 - U-0010FFFF 21-bit 1111 0xxx 10xx xxxx 10xx xxxx 10xx xxxx

* 0b10000000 = 0x80 = 128
* 0b11000000 = 0xC0 = 192
* 0b11100000 = 0xE0 = 224
* 0b11110000 = 0xF0 = 240

Byte Order Mark: U+FEFF

é = U+00E9 = 1110 1001 -> UTF-8 [11]00 0011 [10]10 1001 = 0xC3 0xA9

Python 3.2
>>> s = 'abcdé'.encode('utf_8') ; ['{0:08b}'.format(x) for x in s]
['01100001', '01100010', '01100011', '01100100', '11000011', '10101001']

>>> s = 'abcdé'.encode('utf_8') ; ['{0:x}'.format(x) for x in s]
['61', '62', '63', '64', 'c3', 'a9']

========
 UTF-32
========

UTF-32 uses 4 bytes to encode the characters.  Character index and string length are multiple of four.

Python 3.2
>>> s = 'abcé'.encode('utf_32-BE') ; ['{0:x}'.format(x) for x in s]
['0', '0', '0', '61',
 '0', '0', '0', '62',
 '0', '0', '0', '63',
 '0', '0', '0', 'e9']

>>> s = 'abcé'.encode('utf_32') ; ['{0:x}'.format(x) for x in s]
['ff', 'fe', '0', '0',
 '61',  '0', '0', '0',
 '62',  '0', '0', '0',
 '63',  '0', '0', '0',
 'e9',  '0', '0', '0']
Read right to left and BOM at beginning

Python 2.7
>>> s = u'abcé'.encode('utf_32-BE') ; [x for x in s]
['\x00', '\x00', '\x00', 'a',
 '\x00', '\x00', '\x00', 'b',
 '\x00', '\x00', '\x00', 'c',
 '\x00', '\x00', '\x00', '\xc3',
 '\x00', '\x00', '\x00', '\xa9']

===============
 Text Document
===============

------------------
 Flat / Line View
------------------

A text document is an ordered list of characters encoded in a particular encoding, e.g. ASCII,
ISO-Latin-1, UTF-8.  For unicode encoding like UTF-8, the byte length of the characters run from one
to four bytes, thus the position of the characters must be decoded as a linear byte flow.  A way to
delimit the characters in the document is to create an array structure with a character-byte-length
field and a start position field.

A text document is naturaly structured as an ordered list of lines.  Lines are delimited by a new
line separator, that is commonly based on the following ASCII control characters: Line Feed ``\n``
for UNIX OS flavours, Carriage Return ``\r`` for the legacy Mac OS, and the combination of both
``\r\n`` for Windows OS.  Thus a line separator has one or two bytes.

  Text Document = ( Character 1 , Character 2 , ... , Character N )
                = ( LINE 1 , Line Seperator 1 , LINE 2 , Line Seperator 2 , ... )
                = ( LINE 1 , Line Seperator 1 ) ->
		  ( LINE 2 , Line Seperator 2 ) ->
                  ...


, we cannot only use the position of the line
separator, we have to also track its nature: character code sequence and length.



-----------------
 Cursor Movement
-----------------

 * vertical displacement
  * previous/next line
  * if column index is out of the line:
   * goto end-of-line
   * keep the column index for later movements
  * previous/next n-line page-up/down
  * beginning/end of document  

 * horizontal displacement
  * beginning/end of line
  * previous/next character in the line
   * Unicode => multi-byte
 * previous/next word
  * define what is a word

--------------------
 Insertion/Deletion
--------------------

 * insert a new line
 * insert a character

 * delete a line
 * delete a character

--------
 Region
--------

 * start-marker to end-marker
 * flat index <=> line index + column/char index
  * index versus pointer

---------------------
 Rectangle Operation
---------------------

 * a rectangle is the region:
     for each line in line_region_slice:
       line_subset = line & column_region_slice
 * copy rectangle
 * insert/replace rectangle
 * delete rectangle

--------------------
 Document Structure
--------------------

 * line can be accessed from flat index using bisect algorithm
  * B-Tree
  * bisect data = l0 | l0+l1 | l0+l1+l3
 * line insertion/deletion => to update bisect data
  * to update bisect data:
    * find the insertion/deletion point: i
    * split left | right
    * bisect data -> left | right +/- l
    * use numpy vectorisation
 * highlighting/metadata => vertical and horizontal region
 * concept of text blocks/fragments
  * block: set of lines / vertical
  * fragments: in line / horizontal
  * tree of blocks / fragments

----------
 Painting
----------

 * use Layout structure versus Model structure
 * track the line heights
 * track the fragments widths
 * cursor position is computed from the height/width data

--------------------------
 Mathematica Like Display
--------------------------

 * Text block
  * Title
  * paragraph etc.
 * Code block
  * mono-space font
 * Result block
 * Plot/Image
  * control widget
 * Math display
  * selection

.. End
