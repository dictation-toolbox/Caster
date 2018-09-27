import time
import sys

from dragonfly.actions.action_key import Key
from dragonfly.actions.action_text import Text
from dragonfly import Clipboard

from caster.lib import settings, context

_CAPITALIZATION, _SPACING = 0, 0


def normalize_text_format(capitalization, spacing):
    '''
    Commands for capitalization: 
    1 yell - ALLCAPS
    2 tie  - TitleCase
    3 Gerrish- camelCase
    4 sing - Sentencecase
    5 laws - alllower
    Commands for word spacing: 
    1 gum  - wordstogether
    2 spine- words-with-hyphens
    3 snake- words_with_underscores
	4 pebble - words.with.fullstops
	5 incline - words/with/slashes
    '''
    if capitalization == 0:
        capitalization = 5
    if spacing == 0 and capitalization == 3:
        spacing = 1
    return capitalization, spacing


def set_text_format(capitalization, spacing):
    capitalization, spacing = normalize_text_format(capitalization, spacing)
    global _CAPITALIZATION, _SPACING
    _CAPITALIZATION = capitalization
    _SPACING = spacing
    print("Text formatting: %s" % get_text_format_description(_CAPITALIZATION, _SPACING))


def clear_text_format():
    global _CAPITALIZATION, _SPACING
    _CAPITALIZATION = 0
    _SPACING = 0


def peek_text_format():
    global _CAPITALIZATION, _SPACING
    print("Text formatting: %s" % get_text_format_description(_CAPITALIZATION, _SPACING))


def get_text_format_description(capitalization, spacing):
    caps = {0: "<none>", 1: "yell", 2: "tie", 3: "gerrish", 4: "sing", 5: "laws"}
    spaces = {0: "<none>", 1: "gum", 2: "spine", 3: "snake", 4: "pebble", 5: "incline", 6: "descent"}
    if capitalization == 0 and spacing == 0:
        return "<none>"
    else:
        text = get_formatted_text(capitalization, spacing, str("this is a test"))
        return "%s %s (%s)" % (caps[capitalization], spaces[spacing], text)


def master_format_text(capitalization, spacing, textnv):
    capitalization, spacing = normalize_text_format(capitalization, spacing)
    Text(get_formatted_text(capitalization, spacing, str(textnv))).execute()


def partial_format_text(word_limit, textnv):
    global _CAPITALIZATION, _SPACING
    Text(
        get_formatted_text(_CAPITALIZATION, _SPACING, " ".join(
            str(textnv).split(" ")[0:word_limit]))).execute()


def get_formatted_text(capitalization, spacing, t):
    tlen = len(t)
    if capitalization != 0:
        if capitalization == 1:
            t = t.upper()
        elif capitalization == 2:
            t = t.title()
        elif capitalization == 3:
            if tlen > 1:
                t = t.title()
                t = t[0].lower() + t[1:]
            else:
                t = t[0].lower()
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


def prior_text_format(textnv):
    global _CAPITALIZATION, _SPACING
    Text(get_formatted_text(_CAPITALIZATION, _SPACING, str(textnv))).execute()


def master_text_nav(mtn_mode, mtn_dir, nnavi500, extreme):
    '''
    (<mtn_dir> | <mtn_mode> [<mtn_dir>]) [(<nnavi500> | <extreme>)]
    mtn_mode: "shin" s, "queue" cs, "fly" c, (default None)
    mtn_dir: 0-up, 1-down, 2-left, 3-right, (default right)
    nnavi500: number of keypresses (default 1)
    extreme: home/end (default None)
    '''

    k = None
    if mtn_mode is None:
        if extreme is not None:
            if mtn_dir == "left":
                k = "home"
            elif mtn_dir == "right":
                k = "end"
            elif mtn_dir == "up":
                k = "c-home"
            elif mtn_dir == "down":
                k = "c-end"
        else:
            k = str(mtn_dir) + "/5:" + str(nnavi500)
    elif extreme is None:
        k = str(mtn_mode) + "-" + str(mtn_dir) + "/5:" + str(nnavi500)
    else:
        mtn_dir = str(mtn_dir)
        way = "end" if mtn_dir in ["right", "down"] else "home"
        k = str(mtn_mode) + "-" + str(way)
    Key(k).execute()
    time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/1000.)


def enclose_selected(enclosure):
    ''' 
    Encloses selected text in the appropriate enclosures
    By using the system Clipboard as a buffer ( doesn't delete previous contents)
    '''

    (err, selected_text) = context.read_selected_without_altering_clipboard(True)
    if err == 0:
        opener = enclosure.split('~')[0]
        closer = enclosure.split('~')[1]
        enclosed_text = opener + selected_text + closer
        # Attempt to paste enclosed text without altering clipboard
        if not context.paste_string_without_altering_clipboard(enclosed_text):
            print("failed to paste {}".format(enclosed_text))