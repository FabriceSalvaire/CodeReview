==========
 Comments
==========

.. This is a comment.

..
   This whole indented block
   is a comment.

   Still in the comment.

===============
 Inline markup
===============

*emphasis*
**strong emphasis**
``literal``

=============================
 Lists and Quote-like blocks
=============================

* This is a bulleted list.
* It has two items, the second
  item uses two lines.

1. This is a numbered list.
2. It has two items too.

#. This is a numbered list.
#. It has two items too.

Nested lists
============

* this is
* a list

  * with a nested list
  * and some subitems

* and here the parent list continues

Definition lists
================

term (up to a line of text)
   Definition of the term, which must be indented

   and can even consist of multiple paragraphs

next term
   Description.

Line blocks
===========

| These lines are
| broken exactly like in
| the source file.

=============
 Source Code
=============

This is a normal text paragraph. The next paragraph is a code sample::

   It is not processed in any way, except
   that the indentation is removed.

   It can span multiple lines.

This is a normal text paragraph again.

========
 Tables
========

+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | ...        | ...      |          |
+------------------------+------------+----------+----------+

=====  =====  =======
A      B      A and B
=====  =====  =======
False  False  False
True   False  False
False  True   False
True   True   True
=====  =====  =======

============
 Hyperlinks
============

`Link text <http://example.com/>`_

This is a paragraph that contains `a link`_.

.. _a link: http://example.com/

===========
 Footnotes
===========

Lorem ipsum [#f1]_ dolor sit amet ... [#f2]_

.. rubric:: Footnotes

.. [#f1] Text of the first footnote.
.. [#f2] Text of the second footnote.

===========
 Citations
===========

Lorem ipsum [Ref]_ dolor sit amet.

.. [Ref] Book or article reference, URL or whatever.

===============
 Substitutions
===============

This token |name| will be substituted.

.. |name| replace:: replacement *text*

.. |caution| image:: warning.png
             :alt: Warning!

============
 Directives
============

Admonitions
===========

* attention
* caution
* danger
* error
* hint
* important
* note
* tip
* warning
* admonition

.. danger::
   Beware killer rabbits!

.. note:: This is a note admonition.
   This is the second line of the first paragraph.

   - The note contains all indented body elements
     following.
   - It includes this bullet list.

.. admonition:: And, by the way...

   You can make up your own admonition too.

Image
=====

.. image:: picture.jpeg
   :height: 100px
   :width: 200 px
   :scale: 50 %
   :alt: alternate text
   :align: right

Figure
======

.. figure:: picture.png
   :scale: 50 %
   :alt: map to buried treasure

   This is the caption of the figure (a simple paragraph).

   The legend consists of all elements after the caption.  In this
   case, the legend consists of this paragraph and the following
   table:

   +-----------------------+-----------------------+
   | Symbol                | Meaning               |
   +=======================+=======================+
   | .. image:: tent.png   | Campground            |
   +-----------------------+-----------------------+
   | .. image:: waves.png  | Lake                  |
   +-----------------------+-----------------------+
   | .. image:: peak.png   | Mountain              |
   +-----------------------+-----------------------+

=============
Python Domain
=============

.. py:module:: name

.. py:currentmodule:: name

.. py:data:: name

.. py:exception:: name

.. py:function:: name(signature)

.. py:class:: name[(signature)]

.. py:method:: name(signature)

.. py:staticmethod:: name(signature)

.. py:classmethod:: name(signature)

.. py:decorator:: name

.. py:decorator:: name(signature)

.. py:function:: format_exception(etype, value, tb[, limit=None])

   Format the exception with a traceback.

   :param etype: exception type
   :param value: exception value
   :param tb: traceback object
   :param limit: maximum number of stack frames to show
   :type limit: integer or None
   :rtype: list of strings

Cross-referencing Python objects
================================

:py:mod:
    Reference a module; a dotted name may be used. This should also be used for package names.

:py:func:
    Reference a Python function; dotted names may be used.

:py:data:
    Reference a module-level variable.

:py:const:
    Reference a “defined” constant.

:py:class:
    Reference a class; a dotted name may be used.

:py:meth:
    Reference a method of an object.

:py:attr:
    Reference a data attribute of an object.

:py:exc:
    Reference an exception. A dotted name may be used.

:py:obj:
    Reference an object of unspecified type.

.. End
