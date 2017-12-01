.. include:: project-links.txt
.. include:: abbreviation.txt

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
