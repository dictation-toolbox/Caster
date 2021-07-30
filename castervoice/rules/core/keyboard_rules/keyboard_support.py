import itertools

from castervoice.rules.ccr.standard import SymbolSpecs
from dragonfly import Choice

try:  # Try first loading from caster user directory
    from alphabet_rules.alphabet_support import caster_alphabet
except ImportError:
    from castervoice.rules.core.alphabet_rules.alphabet_support import caster_alphabet

try:  # Try  first loading from caster user directory
    from punctuation_rules.punctuation_support import text_punc_dict
except ImportError:
    from castervoice.rules.core.punctuation_rules.punctuation_support import text_punc_dict

right_spec = "(right | ross)"
left_spec = "(left | lease)"
shift_spec = "(shift | shin)"
control_spec = "(control | fly)"
alt_spec = "alt"
windows_spec = "windows"

# Modifier key names 
modifier_map = {
        control_spec: "c",
        shift_spec: "s",
        alt_spec: "a",
        windows_spec: "w",
    }

# Modifier key names for holding/releasing
modifier_key_name = {
    control_spec: "ctrl ",
    shift_spec: "shift ",
    alt_spec: "alt ",
    windows_spec: "win ",
}


def build_perm_dict(a_dict):
    """
    Builds a dict all possible combinations of spec/key based on dict 
    Returns dict
    """
    choices = {
        ' '.join(key for (key, symbol) in items): ''.join(symbol for (key, symbol) in items)
        for n in range(1, len(a_dict)+1)
        for items in itertools.permutations(a_dict.items(), n)}
    choices.update({"press": ""})
    return choices


modifier_choice_object = Choice("modifier", build_perm_dict(modifier_map))
modifier_choice_key_name = Choice("modifier_key_name", build_perm_dict(modifier_key_name))

class ButtonDict():
    button_dictionary = {}
    reversed_button_dictionary = None

    def getdict(self):
        self.updatedict()
        self.removekeys()
        return(self.button_dictionary)

    def getspec(self, value, dct=button_dictionary):
        # Reverses Keys and Values which allows for dct.get(value)
        # The returned String is the spoken spec for the command
        if self.reversed_button_dictionary is None:
            self.reversed_button_dictionary = dict(map(reversed, dct.items()))
        return self.reversed_button_dictionary.get(value)

    def updatedict(self):
        self.button_dictionary.update(caster_alphabet())
        self.button_dictionary.update(text_punc_dict())
        # Create function keys 1 through 13
        self.button_dictionary.update({"(F{}".format(i) + " | function {})".format(i): "f{}".format(i)
                                       for i in range(1, 13)})
        self.button_dictionary.update({
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

        self.button_dictionary.update({
            self.getspec(' '): "space",
            self.getspec(','): "comma",
            self.getspec('-'): "minus",
            self.getspec('/'): "slash",
            self.getspec(':'): "colon",
        })

    def removekeys(self):
        # in the punctuation dictionary it uses " " which is not the correct dragonfly key name.
        del self.button_dictionary["[is] less [than] [or] equal [to]"]
        del self.button_dictionary["[is] equal to"]
        del self.button_dictionary["[is] greater [than] [or] equal [to]"]


button_dictionary_1 = ButtonDict().getdict()
