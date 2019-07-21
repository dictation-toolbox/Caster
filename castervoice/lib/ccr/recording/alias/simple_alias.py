from castervoice.lib import settings
from castervoice.lib.ccr.recording.alias.base_alias import BaseAliasRule
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails


class Alias(BaseAliasRule):
    pronunciation = "alias"

    def __init__(self):
        super(settings.SETTINGS["paths"]["ALIAS_PATH"])

    def get_pronunciation(self):
        return Alias.pronunciation


def get_rule():
    details = RuleDetails(name="alias",
                          rdp_mode_exclusion=True,
                          transformer_exclusion=True)
    return [Alias, details]
