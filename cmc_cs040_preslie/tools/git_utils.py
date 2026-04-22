import os


def get_repo():
    '''
    Return the git repository rooted at the current working directory.

    >>> import os
    >>> import tempfile
    >>> from git import Repo
    >>> old = os.getcwd()
    >>> with tempfile.TemporaryDirectory() as d:
    ...     try:
    ...         os.chdir(d)
    ...         _ = Repo.init(d)
    ...         repo = get_repo()
    ...         repo.bare
    ...     finally:
    ...         os.chdir(old)
    False
    '''
    from git import Repo

    return Repo(os.getcwd())


def commit_paths(paths, commit_message):
    '''
    Stage the given paths and create a git commit if there are staged changes.

    >>> import os
    >>> import tempfile
    >>> from git import Repo
    >>> old = os.getcwd()
    >>> with tempfile.TemporaryDirectory() as d:
    ...     os.chdir(d)
    ...     repo = Repo.init(d)
    ...     with open('a.txt', 'w', encoding='utf-8') as f:
    ...         _ = f.write('hello')
    ...     commit_paths(['a.txt'], '[docchat] add a')
    ...     repo.head.commit.message
    ...     os.chdir(old)
    '[docchat] add a'
    '''
    repo = get_repo()
    repo.git.add(*paths)
    if repo.git.diff('--cached', '--name-only'):
        repo.index.commit(commit_message)


def commit_removed_paths(paths, commit_message):
    '''
    Stage removals for the given paths and create a git commit if there are staged changes.

    >>> import os
    >>> import tempfile
    >>> from git import Repo
    >>> old = os.getcwd()
    >>> with tempfile.TemporaryDirectory() as d:
    ...     os.chdir(d)
    ...     repo = Repo.init(d)
    ...     with open('a.txt', 'w', encoding='utf-8') as f:
    ...         _ = f.write('hello')
    ...     commit_paths(['a.txt'], '[docchat] add a')
    ...     commit_removed_paths(['a.txt'], '[docchat] rm a')
    ...     os.path.exists('a.txt')
    ...     os.chdir(old)
    False
    '''
    repo = get_repo()
    repo.index.remove(paths, working_tree=True)
    if repo.git.diff('--cached', '--name-only'):
        repo.index.commit(commit_message)
