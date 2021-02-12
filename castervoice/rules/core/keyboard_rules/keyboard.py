from dragonfly import Function, Repeat, Dictation, Choice, ContextAction, MappingRule, ShortIntegerRef
from castervoice.lib.context import AppContext

try:  # Try first loading from caster user directory
    from keyboard_rules import keyboard_support
except ImportError:
    from castervoice.rules.core.keyboard_rules import keyboard_support

try:  # Try first loading from caster user directory
    from punctuation_rules import punctuation_support
except ImportError:
    from castervoice.rules.core.punctuation_rules import punctuation_support

from castervoice.lib.actions import Key

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.actions import AsynchronousAction, ContextSeeker
from castervoice.lib.merge.state.actions2 import UntilCancelled
from castervoice.lib.merge.state.short import S, L, R

_tpd = punctuation_support.text_punc_dict()

def hold_keys(modifier_choice_key_name):
    modifier_list = modifier_choice_key_name.strip().split(" ")
    for key in modifier_list:
        Key("{}:down".format(key)).execute()

class Keyboard(MappingRule):
    mapping = {
        "<modifier> <button_dictionary_1>":
            R(Key("%(modifier)s-%(button_dictionary_1)s"), rdescript="Keyboard: %(modifier)s %(button_dictionary_1)s"),
        "hold <modifier_key_name>":
            R(Function(lambda modifier_key_name: hold_keys(modifier_key_name),rdescript="Keyboard: Hold %(modifier_key_name)s")),
        "release modifier keys": R(Key("shift:up, ctrl:up, alt:up, win:up"))
        }

    extras = [
        keyboard_support.modifier_choice_object,
        keyboard_support.modifier_choice_key_name,
        Choice("button_dictionary_1", keyboard_support.button_dictionary_1),
    ]

    defaults = {
        "modifier": "",
        "modifier_name": "",
        "button_dictionary_1": "",
    }

def get_rule():
    return Keyboard, RuleDetails(name = "keyboard")
