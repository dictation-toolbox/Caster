from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)

from caster.lib import control
from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class IERule(MergeRule):
    pronunciation = "explorer"

    mapping = {
        "address bar":                       R(Key("a-d"), rdescript="Explorer: Address Bar"),
        "new folder":                        R(Key("cs-n"), rdescript="Explorer: New Folder"),
        "new file":                          R(Key("a-f, w, t"), rdescript="Explorer: New File"),
        "(show | file | folder) properties": R(Key("a-enter"), rdescript="Explorer: Properties Dialog"),
        }
    extras = [
              Dictation("text"),
              IntegerRefST("n", 1, 1000),
              
             ]
    defaults = {"n": 1}

#---------------------------------------------------------------------------

context = AppContext(executable="explorer")
grammar = Grammar("Windows Explorer", context=context)

if settings.SETTINGS["apps"]["explorer"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(IERule())
    else:
        rule = IERule(name="explorer")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()