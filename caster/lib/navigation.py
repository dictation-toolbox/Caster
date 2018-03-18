# -*- coding: utf-8 -*-
'''
master_text_nav shouldn't take strings as arguments - it should take ints, so it can be language-agnostic
'''

import time
from ctypes import windll
from subprocess import Popen

import dragonfly
from caster.asynch.mouse.legion import LegionScanner
from caster.lib import settings, utilities
from dragonfly import Choice, Key, Mouse, Text, monitors
from win32clipboard import (CF_TEXT, CF_UNICODETEXT, CloseClipboard,
                            EmptyClipboard, GetClipboardData,
                            GetPriorityClipboardFormat, OpenClipboard,
                            SetClipboardText)

DIRECTION_STANDARD = {
    "sauce [E]": "up",
    "dunce [E]": "down",
    "lease [E]": "left",
    "Ross [E]": "right",
    "back": "left"
}
'''
Note: distinct token types were removed because
A) a general purpose fill token is easier to remember than 10 of them, and
B) the user of a programming language will know what they're supposed to get filled with
'''
TARGET_CHOICE = Choice(
    "target", {
        "comma": ",",
        "(period | dot)": ".",
        "(pair | parentheses)": "(~)",
        "[square] (bracket | brackets)": "[~]",
        "curly [brace]": "{~}",
        "loop": "for~while",
        "L paren": "(",
        "are paren": ")",
        "openers": "(~[~{",
        "closers": "}~]~)",
        "token": "TOKEN"
    })


def get_direction_choice(name):
    global DIRECTION_STANDARD
    return Choice(name, DIRECTION_STANDARD)


def initialize_clipboard(nexus):
    if len(nexus.clip) == 0:
        nexus.clip = utilities.load_json_file(
            settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])


def mouse_alternates(mode, nexus, monitor=1):
    if nexus.dep.PIL:
        if mode == "legion" and not utilities.window_exists(None, "legiongrid"):
            r = monitors[int(monitor) - 1].rectangle
            bbox = [
                int(r.x),
                int(r.y),
                int(r.x) + int(r.dx) - 1,
                int(r.y) + int(r.dy) - 1
            ]
            ls = LegionScanner()
            ls.scan(bbox)
            tscan = ls.get_update()
            Popen([
                "pythonw", settings.SETTINGS["paths"]["LEGION_PATH"], "-t", tscan[0],
                "-m",
                str(monitor)
            ])  # , "-d", "500_500_500_500"
        elif mode == "rainbow" and not utilities.window_exists(None, "rainbowgrid"):
            Popen([
                "pythonw", settings.SETTINGS["paths"]["RAINBOW_PATH"], "-g", "r", "-m",
                str(monitor)
            ])
        elif mode == "douglas" and not utilities.window_exists(None, "douglasgrid"):
            Popen([
                "pythonw", settings.SETTINGS["paths"]["DOUGLAS_PATH"], "-g", "d", "-m",
                str(monitor)
            ])
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
            # time for keypress to execute
            time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"] / 1000.)
            OpenClipboard()
            fmt = GetPriorityClipboardFormat((CF_UNICODETEXT, CF_TEXT))
            if fmt > 0:
                nexus.clip[key] = GetClipboardData(fmt)
            CloseClipboard()
            utilities.save_json_file(nexus.clip,
                                     settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])
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
                OpenClipboard()
                EmptyClipboard()
                SetClipboardText(nexus.clip[key], CF_UNICODETEXT)
                CloseClipboard()
                Key("c-v").execute()
            else:
                dragonfly.get_engine().speak("slot empty")
            time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"] / 1000.)
        except Exception:
            failure = True
        if not failure:
            break


def erase_multi_clipboard(nexus):
    nexus.clip = {}
    utilities.save_json_file(nexus.clip,
                             settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])


def volume_control(n, volume_mode):
    for i in range(0, int(n)):
        Key("volume" + str(volume_mode)).execute()


def kill_grids_and_wait(nexus):
    window_title = utilities.get_active_window_title()
    if (window_title == settings.RAINBOW_TITLE or window_title == settings.DOUGLAS_TITLE
            or window_title == settings.LEGION_TITLE):
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
        amount = amount * -1
    for i in xrange(1, abs(nnavi500) + 1):
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
    if int(dokick) != 0:
        if int(dokick) == 1:
            kick()
        elif int(dokick) == 2:
            kick_right()


def next_line(semi):
    semi = str(semi)
    Key("escape").execute()
    time.sleep(0.25)
    Key("end").execute()
    time.sleep(0.25)
    Text(semi).execute()
    Key("enter").execute()
