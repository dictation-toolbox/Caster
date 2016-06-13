'''
master_text_nav shouldn't take strings as arguments - it should take ints, so it can be language-agnostic
'''

from ctypes import windll
from subprocess import Popen
import time

from dragonfly import (Key, Text, Choice, Mouse, monitors)
import dragonfly
import win32clipboard

from caster.asynch.mouse.legion import LegionScanner
from caster.lib import utilities, settings


DIRECTIONS = ["up", "down", "left", "right"]
DIRECTION_STANDARD={"sauce [E]": 0, "dunce [E]": 1, "lease [E]": 2, "Ross [E]": 3, "back": 2 }

''''
Note: distinct token types were removed because
A) a general purpose fill token is easier to remember than 10 of them, and
B) the user of a programming language will know what they're supposed to get filled with
'''
TARGET_CHOICE = Choice("target",
                            {"comma": ",", "(period | dot)": ".", "(pair | parentheses)": "(~)",
                            "[square] (bracket | brackets)": "[~]", "curly [brace]": "{~}",
                            "loop": "for~while", "L paren": "(", "are paren": ")", "openers": "(~[~{",
                            "closers": "}~]~)", "token": "TOKEN"}
                       )

CAPITALIZATION, SPACING = 0, 0

def get_direction_choice(name):
    global DIRECTION_STANDARD
    return Choice(name, DIRECTION_STANDARD)

def initialize_clipboard(nexus):
    if len(nexus.clip) == 0:
        nexus.clip = utilities.load_json_file(settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])

def mouse_alternates(mode, nexus, monitor=1):
    if nexus.dep.PIL:
        if mode == "legion" and not utilities.window_exists(None, "legiongrid"):
            r = monitors[int(monitor)-1].rectangle
            bbox = [int(r.x), int(r.y), int(r.x) + int(r.dx) - 1, int(r.y) + int(r.dy) - 1]
            ls = LegionScanner()
            ls.scan(bbox)
            tscan = ls.get_update()
            Popen(["pythonw", settings.SETTINGS["paths"]["LEGION_PATH"], "-t", tscan[0], "-m", str(monitor)])#, "-d", "500_500_500_500"
        elif mode == "rainbow" and not utilities.window_exists(None, "rainbowgrid"):
            Popen(["pythonw", settings.SETTINGS["paths"]["RAINBOW_PATH"], "-g", "r", "-m", str(monitor)])
        elif mode == "douglas" and not utilities.window_exists(None, "douglasgrid"):
            Popen(["pythonw", settings.SETTINGS["paths"]["DOUGLAS_PATH"], "-g", "d", "-m", str(monitor)])
    else:
        utilities.availability_message(mode.title(), "PIL")    


def clipboard_to_file(nnavi500, nexus, do_copy=False):
    if do_copy:
        Key("c-c").execute()
    
    max_tries = 20
    
    key = str(nnavi500)
    for i in range(0, max_tries):
        failure = False
        try:
            time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/1000.)   # time for keypress to execute
            win32clipboard.OpenClipboard()
            nexus.clip[key] = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            utilities.save_json_file(nexus.clip, settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])            
        except Exception:
            failure = True
            utilities.simple_log()
        if not failure:
            break

def drop(nnavi500, nexus):
    key = str(nnavi500)
    while True:
        failure = False
        try:
            if key in nexus.clip:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(nexus.clip[key])
                win32clipboard.CloseClipboard()
                Key("c-v").execute()
            else:
                dragonfly.get_engine().speak("slot empty")
            time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/1000.) 
        except Exception:
            failure = True
        if not failure:
            break

def erase_multi_clipboard(nexus):
    nexus.clip = {}
    utilities.save_json_file(nexus.clip, settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])

def volume_control(n, volume_mode):
    for i in range(0, int(n)):
        Key("volume" + str(volume_mode)).execute()
    
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
    global CAPITALIZATION, SPACING
    CAPITALIZATION = capitalization
    SPACING = spacing
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
    global CAPITALIZATION, SPACING
    Text(get_formatted_text(CAPITALIZATION, SPACING, str(textnv))).execute()

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

def kill_grids_and_wait(nexus):
    window_title = utilities.get_active_window_title()
    if window_title == settings.RAINBOW_TITLE or window_title == settings.DOUGLAS_TITLE or window_title == settings.LEGION_TITLE:
        nexus.comm.get_com("grids").kill()
        time.sleep(0.1)

def kick(nexus):
    kill_grids_and_wait(nexus)
    windll.user32.mouse_event(0x00000002, 0, 0, 0, 0)
    windll.user32.mouse_event(0x00000004, 0, 0, 0, 0)

def kick_right(nexus):
    kill_grids_and_wait(nexus)
    windll.user32.mouse_event(0x00000008, 0, 0, 0, 0)
    windll.user32.mouse_event(0x00000010, 0, 0, 0, 0)

def kick_middle(nexus):
    kill_grids_and_wait(nexus)
    windll.user32.mouse_event(0x00000020, 0, 0, 0, 0)
    windll.user32.mouse_event(0x00000040, 0, 0, 0, 0)

def wheel_scroll(direction, nnavi500):
    amount = 120
    if direction != "up":
        amount = amount * -1;
    for i in xrange(1, abs(nnavi500)+1):
        windll.user32.mouse_event(0x00000800, 0, 0, amount, 0)
        time.sleep(0.1)
    
def curse(direction, direction2, nnavi500, dokick):
    x, y = 0, 0
    d = str(direction)
    d2 = str(direction2)
    if d == "up" or d2 == "up":
        y = -nnavi500
    if d == "down" or d2 == "down":
        y = nnavi500
    if d == "left" or d2 == "left":
        x = -nnavi500
    if d == "right" or d2 == "right":
        x = nnavi500
    
    Mouse("<" + str(x) + ", " + str(y) + ">").execute()
    if int(dokick)!=0:
        if int(dokick)==1:
            kick()
        elif int(dokick)==2:
            kick_right()

def next_line(semi):
    semi=str(semi)
    Key("escape").execute()
    time.sleep(0.25)
    Key("end").execute()
    time.sleep(0.25)
    Text(semi).execute()
    Key("enter").execute()



