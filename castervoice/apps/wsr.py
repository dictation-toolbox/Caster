from dragonfly import (Grammar, Function)

from castervoice.lib import utilities, settings
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class WindowsSpeechRecognitionRule(MergeRule):

    mapping = {
        "reboot windows speech recognition":
            R(Function(utilities.reboot, wsr=True),
              rdescript="Reboot Windows Speech Recognition"),
    }
    extras = []
    defaults = {}


#---------------------------------------------------------------------------

if settings.WSR:
    control.non_ccr_app_rule(WindowsSpeechRecognitionRule())