# pylint: skip-file
class ReloadFunctionProvider(object):
    def get_reload_fn(self):
        """
        Reimports an already imported module. Python 2/3 compatible method.
        """
        #Python 3.12 support
        from importlib import reload
        return reload
