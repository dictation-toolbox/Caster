from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)

from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.state.short import R


class CommandRule(MappingRule):

    mapping = {
        "next tab [<n>]":               R(Key("c-tab"), rdescript="Foxit Reader: Next Tab") * Repeat(extra="n"),
        "prior tab [<n>]":              R(Key("cs-tab"), rdescript="Foxit Reader: Previous Tab") * Repeat(extra="n"),
        "close tab [<n>]":              R(Key("c-f4/20"), rdescript="Foxit Reader: Close Tab") * Repeat(extra="n"),
        }
    extras = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRefST("n", 1, 1000),
             ]
    defaults = {"n": 1, "mim":""}

#---------------------------------------------------------------------------

context = AppContext(executable="Foxit Reader")
grammar = Grammar("Foxit Reader", context=context)
grammar.add_rule(CommandRule(name="Foxit Reader"))
if settings.SETTINGS["apps"]["foxitreader"]:
    grammar.load()