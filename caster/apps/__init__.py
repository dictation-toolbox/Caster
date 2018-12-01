import glob
import inspect
import os

from caster.lib import utilities


def is_valid(module):
    ''' This function attempts to import the applications in order to detect
    errors in their implementation . After they are imported, they are garbage collected
    when the function returns.'''
    try:
        _ = __import__(module, globals(), locals())
        return True
    except Exception as e:
        print("Ignoring application '{}'. Failed to load with: ".format(module))
        utilities.simple_log()
        return False


modules = glob.glob(os.path.dirname(__file__) + "/*.py")
# only valid applications will be added to the list
__all__ = [
    os.path.basename(f)[:-3]
    for f in modules
    if (not f.endswith('__init__.py') and is_valid(os.path.basename(f)[:-3]))
]
