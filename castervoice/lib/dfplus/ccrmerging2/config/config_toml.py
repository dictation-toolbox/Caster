from castervoice.lib import utilities, settings
from castervoice.lib.dfplus.ccrmerging2.config.config_base import BaseCCRConfig

'''default CCRConfig implementation'''
class TomlCCRConfig(BaseCCRConfig):
    def save(self):
        utilities.save_toml_file(self._config, settings.SETTINGS["paths"]["CCR_CONFIG_PATH"])
        
    def load(self):
        self._config = utilities.load_toml_file(settings.SETTINGS["paths"]["CCR_CONFIG_PATH"])