####################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2019 Fabrice Salvaire
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

from invoke import task
 # import sys

####################################################################################################

from .clean import clean_flycheck as clean_flycheck

####################################################################################################

@task
def clean_api(ctx):
    ctx.run('rm -rf doc/sphinx/source/api')

####################################################################################################

@task(clean_flycheck, clean_api)
def make_api(ctx):
    print('\nGenerate RST API files')
    ctx.run('pyterate-rst-api {0.Package}'.format(ctx))
    print('\nRun Sphinx')
    with ctx.cd('doc/sphinx/'):
        ctx.run('./make-html') #--clean

####################################################################################################

@task()
def make_readme(ctx):
    from setup_data import long_description
    with open('README.rst', 'w') as fh:
        fh.write(long_description)
    # import subprocess
    # subprocess.call(('rst2html', 'README.rst', 'README.html'))
    ctx.run('rst2html README.rst README.html')

####################################################################################################

@task
def update_authors(ctx):
    # Keep authors in the order of appearance and use awk to filter out dupes
    ctx.run("git log --format='- %aN <%aE>' --reverse | awk '!x[$0]++' > AUTHORS")
