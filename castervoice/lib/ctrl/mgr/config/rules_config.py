from castervoice.lib import settings
from castervoice.lib.ctrl.mgr.config.config_toml import TomlConfig


class RulesActivationConfig(TomlConfig):

    def __init__(self):
        super(self, settings.SETTINGS["paths"]["CONFIG_PATH"])
        self.load()

    def get_active_rule_class_names(self):
        return [rcn for rcn in self._config if self._config[rcn]]
