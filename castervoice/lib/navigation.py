# -*- coding: utf-8 -*-
'''
master_text_nav shouldn't take strings as arguments - it should take ints, so it can be language-agnostic
'''

import time
from ctypes import windll
from subprocess import Popen
import pyperclip
import re

import dragonfly
from dragonfly import Choice, monitors, Pause
from castervoice.asynch.mouse.legion import LegionScanner
from castervoice.lib import control, settings, utilities, textformat
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.clipboard import Clipboard

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

punctuation_list = ["`", "(", ")", ",", "'", "[", "]", "<", ">", "{", "}", "?", "–", "-", ";", "=", "/", "\\", "$", "+", "*", "%",] 

def get_start_end_position(text, phrase, left_right):
    if left_right == "left":
        # if replaced phrase is a single character, don't require a word boundary ( i.e. space or beginning/end of line ) for match
        if len(phrase)==1:
            # phrases a single character
            pattern = re.escape(phrase)
        else:
            # the \b avoids e.g. matching 'and' in 'land' but seems to allow e.g. matching 'and' in 'hello.and'
            # for matching purposes use lowercase

            pattern = r"\b" + re.escape(phrase.lower()) + r"\b"            
        
        if not re.search(pattern, text.lower()):
            # replaced phase not found
            print("'{}' not found".format(phrase))
            return
        
        match_iter = re.finditer(pattern, text.lower())
        match_list = [(m.start(), m.end()) for m in match_iter]
        last_match = match_list[-1]
        left_index, right_index = last_match


    if left_right == "right":
        # if replaced phrase is a single character, don't require a word boundary ( i.e. space or beginning/end of line ) for match
        
        if len(phrase) == 1:
            # phrase is a single character
            pattern = re.escape(phrase.lower())
        
        else:
            # phrase contains a word
            pattern = r"\b" + re.escape(phrase.lower()) + r"\b"
        match = re.search(pattern, text.lower())
        if not match:
            print("'{}' not found".format(phrase))
            return
        else:
            left_index, right_index = match.span()
    return (left_index, right_index)


def replace_phrase_with_phrase(text, replaced_phrase, replacement_phrase, left_right):
    match = get_start_end_position(text, replaced_phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        return
    return text[: left_index] + replacement_phrase + text[right_index:] 
    

# comments show how to do it using casters clipboard functions
    
def copypaste_replace_phrase_with_phrase(replaced_phrase, replacement_phrase, left_right):
    # temporarily store previous clipboard item
    temp_for_previous_clipboard_item = pyperclip.paste()
    Pause("30").execute()

    if left_right == "left":
        # Key("s-home").execute()
        Key("s-home, c-c/2").execute()
    if left_right == "right":
        # Key("s-end").execute()
        Key("s-end, c-c/2").execute()
    Pause("50").execute()
    # err, selected_text = context.read_selected_without_altering_clipboard()
    selected_text = pyperclip.paste()
    # if err != 0:
        # I'm not discriminating between err = 1 and err = 2
        # print("failed to copy text")
        # return
    
    replaced_phrase = str(replaced_phrase)
    replacement_phrase = str(replacement_phrase)
    new_text = replace_phrase_with_phrase(selected_text, replaced_phrase, replacement_phrase, left_right)
    if not new_text:
        # replaced_phrase not found
        Key("c-v").execute()
        if left_right == "right":
            print("right")
            Key("left:%d" %len(selected_text)).execute()
        return
    # if not context.paste_string_without_altering_clipboard(new_text):
    #     print("failed to paste {}".format(new_text))
    pyperclip.copy(new_text)
    Key("c-v").execute()
    if left_right == "right":
        offset = len(new_text)
        Key("left:%d" %offset).execute()
    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)

def remove_phrase_from_text(text, phrase, left_right):
    match = get_start_end_position(text, phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        return
        
    # if the "phrase" is punctuation, just remove it, but otherwise remove an extra space adjacent to the phrase
    if phrase in punctuation_list:
        return text[: left_index] + text[right_index:] 
    else:
        return text[: left_index - 1] + text[right_index:] 


def copypaste_remove_phrase_from_text(phrase, left_right):
    # temporarily store previous clipboard item
    temp_for_previous_clipboard_item = pyperclip.paste()
    Pause("30").execute()

    if left_right == "left":
        Key("s-home, c-c/2").execute()
        
    if left_right == "right":
        Key("s-end, c-c/2").execute()
    Pause("50").execute()
    # get text from clipboard
    selected_text = pyperclip.paste()

    phrase = str(phrase)
    new_text = remove_phrase_from_text(selected_text, phrase, left_right)
    if not new_text:
        # phrase not found
        Key("c-v").execute()
        if left_right == "right":
            print("right")
            Key("left:%d" %len(selected_text)).execute()
        return

    pyperclip.copy(new_text)
    Key("c-v").execute()

    if left_right == "right":
        offset = len(new_text)
        Key("left:%d" %offset).execute()
    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)


