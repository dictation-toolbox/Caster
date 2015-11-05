
from dragonfly import (Grammar, MappingRule, Function)

from caster.lib import utilities, settings
from caster.lib.dfplus.state.short import R


class CommandRule(MappingRule):

    mapping = {
        "reboot windows speech recognition":                R(Function(utilities.reboot, wsr=True), rdescript="Reboot Windows Speech Recognition"),
        }
    extras = [              
             ]
    defaults = {}

#---------------------------------------------------------------------------

grammar = None

if settings.WSR:
    grammar = Grammar("Windows Speech Recognition")
    grammar.add_rule(CommandRule(name="Windows Speech Recognition"))
    if settings.SETTINGS["apps"]["wsr"]:
        grammar.load()