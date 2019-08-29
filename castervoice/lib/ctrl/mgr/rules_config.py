from castervoice.lib import settings, const
from castervoice.lib.config.config_toml import TomlConfig


class RulesActivationConfig(TomlConfig):
    _ACTIVE_DICT = "active"
    _ORDER_LIST = "order"

    def __init__(self):
        super(RulesActivationConfig, self).__init__(settings.SETTINGS["paths"]["ACTIVATED_RULES_CONFIG_PATH"])
        self.load()
        self._initialize()

    def get_active_rule_class_names(self):
        return [rcn for rcn in self._config[RulesActivationConfig._ACTIVE_DICT]
                if self._config[RulesActivationConfig._ACTIVE_DICT][rcn]]

    def get(self, rule_class_name):
        active = self._config[RulesActivationConfig._ACTIVE_DICT]
        return None if rule_class_name not in active else active[rule_class_name]

    def put(self, rule_class_name, active):
        self._config[RulesActivationConfig._ACTIVE_DICT][rule_class_name] = active
        # this 'while' will take care of any duplicates that might end up in this list
        while rule_class_name in self._config[RulesActivationConfig._ORDER_LIST]:
            self._config[RulesActivationConfig._ORDER_LIST].remove(rule_class_name)
        if active:
            self._config[RulesActivationConfig._ORDER_LIST].append(rule_class_name)

    def get_active_rules_order(self):
        return list(self._config[RulesActivationConfig._ORDER_LIST])

    def _initialize(self):
        """
        Initializes default values if the config is empty.
        """
        if len(self._config) == 0:
            self._config[RulesActivationConfig._ACTIVE_DICT] = {}
            self._config[RulesActivationConfig._ORDER_LIST] = const.CORE
            for core_rule_class_name in self._config[RulesActivationConfig._ORDER_LIST]:
                self._config[RulesActivationConfig._ACTIVE_DICT][core_rule_class_name] = True
            self.save()