def move_until_phrase(left_right, phrase):
    """ move until the close end of the phrase"""

    # temporarily store previous clipboard item
    temp_for_previous_clipboard_item = pyperclip.paste()
    
    if left_right == "left":
        Key("s-home, c-c/2").execute()
    if left_right == "right":
        Key("s-end, c-c/2").execute()
    Pause("50").execute()
    selected_text = pyperclip.paste()
    # the print statement below is for debugging purposes and should be removed eventually
    print("selected_text: {}".format(selected_text))
    
    phrase = str(phrase)
    match = get_start_end_position(selected_text, phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        Key("c-v").execute()
        if left_right == "right":
            offset = len(selected_text)
            Key("left:%d" %offset).execute()
        return
    left_index, right_index = get_start_end_position(selected_text, phrase, left_right)
    # I am using the method of pasting over the existing text rather than simply unselecting because of some weird behavior in texstudio
    # comments below indicate the other method
    Key("c-v").execute()
    if left_right == "left": 
        offset = len(selected_text) - right_index
        Key("left:%d" %offset).execute()
    if left_right == "right":
        offset = len(selected_text) - left_index
        Key("left:%d" %offset).execute()
    
    # Alternative method: simply unselect rather than pacing over the existing text. (a little faster) does not work texstudio
    # if left_right == "left":
    #     Key("right").execute() # unselect text
    #     offset = len(selected_text) - right_index
    #     Key("left:%d" %offset).execute()
    # if left_right == "right":
    #     Key("left").execute() # unselect text
    #     offset = left_index
    #     Key("right:%d" %offset).execute()
    
    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)

def select_until_phrase(left_right, phrase):
    """ the selection will include the phrase unless it is punctuation"""
    # temporarily store previous clipboard item
    temp_for_previous_clipboard_item = pyperclip.paste()

    
    if left_right == "left":
        Key("s-home, c-c/2").execute()
    if left_right == "right":
        Key("s-end, c-c/2").execute()
    Pause("50").execute()
    selected_text = pyperclip.paste()
    phrase = str(phrase)
    match = get_start_end_position(selected_text, phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        Key("c-v").execute()
        if left_right == "right":
            offset = len(selected_text)
            Key("left:%d" %offset).execute()
        return
    left_index, right_index = get_start_end_position(selected_text, phrase, left_right)
    
    # I am using the method of pasting over the existing text rather than simply unselecting because of some weird behavior in texstudio
    # comments below indicate the other method
    Key("c-v").execute()
    if left_right == "left":
        offset = len(selected_text) - left_index
        # make noninclusive if it's punctuation
        if phrase in punctuation_list:
            offset -= 1
        Key("s-left:%d" %offset).execute()
    if left_right == "right":
        len_selected_text = len(selected_text)
        offset = right_index
        # make noninclusive if it's punctuation
        if phrase in punctuation_list:
            offset -= 1
        Key("left:%d" %len_selected_text).execute()
        Key("s-right:%d" %offset).execute()
    
    # # alternative method: simply unselects text rather than pasting over the text. a little faster but does not work in tex studio
    # if left_right == "left":
    #     Key("right").execute() # unselect text
    #     offset = len(selected_text) - left_index
    #     # make noninclusive if it's punctuation 
    #     if phrase in punctuation_list:
    #         offset -= 1
    #     Key("s-left:%d" %offset).execute()
    # if left_right == "right":
    #     Key("left").execute() # unselect text
    #     Key("s-right:%d" %(right_index -1)).execute() # make noninclusive if it's punctuation 
   
    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)



