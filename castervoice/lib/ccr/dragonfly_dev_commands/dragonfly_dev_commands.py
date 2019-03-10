# this file contains commands for more quickly creating dragonfly commands.
# users may want to make this context-specific to they're text editors
# Dane Finley helped with this
# inspired by Lunis Orcutt

from dragonfly import (Grammar, MappingRule, Dictation, Function, Choice)
from dragonfly.actions.action_mouse import get_cursor_position
from castervoice.lib import control
from castervoice.lib.actions import Key, Text
from castervoice.lib.ccr.standard import SymbolSpecs
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


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

def type_mouse_current(mouse_button):
    # Type Mouse("[X, Y]"). The typed Mouse action will move the cursor to
    # back to where it was when the command was spoken.
    Text('Mouse("[%d, %d]")' % get_cursor_position()).execute()

def type_mouse_current_position_button(mouse_button = "left"):
    first_part_of_string = 'Mouse("[%d, %d], ' % get_cursor_position()
    second_part_of_string = '%s' % mouse_button
    full_string = first_part_of_string + second_part_of_string
    Text(full_string).execute()

class DragonflyDevCommandsRule(MergeRule):
    mapping = {
        # it doesn't like this pronunciation line i don't know why.
        # pronunciation = "dragonfly dev commands"



        # snippets
        "Key": R(Text('Key("")') + Key("left:2"),  
            rdescript="snippet for key action"),
        "dev Key": R(Text('Key(""),') + Key("left:3"),
            rdescript="snippet for key action"),
        "[dev] Text": R(Text('Text("")') + Key("left:2"),
            rdescript="snippet for text action"),
        "[dev] Pause": R(Text(' + Pause("")') + Key("left:2"),
            rdescript="snippet for pause action"),
        "[dev] Repeat": R(Text(" * Repeat(extra='n'),"), 
            rdescript="snippet for repeat"),
        "[dev] Choice": R(Text('Choice("", {') + Key("enter:2") + Text("}),") +
            Key("up:2, right"),
                rdescript="snippet for the choice extra"),
        "[dev] bring app": R(Text("BringApp(r)") + Key("left"), 
            rdescript="snippet for bring app"),
        "[dev] Mouse [<mouse_button>]": R(Function(type_mouse), 
            rdescript="snippet for mouse click command"),
        "[dev] Mouse current [position]": R(Function(type_mouse_current),
            rdescript="snippet for making a command for clicking at the current cursor position"),
            
        # snippets for emulating recognition.
        "[dev] Mimic [<text>]": R(Function(type_mimic), rdescript="snippet for mimic"),
        "[dev] playback [<text>]": R(Function(type_playback), 
            rdescript="snippet for playback"), # this 1 has been inconsistent. maybe because it's automatically putting in two of each parable character e.g. brackets
        "[dev] split dictation [<text>]": R(Function(type_split_dictation), 
            rdescript="puts quotes around each word and separated by commas"),
                
        
        
        # for creating commands in one fell swoop
        "command [<spec>] key": R(Text('"%(spec)s": Key(""),') + Key("left:3"),
            rdescript="automatically create key command with given spec"),
        "command [<spec>] text": R(Text('"%(spec)s": Text(""),') + Key("left:3"),
            rdescript="automatically create text command with given spec"),
        "command [<spec>] [bring] app": R(Text('"%(spec)s": BringApp(r),') + Key("left"),
            rdescript="automatically create bring app with given spec"),
        "command function [<spec>]": R(Text('"%(spec)s": Function()') + Key("left"),
            rdescript="automatically create function command with given spec"),
        "command [<spec>] mimic [<text>]": R(Text('"%(spec)s": ,') + Key("left") 
            + Function(type_mimic),
                rdescript="automatically create mimic command with given spec"),
        "command [<spec>] playback [<text>]": R(Text('"%(spec)s": ,') + Key("left") 
            + Function(type_playback), 
                rdescript="automatically create playback command with given spec"),
            # the command above has been inconsistent. maybe because it's 
            # automatically putting in two of each parable character e.g. brackets
            # might have to adjust it depending on the editor
        
        "command [<spec>] mouse [<mouse_button>]": R(Text('"%(spec)s": ,') + Key("left")
            + Function(type_mouse_current_position_button, extra={"mouse_button"}), 
                rdescript="automatically create a command to click at the current mouse position with given spec"),
            # for some reason the above command is not putting in the left click by default. perhaps someone can fix this
        
        # same as above but uses the caster standard format with the R and rdescript.
            # maybe somebody knows how to make it so that you can tab through the relevant places
        "commander [<spec>] key": R(Text('"%(spec)s": R(Key(""), rdescript=""')  + Key("right, comma") + Key("left:18"),
            rdescript="caster: automatically create key command with given spec"),
        "commander [<spec>] text": R(Text('"%(spec)s": R(Text(""), rdescript=""')  + Key("right, comma") + Key("left:18"),
            rdescript="caster: automatically create text command with given spec"),
        "commander [<spec>] [bring] app": R(Text('"%(spec)s": R(BringApp(r), rdescript=""')  + Key("right, comma") + Key("left:17"),
            rdescript="caster: automatically create bing app command with given spec"),
        "commander function [<spec>]": R(Text('"%(spec)s": R(Function(), rdescript=""')  + Key("right, comma") + Key("left:17"),
            rdescript="caster: automatically create function command with given spec"),
        "commander [<spec>] mimic [<text>]": R(Text('"%(spec)s": R(')
            + Function(type_mimic) + Text(', rdescript=""')  + Key("right, comma, left:3"),
            rdescript="caster: automatically create mimic command with given spec"),
        "commander [<spec>] mouse [<mouse_button>]": R(Text('"%(spec)s": R(') 
            + Function(type_mouse_current_position_button, extra={"mouse_button"})
                + Key("right") + Text(', rdescript=""') + Key("right, comma, left:3"),
            rdescript="caster: automatically create command to click at current mouse position with given spec"),
        
        # I couldn't get the one for playback to work
        # "commander [<spec>] playback [<text>]": Text('"%(spec)s": R(') # 
         #   + Function(type_playback) + Key("down:2") + Text(", rdescript=''") + Key("right, comma, left:3"),        
        



        # Miscellaneous.
        "plusser": Text(" + "),
        "eaker": Text(" = "),
        "kohler": Key("right") + Text(": "),
        "piping": Text(" | "),   
    }

    extras = [
        Dictation("text"),
        Dictation("dict"),
        Dictation("spec"),

        Choice("mouse_button", {
            "left": "left",
            "right": "right",
            "middle": "middle",
    }),
    ]
    defaults = {"spec": "", "dict": "", "text": "", "mouse_button": ""}


control.nexus().merger.add_global_rule(DragonflyDevCommandsRule())
