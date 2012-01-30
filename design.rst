==========
 Encoding
==========

-------
 UTF-8
-------

* U-00000000 - U-0000007F  7-bit 0xxx xxxx
* U-00000080 - U-000007FF 11-bit 110x xxxx 10xx xxxx
* U-00000800 - U-0000FFFF 16-bit 1110 xxxx 10xx xxxx 10xx xxxx
* U-00010000 - U-0010FFFF 21-bit 1111 0xxx 10xx xxxx 10xx xxxx 10xx xxxx

* 0b10000000 = 0x80 = 128
* 0b11000000 = 0xC0 = 192
* 0b11100000 = 0xE0 = 224
* 0b11110000 = 0xF0 = 240

Byte Order Mark (BOM): U+FEFF = 1111 1110 1111 1111 for Big Endian Architecture

é = U+00E9 = 1110 1001 -> UTF-8 [11]00 0011 [10]10 1001 = 0xC3 0xA9

Python 3.2
>>> s = 'abcdé'.encode('utf_8') ; ['{0:08b}'.format(x) for x in s]
['01100001', '01100010', '01100011', '01100100', '11000011', '10101001']

>>> s = 'abcdé'.encode('utf_8') ; ['{0:x}'.format(x) for x in s]
['61', '62', '63', '64', 'c3', 'a9']

--------
 UTF-32
--------

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

Python 2.7 with -*- coding: utf-8 -*-
>>> s = u'abcé'.encode('utf_32-BE') ; [x for x in s]
['\x00', '\x00', '\x00', 'a',
 '\x00', '\x00', '\x00', 'b',
 '\x00', '\x00', '\x00', 'c',
 '\x00', '\x00', '\x00', '\xe9']

===============
 Text Document
===============

------------------
 Flat / Line View
------------------

A text document is an ordered list of characters encoded in a particular encoding, e.g. ASCII,
ISO-Latin-1, UTF-8.

For the UTF-8 encoding, the byte count of the characters is variable and run from one to four bytes.
This property implies string length and character location are not a multiple of a particular byte
count.  Thus we cannot index and slice easily an UTF-8 string.  However the first bytes (byte
pattern) provides a self-synchronisation feature, to find the start of a character from an arbitrary
location, a program needs to search at most three bytes backward.

A text document is naturaly structured as an ordered list of lines.  Lines are delimited by a new
line separator, that is commonly based on the following ASCII control characters: Line Feed ``\n``
for UNIX OS flavours, Carriage Return ``\r`` for the legacy Mac OS, and the combination of both
``\r\n`` for Windows OS.  Thus a line separator has usually one or two bytes.

  Text Document = ( Character 1 , Character 2 , ... , Character N )
                = ( LINE 1 , Line Seperator 1 , LINE 2 , Line Seperator 2 , ... )
                = ( LINE 1 , Line Seperator 1 ) ->
                  ( LINE 2 , Line Seperator 2 ) ->
                  ...

In order to slice a text document in lines, we can use the locations of the first and last character
of each line and the length of the line separator of each line.  The last character of a line is
thus the last character of the line separator.  If a file ends with a line separator then it has a
virtual empty line at the end.

---------------------------------------
 Meta Data and Text Document Structure
---------------------------------------

Meta Data have to be associated to the text content, like syntax highlighting for example.  Meta
Data implies to split the text document in group of lines (vertical structure) and group of
characters (horizontal structure).  These vertical and horizontal superstructures could be
implemented as trees with a meta-data associated for each node or leaf, where a node stores an
ordered list of nodes or leafs and a leaf store a text fragment.  The meta-data are inherited from
the parent nodes to the leaf node.

The text document structure could be implemented using line and intra-line slices, but slices are
not well suited for dynamic content update.  List or tree structures are better suited for this
purpose.

Vertical structures provide a line iterator and horizontal structure a character/word iterator.

Implementation Notes
~~~~~~~~~~~~~~~~~~~~

* line can be accessed from flat index using bisect algorithm
 * B-Tree
 * bisect data = l0 | l0+l1 | l0+l1+l3
* line insertion/deletion => to update bisect data
 * to update bisect data:
   * find the insertion/deletion point: i
   * split left | right
   * bisect data -> left | right +/- l
   * use numpy vectorisation

====================
 Text Document Diff
====================

The comparison of two (or three) text documents works on static content.  Line based comparison
doesn't need to take care of the encoding scheme, but line comparison does.  Imagine an "e" replaced
by "é" in an UTF-8 encoded document, the first is encoded using one byte and the second using two
bytes.  To compare lines encoded using a variable byte count scheme, a solution is to convert them
to UTF-32 so as to have a fixed byte-count encoding scheme, else the slices have to be corrected to
match the character start location.

The two-way diff algorithm take as input two byte flows and return a list of two-way chunks.  A
chunk is a line slice in a text document.  And a two-way chunk is defined as a line slice in the
frist document and a corresponding one in the second document with a type that define if the content
is identical on both side or was replaced, inserted in the second one or removed from the first one.

Similarly this two-way diff algorithm could be adapted to compare line and to return intra-line
slice.

=======================
 Text Document Edition
=======================

-----------------
 Cursor Movement
-----------------

 * vertical displacement
  * previous/next line
  * if column index is out of the line:
   * goto end-of-line
   * keep the column index for later successive movements
  * previous/next n-line (page-up/down)
  * beginning/end of document  

 * horizontal displacement
  * beginning/end of line
  * previous/next character in the line
   * require an array structure to store the line for efficiency
 * previous/next word
  * require to define what is a word

--------------------
 Insertion/Deletion
--------------------

insert:
* a new line
* a character

delete:
* a new line
* a character
* a region
* a paragraph

--------
 Region
--------

A region is defined as a slice in the text document: from a start-marker to an end-marker location.
There is two equivalent ways to reprensent location:
 * flat index
 * line index + column index

.. index versus pointer

------------------
 Rectangle Region
------------------

A rectangle region is a 2-dimension region.  Like a region, a rectangle rectangle is defined from a
start-marker to an end-marker location, except there is in addition an intra-line slice constrain.
A rectangle region is defined as the union of the intra-line slices in the line slice, where the
line slice and the intra-line slice is defined from the start-marker and end-marker like this:

* line slice = [line of the start-marker,
                line of the end-marker]
* intra-line slice = [location of the start-marker in its respective line,
                      location of the end-marker in its respective line]

Operations on rectangular region:
* copy
* delete
* insert/replace

-----------
 Kill Ring
-----------

----------------
 Search/Replace
----------------

=========================
 Text Document Rendering
=========================

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
