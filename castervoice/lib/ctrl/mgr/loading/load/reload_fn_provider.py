class ReloadFunctionProvider(object):
    def get_reload_fn(self):
        """
        Reimports an already imported module. Python 2/3 compatible method.
        """
        from imp import reload
        return reload
