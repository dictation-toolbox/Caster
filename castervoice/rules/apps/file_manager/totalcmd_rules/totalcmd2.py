from dragonfly import MappingRule

from castervoice.lib.actions import Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class SyncDirsRule(MappingRule):
    mapping = {
        "compare files": R(Key('c-f3')),
        "copy left": R(Key('c-l')),
        "copy right": R(Key('c-r')),
        "view right": R(Key('s-f3')),
        "remove selection": R(Key('c-m')),
        "synchronize": R(Key('a-c')),
    }


def get_rule():
    details = RuleDetails(name="total commander synchronize directories",
                          executable=["totalcmd", "totalcmd64"],
                          title='synchronize directories')
    return SyncDirsRule, details
