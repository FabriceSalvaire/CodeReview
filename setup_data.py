####################################################################################################
#
# CodeReview - A Python/Qt Git GUI
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import glob
import os
import sys

from distutils.core import Extension
from distutils.sysconfig import get_python_lib
site_packages_path = get_python_lib()

####################################################################################################

def merge_include(src_lines, doc_path, included_rst_files=None):
    if included_rst_files is None:
        included_rst_files = {}
    text = ''
    for line in src_lines:
        if line.startswith('.. include::'):
            include_file_name = line.split('::')[-1].strip()
            if include_file_name not in included_rst_files:
                # print "include", include_file_name
                with open(os.path.join(doc_path, include_file_name)) as f:
                    included_rst_files[include_file_name] = True
                    text += merge_include(f.readlines(), doc_path, included_rst_files)
        else:
            text += line
    return text

####################################################################################################

# Utility function to read the README file.
# Used for the long_description.
def read(file_name):

    source_path = os.path.dirname(os.path.realpath(__file__))
    if os.path.basename(source_path) == 'tools':
        source_path = os.path.dirname(source_path)
    elif 'build/bdist' in source_path:
        source_path = source_path[:source_path.find('build/bdist')]
    absolut_file_name = os.path.join(source_path, file_name)
    doc_path = os.path.join(source_path, 'doc', 'sphinx', 'source')

    # Read and merge includes
    if os.path.exists(absolut_file_name):
        with open(absolut_file_name) as f:
            lines = f.readlines()
        text = merge_include(lines, doc_path)
        return text
    else:
        sys.stderr.write("WARNING: README {} not found\n".format(absolut_file_name))
        return ''

####################################################################################################

long_description = read('README.txt')

####################################################################################################

CodeReview_path = os.path.join(site_packages_path, 'CodeReview')

setup_dict = dict(
    name='CodeReview',
    version='0.3.0',
    author='Fabrice Salvaire',
    author_email='fabrice.salvaire@orange.fr',
    description='CodeReview is a Python 3 / Qt5 GUI to perform code review on files and Git repositories.',
    license="GPLv3",
    keywords="code, review, diff, viewer, git",
    url='https://github.com/FabriceSalvaire/CodeReview',
    scripts=['bin/pyqgit', 'bin/diff-viewer'],
    packages=['CodeReview', # Fixme:
              'CodeReview.Application',
              'CodeReview.Config',
              'CodeReview.Diff',
              'CodeReview.GUI',
              'CodeReview.GUI.Base',
              'CodeReview.GUI.DiffViewer',
              'CodeReview.GUI.Forms',
              'CodeReview.GUI.LogBrowser',
              'CodeReview.GUI.Widgets',
              'CodeReview.GUI.ui',
              'CodeReview.Logging',
              'CodeReview.Math',
              'CodeReview.PatienceDiff',
              'CodeReview.Repository',
              'CodeReview.Tools',
          ],
    ext_modules=[Extension('CodeReview.PatienceDiff._patiencediff_c',
                           ['CodeReview/PatienceDiff/_patiencediff_c.c'])],
    # package_dir = {'CodeReview': 'CodeReview'},
    data_files=[
        (os.path.join(CodeReview_path, 'Config'), [os.path.join('CodeReview', 'Config', 'logging.yml')]),
        ('share/CodeReview/icons', glob.glob('share/icons/*.png')),
        ('share/CodeReview/icons/32x32', glob.glob('share/icons/32x32/*.png')),
        ('share/CodeReview/icons/48x48', glob.glob('share/icons/48x48/*.png')),
        ('share/CodeReview/icons/svg', glob.glob('share/icons/svg/*.svg')),
    ],
    long_description=long_description,
    # cf. http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Topic :: Software Development :: Version Control",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        ],
    requires=[
        'Pygments',
        'PyYAML',
        'pygit2',
        # 'PyQt5',
    ],
    )

####################################################################################################
#
# End
#
####################################################################################################
