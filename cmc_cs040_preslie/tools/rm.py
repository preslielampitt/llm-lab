import glob
import os

from cmc_cs040_preslie.tools.git_utils import commit_removed_paths
from cmc_cs040_preslie.tools.path_utils import is_path_safe


def rm(path):
    '''
    Remove one or more safe relative files matched by a glob and commit the deletion.

    >>> rm('/etc/passwd')
    'Invalid path'

    >>> import os
    >>> import tempfile
    >>> from git import Repo
    >>> from cmc_cs040_preslie.tools.git_utils import commit_paths
    >>> old = os.getcwd()
    >>> with tempfile.TemporaryDirectory() as d:
    ...     try:
    ...         os.chdir(d)
    ...         _ = Repo.init(d)
    ...         with open('a.txt', 'w', encoding='utf-8') as f:
    ...             _ = f.write('hello')
    ...         commit_paths(['a.txt'], '[docchat] add a')
    ...         rm('a.txt')
    ...         os.path.exists('a.txt')
    ...     finally:
    ...         os.chdir(old)
    'Removed a.txt'
    False
    >>> import os
    >>> import tempfile
    >>> from git import Repo
    >>> old = os.getcwd()
    >>> with tempfile.TemporaryDirectory() as d:
    ...     try:
    ...         os.chdir(d)
    ...         _ = Repo.init(d)
    ...         rm('missing.txt')
    ...     finally:
    ...         os.chdir(old)
    'No files removed'
    '''
    if not is_path_safe(path):
        return 'Invalid path'

    matched_paths = sorted(glob.glob(path))
    removed_paths = []

    for matched_path in matched_paths:
        if os.path.isfile(matched_path):
            os.remove(matched_path)
            removed_paths.append(matched_path)

    if not removed_paths:
        return 'No files removed'

    commit_removed_paths(removed_paths, f'[docchat] rm {path}')
    return 'Removed ' + ' '.join(removed_paths)


rm_tool_schema = {
    "type": "function",
    "function": {
        "name": "rm",
        "description": "Remove safe relative files matched by a glob and commit the deletion.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The safe relative path or glob to remove."
                }
            },
            "required": ["path"],
        },
    },
}
