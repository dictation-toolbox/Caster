from castervoice.lib import settings, const, utilities
from castervoice.lib.config.config_toml import TomlConfig
import copy


class RulesConfig(TomlConfig):
    """
    This config file persists three things:
    1. which rules get loaded, either in whitelist mode or blacklist mode
    2. which rules are currently enabled
    3. the order of the enabled rules (important for merging)
    """

    _ENABLED_ORDERED = "enabled_ordered"
    _LOADED = "loaded"
    _LOAD_LISTING_MODE = "mode"

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

    def get_active_rcns_ordered(self):
        return list(self._config[RulesConfig._ENABLED_ORDERED])

    def load_is_allowed(self, rcn):
        rcn_in_list = rcn in self._config[RulesConfig._LOADED]
        if self._config[RulesConfig._LOAD_LISTING_MODE] == const.LoadListingMode.WHITELIST:
            return rcn_in_list
        else:
            return not rcn_in_list

    def save(self):
        """
        Don't save internal rules. They get added in memory and removed in memory.
        If anyone really really wants them out permanently, a setting can be added
        to the GrammarManager to take them out.

        As for the specs, they get transformed just like anything else.
        """
        config = copy.deepcopy(self._config)
        config[RulesConfig._ENABLED_ORDERED] = [rcn for rcn in config[RulesConfig._ENABLED_ORDERED]
                                                if rcn not in const.INTERNAL]
        utilities.save_toml_file(config, self._config_path)

    def _validate_enabled(self):
        """
        If you manually cut something from "loaded" but leave it in "enabled", it will
        get cut from "enabled". It doesn't make any sense for something to be
        enabled which is not loaded.
        """
        initial = self._config[RulesConfig._ENABLED_ORDERED][:]
        validated = None
        if self._config[RulesConfig._LOAD_LISTING_MODE] == const.LoadListingMode.WHITELIST:
            validated = [rcn for rcn in initial if rcn in self._config[RulesConfig._LOADED]]
        else:
            validated = [rcn for rcn in initial if rcn not in self._config[RulesConfig._LOADED]]
        if initial != validated:
            self._config[RulesConfig._ENABLED_ORDERED] = validated
            self.save()

    def _initialize(self):
        """
        Initializes default values if the config is empty.
        """
        if len(self._config) == 0:
            self._config[RulesConfig._ENABLED_ORDERED] = list(const.CORE)
            self._config[RulesConfig._LOADED] = list(const.CORE)
            self._config[RulesConfig._LOAD_LISTING_MODE] = const.LoadListingMode.WHITELIST
            self.save()
