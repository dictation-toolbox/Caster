from dragonfly import (Grammar, Function)

from caster.lib import utilities, settings
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class WindowsSpeechRecognitionRule(MergeRule):

    mapping = {
        "reboot windows speech recognition":
            R(Function(utilities.reboot, wsr=True),
              rdescript="Reboot Windows Speech Recognition"),
    }
    extras = []
    defaults = {}


#---------------------------------------------------------------------------

grammar = Grammar("Windows Speech Recognition")

if settings.WSR and settings.SETTINGS["apps"]["wsr"]:
    rule = WindowsSpeechRecognitionRule(name="Windows Speech Recognition")
    gfilter.run_on(rule)
    grammar.add_rule(rule)
    grammar.load()
