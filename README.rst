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

.. |Pypi Version| image:: https://img.shields.io/pypi/v/CodeReview.svg
   :target: https://pypi.python.org/pypi/CodeReview
   :alt: CodeReview last version

.. |Pypi License| image:: https://img.shields.io/pypi/l/CodeReview.svg
   :target: https://pypi.python.org/pypi/CodeReview
   :alt: CodeReview license

.. |Pypi Python Version| image:: https://img.shields.io/pypi/pyversions/CodeReview.svg
   :target: https://pypi.python.org/pypi/CodeReview
   :alt: CodeReview python version

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

============
 CodeReview
============

|Pypi License|
|Pypi Python Version|

|Pypi Version|

..
  * Quick Link to `Production Branch <https://github.com/FabriceSalvaire/CodeReview/tree/master>`_
  * Quick Link to `Devel Branch <https://github.com/FabriceSalvaire/CodeReview/tree/devel>`_

CodeReview Home Page is located at |CodeReviewUrl|

Authored by `Fabrice Salvaire <http://fabrice-salvaire.pagesperso-orange.fr>`_


.. image:: https://raw.github.com/FabriceSalvaire/CodeReview/master/doc/sphinx/source/images/code-review-log.png
.. image:: https://raw.github.com/FabriceSalvaire/CodeReview/master/doc/sphinx/source/images/code-review-diff.png

.. -*- Mode: rst -*-

==============
 Introduction
==============

The aim of CodeReview is to provide tools for code review tasks on local Git repositories.  As
opposite to software like `Gerrit <https://www.gerritcodereview.com>`_ for example, CodeReview is
not designed to perform code review at a team level, but to check the stage before a commit and show
the difference between two versions.  In particular, CodeReview fills the gap with IDEs that don't
provide efficiently these features.

How to use CodeReview ?
-----------------------

CodeReview provides two applications *pyqgit* and *diff-viewer*.

.. -*- Mode: rst -*-

==========
 Features
==========

The main features of CodeReview are:

 * display and browse the log and paches of a Git repository
 * diff side by side using Patience algorithm
 * watch for file system changes

Diff viewer features:

 * stage/unstage file
 * number of context lines
 * font size
 * line number mode
 * align mode
 * complete mode
 * highlight mode


.. _installation-page:

==============
 Installation
==============

On Fedora
---------

RPM packages are available for the Fedora distribution on https://copr.fedorainfracloud.org/coprs/fabricesalvaire/code-review

Run these commands to enable the copr repository and install the last release:

.. code-block:: sh

  dnf copr enable fabricesalvaire/code-review
  dnf install CodeReview

From PyPi Repository
--------------------

CodeReview is available on |Pypi|_ repository: |CodeReview@pypi|

Run this command to install the last release:

.. code-block:: sh

  pip install CodeReview

Notice, it requires Python 3 and a C compiler.

From source
------------

CodeReview source code is hosted at |CodeReview@github|

Clone the Git repository using this command:

.. code-block:: sh

  git clone git@github.com:FabriceSalvaire/CodeReview.git

Then build and install CodeReview using these commands:

.. code-block:: sh

  python setup.py build
  python setup.py install

Dependencies
------------

CodeReview requires the following dependencies:

* |Python|_ 3 (at least v3.4)
* |pygit2|_ and libgit2 see `link <http://www.pygit2.org/install.html#quick-install>`_  for installation instruction
* Pygments
* |PyQt5|_
* PyYAML
* A C compiler to compile a module

=============
 How to help
=============

* test it on Windows and OSX
* fix bugs: look at issues
* sometime pyqgit is slow: profile code to find issues

