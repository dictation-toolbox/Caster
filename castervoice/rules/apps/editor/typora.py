"""
__author__ = 'LexiconCode'
Command-module for Typora
Official Site "https://typora.io/"
"""
from dragonfly import Repeat, Dictation, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class TyporaRule(MappingRule):
    mapping = {
        # File
        "new file": R(Key("c-n")),
        "new window":  # Listed but not implemented
            R(Key("cs-n")),
        # "new tab":      R(Key("")), # Not implemented in Windows OS
        "open file": R(Key("c-o")),
        "go [to] file": R(Key("c-p")),
        "reopen [closed] file": R(Key("cs-t")),
        "save as": R(Key("cs-s")),
        "close file": R(Key("c-w")),
        # Edit
        # "new paragraph": R(Key("enter")) * Repeat(extra="h"), # Caster: "shock"
        "new line <h>": R(Key("s-enter"))*Repeat(extra="h"),
        "copy [as] markdown": R(Key("cs-c")),
        "delete row <n>": R(Key("cs-backspace"))*Repeat(extra="n"),
        "select [cell | scope]": R(Key("c-e")),
        "[select] word <n>": R(Key("c-d"))*Repeat(extra="n"),
        "delete word <n>": R(Key("cs-d"))*Repeat(extra="n"),
        # "jump [to] top":    R(Key("c-home")), # Caster: "sauce wally"
        # "jump [to] selection":  R(Key("c-j")), # Caster: "dunce wally"
        "jump [to] buttom": R(Key("c-end")),
        "find":  # Say "escape" to exit the find/replace context
            R(Key("c-f")),
        "find next": R(Key("f3")),
        "replace": R(Key("c-h")),
        # Paragraph
        "heading <h>": R(Key("c-%(h)d")),
        "paragraph": R(Key("c-o")),
        "increase heading [level] <h>": R(Key("c-equal"))*Repeat(extra="h"),
        "decrease heading [level] <h>": R(Key("c-minus"))*Repeat(extra="h"),
        "table": R(Key("c-t")),  # could be automated.
        "code fences": R(Key("cs-k")),
        "math block": R(Key("cs-m")),
        "quote": R(Key("cs-q")),
        "ordered list": R(Key("cs-[")),
        "indent <h>": R(Key("cs-]"))*Repeat(extra="h"),
        "out dent <h>": R(Key("cs-["))*Repeat(extra="h"),
        # Format
        "strong | bold": R(Key("c-b")),
        "emphasis | italicize": R(Key("c-i")),
        "underline": R(Key("c-u")),
        "code": R(Key("cs-`")),
        "strike": R(Key("as-5")),
        "hyperlink": R(Key("c-k")),
        "image": R(Key("cs-i")),
        "clear [format]": R(Key("c-\\")),
        # View
        "[toggle] sidebar": R(Key("cs-l")),
        "outline": R(Key("cs-1")),
        "articles": R(Key("sc-2")),
        "file tree": R(Key("cs-3")),
        "source code [mode]": R(Key("c-slash")),
        "focus mode": R(Key("f8")),
        "typewriter [mode]": R(Key("f9")),
        "[toggle] fullscreen": R(Key("f11")),
        "actual size": R(Key("cs-0")),
        "zoom in <n>": R(Key("cs-="))*Repeat(extra="n"),
        "zoom out <n>": R(Key("cs--"))*Repeat(extra="n"),
        "switch documnets": R(Key("c-tab")),
        "toggle [dev] tools": R(Key("cs-f12")),
    }

    extras = [
        Dictation("text"),
        ShortIntegerRef("h", 0, 6),
        ShortIntegerRef("n", 1, 30),
    ]

    defaults = {"n": 1, "h": 1}


def get_rule():
    details = RuleDetails(name="tie poor a",
                          executable="typora")
    return TyporaRule, details
