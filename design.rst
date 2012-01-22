--------------------
 New Line Separator
--------------------

 * \n
 * \r
 * \r\n

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
 * line insertion/deletion => to update bisect data
 * highlighting/metadata => vertical and horizontal region

.. End
