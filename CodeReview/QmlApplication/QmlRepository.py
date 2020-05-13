###################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2019 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

__all__ = [
    'QmlBranch',
    'QmlCommit'
    'QmlCommitPool',
    'QmlNote',
    'QmlReference',
    'QmlRepository',
]

####################################################################################################

# import re
import datetime
import logging
import os

fromtimestamp = datetime.datetime.fromtimestamp

from PyQt5.QtQml import QQmlListProperty
from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
)

from CodeReview.Repository.Git import pygit, RepositoryNotFound, GitRepository

####################################################################################################

_module_logger = logging.getLogger(__name__)


####################################################################################################

class QmlRepositoryChild(QObject):

    ##############################################

    def __init__(self, repository):
        # repository: QmlRepository
        super().__init__()
        self._repository = repository

####################################################################################################

class QmlBranch(QmlRepositoryChild):

    # https://www.pygit2.org/branches.html#the-branch-type

    ##############################################

    def __init__(self, repository, branch: pygit.Branch):
        super().__init__(repository)
        self._branch = branch

    ##############################################

    @Property(str, constant=True)
    def name(self):
        return self._branch.name

    ##############################################

    @Property(bool)
    def is_checked_out(self):
        """ True if branch is checked out by any repo connected to the current one, False otherwise."""
        return self._branch.is_checked_out

    @Property(bool)
    def is_head(self):
        """True if HEAD points at the branch, False otherwise."""
        return self._branch.is_head

    @Property(str)
    def remote_name(self):
        """The name of the remote set to be the upstream of this branch."""
        return self._branch.remote_name

    @Property(str)
    def upstream_name(self):
        """The name of the reference set to be the upstream of this one"""
        return self._branch.upstream_name

    # upstream
    # The branch’s upstream branch or None if this branch does not have an upstream set. Set to None
    # to unset the upstream configuration.

    ##############################################

    @Slot()
    def delete(self):
        """Delete this branch. It will no longer be valid!"""
        self._branch.delete() # DANGER

    @Slot(str, bool)
    def rename(self, name, force=False):
        """Move/rename an existing local branch reference. The new branch name will be checked for validity. Returns the new branch."""
        self._branch.rename(name, force)

####################################################################################################

class QmlReference(QmlRepositoryChild):

    # https://www.pygit2.org/references.html#the-reference-type

    ##############################################

    def __init__(self, repository, reference: pygit.Reference):
        super().__init__(repository)
        self._reference = reference

    ##############################################

    @Property(str, constant=True)
    def name(self):
        """The full name of the reference."""
        return self._reference.name

    @Property(str, constant=True)
    def shorthand(self):
        """The shorthand “human-readable” name of the reference."""
        return self._reference.name

    @Slot(bool)
    def is_oid(self, name):
        """"""
        self._reference.type == pygit.GIT_REF_OID

    @Slot(bool)
    def is_symbolic(self, name):
        """"""
        self._reference.type == pygit.GIT_REF_SYMBOLIC

    ##############################################

    @Slot()
    def delete(self, name):
        """Delete this reference. It will no longer be valid!"""
        self._reference.delete() # DANGER

    @Slot(str)
    def rename(self, name):
        """Rename the reference."""
        self._reference.rename(name)

    # .set_target(target[, message])
    # Set the target of this reference.

    # @Slot(result=QmlReference)
    def resolve(self):
        """Resolve a symbolic reference and return a direct reference."""
        return self.__class__(self._repository, self._reference.resolve()) # Fixme: keep ref. ?

    # @Slot(result=QmlCommit)
    def commit(self):
        """"""
        commit = self._reference.peel()
        return self._repository.commit_pool.from_commit(commit)

QmlReference.resolve = Slot(result=QmlReference)(QmlReference.resolve)

####################################################################################################

class QmlCommit(QmlRepositoryChild):

    # https://www.pygit2.org/objects.html#commits

    ##############################################

    def __init__(self, repository, commit: pygit.Commit):
        super().__init__(repository)
        self._commit = commit

    ##############################################

    @Property(str, constant=True)
    def message(self):
        return self._commit.message

    ##############################################

    @Property(str, constant=True)
    def sha(self):
        return str(self._commit.hex)

    ##############################################

    @Property(str, constant=True)
    def time(self):
        return fromtimestamp(self._commit.commit_time).strftime('%Y-%m-%d %H:%M:%S'),

    ##############################################

    @Property(str, constant=True)
    def committer(self):
        committer = self._commit.committer
        return '{} <{}>'.format(committer.name, committer.email),

    ##############################################

    @Property(str, constant=True)
    def author(self):
        author = self._commit.author
        return '{} <{}>'.format(author.name, author.email),

QmlReference.commit = Slot(result=QmlCommit)(QmlReference.commit)

####################################################################################################

class QmlCommitPool(QmlRepositoryChild):

    ##############################################

    def __init__(self, repository):
        super().__init__(repository)
        self._commits = {}

    ##############################################

    def from_commit(self, commit):
        sha = str(commit.hex)
        if sha in self._commits:
            return self._commits[sha]
        else:
            qml_commit = QmlCommit(self._repository, commit)
            self._commits[sha] = qml_commit
            return qml_commit

    ##############################################

    @Slot(str, result=QmlCommit)
    def get(self, sha):
        return self._commits.get(sha, None)

####################################################################################################

class QmlNote(QmlRepositoryChild):

    # https://www.pygit2.org/references.html#notes
    # GIT-NOTES(1)

    ##############################################

    def __init__(self, repository, note):
        super().__init__(repository)
        self._note = {}

    ##############################################

    @property
    def message(self):
        return self._message

####################################################################################################

class QmlRepository(QObject):

    _logger = _module_logger.getChild('QmlRepository')

    ##############################################

    def __init__(self, path=None):

        super().__init__()

        self._logger.info('Init Repository')

        if path is None:
            path = os.getcwd()
        try:
            self._repository = GitRepository(path)
        except RepositoryNotFound:
            raise NameError("Any Git repository was found in path {}".format(path))
            self._repository = None
            return

        self._branches = []
        self._update_branches()

        self._commit_pool = QmlCommitPool(self)
        self._commits = []
        self._update_commits()

        self._tags = []
        self._update_tags()

    ##############################################

    def __bool__(self):
        return self._repository is not None

    ##############################################

    @Property(QmlCommitPool, constant=True)
    def commit_pool(self):
        return self._commit_pool

    ##############################################

    def _update_branches(self):
        self._branches = [QmlBranch(self, branch) for branch in self._repository.branches]
        self.branches_changed.emit()

    branches_changed = Signal()

    @Property(QQmlListProperty, notify=branches_changed)
    def branches(self):
        return QQmlListProperty(QmlBranch, self, self._branches)

    ##############################################

    def _update_commits(self):
        self._commits = [self._commit_pool.from_commit(commit) for commit in self._repository.commits_for_head]
        self.commits_changed.emit()

    commits_changed = Signal()

    @Property(QQmlListProperty, notify=commits_changed)
    def commits(self):
        return QQmlListProperty(QmlCommit, self, self._commits)

    ##############################################

    def _update_tags(self):
        self._tags = [QmlReference(self, reference) for reference in self._repository.tags]
        self.tags_changed.emit()

    tags_changed = Signal()

    @Property(QQmlListProperty, notify=tags_changed)
    def tags(self):
        return QQmlListProperty(QmlReference, self, self._tags)
