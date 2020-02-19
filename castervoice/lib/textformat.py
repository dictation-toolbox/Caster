from builtins import str

from castervoice.lib import settings
from castervoice.lib.actions import Text


class TextFormat():
    '''
    Represents text formatting (capitalization and spacing) rules

    Commands for capitalization:
    1 yell - ALLCAPS
    2 tie - TitleCase
    3 Gerrish - camelCase
    4 sing - Sentencecase
    5 laws (default) - alllower
    6 say - whatever speech engine provides
    7 cop - Whatever speech engine provides, initial letter capitalized
    8 slip - whatever speech engine provides, initial letter lowercase
    Commands for word spacing:
    0 (default except Gerrish) - words with spaces
    1 gum (default for Gerrish)  - wordstogether
    2 spine - words-with-hyphens
    3 snake - words_with_underscores
    4 pebble - words.with.fullstops
    5 incline - words/with/slashes
    6 descent - words\with\backslashes
    '''

    @classmethod
    def formatted_text(cls, capitalization, spacing, t):
        if capitalization != 0:
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
            elif capitalization == 6:
                pass
            elif capitalization == 7:
                t = t[0].upper() + t[1:]
            elif capitalization == 8:
                t = t[0].lower() + t[1:]
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
        caps = {0: "<none>", 1: "yell", 2: "tie", 3: "gerrish", 4: "sing", 5: "laws", 6: "say", 7: "cop", 8: "slip"}
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
        if capitalization == 0:
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


format = TextFormat(*settings.settings(["formats", "_default", "text_format"], default_value=[5, 0]))
secondary_format = TextFormat(
    *settings.settings(["formats", "_default", "secondary_format"], default_value=[1, 0]))


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
