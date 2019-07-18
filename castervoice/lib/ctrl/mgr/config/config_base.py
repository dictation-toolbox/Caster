# from castervoice.lib import const
# TODO: delete castervoice.lib.const if not used, or parts of it which are not


class BaseConfig(object):
    def __init__(self):
        self._config = {}

    def get(self, key):
        return None if key not in self._config else self._config[key]

    def put(self, key, value):
        self._config[key] = value
