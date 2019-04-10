# -*- coding: utf-8 -*-
'''
master_text_nav shouldn't take strings as arguments - it should take ints, so it can be language-agnostic
'''

import time
from ctypes import windll
from subprocess import Popen
import pyperclip

import dragonfly
from dragonfly import Choice, monitors
from castervoice.asynch.mouse.legion import LegionScanner
from castervoice.lib import control, settings, utilities, textformat, context
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


def replace_phrase_with_phrase(text, replaced_phrase, replacement_phrase, left_right):
    if left_right == "left":
        left_index = text.rfind(replaced_phrase)
    if left_right == "right":
        left_index = text.find(replaced_phrase)
    # the if statement below is independent of whetherhim left_right equals left or right
    if left_index == -1:
        raise IndexError("{} not found").format(replaced_phrase)
    right_index = left_index + len(replaced_phrase)
    return text[: left_index] + replacement_phrase + text[right_index:] 
    

# comments show how to do it using pyperclip instead of caster's method
    # unlike pyperclip caster's method does not alter the clipboard 
def copypaste_replace_phrase_with_phrase(replaced_phrase, replacement_phrase, left_right):
    if left_right == "left":
        Key("s-home").execute()
        # Key("s-home, c-c/2").execute()
    if left_right == "right":
        Key("s-end").execute()
        # Key("s-end, c-c/2").execute()
    err, selected_text = context.read_selected_without_altering_clipboard()
        # selected_text = pyperclip.paste()
    if err != 0:
        # I'm not discriminating between err = 1 and err = 2
        print("failed to copy text")
        return

    text = str(selected_text).lower()
    replaced_phrase = str(replaced_phrase).lower()
    replacement_phrase = str(replacement_phrase).lower()
    new_text = replace_phrase_with_phrase(text, replaced_phrase, replacement_phrase, left_right)
    if not context.paste_string_without_altering_clipboard(new_text):
        print("failed to paste {}".format(new_text))
    # pyperclip.copy(output)
    # Key("c-v").execute()
    if left_right == "right":
        offset = len(output)
        Key("left:%d" %offset).execute()

def remove_phrase_from_text(text, phrase, left_right):
    if left_right == "left":
        left_index = text.rfind(phrase)
    if left_right == "right":
        left_index = text.find(phrase)
    # the if statement below is independent of whether left_right equals left or right
    if left_index == -1:
        raise IndexError("{} not found").format(phrase)
    right_index = left_index + len(phrase)
    # if the "phrase" is punctuation, just remove it, but otherwise remove an extra space adjacent to the phrase
    punctuation_list = [".", ",", "'", "[", "]", "<", ">", "{", "}", "?", "–", "-", ";"]
    if phrase in punctuation_list:
        return text[: left_index] + text[right_index:] 
    else:
        return text[: left_index - 1] + text[right_index:] 

# comments show how to do it using pyperclip instead of caster's method
    # unlike pyperclip caster's method does not alter the clipboard 
def copypaste_remove_phrase_from_text(phrase, left_right):
    if left_right == "left":
        Key("s-home").execute()
        # Key("s-home, c-c/2").execute()
    if left_right == "right":
        Key("s-end").execute()
        # Key("s-end, c-c/2").execute()
    err, selected_text = context.read_selected_without_altering_clipboard()
        # selected_text = pyperclip.paste()
    if err != 0:
        # I'm not discriminating between err = 1 and err = 2
        print("failed to copy text")
        return

    text = str(selected_text).lower()
        # don't distinguish between uppercase and lowercase
    phrase = str(phrase).lower()
    new_text = remove_phrase_from_text(text, phrase, left_right)
    context.paste_string_without_altering_clipboard(output)
    if not context.paste_string_without_altering_clipboard(new_text):
                print("failed to paste {}".format(new_text))

    # pyperclip.copy(output)
    # Key("c-v").execute()
    if left_right == "right":
        offset = len(output)
        Key("left:%d" %offset).execute()


# comments show how to do it using pyperclip instead of caster's method
    # unlike pyperclip caster's method does not alter the clipboard 
