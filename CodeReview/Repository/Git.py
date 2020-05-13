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

__all__ = ['GitRepository', 'RepositoryNotFound', 'Diff', 'pygit']

####################################################################################################

from pathlib import Path
import logging
import re

import pygit2 as pygit

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class RepositoryNotFound(Exception):
    pass

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

    ##############################################

    def new_paths(self):
        return [patch.delta.new_file.path for patch in self._patches]

####################################################################################################

class GitRepository:

    """Class to implement a wrapper on top pygit2.
    """

    _logger = _module_logger.getChild('GitRepository')

    INDEX_PATH = Path('.git').joinpath('index')
    REFS_PATH = Path('.git').joinpath('refs', 'heads')

    ##############################################

    def __init__(self, path):

        path = Path(path).absolute().resolve()

        try:
            repository_path = pygit.discover_repository(str(path))
            self._repository = pygit.Repository(repository_path)
            self._workdir = Path(self._repository.workdir)
            self._path_filter = str(path.relative_to(self._workdir))
            if self._path_filter == '.':
                self._path_filter = ''
            template = '\nPath {}\nWork Dir: {}\nPath Filter: {}'
            self._logger.info(template.format(path, self._workdir, self._path_filter))
        except KeyError:
            raise RepositoryNotFound

    ##############################################

    @property
    def workdir(self):
        return self._workdir

    @property
    def index(self):
        return self._repository.index

    @property
    def head(self):
        return self._repository.revparse_single('HEAD')

    @property
    def repository_status(self):
        return self._repository.status()

    @property
    def branch_name(self) -> str:
        # head = self._repository.lookup_reference('HEAD').resolve()
        head = self._repository.head
        return head.name

    ##############################################

    def join_repository_path(self, path):
        return self._workdir.joinpath(path)

    ##############################################

    def references(self, regexp=None) -> pygit.Reference:
        # https://www.pygit2.org/references.html
        if regexp is not None:
            regexp_ = re.compile(str(regexp))
            return [
                self._repository.references[name]
                for name in self._repository.references if regexp_.match(name)
            ]
        else:
            return [self._repository.references[name] for name in self._repository.references]

    ##############################################

    @property
    def tags(self) -> pygit.Reference:
        return self.references('^refs/tags')

    ##############################################

    @property
    def branches(self) -> pygit.Branch:
        # https://www.pygit2.org/branches.html
        return [self._repository.branches[name] for name in self._repository.branches]

    ##############################################

    def commits(self, oid, topological=True, by_time=False): # -> iter on pygit.Commit

        # https://www.pygit2.org/commit_log.html
        # https://www.pygit2.org/commit_log.html?highlight=walk#pygit2.Repository.walk

        # GIT_SORT_TOPOLOGICAL. Sort the repository contents in topological order (parents before children);
        # this sorting mode can be combined with time sorting.
        if topological and not by_time:
            sorting = pygit.GIT_SORT_TOPOLOGICAL
        if topological and by_time:
            sorting = pygit.GIT_SORT_TOPOLOGICAL | pygit.GIT_SORT_TIME
        else:
            sorting = pygit.GIT_SORT_NONE

        commits = self._repository.walk(oid, sorting) # -> pygit.Walker

        return commits

    ##############################################

    @property
    def commits_for_head(self): # -> iter on pygit.Commit

        # https://www.pygit2.org/references.html#the-head
        # Current head reference of the repository
        # head = repo.references['HEAD'].resolve()
        head = self._repository.head # -> pygit.Reference
        head_commit = self._repository[head.target] # -> pygit.Commit
        oid = head_commit.id

        return self.commits(oid)

    ##############################################

    def diff(self, a=None, b=None, cached=False, path_filter=None) -> Diff:

        if isinstance(a, pygit.Commit):
            a_str = a.hex
        else:
            a_str = str(a)
        if isinstance(b, pygit.Commit):
            b_str = b.hex
        else:
            b_str = str(b)
        self._logger.info('{} {} {} {}'.format(a_str, b_str, cached, path_filter))

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

    def file_content(self, oid) -> str:
        try:
            return self._repository[oid].data.decode('utf-8')
        except KeyError:
            return None

    ##############################################

    _STATUS_TEXT = {
        pygit.GIT_STATUS_CONFLICTED: 'conflicted',
        pygit.GIT_STATUS_CURRENT: 'current',
        pygit.GIT_STATUS_IGNORED: 'ignored',
        pygit.GIT_STATUS_INDEX_DELETED: 'index deleted',
        pygit.GIT_STATUS_INDEX_MODIFIED: 'index modified',
        pygit.GIT_STATUS_INDEX_NEW: 'index new',
        pygit.GIT_STATUS_WT_DELETED: 'working tree deleted',
        pygit.GIT_STATUS_WT_MODIFIED: 'working tree modified',
        pygit.GIT_STATUS_WT_NEW: 'working tree new',
    }

    def status(self, path):

        try:
            status = self.repository_status[path]
            status_text = ' | '.join([self._STATUS_TEXT[bit]
                                      for bit in self._STATUS_TEXT
                                      if status & bit])
            self._logger.info("File {} has status {} / {}".format(path, status, status_text))
            return status
        except KeyError:
            return 0 # Fixxme:

    ##############################################

    def is_staged(self, path) -> bool:

        # index = self._repository.index
        # head_tree = self._repository.revparse_single('HEAD').tree
        # try:
        #     head_oid = head_tree[path].oid
        #     index_oid = index[path].oid
        #     return index_oid != head_oid
        # except KeyError:
        #     return False # untracked file
        return self.status(path) == pygit.GIT_STATUS_INDEX_MODIFIED

    ##############################################

    def is_modified(self, path) -> bool:
        return self.status(path) == pygit.GIT_STATUS_WT_MODIFIED

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
            index_entry = pygit.IndexEntry(path, tree_entry.oid, tree_entry.filemode)
            self._logger.info("Reset index to HEAD for {}".format(path))
            index.add(index_entry)
        index.write()
