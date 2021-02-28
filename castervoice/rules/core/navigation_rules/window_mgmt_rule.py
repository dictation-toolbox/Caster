from dragonfly import MappingRule, Function, Repeat, DictListRef, Repetition, get_engine, ShortIntegerRef

from castervoice.lib import utilities
from castervoice.lib import virtual_desktops
from castervoice.lib.actions import Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

try:  # Try first loading from caster user directory
    from navigation_rules.window_mgmt_rule_support import refresh_open_windows_dictlist, debug_window_switching, switch_window, open_windows_dictlist, timerinstance
except ImportError:
    from castervoice.rules.core.navigation_rules.window_mgmt_rule_support import refresh_open_windows_dictlist, debug_window_switching, switch_window, open_windows_dictlist, timerinstance


"""
Window Switch Manager to swap windows by saying words in their title.

Uses a timer to periodically load the list of open windows into a DictList,
so they can be referenced by the "switch window" command.

Commands:

    "window switch <windows>" -> switch to the window with the given word in its
                                 title. If multiple windows have that word in
                                 their title, then you can say more words in the
                                 window's title to disambiguate which one you
                                 mean. If you don't, the caster messaging window will be
                                 foregrounded instead with info on which windows
                                 are ambiguously being matched by your keywords.
    "window switch refresh" -> manually reload the list of windows. Useful while
                         developing if you don't want to use the timer. Command disabled
    "window switch show" -> output information about which keywords can
                                be used on their own to switch windows and which
                                require multiple words.

"""


class WindowManagementRule(MappingRule):
    mapping = {
        'window maximize':
            R(Function(utilities.maximize_window)),
        'window minimize':
            R(Function(utilities.minimize_window)),
        'window restore':
            R(Function(utilities.restore_window)),
        # Window Switcher Management
        "window switch <windows>":
            R(Function(switch_window), rdescript=""), # Block printing out rdescript
        # Manualy refreshes open windows if `timerinstance.set()` not used
        # "window switch refresh": 
        #    R(Function(lambda: refresh_open_windows_dictlist())),
        "window switch show":
            R(Function(debug_window_switching)),
        # Virtual Workspace Management
        "show work [spaces]":
            R(Key("w-tab")),
        "(create | new) work [space]":
            R(Key("wc-d")),
        "close work [space]":
            R(Key("wc-f4")),
        "close all work [spaces]":
            R(Function(virtual_desktops.close_all_workspaces)),
        "next work [space] [<n>]":
            R(Key("wc-right"))*Repeat(extra="n"),
        "(previous | prior) work [space] [<n>]":
            R(Key("wc-left"))*Repeat(extra="n"),
        "go work [space] <n>":
            R(Function(virtual_desktops.go_to_desktop_number)),
        "send work [space] <n>":
            R(Function(virtual_desktops.move_current_window_to_desktop)),
        "move work [space] <n>":
            R(Function(virtual_desktops.move_current_window_to_desktop, follow=True)),
    }

    extras = [
        ShortIntegerRef("n", 1, 20, default=1),
        Repetition(name="windows", min=1, max=5,
                   child=DictListRef("window_by_keyword", open_windows_dictlist))
    ]


# Window switch update sopen_windows_dictlist every 2 second
timerinstance.set()


def get_rule():
    details = RuleDetails(name="window management rule")
    return WindowManagementRule, details
