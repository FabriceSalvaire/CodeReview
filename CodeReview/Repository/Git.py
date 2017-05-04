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

class GitRepository:

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

    @property
    def index(self):
        return self._repository.index

    @property
    def head(self):
        return self._repository.revparse_single('HEAD')

    @property
    def repository_status(self):
        return self._repository.status()

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
            delta = patch.delta
            if path_filter and not delta.old_file.path.startswith(path_filter):
                # self._logger.info('Skip ' + delta.old_file.path)
                continue
            patches.append(patch)

        return Diff(diff, patches)

    ##############################################

    def file_content(self, oid):
        try:
            return self._repository[oid].data.decode('utf-8')
        except KeyError:
            return None

    ##############################################

    __STATUS_TEXT__ = {
        git.GIT_STATUS_CONFLICTED: 'conflicted',
        git.GIT_STATUS_CURRENT: 'current',
        git.GIT_STATUS_IGNORED: 'ignored',
        git.GIT_STATUS_INDEX_DELETED: 'index deleted',
        git.GIT_STATUS_INDEX_MODIFIED: 'index modified',
        git.GIT_STATUS_INDEX_NEW: 'index new',
        git.GIT_STATUS_WT_DELETED: 'working tree deleted',
        git.GIT_STATUS_WT_MODIFIED: 'working tree modified',
        git.GIT_STATUS_WT_NEW: 'working tree new',
    }

    def status(self, path):

        try:
            status = self.repository_status[path]
            status_text = ' | '.join([self.__STATUS_TEXT__[bit]
                                      for bit in self.__STATUS_TEXT__
                                      if status & bit])
            self._logger.info("File {} has status {} / {}".format(path, status, status_text))
            return status
        except KeyError:
            return 0 # Fixxme:

    ##############################################

    def is_staged(self, path):

        # index = self._repository.index
        # head_tree = self._repository.revparse_single('HEAD').tree
        # try:
        #     head_oid = head_tree[path].oid
        #     index_oid = index[path].oid
        #     return index_oid != head_oid
        # except KeyError:
        #     return False # untracked file
        return self.status(path) == git.GIT_STATUS_INDEX_MODIFIED

    ##############################################

    def is_modified(self, path):

        return self.status(path) == git.GIT_STATUS_WT_MODIFIED

    ##############################################

    def stage(self, path):

        index = self.index
        index.add(path)
        index.write()

    ##############################################

    def unstage(self, path):

        self._logger.info("Unstage {}".format(path))
        index = self.index
        index.remove(path)
        head_tree = self.head.tree
        if path in head_tree:
            # Restore index to HEAD
            tree_entry = head_tree[path]
            index_entry = git.IndexEntry(path, tree_entry.oid, tree_entry.filemode)
            self._logger.info("Reset index to HEAD for {}".format(path))
            index.add(index_entry)
        index.write()

####################################################################################################

class Diff:

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
