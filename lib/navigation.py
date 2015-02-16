from ctypes import windll
import sys, win32api, time, win32clipboard

from dragonfly import (Key, Text , Playback, BringApp, Mouse)
import dragonfly
from win32con import MOUSEEVENTF_WHEEL

from asynch.legion import LegionScanner
from lib import control
from lib import utilities
from lib.dragonfree import launch
import  settings
from dragonfly.actions.action_base import Repeat


BASE_PATH = settings.SETTINGS["paths"]["BASE_PATH"]
NIRCMD_PATH = settings.SETTINGS["paths"]["NIRCMD_PATH"]

def word_number(wn):
    numbers_to_words={
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
    d1=str(dict1)
    if d1!="":
        Text(d1)._execute()
    if str(big)!="":
        Key("shift:down")._execute()
    letter._execute()
    if str(big)!="":
        Key("shift:up")._execute()
    d2=str(dict2)
    if d2!="":
        Text(d2)._execute()
    
def numbers2(wnKK):
    ''''''
    Text(str(wnKK))._execute()

def mouse_alternates(mode):
    try:
        if mode=="legion":
            if utilities.window_exists(None, "legiongrid"):
                pass
            else:
                ls=LegionScanner()
                ls.scan()
                tscan=ls.get_update()
                launch.run(["pythonw", settings.SETTINGS["paths"]["LEGION_PATH"], "-t", tscan[0]])
            
        elif mode=="rainbow":
            launch.run(["pythonw", settings.SETTINGS["paths"]["RAINBOW_PATH"], "-m", "r"])
        elif mode=="douglas":
            launch.run(["pythonw", settings.SETTINGS["paths"]["DOUGLAS_PATH"], "-m", "d"])
    except Exception:
        utilities.simple_log(False)
    

def initialize_clipboard():
    control.MULTI_CLIPBOARD = utilities.load_json_file(settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])

def clipboard_to_file(nnavi500):
    key = str(nnavi500)
    while True:
        failure=False
        try:
            time.sleep(0.05)  # time for keypress to execute
            win32clipboard.OpenClipboard()
            control.MULTI_CLIPBOARD[key] = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            settings.save_json_file(control.MULTI_CLIPBOARD, settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])
        except Exception:
            failure=True
        if not failure:
            break

def drop(nnavi500):
    key = str(nnavi500)
    while True:
        failure=False
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
            failure=True
        if not failure:
            break

def volume_control(n, volume_mode):
    for i in range(0, int(n)):
        Key("volume"+str(volume_mode))._execute()
    
def auto_spell(mode, textnv):
    # to do: add support for other modes
    format_mode = str(mode)
    if format_mode == "spell":
        base = "".join(str(textnv).split(" ")).lower()
        Text(base)._execute()
    elif format_mode == "crunch":
        Text(str(textnv).lower())._execute()
    elif format_mode == "caps":
        Text(str(textnv).upper())._execute()
    elif format_mode == "sent":
        base = str(textnv).capitalize()
        Text(base)._execute()
        
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
    elif window_title=="rainbowgrid" or window_title=="douglasgrid" or window_title=="legiongrid":
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
    elif window_title=="rainbowgrid" or window_title=="douglasgrid" or window_title=="legiongrid":
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

