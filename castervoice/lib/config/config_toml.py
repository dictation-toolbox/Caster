from castervoice.lib import utilities
from castervoice.lib.config.config_base import BaseConfig


class TomlConfig(BaseConfig):

    def __init__(self, config_path):
        super(TomlConfig, self)
        self._config_path = config_path

    def save(self):
        utilities.save_toml_file(self._config, self._config_path)

    def load(self):
        self._config = utilities.load_toml_file(self._config_path)
