from castervoice.lib import settings
from castervoice.lib.config.config_toml import TomlConfig


class TransformersConfig(TomlConfig):

    def __init__(self):
        super(TransformersConfig, self).__init__(settings.SETTINGS["paths"]["TRANSFORMERS_CONFIG_PATH"])
        self.load()

    def set_transformer_active(self, hcn, active):
        self._config[hcn] = active

    def is_transformer_active(self, hcn):
        return self._config[hcn]

    def __contains__(self, hcn):
        return hcn in self._config
