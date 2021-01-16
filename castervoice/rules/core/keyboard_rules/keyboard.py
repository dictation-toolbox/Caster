from dragonfly import Choice, MappingRule

from castervoice.rules.core.keyboard_rules import keyboard_support
from castervoice.lib.actions import Key

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class Keyboard(MappingRule):
    mapping = {
        "<modifier> <button_dictionary_1>":
              R(Key("%(modifier)s%(button_dictionary_1)s"),
              rdescript="press button: %(modifier)s%(button_dictionary_1)s"),
        "<hold_release> <button_dictionary_1>":
              R(Key("%(button_dictionary_1)s:%(hold_release)s"),
              rdescript="%(hold_release)s button: %(button_dictionary_1)s"),
    }

    extras = [
        keyboard_support.modifier_choice_object,
        Choice("button_dictionary_1", keyboard_support.button_dictionary_1),
        Choice("hold_release", {
            "hold": "down",
            "release": "up"
        }),
    ]

    defaults = {
        "modifier": ""
    }

def get_rule():
    return Keyboard, RuleDetails(name = "keyboard")
