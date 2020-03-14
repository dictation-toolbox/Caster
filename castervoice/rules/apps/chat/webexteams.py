from castervoice.lib.actions import Key, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from dragonfly import (Dictation, MappingRule, Repeat)

class WebexTeamsRule(MappingRule):
    # See https://help.webex.com/en-us/7wr87q/Keyboard-Navigation-and-Shortcuts-for-Cisco-Webex-Teams
    mapping = {
        # Navigation - Primary
        "show spaces":
            R(Key("c-1")),
        "show teams":
            R(Key("c-2")),
        "show calls":
            R(Key("c-3")),
        "show meetings":
            R(Key("c-4")),
        "help":
            R(Key("f1")),
        "create space":
            R(Key("cs-n")),
        "contact person [<person>]":
            R(Key("c-n") + Text("%(person)s")),
        "(search | find)":
            R(Key("c-f")),

        # Navigation - Primary - Filtering
        # There does not appear to be a hotkey to reset filters at this time
        #"show all":
        #    R(Key("sa-?")),
        "show drafts":
            R(Key("sa-d")),
        "show favorites":
            R(Key("cs-u")),
        "show flags":
            R(Key("sa-f")),
        "show mentions all":
            R(Key("cs-l")),
        "show mentions me":
            R(Key("cs-o")),
        "show notifications":
            R(Key("sa-n")),
        "show unread":
            R(Key("sa-r")),

        # Navigation - Space
        # Note - A number of space navigation items do not have documented hotkeys
        "add (person | people) [<person>]":
            R(Key("cs-p") + Text("%(person)s")),
        "create whiteboard":
            R(Key("cs-b")),
        "show whiteboards":
            R(Key("cs-w")),
        "leave space":
            R(Key("cs-e")),
         "(search | find) space":
            R(Key("cs-j")),

        # Navigation - Extra
        "previous (space | item) [<nnavi10>]":
            R(Key("a-up"))*Repeat(extra="nnavi10"),
        "next (space | item) [<nnavi10>]":
            R(Key("a-down"))*Repeat(extra="nnavi10"),

        # Messaging
        "attach":
            R(Key("c-o")),
        "emoji":
            R(Key("w-.")),
        "gif | jeff":
            R(Key("c-g")),
        "toggle markdown":
            R(Key("c-m")),
        "new-line":
            R(Key("s-enter")),
        "personal meeting link":
            R(Key("sa-p")),  
        "send":
            R(Key("enter")),

        # Formatting - Non-markdown
        "strong | bold": 
            R(Key("c-b")),
        "emphasis | italicize": 
            R(Key("c-i")),
        "underline": 
            R(Key("c-u")),
        "(number | numbered) list":
            R(Key("sa-o")),
        "(bullet | bulletted) list":
            R(Key("sa-u")),
        "heading one":
            R(Key("sa-1")),
        "heading two":
            R(Key("sa-2")),
        "heading three":
            R(Key("sa-3")),
            
        # Formatting - markdown
        # Use "markdown" rule
    }
    exported = True
    extras = [
        IntegerRefST("nnavi10", 1, 11),
        Dictation("person"),
    ]
    defaults = {
        "nnavi10": 1,
        "person": "",
    }

def get_rule():
    return WebexTeamsRule, RuleDetails(name="Web X Teams", executable="CiscoCollabHost")