def delete_until_phrase(text, phrase, left_right):
    match = get_start_end_position(text, phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        return
    if left_right == "left":
        return text[: right_index]
    if left_right == "right":
        return text[right_index :]

def copypaste_delete_until_phrase(left_right, phrase):
    phrase = str(phrase)
    # temporarily store previous clipboard item
    temp_for_previous_clipboard_item = pyperclip.paste()
    Pause("30").execute()

    if left_right == "left":
        Key("s-home, c-c/2").execute()
        
    if left_right == "right":
        Key("s-end, c-c/2").execute()
    Pause("50").execute()
    # get text from clipboard
    selected_text = pyperclip.paste()

    phrase = str(phrase)
    new_text = delete_until_phrase(selected_text, phrase, left_right)
    if not new_text:
        # phrase not found
        Key("c-v").execute()
        if left_right == "right":
            Key("left:%d" %len(selected_text)).execute()
        return

    # put modified text on the clipboard
    pyperclip.copy(new_text)
    Key("c-v").execute()

    if left_right == "right":
        offset = len(new_text)
        Key("left:%d" %offset).execute()
    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)


def get_direction_choice(name):
    global DIRECTION_STANDARD
    return Choice(name, DIRECTION_STANDARD)


def initialize_clipboard(nexus):
    if len(nexus.clip) == 0:
        nexus.clip = utilities.load_toml_file(
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
                settings.SETTINGS["paths"]["PYTHONW"],
                settings.SETTINGS["paths"]["LEGION_PATH"], "-t", tscan[0], "-m",
                str(monitor)
            ])  # , "-d", "500_500_500_500"
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
    else:
        utilities.availability_message(mode.title(), "PIL")

def _text_to_clipboard(keystroke, nnavi500, nexus):
    if nnavi500 == 1:
        Key(keystroke).execute()
    else:
        max_tries = 20
        cb = Clipboard(from_system=True)
        Key(keystroke).execute()
        key = str(nnavi500)
        for i in range(0, max_tries):
            failure = False
            try:
                # time for keypress to execute
                time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/1000.)
                nexus.clip[key] = unicode(Clipboard.get_system_text())
                utilities.save_toml_file(
                    nexus.clip, settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])
            except Exception:
                failure = True
                utilities.simple_log()
            if not failure:
                break
        cb.copy_to_system()

def stoosh_keep_clipboard(nnavi500, nexus):
    _text_to_clipboard("c-c", nnavi500, nexus)

def cut_keep_clipboard(nnavi500, nexus):
    _text_to_clipboard("c-x", nnavi500, nexus)

def drop_keep_clipboard(nnavi500, nexus, capitalization, spacing):
    # Maintain standard spark functionality for non-strings
    if capitalization == 0 and spacing == 0 and nnavi500 == 1:
        Key("c-v").execute()
        return
    # Get clipboard text
    if nnavi500 > 1:
        key = str(nnavi500)
        if key in nexus.clip:
            text = nexus.clip[key]
        else:
            dragonfly.get_engine().speak("slot empty")
            text = None
    else:
        text = Clipboard.get_system_text()
    # Format if necessary, and paste
    if text is not None:
        cb = Clipboard(from_system=True)
        if capitalization != 0 or spacing != 0:
            text = textformat.TextFormat.formatted_text(capitalization, spacing, text)
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


def erase_multi_clipboard(nexus):
    nexus.clip = {}
    utilities.save_toml_file(nexus.clip,
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


def left_click(nexus):
    kill_grids_and_wait(nexus)
    windll.user32.mouse_event(0x00000002, 0, 0, 0, 0)
    windll.user32.mouse_event(0x00000004, 0, 0, 0, 0)


def right_click(nexus):
    kill_grids_and_wait(nexus)
    windll.user32.mouse_event(0x00000008, 0, 0, 0, 0)
    windll.user32.mouse_event(0x00000010, 0, 0, 0, 0)


def middle_click(nexus):
    kill_grids_and_wait(nexus)
    windll.user32.mouse_event(0x00000020, 0, 0, 0, 0)
    windll.user32.mouse_event(0x00000040, 0, 0, 0, 0)


def left_down(nexus):
    kill_grids_and_wait(nexus)
    windll.user32.mouse_event(0x00000002, 0, 0, 0, 0)


def left_up(nexus):
    kill_grids_and_wait(nexus)
    windll.user32.mouse_event(0x00000004, 0, 0, 0, 0)


def wheel_scroll(direction, nnavi500):
    amount = 120
    if direction != "up":
        amount = amount* -1
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
            left_click(control.nexus())
        elif int(dokick) == 2:
            right_click(control.nexus())


def next_line(semi):
    semi = str(semi)
    Key("escape").execute()
    time.sleep(0.25)
    Key("end").execute()
    time.sleep(0.25)
    Text(semi).execute()
    Key("enter").execute()
