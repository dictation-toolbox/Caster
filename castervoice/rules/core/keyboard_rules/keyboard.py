from dragonfly import Function, Repeat, Dictation, Choice, ContextAction
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

class Keyboard(MergeRule):
    pronunciation = "keyboard"
    
    mapping = {
        "<modifier> <button_dictionary_1>":
              R(Key("%(modifier)s%(button_dictionary_1)s"),
              rdescript="press modifiers plus buttons from button_dictionary_1, non-repeatable"),
        "<hold_release> [<modifier>] <button_dictionary_1>":
              R(Key("%(modifier)s%(button_dictionary_1)s:%(hold_release)s"),
              rdescript="press modifiers plus buttons from button_dictionary_1, non-repeatable"),
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
    longhand_punctuation_names = {
        "minus": "hyphen",
        "hyphen": "hyphen",
        "comma": "comma",
        "deckle": "colon",
        "colon": "colon",
        "slash": "slash",
        "backslash": "backslash"
    }
    button_dictionary_1.update(longhand_punctuation_names)
    shift_spec = "(shift | shin)"
    control_spec = "(control | fly)"
    alt_spec = "alt"
    windows_spec = "windows"
    # in the punctuation dictionary it uses " " which is not the correct dragonfly key name.
    del button_dictionary_1["ace"]
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
        "(ace | space)": "space",
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
        right_spec + shift_spec: "rshift",
        right_spec + control_spec: "rcontrol",
        right_spec + alt_spec: "ralt",
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
            "(control | fly)": "c-",
            "(shift | shin)": "s-",
            "alt": "a-",
            "(control shift | queue)": "cs-",
            "control alt": "ca-",
            "(shift alt | alt shift)": "sa-",
            "(control alt shift | control shift alt)": "csa-",  # control must go first
            "windows": "w-",  # windows should go before alt/shift
            "control windows": "cw-",
            "control windows alt": "cwa-",
            "control windows shift": "cws-",
            "windows shift alt": "wsa-",
            "windows alt shift": "was-",
            "windows shift": "ws-",
            "windows alt": "wa-",
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
    return Keyboard, RuleDetails(ccrtype=CCRType.GLOBAL)
