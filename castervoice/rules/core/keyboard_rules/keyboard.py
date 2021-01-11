from dragonfly import Function, Repeat, Dictation, Choice, ContextAction, MappingRule
from castervoice.lib.context import AppContext

from castervoice.lib import navigation, context, textformat, text_utils
from castervoice.rules.core.navigation_rules import navigation_support
from dragonfly.actions.action_mimic import Mimic

from castervoice.lib.actions import Key, Mouse
from castervoice.rules.ccr.standard import SymbolSpecs

try:  # Try first loading from caster user directory
    from alphabet_rules.alphabet_support import caster_alphabet
except ImportError: 
    from castervoice.rules.core.alphabet_rules.alphabet_support import caster_alphabet

try:  # Try  first loading  from caster user directory
    from punctuation_rules.punctuation_support import double_text_punc_dict, text_punc_dict
except ImportError: 
    from castervoice.rules.core.punctuation_rules.punctuation_support import double_text_punc_dict, text_punc_dict

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.actions import AsynchronousAction, ContextSeeker
from castervoice.lib.merge.state.actions2 import UntilCancelled
from castervoice.lib.merge.state.short import S, L, R

_tpd = text_punc_dict()

cat_spec_and_reverse = lambda s1, s2: "(" + s1 + " " + s2 + ")" + " | " + "(" + s2 + " " + s1 + ")"

cat_spec_and_reverse_3 = lambda s1, s2, s3: "(" + s1 + " (" + cat_spec_and_reverse(s2, s3) + ")) | (" + s2 + " (" + cat_spec_and_reverse(s1, s3) + ")) | (" + s3 + " (" + cat_spec_and_reverse(s1, s2) + "))"

class Keyboard(MappingRule):
    mapping = {
        "<modifier> <button_dictionary_1>":
              R(Key("%(modifier)s%(button_dictionary_1)s"),
              rdescript="press button: %(modifier)s%(button_dictionary_1)s"),
        "<hold_release> <button_dictionary_1>":
              R(Key("%(button_dictionary_1)s:%(hold_release)s"),
              rdescript="%(hold_release)s button: %(button_dictionary_1)s"),
    }

    # These buttons can be used without using the "press" prefix.
    right_spec = "(right | ross)"
    left_spec = "(left | lease)"
    button_dictionary_1 = {
        "(F{}".format(i) + " | function {})".format(i) : "f{}".format(i)
        for i in range(1, 13)
    }
    button_dictionary_1.update(caster_alphabet())
    button_dictionary_1.update(_tpd)
    shift_spec = "(shift | shin)"
    control_spec = "(control | fly)"
    alt_spec = "alt"
    windows_spec = "windows"
    # in the punctuation dictionary it uses " " which is not the correct dragonfly key name.
    del button_dictionary_1["[is] less [than] [or] equal [to]"]
    del button_dictionary_1["[is] equal to"]
    del button_dictionary_1["[is] greater [than] [or] equal [to]"]

    ace_key = list(button_dictionary_1.keys())[list(button_dictionary_1.values()).index(' ')]
    slash_key = list(button_dictionary_1.keys())[list(button_dictionary_1.values()).index('/')]
    minus_key = list(button_dictionary_1.keys())[list(button_dictionary_1.values()).index('-')]
    colon_key = list(button_dictionary_1.keys())[list(button_dictionary_1.values()).index(':')]
    comma_key = list(button_dictionary_1.keys())[list(button_dictionary_1.values()).index(',')]

    button_dictionary_1.update({
        "(tab | tabby)": "tab",
        "(backspace | clear)": "backspace",
        "(delete | deli)": "del",
        "(enter | shock)": "enter",
        left_spec: "left",
        right_spec: "right",
        "(up | sauce)": "up",
        "(down | dunce)": "down",
        "page (down | dunce)": "pgdown",
        "page (up | sauce)": "pgup",
        ace_key: "space",
        comma_key: "comma",
        minus_key: "minus",
        slash_key: "slash",
        colon_key: "colon",
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        shift_spec: "shift",
        control_spec: "control",
        alt_spec: "alt",
        right_spec + " " + shift_spec: "rshift",
        right_spec + " " + control_spec: "rcontrol",
        right_spec + " " + alt_spec: "ralt",
        SymbolSpecs.CANCEL: "escape",
        "insert": "insert",
        "pause": "pause",
        windows_spec: "win",
        "(apps | popup)": "apps",
        "print screen": "printscreen",
        "scroll lock": "scrolllock",
        "num lock": "numlock",
        "caps lock": "capslock",
        "(home | lease wally | latch)": "home",
        "(end | ross wally | ratch)": "end",
        # number pad numbers deliberately left off
        # volume control deliberately left off as these are dealt with in HardwareRule and I don't think there's a use case for modifiers there
        # track control deliberately left off as these are (or will be) dealt with in HardwareRule and I don't think there's a use case for modifiers there
        # browser forward/back are deliberately left off. These functions are implemented at the browser rule level
    })
    
    modifier_choice_object = Choice("modifier", {
            control_spec: "c-",
            shift_spec: "s-",
            alt_spec: "a-",
            cat_spec_and_reverse(control_spec, shift_spec) + " | queue": "cs-",
            cat_spec_and_reverse(control_spec, alt_spec): "ca-",
            cat_spec_and_reverse(alt_spec, shift_spec): "sa-",
            cat_spec_and_reverse_3(alt_spec, control_spec, shift_spec): "csa-",
            windows_spec: "w-",
            cat_spec_and_reverse(control_spec, windows_spec): "cw-",
            cat_spec_and_reverse_3(alt_spec, control_spec, windows_spec): "cwa-",
            cat_spec_and_reverse_3(shift_spec, control_spec, windows_spec): "cws-",
            cat_spec_and_reverse_3(alt_spec, shift_spec, windows_spec): "wsa-",
            cat_spec_and_reverse(windows_spec, shift_spec): "ws-",
            cat_spec_and_reverse(windows_spec, alt_spec): "wa-",
            # We will leave this as is as it is seldom used
            "control windows alt shift": "cwas-",
            "press": "",
        })
    extras = [
        modifier_choice_object,
        Choice("button_dictionary_1", button_dictionary_1),
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

