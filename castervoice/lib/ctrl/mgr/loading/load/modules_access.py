import sys


class SysModulesAccessor(object):
    """read-only access to sys.modules"""

    def has_module(self, module_name):
        return module_name in sys.modules

    def get_module(self, module_name):
        return sys.modules[module_name]
