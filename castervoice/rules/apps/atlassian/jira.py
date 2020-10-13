from castervoice.lib.actions import Key, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from dragonfly import AppContext, Dictation, Function, MappingRule, Pause, Repeat
from dragonfly.actions import ContextAction

class JiraRule(MappingRule):

    mapping = {
        # Global Shortcuts
        "go to dashboards":
            R(Key("g") + Key("d")),
        "go to projects":
            R(Key("g") + Key("p")),
        "go to boards":
            R(Key("g") + Key("a")),
        "go to issues":
            R(Key("g") + Key("i")),
        # This requires a plugin
        "go to tempo [teams]":
            R(Key("g") + Key("t")),
        # This requires a plugin
        "go to portfolio":
            R(Key("p") + Key("v")),
        "quick search":
            R(Key("slash")),
        "create issue":
            R(Key("c")),
        "submit [form]":
            R(Key('as-s')),

        # Navigating Issues
        "view issue":
            R(Key("o")),
        "next (issue | item) [<nnavi10>]":
            R(Key("j"))*Repeat(extra="nnavi10"),
        "previous (issue | item) [<nnavi10>]":
            R(Key("k"))*Repeat(extra="nnavi10"),
        
        # Issue Actions
        "edit issue":
            R(Key("e")),

        "(action | actions)":
            R(Key(".")),
        # Opens the action menu and attempts the given action. If the action does not exist the menu remains open.
        # Depending on the context the verb "edit" is more natural
        "(action | edit) <action>":
            R(Key(".") + Pause("20") + Text("%(action)s") + Pause("20") + Key("enter")),

        # JIRA contains dedicated hotkeys for some operations. However, the above action command makes them redundant.
        # - assign issue
        # - comment issue
        # - edit issue labels
        # - log time
        # - assign to me
        "share issue":
            R(Key("s")),

        # Board Shortcuts
        "go to backlog":
            R(Key("1")),
        "go to sprint":
            R(Key("2")),
        "go to reports":
            R(Key("3")),
        "toggle details":
            R(Key("t")),
        "toggle presentation [mode]":
            R(Key("z")),
        "toggle swim lanes":
            R(Key("minus")),
        "send to top":
            R(Key("s") + Key("t")),
        "send to bottom":
            R(Key("s") + Key("b")),
    }

    exported = True
    extras = [
        IntegerRefST("nnavi10", 1, 11),
        Dictation("action"),
    ]
    defaults = {
        "nnavi10": 1,
        "action": "",
    }

def get_rule():
    return JiraRule, RuleDetails(name="Jira", executable=["chrome", "firefox"])
