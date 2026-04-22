import glob
import os
import re
from cmc_cs040_preslie.tools.path_utils import is_path_safe


def grep(pattern, path):
    '''
    Search for lines matching a regular expression in files matched by a glob.

    Returns an empty string when no lines match.

    >>> grep('hello', 'cmc_cs040_preslie/chat.py')
    ''

    Returns the matching lines when the pattern appears in one or more files.

    >>> grep('def', 'cmc_cs040_preslie/tools/*.py') != ''
    True

    Returns an empty string for binary files and directories.

    >>> with open('bad.bin', 'wb') as f:
    ...     _ = f.write(b'\\xff\\xfe\\x00\\x00')
    >>> grep('x', 'bad.bin')
    ''
    >>> os.remove('bad.bin')

    >>> grep('x', 'cmc_cs040_preslie/tools')
    ''

    Returns an error for invalid paths and invalid regular expressions.

    >>> grep('abc', '../secret.txt')
    'Invalid path'
    >>> grep('root', '/etc/passwd')
    'Invalid path'
    >>> grep('[', 'cmc_cs040_preslie/tools/*.py')
    'Invalid regex'
    '''
    if not is_path_safe(path):
        return 'Invalid path'

    try:
        result = []

        for filename in sorted(glob.glob(path)):
            if not os.path.isfile(filename):
                continue
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    for line in f:
                        if re.search(pattern, line):
                            result.append(line.rstrip('\n'))
            except UnicodeDecodeError:
                continue

        return '\n'.join(result)
    except re.error:
        return 'Invalid regex'


grep_tool_schema = {
    "type": "function",
    "function": {
        "name": "grep",
        "description": "Search for lines matching a regular expression in one or more files.",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "The regular expression to search for.",
                },
                "path": {
                    "type": "string",
                    "description": "A relative file path or glob pattern to search.",
                },
            },
            "required": ["pattern", "path"],
        },
    },
}
