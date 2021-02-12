from dragonfly import Dictation, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class EmacsRule(MappingRule):
    mapping = {
        "open file": R(Key("c-x, c-f")),
        "save file": R(Key("c-x, c-s")),
        "save as": R(Key("c-x, c-w")),
        "save all": R(Key("c-x, s")),
        "revert to file": R(Key("c-x, c-v")),
        "revert buffer": R(Key("a-x")),
        "close buffer": R(Key("c-x, c-c")),
        "undo": R(Key("c-underscore")),
        "begin selection": R(Key("c-space")),
        "cancel selection": R(Key("c-g")),
        "cut selection": R(Key("c-w")),
        "paste": R(Key("c-y")),
        "copy number <n>": R(Key("c-x, r, s, %(n)d")),
        "paste number <n>": R(Key("c-x, r, i, %(n)d")),
        # delete
        "forward delete": R(Key("c-delete")),
        "delete word": R(Key("a-delete")),
        "forward delete word": R(Key("a-d")),
        "word forward": R(Key("a-f")),
        "word backward": R(Key("a-b")),
        "line forward": R(Key("c-a")),
        "line backward": R(Key("c-e")),
        "paragraph forward": R(Key("a-lbrace")),
        "paragraph backward": R(Key("a-rbrace")),
        "document forward": R(Key("a-langle")),
        "document backward": R(Key("a-rangle")),
        "C function forward": R(Key("ac-a")),
        "C function backward": R(Key("ac-e")),
        "incremental search": R(Key("c-s")),
        "incremental reverse": R(Key("c-r")),
        "interactive search": R(Key("a-percent")),
        "go to line <n>": R(Key("a-x, %(n)d")),
        "prior bracket": R(Key("escape:down, c-b, escape:up")),
        "next bracket": R(Key("escape:down, c-f, escape:up")),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        ShortIntegerRef("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


def get_rule():
    return EmacsRule, RuleDetails(name="E max", executable="emacs", title="emacs")
