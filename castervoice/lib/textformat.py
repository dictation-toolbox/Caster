from builtins import str

from castervoice.lib import settings, context
from castervoice.lib.actions import Text, Key


class TextFormat():
    '''
    Represents text formatting (capitalization and spacing) rules

    Commands for capitalization:
    -1 rarb - capitals determined by Dragon vocabulary and by the use of the prefix "cap"
        (ideally "cap" would override any capitalization commands by default but that is tricky 
        so this is a temporary solution. it may not work perfectly with the "set format" command.) 
    0 - (default) if word spacing is specified, then alllower (5), but
        if word spacing is not specified, then capitals are determined by engine
        vocabulary and by the use of the prefix "cap"
    1 yell - ALLCAPS
    2 tie - TitleCase
    3 Gerrish - camelCase
    4 sing - Sentencecase
    5 laws - alllower
    Commands for word spacing:
    0 (default except Gerrish) - words with spaces
    1 gum (default for Gerrish)  - wordstogether
    2 spine - words-with-hyphens
    3 snake - words_with_underscores
    4 pebble - words.with.fullstops
    5 incline - words/with/slashes
    '''

    @classmethod
    def formatted_text(cls, capitalization, spacing, t):
        if capitalization != 0 and capitalization != -1:
            if capitalization == 1:
                t = t.upper()
            elif capitalization == 2:
                t = t.title()
            elif capitalization == 3:
                t = t[0].lower() + t.title()[1:]
            elif capitalization == 4:
                t = t.capitalize()
            elif capitalization == 5:
                t = t.lower()
        if spacing != 0:
            if spacing == 1:
                t = "".join(t.split(" "))
            elif spacing == 2:
                t = "-".join(t.split(" "))
            elif spacing == 3:
                t = "_".join(t.split(" "))
            elif spacing == 4:
                t = ".".join(t.split(" "))
            elif spacing == 5:
                t = "/".join(t.split(" "))
            elif spacing == 6:
                t = "\\".join(t.split(" "))
        return t

    @classmethod
    def get_text_format_description(cls, capitalization, spacing):
        caps = {0: "<none>", 1: "yell", 2: "tie", 3: "gerrish", 4: "sing", 5: "laws"}
        spaces = {
            0: "<none>",
            1: "gum",
            2: "spine",
            3: "snake",
            4: "pebble",
            5: "incline",
            6: "descent"
        }
        if capitalization == 0 and spacing == 0:
            return "<none>"
        else:
            text = cls.formatted_text(capitalization, spacing, str("this is a test"))
            return "%s %s (%s)" % (caps[capitalization], spaces[spacing], text)

    @classmethod
    def normalize_text_format(cls, capitalization, spacing):
        if capitalization == 0 and not spacing == 0:
            # capitalization defaults to lower unless no spacing is provided
            # in which case capitalization is determined by the engine vocabulary
            # and by "cap" prefixes 
            
            capitalization = 5
        if spacing == 0 and capitalization == 3:
            spacing = 1
        return (capitalization, spacing)

    def __init__(self, default_cap, default_spacing):
        self.default_cap = default_cap
        self.default_spacing = default_spacing
        self.capitalization = 0
        self.spacing = 0

    def set_text_format(self, capitalization, spacing):
        self.capitalization, self.spacing = self.normalize_text_format(
            capitalization, spacing)

    def clear_text_format(self):
        self.capitalization = self.default_cap
        self.spacing = self.default_spacing

    def __str__(self):
        return self.get_text_format_description(self.capitalization, self.spacing)

    def get_formatted_text(self, t):
        return TextFormat.formatted_text(self.capitalization, self.spacing, t)


format = TextFormat(*settings.SETTINGS["formats"]["_default"]["text_format"])
secondary_format = TextFormat(
    *settings.SETTINGS["formats"]["_default"]["secondary_format"])


def _choose_format(big):
    return format if not big else secondary_format


# module interface
def set_text_format(big, capitalization, spacing):
    _choose_format(big).set_text_format(capitalization, spacing)


def clear_text_format(big):
    _choose_format(big).clear_text_format()


def peek_text_format(big):
    print("Text formatting: %s" % str(_choose_format(big)))


def partial_format_text(big, word_limit, textnv):
    Text(
        _choose_format(big).get_formatted_text(" ".join(
            str(textnv).split(" ")[0:word_limit]))).execute()


def prior_text_format(big, textnv):
    Text(_choose_format(big).get_formatted_text(str(textnv))).execute()


def master_format_text(capitalization, spacing, textnv):
    capitalization, spacing = TextFormat.normalize_text_format(capitalization, spacing)
    Text(TextFormat.formatted_text(capitalization, spacing, str(textnv))).execute()


def enclose_format(enclosure, capitalization, spacing, textnv, hug=False, inner_formatting=True):
    if isinstance(enclosure, tuple):
        left_side, right_side = enclosure
    else:
        left_side = enclosure; right_side = enclosure
    if hug == True: # we are enclosing something that is already there
        (err, selected_text) = context.read_selected_without_altering_clipboard(True)
        if err == 0:
            textnv = selected_text
    if textnv == "": # no dictation has been provided
        Text(left_side + right_side).execute()
        offset = len(right_side)
        Key("left:%d" %offset).execute()
    else: # dictation has been provided 
        
        capitalization, spacing = TextFormat.normalize_text_format(capitalization, spacing)
        inner_text = TextFormat.formatted_text(capitalization, spacing, str(textnv))
        output_text = left_side + inner_text + right_side
        Text(output_text).execute()
        # Alternate method: faster but not as reliable
        # if not context.paste_string_without_altering_clipboard(enclosed_text):
        #     print("failed to paste {}".format(enclosed_text))
