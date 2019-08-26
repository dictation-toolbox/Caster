import copy
from castervoice.lib.config.config_toml import TomlConfig


class SelfModStateSavingConfig(TomlConfig):

    def __init__(self, config_path):
        super(SelfModStateSavingConfig, self).__init__(config_path)

    def replace(self, config):
        self._config = config
        self.save()

    def get_copy(self):
        return copy.deepcopy(self._config.copy())
