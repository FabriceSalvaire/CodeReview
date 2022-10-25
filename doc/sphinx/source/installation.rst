.. include:: project-links.txt
.. include:: abbreviation.txt

.. _installation-page:

==============
 Installation
==============

CodeReview is written in Python and uses the GUI framework |PyQt5|_ and the Git library |pygit2|_.
Thus, CodeReview is operating system agnostic and should work on Linux, Windows and OSX.

To install CodeReview from `source code <https://github.com/FabriceSalvaire/CodeReview>`_, you need a working Python environment and a C compiler.
   
On Linux
--------

To summarise, you can easily install CodeReview on Linux with just :code:`pip install CodeReview` but read the followings.

First you need to verify that Python is installed on your distribution.

If you install CodeReview from source, you will also need the GCC C compiler.

You can create a `Python virtual environment <https://docs.python.org/3/library/venv.html>`_ to install CodeReview in its own container:

.. code-block:: sh

    # create the venv
    python3.10 -m venv $HOME/codereview
    # enter in the venv
    source $HOME/codereview/bin/activate

This is not mandatory, but it is a good practice if you don't know exactly what you are doing.
Especially, if you don't want to spoil your distribution.

Notice, you can later create a shell script to wrap the venv activation and the pyqgit command.

Then install CodeReview either from |Pypi|_ (official Python package repository) or from source:

.. code-block:: sh

    # wheel/binary from PyPI
    pip install CodeReview

    # from Git repository (require GCC C compiler)
    pip install git+https://github.com/FabriceSalvaire/CodeReview

If the `pip` command is not available, you must install the corresponding package of your distribution.

Finally, run CodeReview to verify that the installation was successful:

.. code-block:: sh

    pyqgit --help
    diff-viewer --help

    pyqgit git_repository_path
    diff-viewer a.txt b.txt

    cd git_repository_path
    pyqgit

Example of shell wrapper:

.. code-block:: sh

    #! /usr/bin/bash
    PY_ENV=${HOME}/codereview
    source ${PY_ENV}/bin/activate
    CodeReviewLogLevel='WARNING' ${PY_ENV}/bin/pyqgit $1 &

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
