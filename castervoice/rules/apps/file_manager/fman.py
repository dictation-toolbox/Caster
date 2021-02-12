from dragonfly import Pause, Choice, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key, Text

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class fmanRule(MappingRule):
    mapping = {
        "copy": R(Key("f5")),
        "deselect": R(Key("c-d")),
        "edit": R(Key("f4")),
        "explorer": R(Key("f10")),
        # Set these yourself and add them to the Choice at the bottom
        # Requires the favourites plug-in
        "go <fav>": R(Key("c-0") + Pause("15") + Text("%(fav)s") + Key("enter")),
        "go see": R(Key("c-p") + Pause("15") + Text("c") + Key("enter")),
        "go to": R(Key("c-p")),
        "move": R(Key("f6")),
        "new file": R(Key("s-f4")),
        "new folder": R(Key("f7")),
        "open left": R(Key("c-left")),
        "open right": R(Key("c-right")),
        "properties": R(Key("a-enter")),
        "refresh": R(Key("c-r")),
        "rename": R(Key("s-f6")),
        "search": R(Key("cs-f")),
        "set favourite": R(Key("s-f")),
        "show favourites": R(Key("c-0")),
        "(show | hide) hidden": R(Key("c-dot")),
        "sort [by] name": R(Key("c-f1")),
        "sort [by] size": R(Key("c-f2")),
        "sort [by] (modified | date)": R(Key("c-f3")),
        "(stoosh | copy) path": R(Key("f11")),
        "terminal": R(Key("f9")),
        "command pallette": R(Key("cs-p")),
    }
    extras = [
        ShortIntegerRef("num", 1, 4),
        Choice("fav", {
            "example favourite": "ef",
        }),
    ]
    defaults = {
        "num": 1,
    }


def get_rule():
    return fmanRule, RuleDetails(name="F man", executable="fman", title="fman")
