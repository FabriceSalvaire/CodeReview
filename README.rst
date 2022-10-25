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
.. _pygit2: http://www.pygit2.org

.. |PyQt5| replace:: PyQt5
.. _PyQt5: https://www.riverbankcomputing.com/software/pyqt

..
  http://www.pygit2.org/install.html
  http://www.riverbankcomputing.com/software/pyqt/download5

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

.. image:: https://raw.github.com/FabriceSalvaire/CodeReview/master/doc/sphinx/source/images/code-review-log.png
.. image:: https://raw.github.com/FabriceSalvaire/CodeReview/master/doc/sphinx/source/images/code-review-diff.png

Credits
-------

Authors: `Fabrice Salvaire <http://fabrice-salvaire.fr>`_

News
----

.. -*- Mode: rst -*-


.. no title here

V1.1 2022-25-10
---------------

- Updated install process
   
V1 2017-12-20
-------------

- Redesigned INotify support

.. -*- Mode: rst -*-

==============
 Introduction
==============

The goal of CodeReview is to provide tools for code review tasks on local Git repositories.  Unlike
software like `Gerrit <https://www.gerritcodereview.com>`_, CodeReview is not designed to do
team-level code review, but to check the stage before a commit and show the difference between two
versions.  In particular, CodeReview fills the gap with IDEs that don't efficiently provide these
features.

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

CodeReview is written in Python and uses the GUI framework |PyQt5|_ and the Git library |pygit2|_.
Thus, CodeReview is operating system agnostic and should work on Linux, Windows and OSX.

To install CodeReview from `source code <https://github.com/FabriceSalvaire/CodeReview>`_, you need a working Python environment and a C compiler.
   
On Linux
--------

To summarise, you can easily install CodeReview on Linux with just :code:`pip install CodeReview`

First you need to verify that Python is installed on your distribution.

If you install CodeReview from source, you will also need the GCC compiler.

You can create a `Python virtual environment <https://docs.python.org/3/library/venv.html>`_ to install CodeReview in its own container:

.. code-block:: sh

    # create the venv
    python3.10 -m venv $HOME/codereview
    # enter in the venv
    source $HOME/codereview/bin/activate

This is not mandatory, but a good practice if you don't know exactly what you are doing.

Then install CodeReview either from |Pypi|_ or from source:

.. code-block:: sh

    # wheel/binary from PyPI
    pip install CodeReview

    # from Git repository (require GCC C compiler)
    pip install git+https://github.com/FabriceSalvaire/CodeReview

If the `pip` command is not available, you must install the corresponding package of your distribution.

Finally, run CodeReview to verify that the installation was successful:

.. code-block:: sh

    cd a-git-repository
    pyqgit

You can also clone the repository and install it using theses commands:

.. code-block:: sh

     git clone git@github.com:FabriceSalvaire/CodeReview.git
     python setup.py build
     python setup.py install

On Windows
----------

**Actually there is no installer available, but it is welcome.**

You must follow the same procedure than for Linux.  However it is a bit more difficult to achieve.

A suggestion is to install the `Anaconda Python Distribution <https://www.anaconda.com/products/distribution>`_ and got a working compiler.

On OSX
------

**An up to date installation procedure is welcome.**

..  On Fedora
..  ---------
..  
..  RPM packages are available for the Fedora distribution on https://copr.fedorainfracloud.org/coprs/fabricesalvaire/code-review
..  
..  Run these commands to enable the copr repository and install the last release:
..  
..  .. code-block:: sh
..  
..    dnf copr enable fabricesalvaire/code-review
..    dnf install CodeReview

Dependencies
------------

CodeReview requires the dependencies listed in `requirements.txt <https://github.com/FabriceSalvaire/CodeReview/blob/master/requirements.txt>`_

=============
 How to help
=============

* test it on Windows and OSX
* fix bugs: look at issues
* sometime pyqgit is slow: profile code to find issues

