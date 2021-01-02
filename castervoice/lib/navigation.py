# -*- coding: utf-8 -*-
'''
master_text_nav shouldn't take strings as arguments - it should take ints, so it can be language-agnostic
'''
import six
import subprocess
import time
from dragonfly import get_current_engine, monitors
from castervoice.lib import control, settings, utilities, textformat
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.clipboard import Clipboard

_CLIP = {}
GRID_PROCESS = None


def initialize_clipboard():
    global _CLIP
    if len(_CLIP) == 0:
        _CLIP = utilities.load_json_file(
            settings.settings(["paths", "SAVED_CLIPBOARD_PATH"]))


initialize_clipboard()


def mouse_alternates(mode, monitor=1, rough=True):
    args = []

    if mode == "legion" and not utilities.window_exists("legiongrid", None):
        from castervoice.asynch.mouse.legion import LegionScanner
        r = monitors[int(monitor) - 1].rectangle
        bbox = [
            int(r.x),
            int(r.y),
            int(r.x) + int(r.dx) - 1,
            int(r.y) + int(r.dy) - 1
        ]
        ls = LegionScanner()
        ls.scan(bbox, rough)
        tscan = ls.get_update()
        args = [
            settings.settings(["paths", "PYTHONW"]),
            settings.settings(["paths", "LEGION_PATH"]), "-t", tscan[0], "-m",
            str(monitor)
        ]
    elif mode == "rainbow" and not utilities.window_exists("rainbowgrid", None):
        args = [
            settings.settings(["paths", "PYTHONW"]),
            settings.settings(["paths", "RAINBOW_PATH"]), "-g", "r", "-m",
            str(monitor)
        ]
    elif mode == "douglas" and not utilities.window_exists("douglasgrid", None):
        args = [
            settings.settings(["paths", "PYTHONW"]),
            settings.settings(["paths", "DOUGLAS_PATH"]), "-g", "d", "-m",
            str(monitor)
        ]
    elif mode == "sudoku" and not utilities.window_exists("sudokugrid", None):
        args = [
            settings.settings(["paths", "PYTHONW"]),
            settings.settings(["paths", "SUDOKU_PATH"]), "-g", "s", "-m",
            str(monitor)
        ]
    global GRID_PROCESS
    GRID_PROCESS = subprocess.Popen(args) if args else None


def wait_for_grid_exit(timeout=5):
    global GRID_PROCESS
    if GRID_PROCESS:
        # TODO Remove if-part after fully migrating to Python3
        if six.PY2:
            t = 0.0
            inc = 0.1
            while t < timeout:
                GRID_PROCESS.poll()
                if GRID_PROCESS.returncode is not None:
                    break
                t += inc
                time.sleep(inc)
            if t >= timeout:
                GRID_PROCESS.kill()
        else:
            try:
                GRID_PROCESS.wait(timeout)
            except subprocess.TimeoutExpired:  # pylint: disable=no-member
                GRID_PROCESS.kill()
    GRID_PROCESS = None


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
                    settings.settings([u'miscellaneous', u'keypress_wait'])/1000.)
                _CLIP[key] = Clipboard.get_system_text()
                utilities.save_json_file(
                    _CLIP, settings.settings([u'paths', u'SAVED_CLIPBOARD_PATH']))
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
            get_current_engine().speak("slot empty")
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
        time.sleep(settings.settings([u'miscellaneous', u'keypress_wait'])/1000.)
        Key("c-v").execute()
        time.sleep(settings.settings([u'miscellaneous', u'keypress_wait'])/1000.)
        # Restore the clipboard contents.
        cb.copy_to_system()


def duple_keep_clipboard(nnavi50):
    cb = Clipboard(from_system=True)
    Key("escape, home, s-end, c-c, end").execute()
    time.sleep(settings.settings([u'miscellaneous', u'keypress_wait'])/1000.)
    for i in range(0, nnavi50):
        Key("enter, c-v").execute()
        time.sleep(settings.settings([u'miscellaneous', u'keypress_wait'])/1000.)
    cb.copy_to_system()


def erase_multi_clipboard():
    global _CLIP
    _CLIP = {}
    utilities.save_json_file(_CLIP,
                             settings.settings([u'paths', u'SAVED_CLIPBOARD_PATH']))


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
    wheel = "wheelup" if direction == "up" else "wheeldown"
    for i in range(1, abs(nnavi500) + 1):
        Mouse("{}:1/10".format(wheel)).execute()


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
            left_click()
        elif int(dokick) == 2:
            right_click()

def previous_line(semi):
    semi = str(semi)
    Key("escape").execute()
    time.sleep(0.05)
    Key("end").execute()
    time.sleep(0.05)
    Text(semi).execute()
    time.sleep(0.05)
    Key("up").execute()
    time.sleep(0.05)
    Key("enter").execute()

def next_line(semi):
    semi = str(semi)
    Key("escape").execute()
    time.sleep(0.05)
    Key("end").execute()
    time.sleep(0.05)
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
    "delete": "backspace",
    "comment": "c-slash",
}
