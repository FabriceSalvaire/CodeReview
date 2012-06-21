import pygit2 as git
repository_path = 'git-repo/repo1/.git'
repository = git.Repository(repository_path)

# head = repository.lookup_reference('HEAD')
# head = head.resolve()
# head_commit = repository[head.oid]
# 
# head1 = repository.lookup_reference('MASTER~')
# head1 = head.resolve()
# head1_commit = repository[head.oid]

translate_diff = {
    git.GIT_DELTA_UNMODIFIED:' GIT_DELTA_UNMODIFIED',
    git.GIT_DELTA_ADDED:' GIT_DELTA_ADDED',
    git.GIT_DELTA_DELETED:' GIT_DELTA_DELETED',
    git.GIT_DELTA_MODIFIED:' GIT_DELTA_MODIFIED',
    git.GIT_DELTA_RENAMED:' GIT_DELTA_RENAMED',
    git.GIT_DELTA_COPIED:' GIT_DELTA_COPIED',
    git.GIT_DELTA_IGNORED:' GIT_DELTA_IGNORED',
    git.GIT_DELTA_UNTRACKED:' GIT_DELTA_UNTRACKED',
    }

commit_a = repository.head
commit_b = repository.head.parents[0]
diff = commit_b.tree.diff(commit_a.tree)
for file_diff in diff.changes['files']:
    print file_diff[0:2], translate_diff[file_diff[2]]

####################################################################################################
#
# End
#
####################################################################################################
