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

The official CodeReview Home Page is located at |CodeReviewUrl|

The latest documentation build from the git repository is available at readthedocs.org |CodeReview@readthedocs-badge|

Written by `Fabrice Salvaire <http://fabrice-salvaire.pagesperso-orange.fr>`_.

|Build Status|

-----

.. -*- Mode: rst -*-


==============
 Introduction
==============

.. End

.. -*- Mode: rst -*-

.. _installation-page:


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

.. End
