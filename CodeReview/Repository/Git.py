####################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If
# not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import logging
import os

import pygit2 as git

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class RepositoryNotFound(Exception):
    pass

####################################################################################################

class GitRepository(object):

    _logger = _module_logger.getChild('GitRepository')

    ##############################################

    def __init__(self, path):

        path = os.path.realpath(path)

        try:
            repository_path = git.discover_repository(path)
            self._repository = git.Repository(repository_path)
            workdir = self._repository.workdir
            if os.path.isdir(path) and not path.endswith(os.sep):
                path += os.sep
            self._path_filter = path.replace(workdir, '')
            self._logger.info('\nPath %s\nWork Dir: %s\nPath Filter: %s',
                              path, workdir, self._path_filter)
        except KeyError:
            raise RepositoryNotFound

    ##############################################

    @property
    def workdir(self):
        return self._repository.workdir

    ##############################################

    def commits(self):

        head = self._repository.head
        head_commit = self._repository[head.target]
        commits = [commit
                   for commit in self._repository.walk(head_commit.id, git.GIT_SORT_TIME)]
        
        return commits

    ##############################################

    def diff(self, a=None, b=None, cached=False, path_filter=None):

        if path_filter is None:
            path_filter = self._path_filter
        
        patches = []
        
        # GIT_DIFF_PATIENCE
        diff = self._repository.diff(a=a, b=b, cached=cached)
        diff.find_similar()
        # flags, rename_threshold, copy_threshold, rename_from_rewrite_threshold, break_rewrite_threshold, rename_limit
        for patch in diff:
            if path_filter and not patch.old_file_path.startswith(path_filter):
                # self._logger.info('Skip ' + patch.old_file_path)
                continue
            patches.append(patch)
        
        return Diff(diff, patches)

    ##############################################

    def file_content(self, oid):
        try:
            return self._repository[oid].data.decode('utf-8')
        except KeyError:
            return None

####################################################################################################

class Diff(object):

    ##############################################

    def __init__(self, diff, patches):

        self.diff = diff
        self._patches = patches

    ##############################################

    def __len__(self):
        return len(self._patches)

    ##############################################

    def __iter__(self):
        return iter(self._patches)

    ##############################################

    def __getitem__(self, i):
        return self._patches[i]

####################################################################################################
#
# End
#
####################################################################################################
