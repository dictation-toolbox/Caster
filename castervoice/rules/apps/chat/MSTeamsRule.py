from dragonfly import ShortIntegerRef 
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R
from dragonfly import (AppContext, Choice, Dictation, Function, MappingRule,
                       Repeat)

class MSTeamsRule(MappingRule):
    name = "microsoft teams"
    mapping = {
        # General
        "search":
            R(Key("c-e")),
        "keyboard shortcuts":
            R(Key("c-.")),
        "settings":
            R(Key("c-comma")),
        "help":
            R(Key("f1")),
        "commands":
            R(Key("c-slash")),
        "filter":
            R(Key("cs-f")),
        "go to":
            R(Key("c-g")),
        "new chat":
            R(Key("c-n")),

        # Navigation
        "activity":
            R(Key("c-1")),
        "chat":
            R(Key("c-2")),
        "teams":
            R(Key("c-3")),
        "calendar":
            R(Key("c-4")),
        "calls":
            R(Key("c-5")),
        "files":
            R(Key("c-6")),
        "shifts":
            R(Key("c-7")),
        "previous item [<nnavi10>]":
            R(Key("a-up"))*Repeat(extra="nnavi10"),
        "next item [<nnavi10>]":
            R(Key("a-down"))*Repeat(extra="nnavi10"),
        "previous team":
            R(Key("cs-up")),
        "next team":
            R(Key("cs-down")),
        "previous section":
            R(Key("cs-f6")),
        "next section":  
            R(Key("c-f6")),

        # Messaging
        "focus compose":
            R(Key("c")),
        "expand compose":
            R(Key("cs-x")),
        "send":
            R(Key("c-enter")),
        "attach":
            R(Key("c-o")),
        "new-line":
            R(Key("s-enter")),
        "reply":
            R(Key("r")),

        # meetings calls and calendar
        "Accept [video] call":
            R(Key("cs-a")),
        "Accept [audio] call":
            R(Key("cs-s")),
        "decline [call]":
            R(Key("cs-d")),
        "start audio call":
            R(Key("cs-c")),
        "Start video call":
            R(Key("cs-u")),
        "toggle mute":
            R(Key("cs-m")),
        "screen share":
            R(Key("cs-e")),
        "toggle video":
            R(Key("cs-o")),
        "sharing toolbar":
            R(Key("cs-space")),
        "decline screen share":
            R(Key("cs-d")),
        "Accept screen share":
            R(Key("cs-a")),
        "Schedule meeting":
            R(Key("as-n")),
         "go to current time":
            R(Key("a-.")),
         "go to previous (day | week)":
            R(Key("ca-left")),
         "go to next (day | week)":
            R(Key("ca-right")),
         "View day":
            R(Key("ca-1")),
         "View workweek":
            R(Key("ca-2")),
         "View week":
            R(Key("ca-3")),
   }
    exported = True
    extras = [
        ShortIntegerRef("nnavi10", 1, 11)
    ]
    defaults = {
        "nnavi10": 1
    }


def get_rule():
    return MSTeamsRule, RuleDetails(name="Microsoft Teams", executable="teams")
