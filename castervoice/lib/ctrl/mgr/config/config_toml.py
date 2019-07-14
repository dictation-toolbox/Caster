from castervoice.lib import utilities, settings
from castervoice.lib.ctrl.mgr.config.config_base import BaseConfig


class TomlConfig(BaseConfig):

    def __init__(self):
        super(self)
        self.load()

    def save(self):
        utilities.save_toml_file(self._config, settings.SETTINGS["paths"]["CONFIG_PATH"])

    def load(self):
        self._config = utilities.load_toml_file(settings.SETTINGS["paths"]["CONFIG_PATH"])
