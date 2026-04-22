import glob
from cmc_cs040_preslie.tools.path_utils import is_path_safe


def ls(folder=None):
    '''
    This function behaves just like the ls program in the shell.

    >>> result = ls()
    >>> result.split()[0] == 'AGENTS.md' or result.split()[0] == 'README.md'
    True

    >>> ls('cmc_cs040_preslie/tools').split()[0]
    'cmc_cs040_preslie/tools/__pycache__'

    >>> ls('../')
    'Invalid path'
    '''
    if not is_path_safe(folder):
        return 'Invalid path'

    if folder is not None:
        result = ''
        # folder + '/*' ==> tools /*
        # glob is nondeterministic; no guarantees about order of glob results
        # need to convert nondeterministic to deterministic
        # llm we did that by adjusting the temperature
        # best way to make a list deterministic is to sort it
        for path in sorted(glob.glob(folder + '/*')):
            result += path + ' '
        return result
    else:
        result = ''
        for path in sorted(glob.glob('*')):
            result += path + ' '
        return result.strip()


ls_tool_schema = {
    "type": "function",
    "function": {
        "name": "ls",
        "description": "List files in a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "folder": {
                    "type": "string",
                    "description": "The folder to list. If omitted, list the current directory."
                }
            },
            "required": [],
        },
    },
}
