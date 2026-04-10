# 3b: may have to modify doctests to get the doctests to pass
# 4
import glob

def ls(folder=name):
    '''
    This function behaves just like the ls program in the shell.

    >>> ls()
    '__pychace__ chat.py htmlcov requirements.txt tools venv'
    
    >>> ls ('tools')
    'tools/ls.py tools/__pychache__'
    '''
    if folder:
        result = ''
        # folder + '/*' ==> tools /*
        # glob is nondeterministic; no guarantees about order of glob results
        # need to convert nondeterministic to deterministic
        # llm we did that by adjusting the temperature
        # best way to make a list determ is to sort it
        for path in sorted(glob.glob(folder + '/*')):
            result += path + ' '
        return result
    else:
        result = ''
        for path in sorted(glob.glob('*')):
            result += path + ' '
        return result.strip()
        # handle this case