#! /usr/bin/env python

####################################################################################################
#
# Diff Viewer
# Copyright (C) 2012 Salvaire Fabrice
#
####################################################################################################

####################################################################################################

import os
from distutils.core import setup, Extension

####################################################################################################

# Utility function to read the README file.
# Used for the long_description.
def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

####################################################################################################

setup(name='Diff Viewer',
      version='1.0',
      author='Fabrice Salvaire',
      author_email='fabrice.salvaire@orange.fr',
      description='a diff viewer',
      license='GPLv3',
      keywords=('diff',),
      url='http://fabrice-salvaire.pagesperso-orange.fr/software/index.html',
      packages=['DiffViewer'],
      long_description=read('README'),
      # cf. http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          # 'Topic :: ',
          # 'Intended Audience :: ',
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          ],
      requires=[
        'pyqt (>= 4.6)',
        ],
      ext_modules=[Extension('PatienceDiff._patiencediff_c', ['PatienceDiff/_patiencediff_c.c'])],
      )

####################################################################################################
#
# End
#
####################################################################################################
