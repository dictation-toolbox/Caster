# from castervoice.lib import const
# TODO: delete castervoice.lib.const if not used, or parts of it which are not


class BaseConfig(object):
    def __init__(self):
        self._config = {}

    def update(self, rule_class_name, active):
        self._config[rule_class_name] = active

    def get_active_rule_class_names(self):
        return [rcn for rcn in self._config if self._config[rcn]]
