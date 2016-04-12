from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)

from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.state.short import R


from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib import control


class CommandRule(MergeRule):
    pronunciation = "K diff"

    mapping = {
        "refresh":                          R(Key("f5"), rdescript="Refresh"),
        }
    extras = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRefST("n", 1, 1000),
              
             ]
    defaults = {"n": 1, "mim":""}

#---------------------------------------------------------------------------

context = AppContext(executable="kdiff3")
grammar = Grammar("KDiff3", context=context)
grammar.add_rule(CommandRule(name="kdiff3"))
if settings.SETTINGS["apps"]["kdiff3"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(CommandRule())
    else:
        grammar.load()