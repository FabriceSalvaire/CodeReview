.. -*- Mode: rst -*-

.. -*- Mode: rst -*-

..
   |CodeReviewUrl|
   |CodeReviewHomePage|_
   |CodeReviewDoc|_
   |CodeReview@github|_
   |CodeReview@readthedocs|_
   |CodeReview@readthedocs-badge|
   |CodeReview@pypi|_

.. |ohloh| image:: https://www.openhub.net/accounts/230426/widgets/account_tiny.gif
   :target: https://www.openhub.net/accounts/fabricesalvaire
   :alt: Fabrice Salvaire's Ohloh profile
   :height: 15px
   :width:  80px

.. |CodeReviewUrl| replace:: http://fabricesalvaire.github.io/CodeReview

.. |CodeReviewHomePage| replace:: CodeReview Home Page
.. _CodeReviewHomePage: http://fabricesalvaire.github.io/CodeReview

.. |CodeReviewDoc| replace:: CodeReview Documentation
.. _CodeReviewDoc: http://CodeReview.readthedocs.org/en/latest

.. |CodeReview@readthedocs-badge| image:: https://readthedocs.org/projects/CodeReview/badge/?version=latest
   :target: http://CodeReview.readthedocs.org/en/latest

.. |CodeReview@github| replace:: https://github.com/FabriceSalvaire/CodeReview
.. .. _CodeReview@github: https://github.com/FabriceSalvaire/CodeReview

.. |CodeReview@readthedocs| replace:: http://CodeReview.readthedocs.org
.. .. _CodeReview@readthedocs: http://CodeReview.readthedocs.org

.. |CodeReview@pypi| replace:: https://pypi.python.org/pypi/CodeReview
.. .. _CodeReview@pypi: https://pypi.python.org/pypi/CodeReview

.. |Build Status| image:: https://travis-ci.org/FabriceSalvaire/CodeReview.svg?branch=master
   :target: https://travis-ci.org/FabriceSalvaire/CodeReview
   :alt: CodeReview build status @travis-ci.org

.. End
.. -*- Mode: rst -*-

.. |Python| replace:: Python
.. _Python: http://python.org

.. |PyPI| replace:: PyPI
.. _PyPI: https://pypi.python.org/pypi

.. |pip| replace:: pip
.. _pip: https://python-packaging-user-guide.readthedocs.org/en/latest/projects.html#pip

.. |Sphinx| replace:: Sphinx
.. _Sphinx: http://sphinx-doc.org

.. |pygit2| replace:: pygit2
.. _pygit2: http://www.pygit2.org/install.html

.. |PyQt5| replace:: PyQt5
.. _PyQt5: http://www.riverbankcomputing.com/software/pyqt/download5

.. End

============
 CodeReview
============

The official CodeReview home page is located at |CodeReviewUrl|

The latest documentation built from the git repository is available at readthedocs.org |CodeReview@readthedocs-badge|

Written by `Fabrice Salvaire <http://fabrice-salvaire.pagesperso-orange.fr>`_.

|Build Status|

.. image:: https://raw.github.com/FabriceSalvaire/CodeReview/master/doc/sphinx/source/images/code-review-log.png
.. image:: https://raw.github.com/FabriceSalvaire/CodeReview/master/doc/sphinx/source/images/code-review-diff.png

-----

.. -*- Mode: rst -*-


==============
 Introduction
==============

I started to write some pieces of code of CodeReview at the end of 2011, as a port of the Bzr Qt
plugin `QBzr <http://wiki.bazaar.canonical.com/QBzr>`_ for Git when Bzr started to seriously fall
down.  I am an addict of code review and I cannot work without it.  QBzr features two nice tools,
qlog and qdiff for this task.  It was the main reason why I am still using Bzr in 2015.  But now I
succeed to release an alternative.

The aim of CodeReview is to provide tools for code review tasks, like to show the difference between
two versions.  However I am not a fan of any GUI that aims to deal with Git with only a mouse and
one finger.  Thus CodeReview is not intended to compete with a "power" IDE like eclipse, idea,
pycharm, kate ...  But just to provide features not available in Emacs (my editor) or github like a
diff side-by-side on local changes.

CodeReview is written in Python 3 and the GUI is based on the Qt5 framework.  The libgit2 and
|pygit2|_ provides a Python API to deal with Git repositories.  I tried to achieve a clever design
and to write a clean code.

.. -*- Mode: rst -*-

==========
 Features
==========

The main features of CodeReview are:

 * display and browse the log and paches of a Git repository
 * diff side by side using Patience algorithm

Diff viewer features:

 * number of context lines
 * font size
 * line number mode
 * align mode
 * complete mode
 * highlight mode

.. end
.. -*- Mode: rst -*-

===============================
 Ideas for Additional Features
===============================

Actually CodeReview has a limited number of features.  The followings list gives some ideas to extend its
features:

 * Add Mercurial support. (Git and Mercurial are actually the most cool VCS)

 * Add a graphical representation of the branches.  I don't understand the crappy code of qlog and I
   don't know any algorithm on this topic (graphviz, qgit ?).  To summarize I don't what and how to do.

 * Implement the detection of code translocations.  Sometimes we move code within a file or a
   project.  Such changes are related as deletion and addition in the code, which don't help to
   review code.  We can do something clever by computing a distance between all the added and
   deleted chuncks.  The distance could be computed using a Levenshtein, Damerau–Levenshtein,
   Needleman–Wunsch or Smith–Waterman algorithm (DNA alignment algorithms).

 * Implement code analyser/validator as language plugins.  The idea is to annotate change as
   cosmetic or dangerous modifications.  For example a deleted or added space is a cosmetic change
   in C, but it can be a regression in Python where the indentation is part of the grammar.

 * Implement blame wich is another important feature.

 * Implement comments and maybe as a client-server architecture.

 * look https://docs.python.org/3.4/library/difflib.html

.. end

.. End

.. -*- Mode: rst -*-

.. _installation-page:


==============
 Installation
==============

CodeReview requires some dependencies wich are easier to install on a Linux distribution.

Dependencies
------------

CodeReview requires the following dependencies:

 * |Python|_ v3.4
 * |PyQt5|_ v5.4
 * libgit2 see `link <http://www.pygit2.org/install.html#quick-install>`_  for installation instruction

Theses packages are available via |pip|_:

 * |pygit2|_
 * Pygments
 * PyYAML

For development, you will need in addition:

 * |Sphinx|_

Installation from PyPi Repository
---------------------------------

CodeReview is made available on the |Pypi|_ repository at |CodeReview@pypi|

Run this command to install the last release:

.. code-block:: sh

  pip install CodeReview

Installation from Source
------------------------

The CodeReview source code is hosted at |CodeReview@github|

To clone the Git repository, run this command in a terminal:

.. code-block:: sh

  git clone git@github.com:FabriceSalvaire/CodeReview.git

Then to build and install CodeReview run these commands:

.. code-block:: sh

  python setup.py build
  python setup.py install

.. End

.. End
