####################################################################################################
#
# -
# Copyright (C) 2012
#
####################################################################################################

####################################################################################################

import os
import sys

import pygit2 as git

####################################################################################################
#
# A repository has a head and possibly uncommited changes.
#
# A commit represents a state of the file hierarchy and their contents.  The file hierarchy (and the
# file attributes) is stored in trees and the file contents in blobs.
#
# A commit has ancestors.  A commit having more than one ancestor is a merge of branches.  A commit
# having more than one successor is the root of a branch.
#
# Git only records the ancestors of each commit.  Thus we can only perform a top-down walk in the
# commit graph using this information.
#
# Top-down walk algorithm:
#
#   top_down_walk(commit id, parent):
#     retrieve commit from commit id
#     for each ancestor id do:
#       top_down_walk(ancestor id, commit)
#
# A commit has the following additional information:
#  - message
#  - an author and committer signature (person that written/committed the code)
#    a signature is made of a name, an email and a date
#
####################################################################################################

####################################################################################################

class Repository(object):

    ##############################################

    def __init__(self, repository_path):

        self._repository = git.Repository(os.path.join(repository_path, '.git'))

        self._keys = {}
        self.head = self._head_commit()

    ##############################################

    def __contains__(self, key):

        return key in self._keys

    ##############################################

    def __getitem__(self, key):

        return self._keys[key]

    ##############################################

    def __setitem__(self, key, value):

        if key not in self._keys:
            self._keys[key] = value
        else:
            raise IndexError

    ##############################################

    def _head_commit(self):

        head = self._repository.lookup_reference('HEAD')
        head = head.resolve()
        raw_head_commit = self._repository[head.oid]

        return Commit.create_from_raw_commit(self, raw_head_commit)

####################################################################################################

class Commit(object):

    ##############################################

    @staticmethod
    def create_from_raw_commit(repository, raw_commit):

        return Commit(repository,
                      raw_commit.hex,
                      raw_commit.author,
                      raw_commit.committer,
                      raw_commit.message,
                      raw_commit.parents
                      )

    ##############################################

    def __init__(self,
                 repository,
                 hex_,
                 author,
                 committer,
                 message,
                 raw_ancestors,
                 ancestors=[],
                 successors=[],
                 ):

        self.repository = repository
        self.hex = hex_
        self.author = author
        self.committer = committer
        self.message = message
        self.raw_ancestors = raw_ancestors
        self.ancestors = list(ancestors) # /!\ copy default
        self.successors = list(successors)
        self._ancestors_visited = False

        self.repository[self.hex] = self

    ##############################################

    @staticmethod
    def _join_commit_keys(commits):

        return ', '.join([str(x.hex) for x in commits])

    ##############################################

    def __str__(self):

        line = '='*50
        message_template = line + """
Commit:
  hex: %s
  author: %s
  committer: %s
  ancestors: %s
  raw: %s
  message: %s
""" + line

        return message_template % (self.hex,
                                   self.author.name,
                                   self.committer.name,
                                   self._join_commit_keys(self.ancestors),
                                   self._join_commit_keys(self.raw_ancestors),
                                   self.message,
                                   )

    ##############################################

    def top_down_builder(self, max_level=sys.maxsize, level=0):

        print("top_down_builder", level, self.message)
        for raw_commit in self.raw_ancestors:
            seen = raw_commit.hex in self.repository
            if seen:
                commit = self.repository[raw_commit.hex]
                print("Commit %s already seen" % (commit.hex))
            else:
                commit = self.create_from_raw_commit(self.repository, raw_commit)
                print('Create:', commit.hex)
                # print str(commit)
            commit.successors.append(self)
            self.ancestors.append(commit)
        print("<<Current Commit Node>>:\n", str(self))
        level += 1
        if level <= max_level:
            for commit in self.ancestors:
                if not commit._ancestors_visited:
                    commit.top_down_builder(max_level, level)
        self._ancestors_visited = True

    ##############################################

    def top_down_visitor(self, max_level=sys.maxsize, level=0):

        print(str(self))
        level += 1
        if level <= max_level:
            for commit in reversed(self.ancestors):
                if commit.successors[0] is self:
                    commit.top_down_visitor(max_level, level)

####################################################################################################
#
# End
#
####################################################################################################
