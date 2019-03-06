"""
    This module contains a grammar for writing Dragonfly rules.
"""

from dragonfly import (Grammar, MappingRule, Dictation, Key, Text, Function,
                       Choice)
from dragonfly.actions.action_mouse import get_cursor_position


def split_dictation(text):
    if text:
        words = ['"%s"' % word for word in text.format().split()]
        words = ', '.join(words)
    else:
        words = '""'

    return words


def type_split_dictation(text):
    Text(split_dictation(text)).execute()


def type_mimic(text):
    # Create an argument list for Mimic from text.
    words = split_dictation(text)

    # Define the action to execute. Move back only if no words were
    # specified.
    action = Text('Mimic(%s)' % words)
    if not text:
        action += Key("left:2")

    # Execute the action.
    action.execute()


def type_playback(text):
    # Create an argument list for Playback from text.
    words = split_dictation(text)

    # Define the action to execute.
    # This will press enter a few times. Indentation will depend on your
    # editor.
    enter = Key("enter")
    action = (Text('Playback([') + enter +
              Text('([%s], 0.0),' % words) + enter +
              Text('])') + Key("up, end"))

    # Move back only if no words were specified.
    if not text:
        action += Key("left:9")

    # Execute the action.
    action.execute()


def type_mouse(mouse_button):
    action = Text('Mouse("%s")' % mouse_button)

    # Move back only if no words were specified.
    if not mouse_button:
        action += Key("left:2")

    # Execute the action.
    action.execute()

def type_mouse_current():
    # Type Mouse("[X, Y]"). The typed Mouse action will move the cursor to
    # back to where it was when the command was spoken.
    Text('Mouse("[%d, %d]")' % get_cursor_position()).execute()


class DevRule(MappingRule):
    mapping = {
        mapping = {
        # mimic/playback-related mappings for emulating recognition.
        "[dev] Mimic [<text>]": Function(type_mimic),
        "[dev] [<text>]": Function(type_playback),
        "[dev] split dictation [<text>]": Function(type_split_dictation),
    
        # Mouse action mappings.
        "[dev] Mouse [<mouse_button>]": Function(type_mouse),
        "[dev] Mouse current [position]": Function(type_mouse_current),

        # Other action mappings.
        "[dev] Key": Text('Key("")') + Key("left:2"),
        "[dev] Text": Text('Text("")') + Key("left:2"),
        "[dev] Pause": Text(' + Pause("")') + Key("left:2"),
        "[dev] Repeat": Text(" * Repeat(extra='n'),"),
        "[dev] Choice": Text('Choice("", {') + Key("enter:2") + Text("}),") +
            Key("up:2, right"),
        "[dev] bring app": Text("BringApp(r)") + Key("left"),
        "[dev] Pause": (Text(' + Pause("")') + Key("left:2")),


        # Miscellaneous.
        "plusser": Text(" + "),
        "eaker": Text(" = "),
        "kohler": Key("right") + Text(": "),
        "piping": Text(" | "),
    }

    extras = [
        Dictation("text"),
        Choice("mouse_button", {
            "left": "left",
            "right": "right",
            "middle": "middle",
        }),
    ]

    defaults = {
        "text": "",
        "mouse_button": "",
    }


# Create a grammar instance and add DevRule to it.
grammar = Grammar("dragonfly_dev")
grammar.add_rule(DevRule())


# --------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.
grammar.load()


# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
