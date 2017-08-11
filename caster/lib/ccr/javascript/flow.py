from dragonfly import Key, Text, Dictation, Function, Choice

from caster.lib import control, textformat
from caster.lib.ccr.standard import SymbolSpecs
from caster.lib.dfplus.additions import SelectiveAction
from caster.lib.dfplus.merge.mergerule import MergeRule, TokenSet
from caster.lib.dfplus.state.short import R

class Flow(MergeRule):
    auto = [".js"]
    pronunciation = "flow"
        
    mapping = {
        # flow
        "using flow":                   R(Text("// @flow") + Key("enter, backspace:3"), rdescript="enable flow"),
        "maybe":                        R(Text(": ?"), rdescript="maybe type"),
        "optional":                     R(Text("?: "), rdescript="optional property"),
          }

    extras = [
        ]

    defaults = {
    }
    
        
control.nexus().merger.add_global_rule(Flow())
