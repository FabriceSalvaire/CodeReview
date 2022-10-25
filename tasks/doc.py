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

from pathlib import Path

from invoke import task

####################################################################################################

from .clean import clean_flycheck as clean_flycheck

####################################################################################################

CODEREVIEW_SOURCE_PATH = Path(__file__).resolve().parents[1]

SPHINX_PATH = CODEREVIEW_SOURCE_PATH.joinpath('doc', 'sphinx')
BUILD_PATH = SPHINX_PATH.joinpath('build')
RST_SOURCE_PATH = SPHINX_PATH.joinpath('source')
RST_API_PATH = RST_SOURCE_PATH.joinpath('api')
RST_EXAMPLES_PATH = RST_SOURCE_PATH.joinpath('examples')

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

@task
def run_sphinx(ctx):
    print()
    print('Run Sphinx')
    working_path = SPHINX_PATH
    # subprocess.run(('make-html'), cwd=working_path)
    # --clean
    with ctx.cd(str(working_path)):
        ctx.run('make-html')

@task(run_sphinx)
def publish(ctx):
    with ctx.cd(str(CODEREVIEW_SOURCE_PATH.joinpath('gh-pages'))):
        ctx.run('update-gh-pages')

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
