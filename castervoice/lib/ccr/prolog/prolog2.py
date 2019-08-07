from dragonfly import MappingRule, Key

from castervoice.lib.actions import Text
from castervoice.lib.ccr.standard import SymbolSpecs
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class PrologNon(MappingRule):
    mapping = {
        "Rule":
            R(Text("() :-.") + Key("left/6")),
        SymbolSpecs.IF:
            R(Text("( ") + Key("enter") + Text(";") + Key("enter") + Text(")")),
    }


def get_rule():
    return PrologNon, RuleDetails(name="prolog companion")
