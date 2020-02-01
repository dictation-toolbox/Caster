from dragonfly import MappingRule, Playback, Function, Repeat

from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.actions import Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R
from castervoice.lib import windows_virtual_desktops

class WindowManagementRule(MappingRule):
    mapping = {
        'minimize':
            R(Playback([(["minimize", "window"], 0.0)])),
        'maximize':
            R(Playback([(["maximize", "window"], 0.0)])),
        "remax":
            R(Key("a-space/10,r/10,a-space/10,x")),

        # Workspace management
        "show work [spaces]":
            R(Key("w-tab")),
        "(create | new) work [space]":
            R(Key("wc-d")),
        "close work [space]":
            R(Key("wc-f4")),
        "close all work [spaces]":
            R(Function(windows_virtual_desktops.close_all_workspaces)),
        "next work [space] [<n>]":
            R(Key("wc-right"))*Repeat(extra="n"),
        "(previous | prior) work [space] [<n>]":
            R(Key("wc-left"))*Repeat(extra="n"),

        "go work [space] <n>":
            R(Function(windows_virtual_desktops.go_to_desktop_number)),
        "send work [space] <n>":
            R(Function(windows_virtual_desktops.move_current_window_to_desktop)),
        "move work [space] <n>":
            R(Function(windows_virtual_desktops.move_current_window_to_desktop, follow=True)),
    }

    extras = [
        IntegerRefST("n", 1, 20, default=1),
    ]


def get_rule():
    details = RuleDetails(name="window management rule")
    return WindowManagementRule, details
