from castervoice.lib import settings, const
from castervoice.lib.config.config_toml import TomlConfig


class RulesConfig(TomlConfig):
    """
    This config file persists three things:
    1. which rules get loaded, either in whitelist mode or blacklist mode
    2. which rules are currently enabled
    3. the order of the enabled rules (important for merging)
    """

    _WHITELISTED = "whitelisted"
    _ENABLED_ORDERED = "_enabled_ordered"
    _INTERNAL = "_internal"

    def __init__(self):
        super(RulesConfig, self).__init__(settings.SETTINGS["paths"]["RULES_CONFIG_PATH"])
        self.load()
        self._initialize()
        self._validate_enabled()

    def put(self, rule_class_name, active):
        """
        Puts an rcn at the end of the "active" list. If it's not in the list,
        it's appended. If it is in the list, it's moved.

        :param rule_class_name: (str)
        :param active: (boolean)
        :return:
        """
        active_rules = self._config[RulesConfig._ENABLED_ORDERED]
        active_rules = [rcn for rcn in active_rules if rcn != rule_class_name]
        if active:
            active_rules.append(rule_class_name)
        self._config[RulesConfig._ENABLED_ORDERED] = active_rules

    def replace_enabled(self, enabled_ordered_rcns):
        self._config[RulesConfig._ENABLED_ORDERED] = enabled_ordered_rcns

    def get_enabled_rcns_ordered(self):
        return list(self._config[RulesConfig._ENABLED_ORDERED])

    def load_is_allowed(self, rcn):
        """
        EAFP here, since it shouldn't often be the case that unknown rules are
        getting added.
        """
        try:
            return self._config[RulesConfig._WHITELISTED][rcn]
        except KeyError:
            self._config[RulesConfig._WHITELISTED][rcn] = True
            self.save()
            return self._config[RulesConfig._WHITELISTED][rcn]

    def _validate_enabled(self):
        """
        Only internal and whitelisted rules should be able to get enabled.
        """
        initial = self._config[RulesConfig._ENABLED_ORDERED]
        validated = []
        for rcn in initial:
            is_internal = rcn in self._config[RulesConfig._INTERNAL]
            if is_internal:
                validated.append(rcn)
                continue
            is_whitelisted = rcn in self._config[RulesConfig._WHITELISTED] \
                             and self._config[RulesConfig._WHITELISTED][rcn]
            if is_whitelisted:
                validated.append(rcn)
        if initial != validated:
            self._config[RulesConfig._ENABLED_ORDERED] = validated
            self.save()

    def _initialize(self):
        """
        Initializes default values if the config is empty.
        """
        if len(self._config) == 0:
            self._config[RulesConfig._ENABLED_ORDERED] = list(const.CORE)
            self._config[RulesConfig._WHITELISTED] = {rcn: True for rcn in const.CORE}
            self._config[RulesConfig._INTERNAL] = list(const.INTERNAL)
            self.save()
