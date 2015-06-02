.. -*- Mode: rst -*-

.. _installation-page:

.. include:: project-links.txt
.. include:: abbreviation.txt

==============
 Installation
==============

The installation of CodeReview by itself is quite simple. However it will be easier to get the
dependencies on a Linux desktop.

Dependencies
------------

CodeReview requires the following dependencies:

 * |Python|_ 3
 * |PyQt5|_ 5
 * libgit2 see `link <http://www.pygit2.org/install.html#quick-install>`_ to install

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
