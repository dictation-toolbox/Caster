# -*- coding: utf-8 -*-
'''
master_text_nav shouldn't take strings as arguments - it should take ints, so it can be language-agnostic
'''

import time
from ctypes import windll
from subprocess import Popen

import dragonfly
from dragonfly import Choice, monitors
from castervoice.asynch.mouse.legion import LegionScanner
from castervoice.lib import control, settings, utilities, textformat, printer
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.clipboard import Clipboard


_CLIP = {}


def initialize_clipboard():
    global _CLIP
    if len(_CLIP) == 0:
        _CLIP = utilities.load_json_file(
            settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])


def mouse_alternates(mode, monitor=1):
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
            settings.SETTINGS["paths"]["PYTHONW"],
            settings.SETTINGS["paths"]["LEGION_PATH"], "-t", tscan[0], "-m",
            str(monitor)
        ])
    elif mode == "rainbow" and not utilities.window_exists(None, "rainbowgrid"):
        Popen([
            settings.SETTINGS["paths"]["PYTHONW"],
            settings.SETTINGS["paths"]["RAINBOW_PATH"], "-g", "r", "-m",
            str(monitor)
        ])
    elif mode == "douglas" and not utilities.window_exists(None, "douglasgrid"):
        Popen([
            settings.SETTINGS["paths"]["PYTHONW"],
            settings.SETTINGS["paths"]["DOUGLAS_PATH"], "-g", "d", "-m",
            str(monitor)
        ])


def _text_to_clipboard(keystroke, nnavi500):
    if nnavi500 == 1:
        Key(keystroke).execute()
    else:
        max_tries = 20
        cb = Clipboard(from_system=True)
        Key(keystroke).execute()
        key = str(nnavi500)
        global _CLIP
        for i in range(0, max_tries):
            failure = False
            try:
                # time for keypress to execute
                time.sleep(
                    settings.SETTINGS["miscellaneous"]["keypress_wait"]/1000.)
                _CLIP[key] = unicode(Clipboard.get_system_text())
                utilities.save_json_file(
                    _CLIP, settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])
            except Exception:
                failure = True
                utilities.simple_log()
            if not failure:
                break
        cb.copy_to_system()


def stoosh_keep_clipboard(nnavi500):
    _text_to_clipboard("c-c", nnavi500)


def cut_keep_clipboard(nnavi500):
    _text_to_clipboard("c-x", nnavi500)


def drop_keep_clipboard(nnavi500, capitalization, spacing):
    # Maintain standard spark functionality for non-strings
    if capitalization == 0 and spacing == 0 and nnavi500 == 1:
        Key("c-v").execute()
        return
    # Get clipboard text
    if nnavi500 > 1:
        key = str(nnavi500)
        if key in _CLIP:
            text = _CLIP[key]
        else:
            dragonfly.get_engine().speak("slot empty")
            text = None
    else:
        text = Clipboard.get_system_text()
    # Format if necessary, and paste
    if text is not None:
        cb = Clipboard(from_system=True)
        if capitalization != 0 or spacing != 0:
            text = textformat.TextFormat.formatted_text(
                capitalization, spacing, text)
        Clipboard.set_system_text(text)
        time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/1000.)
        Key("c-v").execute()
        time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/1000.)
        # Restore the clipboard contents.
        cb.copy_to_system()


def duple_keep_clipboard(nnavi50):
    cb = Clipboard(from_system=True)
    Key("escape, home, s-end, c-c, end").execute()
    time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/1000.)
    for i in range(0, nnavi50):
        Key("enter, c-v").execute()
        time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/1000.)
    cb.copy_to_system()


def erase_multi_clipboard():
    global _CLIP
    _CLIP = {}
    utilities.save_json_file(_CLIP,
                             settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])


def volume_control(n, volume_mode):
    for i in range(0, int(n)):
        Key("volume" + str(volume_mode)).execute()


def kill_grids_and_wait():
    window_title = utilities.get_active_window_title()
    if (window_title == settings.RAINBOW_TITLE or window_title == settings.DOUGLAS_TITLE
            or window_title == settings.LEGION_TITLE):
        control.nexus().comm.get_com("grids").kill()
        time.sleep(0.1)


def mouse_click(button):
    kill_grids_and_wait()
    Mouse(button).execute()


left_click   = lambda: mouse_click("left")
right_click  = lambda: mouse_click("right")
middle_click = lambda: mouse_click("middle")
left_down    = lambda: mouse_click("left:down")
left_up      = lambda: mouse_click("left:up")
right_down   = lambda: mouse_click("right:down")
right_up     = lambda: mouse_click("right:up")

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
            left_click(control.nexus()) # pylint: disable=too-many-function-args
        elif int(dokick) == 2:
            right_click(control.nexus()) # pylint: disable=too-many-function-args



def next_line(semi):
    semi = str(semi)
    Key("escape").execute()
    time.sleep(0.07)
    Key("end").execute()
    time.sleep(0.07)
    Text(semi).execute()
    Key("enter").execute()


'''
function for performing an action on one or more lines in a text editor.
E.g.: "cut 128 by 148"

action: key combination to be pressed once the body of text has been highlighted, could be an empty string
ln1, ln2: line numbers, usually ShortIntegerRef, the default for ln2 should be an empty string
go_to_line: key combo to navigate by line number
select_line_down: key combo to select the line below
wait: some applications are slow and need a pause between keystrokes, e.g. wait="/10"
upon_arrival: keystroke to be pressed after arriving at the first line. Should have a comma afterwards, e.g. "home, "
'''


def action_lines(action,
                 ln1,
                 ln2,
                 go_to_line="c-g",
                 select_line_down="s-down",
                 wait="",
                 upon_arrival=""):
    num_lines = max(int(ln2) - int(ln1) + 1, int(ln1) -
                    int(ln2) + 1) if ln2 else 1
    top_line = min(int(ln2), int(ln1)) if ln2 else int(ln1)
    command = Key(go_to_line) + Text(str(top_line)) + Key(
        "enter%s, %s%s%s:%s, %s" %
        (wait, upon_arrival, select_line_down, wait, str(num_lines), action))
    command.execute()


actions = {
    "select": "",
    "copy": "c-c",
    "cut": "c-x",
    "paste": "c-v",
    "delete": "backspace"
}
