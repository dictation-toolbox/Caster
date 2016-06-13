import time

from dragonfly.actions.action_key import Key
from dragonfly.actions.action_text import Text

from caster.lib import settings
from caster.lib.navigation import DIRECTIONS

_CAPITALIZATION, _SPACING = 0, 0

def set_text_format(capitalization, spacing):
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
    '''
    if capitalization == 0: 
        capitalization = 5
    if spacing == 0 and capitalization == 3: 
        spacing = 1
    global _CAPITALIZATION, _SPACING
    _CAPITALIZATION = capitalization
    _SPACING = spacing
    return capitalization, spacing

def master_format_text(capitalization, spacing, textnv):
    capitalization, spacing = set_text_format(capitalization, spacing)
    Text(get_formatted_text(capitalization, spacing, str(textnv))).execute()    

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
    
    '''convert language-agnostic int back into string for keypress'''
    mtn_dir = DIRECTIONS[int(mtn_dir)] 
    
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