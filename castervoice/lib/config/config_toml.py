from castervoice.lib import utilities
from castervoice.lib.config.config_base import BaseConfig


class TomlConfig(BaseConfig):

    def __init__(self, config_path):
        super(TomlConfig, self).__init__()
        self._config_path = config_path

    def save(self):
        if not self._config_path:
            return 
        utilities.save_toml_file(self._config, self._config_path)

    def load(self):
        if not self._config_path:
            return {}
        self._config = utilities.load_toml_file(self._config_path)
