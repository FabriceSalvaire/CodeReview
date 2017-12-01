.. include:: abbreviation.txt

==========
 Colophon
==========

CodeReview is written in Python 3 and the GUI is based on the Qt5 framework.  The libgit2 and
|pygit2|_ provides the Python API to deal with Git repositories.  I tried to achieve a clever design
and to write a clean code.

I am not a fan of GUI softwares that aim to deal with Git with only a mouse and one finger.  Thus
CodeReview is not intended to compete with a "power" IDE like Eclipse, Idea, PyCharm, Kate ...  But
just to provide features which are not available in `Emacs <https://www.gnu.org/software/emacs>`_
and the `Magit Mode <https://magit.vc/>`_ (my editor) or Github like a diff side-by-side on local
changes.

I started to write some pieces of code of CodeReview at the end of 2011, as a port of the Bzr Qt
plugin `QBzr <http://wiki.bazaar.canonical.com/QBzr>`_ for Git when Bzr started to seriously fall
down.  I am an addict of code review and I cannot work without it.  QBzr features two nice tools for
this task: qlog and qdiff.  It was the main reason why I used Bzr until 2015 and didn't switched to
Git before this date.  But I succeed to release an alternative.
