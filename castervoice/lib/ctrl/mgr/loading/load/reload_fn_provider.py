# pylint: skip-file
class ReloadFunctionProvider(object):
    def get_reload_fn(self):
        """
        Reimports an already imported module. Python 2/3 compatible method.
        """
        try:
            reload
        except NameError:
            # Python 3
            from imp import reload
        return reload
