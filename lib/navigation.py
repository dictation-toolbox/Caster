from ctypes import windll
import sys, win32api, time, win32clipboard

from dragonfly import (Key, Text , Playback, BringApp, Mouse)
import dragonfly
from win32con import MOUSEEVENTF_WHEEL

from asynch.mouse.legion import LegionScanner
from lib import control
from lib import utilities
from lib.dragonfree import launch
from lib.pita import scanner, selector, strings
import settings


OLD_ACTIVE_WINDOW_TITLE = None
ACTIVE_FILE_PATH = [None, None]

def pita(textnv):
    global OLD_ACTIVE_WINDOW_TITLE, ACTIVE_FILE_PATH
    '''this function is for tests'''
    try:
        print 1, 2
        '''check to see if the active file has changed;
        if not, skip this step
        '''
        active_window_title = utilities.get_active_window_title().replace("\\", "/")
        active_has_changed = OLD_ACTIVE_WINDOW_TITLE != active_window_title
        filename = None
        path_folders = None
         
        
        if active_has_changed:
            OLD_ACTIVE_WINDOW_TITLE = active_window_title
            '''get name of active file and folders in path;
            will be needed to look up collection of symbols
            in scanner data'''
            # active file
            match_object = scanner.FILENAME_PATTERN.findall(active_window_title)
            if len(match_object) > 0:  
                filename = match_object[0]
            else:
                nothing_found()
                return
            # path folders
            path_folders = active_window_title.split("/")[:-1]
            ACTIVE_FILE_PATH = selector.guess_file_based_on_window_title(filename, path_folders)
         
        if ACTIVE_FILE_PATH[0] != None:
            result=strings.get_similar_symbol_name(str(textnv), scanner.DATA["directories"][ACTIVE_FILE_PATH[0]]["files"][ACTIVE_FILE_PATH[1]]["names"])
            print "fuzzy match: ", str(textnv), "->", result
            Text(result)._execute()
        else:
            print "ACTIVE_FILE_PATH: ", ACTIVE_FILE_PATH
            print "filename: ", filename
            print "path_folders: ", path_folders
        
    except Exception:
        utilities.simple_log(False)

def nothing_found():
    utilities.report("pita: nothing found")

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

def numbers(n10a, n10b, n10c):
    n10b_str = ""
    n10c_str = ""
    if n10b != -1:
        n10b_str = str(n10b)
    if n10c != -1:
        n10c_str = str(n10c)
    Text(str(n10a) + n10b_str + n10c_str)._execute()

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
    
def numbers2(wnKK):
    Text(str(wnKK))._execute()

def mouse_alternates(mode):
    try:
        if mode == "legion":
            if utilities.window_exists(None, "legiongrid"):
                pass
            else:
                ls = LegionScanner()
                ls.scan()
                tscan = ls.get_update()
                launch.run(["pythonw", settings.SETTINGS["paths"]["LEGION_PATH"], "-t", tscan[0]])
            
        elif mode == "rainbow":
            launch.run(["pythonw", settings.SETTINGS["paths"]["RAINBOW_PATH"], "-m", "r"])
        elif mode == "douglas":
            launch.run(["pythonw", settings.SETTINGS["paths"]["DOUGLAS_PATH"], "-m", "d"])
    except Exception:
        utilities.simple_log(False)
    

def initialize_clipboard():
    control.MULTI_CLIPBOARD = utilities.load_json_file(settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])

def clipboard_to_file(nnavi500):
    key = str(nnavi500)
    while True:
        failure = False
        try:
            time.sleep(0.05)  # time for keypress to execute
            win32clipboard.OpenClipboard()
            control.MULTI_CLIPBOARD[key] = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            settings.save_json_file(control.MULTI_CLIPBOARD, settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])
        except Exception:
            failure = True
        if not failure:
            break

