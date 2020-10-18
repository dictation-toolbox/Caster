from castervoice.lib import settings
from castervoice.rules.ccr.recording_rules.alias.base_alias import BaseAliasRule
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails


class ChainAlias(BaseAliasRule):
    pronunciation = "chain alias"

    def __init__(self, **kwargs):
        super(ChainAlias, self).__init__(settings.settings(["paths", "SM_CHAIN_ALIAS_PATH"]), **kwargs)

    def get_pronunciation(self):
        return ChainAlias.pronunciation


def get_rule():
    return ChainAlias, RuleDetails(ccrtype=CCRType.SELFMOD,
                          transformer_exclusion=True)
