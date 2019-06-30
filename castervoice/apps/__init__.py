import glob
import inspect
import os
import fnmatch

from castervoice.lib import utilities


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


modules = []
base = os.path.dirname(__file__)
for root, dirnames, filenames in os.walk(base, topdown=True):

    diff = len(root) - len(base)

    if diff > 0:
        package_prefix = root[-diff+1:].replace("\\",".") + "."
    else:
        package_prefix = ""

    for filename in fnmatch.filter(filenames, '*.py'):
        modules.append(package_prefix + filename)

# only valid applications will be added to the list
__all__ = [
    f[:-3]
    for f in modules
    if (not f.endswith('__init__.py') and is_valid(f[:-3]))
]
