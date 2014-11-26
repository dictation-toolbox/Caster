from dragonfly import (Key, Text , Playback, Function, Repeat,
                        BringApp, Mouse, Choice, WaitWindow)
import sys, win32api, time, win32clipboard, natlink
from ctypes import windll
from win32con import MOUSEEVENTF_WHEEL
from win32api import GetSystemMetrics
import paths, utilities, settings

BASE_PATH = paths.BASE_PATH
MMT_PATH = paths.MMT_PATH
NIRCMD_PATH = paths.NIRCMD_PATH

def initialize_clipboard():
    utilities.MULTI_CLIPBOARD = utilities.load_json_file(paths.SAVED_CLIPBOARD_PATH)

def clipboard_to_file(nnavi500):
    key = str(nnavi500)
    while True:
        failure=False
        try:
            time.sleep(0.05)  # time for keypress to execute
            win32clipboard.OpenClipboard()
            utilities.MULTI_CLIPBOARD[key] = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            utilities.save_json_file(utilities.MULTI_CLIPBOARD, paths.SAVED_CLIPBOARD_PATH)
        except Exception:
            failure=True
        if not failure:
            break

def drop(nnavi500):
    key = str(nnavi500)
    while True:
        failure=False
        try:
            if key in utilities.MULTI_CLIPBOARD:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(utilities.MULTI_CLIPBOARD[key])
                win32clipboard.CloseClipboard()
                Key("c-v")._execute()
            else:
                natlink.execScript ("TTSPlayString \"slot empty\"")
            time.sleep(0.05)
        except Exception:
            failure=True
        if not failure:
            break

def volume_control(n, volume_mode):
    global NIRCMD_PATH
    max_volume = 65535
    sign = 1
    command = "setsysvolume"  # default
    mode = str(volume_mode)
    message = "setting volume to "
    if mode == "up":
        command = "changesysvolume"
        message = "increasing volume by "
    elif mode == "down":
        command = "changesysvolume"
        message = "decreasing volume by "
        sign = -1
    chosen_level = str(int(n * sign * 1.0 / 100 * max_volume))
    try:
        BringApp(NIRCMD_PATH, command, chosen_level).execute()
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))
    utilities.report(message + str(n), speak=settings.SPEAK)

def numbers(n10a, n10b, n10c):
    n10b_str = ""
    n10c_str = ""
    if n10b != -1:
        n10b_str = str(n10b)
    if n10c != -1:
        n10c_str = str(n10c)
    Text(str(n10a) + n10b_str + n10c_str)._execute()
    
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
    elif window_title=="rainbowgrid" or window_title=="douglasgrid":
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
    elif window_title=="rainbowgrid" or window_title=="douglasgrid":
        for i in range(0, 2):
            Key("x")._execute()
        time.sleep(0.1)
        Playback([(["mouse", "right", "click"], 0.0)])._execute()
    else:
        Playback([(["mouse", "right", "click"], 0.0)])._execute()

def kick_middle():
    windll.user32.mouse_event(0x00000020, 0, 0, 0, 0)
    windll.user32.mouse_event(0x00000040, 0, 0, 0, 0)

def grid_to_window():
    BringApp("pythonw", paths.GRID_PATH, "--rowheight", "20" , "--columnwidth", "20" , "--numrows", "20" ,
             "--numcolumns", "20", "--sizeToClient", utilities.get_active_window_hwnd())._execute()
             
def grid_full():
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)
    BringApp(paths.GRID_PATH,
        "--width", str((screen_width - 20)), "--height", str((screen_height - 30)), "--locationx", "10", "--locationy", "15",
        "--rowheight", "20" , "--columnwidth", "20" , "--numrows", "20", "--numcolumns", "20")._execute()
    WaitWindow(executable="CustomGrid.exe")._execute()
    Key("h")._execute()
    
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

