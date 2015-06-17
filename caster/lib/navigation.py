from ctypes import windll
import time

from dragonfly import (Key, Text , Playback, Choice, Mouse)
import dragonfly
import win32clipboard
from subprocess import Popen

from caster.asynch.mouse import grids
from caster.asynch.mouse.legion import LegionScanner
from caster.lib import control, utilities, settings
from caster.lib.pita import scanner, selector

DIRECTION_STANDARD={"sauce": "up", "dunce": "down", "lease": "left", "Ross": "right", "back": "left" }
TARGET_CHOICE = Choice("target",
                {"comma": ",", "(period | dot)": ".", "(pair | parentheses)": "(~)",
                "[square] (bracket | brackets)": "[~]", "curly [brace]": "{~}",
                "loop": "for~while", "L paren": "(", "are paren": ")", "openers": "(~[~{",
                "closers": "}~]~)",
                "parameter": "PARAMETER", "variable": "VARIABLE", "type": "TYPE",
                "name": "NAME", "object": "OBJECT", "list": "LIST", "scope": "SCOPE",
                "value": "VALUE", "class": "CLASS", "function": "FUNCTION",
                })

def get_alphabet_choice(spec):
    return Choice(spec,
              {
            "arch": "a", 
            "brov": "b", 
            "char": "c", 
            "delta": "d", 
            "echo": "e", 
            "foxy": "f", 
            "goof": "g", 
            "hotel": "h", 
            "India": "i", 
            "julia": "j", 
            "kilo": "k", 
            "Lima": "l", 
            "Mike": "m", 
            "Novakeen": "n", 
            "oscar": "o", 
            "prime": "p", 
            "Quebec": "q", 
            "Romeo": "r", 
            "Sierra": "s", 
            "tango": "t", 
            "uniform": "u", 
            "victor": "v", 
            "whiskey": "w", 
            "x-ray": "x", 
            "yankee": "y", 
            "Zulu": "z", 
               })

def get_direction_choice(spec):
    global DIRECTION_STANDARD
    return Choice(spec, DIRECTION_STANDARD)

def initialize_clipboard():
    if len(control.nexus().clip) == 0:
        control.nexus().clip = utilities.load_json_file(settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])
    
OLD_ACTIVE_WINDOW_TITLE = None
ACTIVE_FILE_PATH = [None, None]

def pita(textnv):
    global OLD_ACTIVE_WINDOW_TITLE, ACTIVE_FILE_PATH
    
    filename, folders, title = utilities.get_window_title_info()
    active_has_changed = OLD_ACTIVE_WINDOW_TITLE != title
    
    # check to see if the active file has changed; if not, skip this step
    if active_has_changed:
        OLD_ACTIVE_WINDOW_TITLE = title
        ACTIVE_FILE_PATH = scanner.guess_file_based_on_window_title(filename, folders)
    
    if filename == None:
        utilities.report("pita: filename pattern not found in window title")
        return
    
    if ACTIVE_FILE_PATH[0] != None:
        result = selector.get_similar_symbol_name(str(textnv), scanner.DATA["directories"][ACTIVE_FILE_PATH[0]][ACTIVE_FILE_PATH[1]]["names"])
        # print "fuzzy match: ", str(textnv), "->", result
        Text(result)._execute()

def word_number(wn):
    numbers_to_words = {
                      0: "zero",
                      1: "one",
                      2: "two",
                      3: "three",
                      4: "four",
                      5: "five",
                      6: "six",
                      7: "seven",
                      8: "eight",
                      9: "nine"
    }
    Text(numbers_to_words[int(wn)])._execute()

def numbers2(wnKK):
    Text(str(wnKK))._execute()

def letters(big, dict1, dict2, letter):
    '''used with alphabet.txt'''
    d1 = str(dict1)
    if d1 != "":
        Text(d1)._execute()
    if str(big) != "":
        Key("shift:down")._execute()
    letter._execute()
    if str(big) != "":
        Key("shift:up")._execute()
    d2 = str(dict2)
    if d2 != "":
        Text(d2)._execute()
    
def letters2(big, letter):
    if str(big) != "":
        Key("shift:down")._execute()
    Key(letter)._execute()
    if str(big) != "":
        Key("shift:up")._execute()

