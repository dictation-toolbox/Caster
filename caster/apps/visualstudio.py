from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)

from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.state.short import R


class CommandRule(MappingRule):

    mapping = {
        "next tab [<n>]":               R(Key("ca-pgdown"), rdescript="Next Tab") * Repeat(extra="n"),
        "prior tab [<n>]":              R(Key("ca-pgup"), rdescript="Previous Tab") * Repeat(extra="n"),
        "close tab [<n>]":              R(Key("c-f4/20"), rdescript="Close Tab") * Repeat(extra="n"),
        
        "go to line":                   R(Key("c-g"), rdescript="Visual Studio: Go To Line"),
        
        "comment line":                 R(Key("c-k, c-c"), rdescript="Visual Studio: Comment Selection"),
        "comment block":                R(Key("c-k, c-c"), rdescript="Visual Studio: Comment Block"),
        "(un | on) comment line":       R(Key("c-k/50, c-u"), rdescript="Visual Studio: Uncomment Selection"),
        "(un | on) comment block":      R(Key("c-k/50, c-u"), rdescript="Visual Studio: Uncomment Block"),
        "[toggle] full screen":         R(Key("sa-enter"), rdescript="Visual Studio: Fullscreen"),
        "(set | toggle) bookmark":      R(Key("c-k, c-k"), rdescript="Visual Studio: Toggle Bookmark"),
        "next bookmark":                R(Key("c-k, c-k"), rdescript="Visual Studio: Next Bookmark"),
        "prior bookmark":               R(Key("c-k, c-k"), rdescript="Visual Studio: Previous Bookmark"),
        "[toggle] breakpoint":          R(Key("f9"), rdescript="Visual Studio: Breakpoint"),
        
        "step over [<n>]":              R(Key("f10/50") * Repeat(extra="n"), rdescript="Visual Studio: Step Over"),
        "step into":                    R(Key("f11"), rdescript="Visual Studio: Step Into"),
        "step out [of]":                R(Key("s-f11"), rdescript="Visual Studio: Step Out"),
        "resume":                       R(Key("f5"), rdescript="Visual Studio: Resume"),
        }
    extras = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRefST("n", 1, 1000),
              
             ]
    defaults = {"n": 1, "mim":""}

#---------------------------------------------------------------------------

context = AppContext(executable="devenv")
grammar = Grammar("Visual Studio", context=context)
grammar.add_rule(CommandRule(name="visualstudio"))
if settings.SETTINGS["apps"]["visualstudio"]:
    grammar.load()