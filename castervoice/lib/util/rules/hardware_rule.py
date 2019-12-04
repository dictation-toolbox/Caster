from dragonfly import MappingRule, Playback, Function, Pause, Choice

from castervoice.lib.actions import Key
from castervoice.lib import settings, navigation
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R


def change_monitor():
    if settings.SETTINGS["sikuli"]["enabled"]:
        Playback([(["monitor", "select"], 0.0)]).execute()
    else:
        print("This command requires SikuliX to be enabled in the settings file")


class HardwareRule(MappingRule):
    mapping = {
        "volume <volume_mode> [<n>]":
            R(Function(navigation.volume_control, extra={'n', 'volume_mode'})),

        "change monitor":
            R(Key("w-p") + Pause("100") + Function(change_monitor))
    }
    extras = [
        IntegerRefST("n", 1, 50),
        Choice("volume_mode", {
            "mute": "mute",
            "up": "up",
            "down": "down"
        })
    ]
    defaults = {"n": 1, "volume_mode": "setsysvolume"}


def get_rule():
    return HardwareRule, RuleDetails(name="hardware rule")
