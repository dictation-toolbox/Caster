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


def get_modifiers():
    cat_spec_and_reverse = lambda s1, s2: "(" + s1 + " " + s2 + ")" + " | " + "(" + s2 + " " + s1 + ")"
    cat_spec_and_reverse_3 = lambda s1, s2, s3: "(" + s1 + " (" + cat_spec_and_reverse(s2, s3) + ")) | (" + s2 + " (" + cat_spec_and_reverse(s1, s3) + ")) | (" + s3 + " (" + cat_spec_and_reverse(s1, s2) + "))"
    modifiers = {
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
            }

    return modifiers
            

modifier_choice_object = Choice("modifier", get_modifiers())

class ButtonDict():
    button_dictionary = {
            "(F{}".format(i) + " | function {})".format(i) : "f{}".format(i)
            for i in range(1, 13)}
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