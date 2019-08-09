from dragonfly import Key

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class SyncDirsRule(MergeRule):
    pronunciation = "total commander synchronize directories"

    mapping = {
        "compare files": R(Key('c-f3')),
        "copy left": R(Key('c-l')),
        "copy right": R(Key('c-r')),
        "view right": R(Key('s-f3')),
        "remove selection": R(Key('c-m')),
        "synchronize": R(Key('a-c')),
    }


def get_rule():
    details = RuleDetails(executable=["totalcmd", "totalcmd64"], title='Synchronize directories')
    return SyncDirsRule, details