def drop(nnavi500):
    key = str(nnavi500)
    while True:
        failure = False
        try:
            if key in control.MULTI_CLIPBOARD:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(control.MULTI_CLIPBOARD[key])
                win32clipboard.CloseClipboard()
                Key("c-v")._execute()
            else:
                dragonfly.get_engine().speak("slot empty")
            time.sleep(0.05)
        except Exception:
            failure = True
        if not failure:
            break

def volume_control(n, volume_mode):
    for i in range(0, int(n)):
        Key("volume" + str(volume_mode))._execute()
    
def master_format_text(capitalization, spacing, textnv):
    '''
    Commands for capitalization: 
    1 yell - ALLCAPS
    2 tie  - TitleCase
    3 k    - camelCase
    4 sing - Sentencecase
    5 low  - alllower
    Commands for word spacing: 
    1 gum  - wordstogether
    2 spine- words-with-hyphens
    3 snake- words_with_underscores
    '''
    t = str(textnv)
    tlen = len(t)
    
    if capitalization == 0 and settings.SETTINGS["ccr"]["default_lower"]:
        capitalization = 5
    
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
    
        
def scroll(direction, nnavi500):
    updown = -100
    if str(direction) == "up":
        updown = 100
    (x, y) = win32api.GetCursorPos()
    win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, updown * nnavi500, 0)
    
def kick():
    window_title = utilities.get_active_window_title()
    if window_title == "Custom Grid":
        Playback([(["I", "left"], 0.0)])._execute()
    elif window_title == "rainbowgrid" or window_title == "douglasgrid" or window_title == "legiongrid":
        for i in range(0, 2):
            Key("x")._execute()
        time.sleep(0.1)
        Playback([(["mouse", "left", "click"], 0.0)])._execute()
    else:
        Playback([(["mouse", "left", "click"], 0.0)])._execute()

def kick_right():
    window_title = utilities.get_active_window_title()
    if window_title == "Custom Grid":
        Playback([(["I", "right"], 0.0)])._execute()
    elif window_title == "rainbowgrid" or window_title == "douglasgrid" or window_title == "legiongrid":
        for i in range(0, 2):
            Key("x")._execute()
        time.sleep(0.1)
        Playback([(["mouse", "right", "click"], 0.0)])._execute()
    else:
        Playback([(["mouse", "right", "click"], 0.0)])._execute()

def kick_middle():
    windll.user32.mouse_event(0x00000020, 0, 0, 0, 0)
    windll.user32.mouse_event(0x00000040, 0, 0, 0, 0)


    
def pixel_jump(direction, direction2, nnavi500):
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
    
def shin(color_mode, nnavi500):
    c = str(color_mode)
    if c == "left" or c == "back":
        Key("s-left/5:" + str(nnavi500)).execute()
    elif c == "right":
        Key("s-right/5:" + str(nnavi500)).execute()
    time.sleep(0.05)

def color(color_mode, nnavi500):
    c = str(color_mode)
    if c == "up":
        Key("shift:down, up/5:" + str(nnavi500) + ", shift:up").execute()
    elif c == "down":
        Key("shift:down, down/5:" + str(nnavi500) + ", shift:up").execute()
    elif c == "left" or c == "back":
        Key("cs-left/5:" + str(nnavi500)).execute()
    elif c == "right":
        Key("cs-right/5:" + str(nnavi500)).execute()
    elif c == "home":
        Key("s-home").execute()
    elif c == "end":
        Key("s-end").execute()
    time.sleep(0.05)

def fly(fly_mode, nnavi500):
    f = str(fly_mode)
    if f == "top":
        Key("c-home").execute()
    elif f == "bottom":
        Key("c-end").execute()
    elif f == "left" or f == "back":
        Key("c-left/5:" + str(nnavi500)).execute()
    elif f == "right":
        Key("c-right/5:" + str(nnavi500)).execute()
    elif f == "home":
        Key("home").execute()
    elif f == "end":
        Key("end").execute()
    time.sleep(0.05)

