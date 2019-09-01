from castervoice.lib import settings, const
from castervoice.lib.config.config_toml import TomlConfig


class RulesActivationConfig(TomlConfig):
    _ORDER_LIST = "order"

    def __init__(self):
        super(RulesActivationConfig, self).__init__(settings.SETTINGS["paths"]["ACTIVATED_RULES_CONFIG_PATH"])
        self.load()
        self._initialize()

    def put(self, rule_class_name, active):
        """
        Puts an rcn at the end of the "active" list. If it's not in the list,
        it's appended. If it is in the list, it's moved.

        :param rule_class_name: (str)
        :param active: (boolean)
        :return:
        """
        active_rules = self._config[RulesActivationConfig._ORDER_LIST]
        active_rules = [rcn for rcn in active_rules if rcn != rule_class_name]
        if active:
            active_rules.append(rule_class_name)
        self._config[RulesActivationConfig._ORDER_LIST] = active_rules

    def get_active_rcns_ordered(self):
        return list(self._config[RulesActivationConfig._ORDER_LIST])

    def _initialize(self):
        """
        Initializes default values if the config is empty.
        """
        if len(self._config) == 0:
            self._config[RulesActivationConfig._ORDER_LIST] = list(const.CORE)
            self.save()
