from castervoice.lib.config.config_toml import TomlConfig
from castervoice.lib.merge.ccrmerging2.hooks.events.event_types import EventType
from castervoice.lib.merge.state.actions2 import NullAction
from dragonfly import Playback, Pause

from castervoice.lib import settings, const
from castervoice.lib.merge.ccrmerging2.hooks.base_hook import BaseHook


class CompanionConfig(TomlConfig):
    """
    Controls companion rules. It is possible to make a circular companion rule relationship. Do not do this.
    """

    def __init__(self):
        super(CompanionConfig, self).__init__(settings.SETTINGS["paths"]["COMPANION_CONFIG_PATH"])
        self.load()
        self._initialize()

    def _initialize(self):
        if len(self._config) == 0:
            self._config = const.COMPANION_STARTER
            self.save()

    def expose_config(self):
        return self._config


class CompanionRuleHook(BaseHook):

    def __init__(self):
        super(CompanionRuleHook, self).__init__(EventType.ACTIVATION)
        self._companion_rules = CompanionConfig()

    def get_pronunciation(self):
        return "companion"

    def run(self, event):
        change = "enable" if event.active else "disable"
        triggers = self._get_companion_rule_triggers(event.rule_class_name)

        # build and execute the de/activation action
        action = NullAction()
        for trigger in triggers:
            action = action + Pause("50")
            action = action + Playback([([change, trigger], 0.0)])
        action.execute()

    def _get_companion_rule_triggers(self, class_name):
        """
        Gets a list of companion rule triggers for a given rule.

        The original design was to allow, for example, A to link to B, and B to link to C and D,
        and D to link to E, so that if you activated A, you'd also activate B, C, D, and E. This
        turns out to be fairly unintuitive in practice though, and not that useful. So now if you
        want to activate B-E with A, you need to list B-E with A, not chain through B.

        :param class_name: str
        :return: set
        """
        if class_name in self._companion_rules.expose_config():
            return self._companion_rules.get(class_name)
        return []


def get_hook():
    return CompanionRuleHook
