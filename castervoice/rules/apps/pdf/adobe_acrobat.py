from dragonfly import Dictation, Repeat, Pause, MappingRule, ShortIntegerRef
from castervoice.lib.actions import Text, Key, Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

_SHOW_HIDE_MENU = Key("a-v, s")


class AcrobatRule(MappingRule):
    mapping = {
        "[go to] page <n>":
            R(Key("a-v, n, g/15") + Text("%(n)s") + Key("enter")),
        "set zoom <n>":
            R(Key("c-y/40") + Text("%(n)s") + Key("enter")),
        "open file":
            R(Key("c-o")),
        "duplicate tab":
            R(Key("a-w,n/40,ws-left")),
        "enable scrolling":
            R(Key("a-v, p, c")),
        "(disable scrolling | single page mode)":
            R(Key("a-v, p, s")),
        "next tab [<n>]":
            R(Key("c-tab"))*Repeat(extra="n"),
        "prior tab [<n>]":
            R(Key("cs-tab"))*Repeat(extra="n"),
        "home button":
            R(Mouse("[100, 101], left")),  # coordinates may be user dependent

        # Sticky Note Commands
        # must have the cursor over the location where you want the sticky note
        "add note [<dict>]":
            R(Mouse("right") + Key("t/5") + Text("%(dict)s")),
        "fast [add] note [<dict>]":
            R(Mouse("right") + Key("t/5") + Text("%(dict)s") + Pause("10") +
              Key("escape/5, c-s")),
        "open blank note":
            R(Mouse("right") + Key("t/5")),
        "add blank note":
            R(Mouse("right") + Key("t/5, escape/5, c-s")),
        "delete note":
            R(Mouse("right") + Key("l, c-s")),
        "go back [<n>]":
            R(Key("a-left"))*Repeat(extra='n'),
        "save as":
            R(Key("a-f, a")),

        # when you open up a document that you have previously saved, and then click save,
        # Adobe will sometimes make you go back into the save dialogbox
        # and choose the location you want to save it in and then make you say that you want
        # to overwrite the file. This is annoying, but this command "fast save" will automatically
        # do all that for you.
        "fast save":
            R(Key("c-s/10, enter/10, enter/10, left, enter")),

        # if page down goes too far down then try this command
        "down it [<n>]":
            R(Key("pgdown:%(n)s, up:4")),
        "up it [<n>]":
            R(Key("pgup:%(n)s, down:4")),
        "tools pane":
            R(_SHOW_HIDE_MENU + Key("t")),
        "menu bar":
            R(_SHOW_HIDE_MENU + Key("m")),
        "model tree":
            R(_SHOW_HIDE_MENU + Key("n, e")),
        "bookmarks":
            R(_SHOW_HIDE_MENU + Key("n, b")),
        "[page] thumbnails":
            R(_SHOW_HIDE_MENU + Key("n, b")),
        "rotate [<n>]":
            R(Key("c-plus"))*Repeat(extra='n'),

        # Scrolling Commands
        # Acrobat has a built-in scrolling function with nine speeds.
        # Unfortunately, there are not separate commands for our scrolling up and down
        # You have to start by scrolling in the most recently used direction and then reverse the direction
        "scroll <speed_one_to_nine>":
            R(Key("cs-h/2, %(speed_one_to_nine)s")),
        "scroll":
            R(Key("cs-h/2, 6")),
        "change speed <speed_one_to_nine>":
            R(Key("%(speed_one_to_nine)s, %(speed_one_to_nine)s")),
        "reverse [direction]":
            R(Key("minus")),
        "stop [scrolling]":
            R(Key("escape")),

        # cursor commands
        # (must enable "you single key accelerators to access tools" by going to: edit -> preferences -> general)
        "highlight":
            R(Key("u")),
        "hand tool":
            R(Key("h")),
        "select tool":
            R(Key("v")),
    }
    extras = [
        Dictation("dict"),
        ShortIntegerRef("n", 1, 1000),
        ShortIntegerRef("m", 1, 9),
        ShortIntegerRef("speed_one_to_nine", 1, 9),
    ]
    defaults = {"n": 1, "dict": "nothing"}


def get_rule():
    return AcrobatRule, RuleDetails(name="acrobat", executable="acrobat")
