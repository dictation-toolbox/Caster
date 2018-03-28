import glob
import inspect
import os


def is_valid(module):
    try:
        _=__import__(module,globals(),locals())
        return True
    except Exception as e:
        print("Ignoring application '{}'. Failed to load with: ".format(module))
        print(e)
        return False


modules = glob.glob(os.path.dirname(__file__)+"/*.py" )
__all__ = [ os.path.basename(f)[:-3] for f in modules if (not f.endswith('__init__.py')  and is_valid(os.path.basename(f)[:-3]))]
