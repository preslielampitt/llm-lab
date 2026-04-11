import glob

def ls(folder=None):
    '''
    This function behaves just like the ls program in the shell.

    >>> ls()
    '__init__.py __pycache__ chat.py tools'
    
    >>> ls('tools')
    'tools/__pycache__ tools/calculate.py tools/ls.py '
    '''
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