def mouse_alternates(mode):
    try:
        if mode == "legion":
            if control.nexus().dep.PIL:
                if utilities.window_exists(None, "legiongrid"):
                    pass
                else:
                    ls = LegionScanner()
                    ls.scan()#[500, 500, 1000, 1000]
                    tscan = ls.get_update()
                    Popen(["pythonw", settings.SETTINGS["paths"]["LEGION_PATH"], "-t", tscan[0]])#, "-d", "500_500_500_500"
            else:
                utilities.availability_message("Legion", "PIL")
            
        elif mode == "rainbow":
            Popen(["pythonw", settings.SETTINGS["paths"]["RAINBOW_PATH"], "-m", "r"])
        elif mode == "douglas":
            Popen(["pythonw", settings.SETTINGS["paths"]["DOUGLAS_PATH"], "-m", "d"])
    except Exception:
        utilities.simple_log(True)
    

def clipboard_to_file(nnavi500, do_copy=False):
    if do_copy:
        Key("c-c").execute()
    
    key = str(nnavi500)
    while True:
        failure = False
        try:
            time.sleep(0.05)  # time for keypress to execute
            win32clipboard.OpenClipboard()
            control.nexus().clip[key] = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            utilities.save_json_file(control.nexus().clip, settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])
        except Exception:
            failure = True
        if not failure:
            break

def drop(nnavi500):
    key = str(nnavi500)
    while True:
        failure = False
        try:
            if key in control.nexus().clip:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(control.nexus().clip[key])
                win32clipboard.CloseClipboard()
                Key("c-v")._execute()
            else:
                dragonfly.get_engine().speak("slot empty")
            time.sleep(0.05)
        except Exception:
            failure = True
        if not failure:
            break

def erase_multi_clipboard():
    control.nexus().clip = {}
    utilities.save_json_file(control.nexus().clip, settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])

def volume_control(n, volume_mode):
    for i in range(0, int(n)):
        Key("volume" + str(volume_mode))._execute()
    
def master_format_text(capitalization, spacing, textnv):
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
    t = str(textnv)
    tlen = len(t)
    
    if capitalization == 0 and settings.SETTINGS["ccr"]["default_lower"]:
        capitalization = 5
    
    if spacing == 0 and capitalization == 3:
        spacing = 1
    
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
    Text(t)._execute()

def master_text_nav(mtn_mode, mtn_dir, nnavi500, extreme):
    '''
    (<mtn_dir> | <mtn_mode> [<mtn_dir>]) [(<nnavi500> | <extreme>)]
    mtn_mode: "shin" s, "queue" cs, "fly" c, (default None)
    mtn_dir: up, down, left, right, (default right)
    nnavi500: number of keypresses (default 1)
    extreme: home/end (default None)
    '''
    
    k = None
    if mtn_mode == None:
        if extreme != None:
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
    elif extreme == None:
        k = str(mtn_mode) + "-" + str(mtn_dir) + "/5:" + str(nnavi500)
    else:
        mtn_dir = str(mtn_dir)
        way = "end" if mtn_dir in ["right", "down"] else "home"
        k = str(mtn_mode) + "-" + str(way)
    Key(k).execute()
    time.sleep(0.05)

def kill_grids_and_wait():
    window_title = utilities.get_active_window_title()
    if window_title == settings.RAINBOW_TITLE or window_title == settings.DOUGLAS_TITLE or window_title == settings.LEGION_TITLE:
        control.nexus().comm.get_com("grids").kill()
        time.sleep(0.1)

def kick():
    kill_grids_and_wait()
    Playback([(["mouse", "left", "click"], 0.0)])._execute()

def kick_right():
    kill_grids_and_wait()
    Playback([(["mouse", "right", "click"], 0.0)])._execute()

def kick_middle():
    kill_grids_and_wait()
    windll.user32.mouse_event(0x00000020, 0, 0, 0, 0)
    windll.user32.mouse_event(0x00000040, 0, 0, 0, 0)


    
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
        

def elite_text(text):
    elite_map={"a": "@", "b":"|3", "c": "(", "d": "|)", "e": "3", 
               "f": "|=", "g":"6", "h": "]-[", "i": "|", "j": "_|", 
               "k": "|{", "l": "|_", "m": "|\/|", "n": "|\|", "o": "()", 
               "p": "|D", "q": "(,)", "r": "|2", "s": "$", "t": "']['", 
               "u": "|_|", "v": "\/", "w": "\/\/", "x": "}{", "y": "`/", "z": "(\\)"}
    text=str(text).lower()
    result=""
    for c in text:
        if c in elite_map:
            result+=elite_map[c]
        else:
            result+=c
    Text(result).execute()


def next_line(semi):
    semi=str(semi)
    Key("escape").execute()
    time.sleep(0.25)
    Key("end").execute()
    time.sleep(0.25)
    Text(semi).execute()
    Key("enter").execute()







