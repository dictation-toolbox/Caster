from dragonfly import Repeat, Dictation, Function, Choice, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key

try: # Try first loading from caster user directory
    from eclipse_support import ec_con
except ImportError: 
    from castervoice.rules.apps.editor.eclipse_rules.eclipse_support import ec_con

from castervoice.rules.core.alphabet_rules import alphabet_support # Manually change import path if in user directory.
from castervoice.lib.merge.additions import Boolean
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class EclipseRule(MappingRule):
    mapping = {
        "prior tab [<n>]":
            R(Key("cs-f6"))*
            Repeat(extra="n"),  # these two must be set up in the eclipse preferences
        "next tab [<n>]":
            R(Key("c-f6"))*Repeat(extra="n"),
        "open resource":
            R(Key("cs-r")),
        "open type":
            R(Key("cs-t")),
        "jump to source":
            R(Key("f3")),
        "editor select":
            R(Key("c-e")),
        "step over [<n>]":
            R(Key("f6/50")*Repeat(extra="n")),
        "step into":
            R(Key("f5")),
        "step out [of]":
            R(Key("f7")),
        "resume":
            R(Key("f8")),
        "(debug | run) last":
            R(Key("f11")),
        "mark occurrences":
            R(Key("as-o")),

        # "terminate" changes to the settings for this hotkey: (when: in dialogs and windows)
        "terminate":
            R(Key("c-f2")),
        "refractor symbol":
            R(Key("sa-r")),
        "symbol next [<n>]":
            R(Key("c-k"))*Repeat(extra="n"),
        "symbol prior [<n>]":
            R(Key("cs-k"))*Repeat(extra="n"),
        "format code":
            R(Key("cs-f")),
        "do imports":
            R(Key("cs-o")),
        "comment line":
            R(Key("c-slash")),
        "build it":
            R(Key("c-b")),
        "split view horizontal":
            R(Key("cs-underscore")),
        "split view vertical":
            R(Key("cs-lbrace")),

        #Line Ops
        "find everywhere":
            R(Key("ca-g")),
        "find word <text> [<back>] [<go>]":
            R(Key("c-f") + Function(ec_con.regex_off) + Function(ec_con.find)),
        "find regex <text> [<back>] [<go>]":
            R(Key("c-f") + Function(ec_con.regex_on) + Function(ec_con.find)),
        "find <a> [<b> [<c>]] [<back>] [<go>]":
            R(Key("c-f") + Function(ec_con.find)),
        "find <punctuation> [<back>] [<go>]":
            R(Key("c-f") + Function(ec_con.find)),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        ShortIntegerRef("n", 1, 3000),
        alphabet_support.get_alphabet_choice("a"),
        alphabet_support.get_alphabet_choice("b"),
        alphabet_support.get_alphabet_choice("c"),
        Choice("punctuation", {"hash tag": "#"}),
        Boolean("back"),
        Boolean("go"),
    ]
    defaults = {
        "n": 1,
        "mim": "",
        "a": None,
        "b": None,
        "c": None,
        "punctuation": None,
        "back": False,
        "go": False
    }


def get_rule():
    return EclipseRule, RuleDetails(name="eclipse", executable="eclipse", title="Eclipse")
