from castervoice.lib.dfplus.ccrmerging2.hooks.events.event_types import EventType
from castervoice.lib.dfplus.state.actions2 import NullAction
from dragonfly import Playback, Pause

from castervoice.lib import settings
from castervoice.lib.ctrl.mgr.config.config_toml import TomlConfig
from castervoice.lib.dfplus.ccrmerging2.hooks.base_hook import BaseHook


class CompanionConfig(TomlConfig):
    """
    COMPANION_CONFIG_PATH is a dict of {rule_class_name: [companion_pronunciations...]}

    In order to enable this feature, you need to:
    1. Copy this file into the .caster directory.
    2. Provide both ["paths"]["COMPANION_CONFIG_PATH"] and a path in the settings config file.
        This mechanism allows for feature expansion purely in the user space without growing
        the settings file for everyone.
    """

    def __init__(self):
        super(self, settings.SETTINGS["paths"]["COMPANION_CONFIG_PATH"])
        self.load()

    def expose_config(self):
        return self._config


class CompanionRuleHook(BaseHook):
    """
    Copying this into the .caster dir enables companion rules.
    """

    def __init__(self):
        super(EventType.ACTIVATION)
        self._companion_rules = CompanionConfig()

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
    return CompanionRuleHook()
