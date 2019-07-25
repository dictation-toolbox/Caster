from castervoice.lib import settings, const
from castervoice.lib.config.config_toml import TomlConfig


class RulesActivationConfig(TomlConfig):
    """
    This needs to extend JsonConfig rather than TomlConfig
    b/c TomlConfig does not preserve order.
    """

    _ACTIVE = "active"
    _ORDER = "order"

    def __init__(self):
        super(self, settings.SETTINGS["paths"]["ACTIVATED_RULES_CONFIG_PATH"])
        self.load()
        self._initialize()

    def get_active_rule_class_names(self):
        return [rcn for rcn in self._config if self._config[RulesActivationConfig._ACTIVE][rcn]]

    def get(self, rule_class_name):
        active = self._config[RulesActivationConfig._ACTIVE]
        return None if rule_class_name not in active else active[rule_class_name]

    def put(self, rule_class_name, active):
        self._config[RulesActivationConfig._ACTIVE][rule_class_name] = active
        self._config[RulesActivationConfig._ORDER].remove(rule_class_name)
        if active:
            self._config[RulesActivationConfig._ORDER].append(rule_class_name)

    def get_active_rules_order(self):
        return list(self._config[RulesActivationConfig._ORDER])

    def _initialize(self):
        """
        Initializes default values if the config is empty.
        """
        if len(self._config) == 0:
            self._config[RulesActivationConfig._ACTIVE] = {}
            self._config[RulesActivationConfig._ORDER] = const.CORE
            for core_rule_class_name in self._config[RulesActivationConfig._ORDER]:
                self._config[RulesActivationConfig._ACTIVE][core_rule_class_name] = True
            self.save()