def move_until_character_sequence(left_right, character_sequence):
    if left_right == "left":
        Key("s-home").execute()
        # Key("s-home, c-c/2").execute()
    if left_right == "right":
        Key("s-end").execute()
        # Key("s-end, c-c/2").execute()
    err, selected_text = context.read_selected_without_altering_clipboard()
        # selected_text = pyperclip.paste()
    if err != 0:
        # I'm not discriminating between err = 1 and err = 2
        print("failed to copy text")
        return
    
    text = str(selected_text).lower()
        # don't distinguish between upper and lowercase
    character_sequence = str(character_sequence).lower()
    if left_right == "left":
        Key("right").execute() # unselect text
        if text.rfind(character_sequence) == -1:
            raise IndexError("{} not found".format(character_sequence))
        else:
            character_sequence_start_position = text.rfind(character_sequence) + len(character_sequence)
            offset = len(text) - character_sequence_start_position 
            Key("left:%d" %offset).execute()
    if left_right == "right":
        Key("left").execute() # unselect text
        if text.find(character_sequence) == -1:
            raise IndexError("{} not found".format(character_sequence))
        else:
            character_sequence_start_position = text.find(character_sequence) 
            offset = character_sequence_start_position 
            Key("right:%d" %offset).execute()
        


def delete_until_character_sequence(text, character_sequence, left_right):
    if left_right == "left":
        if text.rfind(character_sequence) == -1:
            raise IndexError("{} not found".format(character_sequence))
        else:
            character_sequence_start_position = text.rfind(character_sequence)
            # if character sequence goes to the end of the line
            if character_sequence_start_position == 0:
                Key("del").execute()
            else:
                new_text_start_position = character_sequence_start_position 
                new_text = text[:new_text_start_position]
                return new_text
    if left_right == "right":
        if text.find(character_sequence) == -1:
            raise IndexError("{} not found".format(character_sequence))
        else:
            character_sequence_start_position = text.find(character_sequence)
            # if character sequence goes to the end of the line
            if character_sequence_start_position + len(character_sequence) == len(text):
                Key("del").execute()
            else:
                new_text_start_position = character_sequence_start_position + len(character_sequence)
                new_text = text[new_text_start_position:]
                return new_text

      
# comments show how to do it using pyperclip instead of caster's method 
    # unlike pyperclip caster's method does not alter the clipboard 
def copypaste_delete_until_character_sequence(left_right, character_sequence):
        if left_right == "left":
            Key("s-home").execute()
            # Key("s-home, c-c/2").execute()
        if left_right == "right":
            Key("s-end").execute()
            # Key("s-end, c-c/2").execute()
        err, selected_text = context.read_selected_without_altering_clipboard()
        # selected_text = pyperclip.paste()
        if err != 0:
            # I'm not discriminating between err = 1 and err = 2
            print("failed to copy text")
            return
    
        text = str(selected_text).lower()      
            # don't distinguish between upper and lowercase
        character_sequence = str(character_sequence).lower()
        text = text.lower()
        new_text = delete_until_character_sequence(text, character_sequence, left_right)
        offset = len(new_text)
        if not context.paste_string_without_altering_clipboard(new_text):
            print("failed to paste {}".format(new_text))
        # pyperclip.copy(new_text)
        # Key("c-v/2").execute()
        # move cursor back into the right spot. only necessary for left_right = "right"
        if left_right == "right":
            Key("left:%d" %offset).execute()



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


def stoosh_keep_clipboard(nnavi500, nexus):
    if nnavi500 == 1:
        Key("c-c").execute()
    else:
        max_tries = 20
        cb = Clipboard(from_system=True)
        Key("c-c").execute()
        key = str(nnavi500)
        for i in range(0, max_tries):
            failure = False
            try:
                # time for keypress to execute
                time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/1000.)
                nexus.clip[key] = Clipboard.get_system_text()
                utilities.save_toml_file(
                    nexus.clip, settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])
            except Exception:
                failure = True
                utilities.simple_log()
            if not failure:
                break
        cb.copy_to_system()


def cut_keep_clipboard(nnavi500, nexus):
    if nnavi500 == 1:
        Key("c-x").execute()
    else:
        max_tries = 20
        cb = Clipboard(from_system=True)
        Key("c-x").execute()
        key = str(nnavi500)
        for i in range(0, max_tries):
            failure = False
            try:
                # time for keypress to execute
                time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/1000.)
                nexus.clip[key] = Clipboard.get_system_text()
                utilities.save_toml_file(
                    nexus.clip, settings.SETTINGS["paths"]["SAVED_CLIPBOARD_PATH"])
            except Exception:
                failure = True
                utilities.simple_log()
            if not failure:
                break
        cb.copy_to_system()


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
    time.sleep(0.01)
    Key("end").execute()
    time.sleep(0.01)
    Text(semi).execute()
    Key("enter").execute()
