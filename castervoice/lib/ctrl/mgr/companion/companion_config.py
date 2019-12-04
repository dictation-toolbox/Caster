from castervoice.lib import settings, const
from castervoice.lib.config.config_toml import TomlConfig


class CompanionConfig(TomlConfig):
    """
    Controls companion rules. It is possible to make a circular companion rule relationship. Do not do this.
    """

    def __init__(self):
        super(CompanionConfig, self).__init__(settings.settings(["paths", "COMPANION_CONFIG_PATH"]))
        self.load()
        self._initialize()

    def _initialize(self):
        if len(self._config) == 0:
            self._config = const.COMPANION_STARTER
            self.save()

    def get_companions(self, rcn):
        return [] if rcn not in self._config else list(self._config[rcn])
