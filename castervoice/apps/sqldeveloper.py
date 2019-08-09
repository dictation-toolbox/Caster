from dragonfly import Key, Dictation

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class SQLDeveloperRule(MergeRule):
    pronunciation = "sequel developer"

    mapping = {
        "run this query": R(Key("f9")),
        "format code": R(Key("c-f7")),
        "comment line": R(Key("c-slash")),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1}


def get_rule():
    return SQLDeveloperRule, RuleDetails(executable="sqldeveloper64W", title="SQL Developer")
