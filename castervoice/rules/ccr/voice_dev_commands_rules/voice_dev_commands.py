'''
Alex Boche 2019
this file contains commands for more quickly creating dragonfly commands.
users may want to make this context-specific to their text editors
'''
import copy

from dragonfly import Pause, Choice, Dictation, Function
from dragonfly.actions.action_mouse import get_cursor_position

from castervoice.lib.actions import Text, Key
from castervoice.rules.core.keyboard_rules.keyboard import Keyboard
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R

new_modifier_choice_object = copy.deepcopy(Keyboard.modifier_choice_object)

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
    enter = Key("enter") + Pause("10")
    action = (Text('Playback([') + enter + Text('([%s], 0.0),' % words) + enter +
              Key("up, end"))

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
    # Type Mouse("[X, Y]"). the typed Mouse action will move the cursor to
    # back to where it was when the command was spoken.
    Text('Mouse("[%d, %d]")' % get_cursor_position()).execute()


def type_mouse_current_position_button(mouse_button="left"):
    first_part_of_string = 'Mouse("[%d, %d], ' % get_cursor_position()
    second_part_of_string = '%s' % mouse_button
    full_string = first_part_of_string + second_part_of_string
    Text(full_string).execute()


class VoiceDevCommands(MergeRule):
    pronunciation = "voice dev commands"

    mapping = {

        # Dragonfly Snippets
        # this first command is probably the most useful one
        "dev key [<modifier>] <button_dictionary_1>": 
            R(Text('Key("%(modifier)s%(button_dictionary_1)s")'),
            rdescript="DragonflyDev: Snippet for creating a full Key action"),
        "dev key":
            R(Text('Key("")') + Key("left:2"), rdescript="DragonflyDev: Snippet for Key Action"),
        "dev text":
            R(Text('Text("")') + Key("left:2"), rdescript="DragonflyDev: Snippet for Text Action"),
        "dev pause":
            R(Text('Pause("")') + Key("left:2"), rdescript="DragonflyDev: Snippet for Pause Action"),
        "dev function":
            R(Text("Function()") + Key("left")),
        "dev repeat":
            R(Text(" * Repeat(extra='n')"), rdescript="DragonflyDev: Snippet for Repeat"),
        "dev choice":
            R(Text('Choice("", {') + Pause("10") + Key("enter, up, right:4"),
              rdescript="DragonflyDev: Snippet for the Choice Extra"),
        "dev mouse [<mouse_button>]":
            R(Function(type_mouse), rdescript="DragonflyDev: Snippet for Mouse Click Command"),
        "dev mouse current [position]":
            R(Function(type_mouse_current),
              rdescript="DragonflyDev: Snippet for Making a Command for Clicking at the Current Cursor Position"),
        "dev execute": R(Key("end")+Text(".execute()"),
            rdescript="call 'execute' method at end of line"),

 # Caster Snippets
        "dev bring app":
            R(Text("BringApp()") + Key("left"), rdescript="CasterDev: Snippet for Bring App"),
        "dev descript":
            R(Text(' rdescript="MyGrammar: "') + Key("left"), rdescript="CasterDev: Add the rdescript"),

 # Snippets for emulating Dragonfly or Caster recognition.
        "dev mimic [<text>]":
            R(Function(type_mimic),
              rdescript="DragonflyDev: Snippet for Mimic"),
        "dev playback [<text>]": # This command has been inconsistent.
            # maybe because it's automatically putting in two of each parable character e.g. brackets
            R(Function(type_playback),
              rdescript="DragonflyDev: Snippet for Playback"),
        "dev split dictation [<text>]":
            R(Function(type_split_dictation),
              rdescript="DragonflyDev: Puts Quotes Around Each Word and Separated by Commas"),

 # Dragonfly Development: Standard dragonfly commands
        "command [<spec>] key":
            R(Text('"%(spec)s": Key(""),') + Key("left:3"),
              rdescript="DragonflyDev: Automatically Create Key Command with Given Spec"),
        "command [<spec>] key repeat":
            R(Text('"%(spec)s [<n>]": Key("") * Repeat(extra="n"),') + Key("left:23"),
              rdescript="DragonflyDev: Automatically Create Repeatable Key Command with Given Spec"),
        "command [<spec>] text":
            R(Text('"%(spec)s": Text(""),') + Key("left:3"),
              rdescript="DragonflyDev: Automatically Create Text Command with Given Spec"),
        "command [<spec>] [bring] app":
            R(Text('"%(spec)s": BringApp(),') + Key("left"),
              rdescript="DragonflyDev: Automatically Create Bring App with Given Spec"),
        "command [<spec>] function":
            R(Text('"%(spec)s": Function()') + Key("left"),
              rdescript="DragonflyDev: Automatically Create Function Command with Given Spec"),
        "command [<spec>] mimic [<text>]":
            R(Text('"%(spec)s": ,') + Key("left") + Function(type_mimic),
              rdescript="DragonflyDev: Automatically Create Mimic Command with Given Spec"),
        "command [<spec>] playback [<text>]":# This command has been inconsistent.
                                             # maybe because it's automatically putting in two of each parable character e.g. bracket
                                             # might have to adjust it depending on the editor
            R(Text('"%(spec)s": ,') + Key("left") + Function(type_playback),
              rdescript="DragonflyDev: Automatically Create Playback Command with Given Spec"),
        "command [<spec>] mouse [<mouse_button>]": # for some reason the above command is not putting in the left click by default.
                                                   # perhaps someone can fix this
            R(Text('"%(spec)s": ,') + Key("left") + Function(
                type_mouse_current_position_button, extra={"mouse_button"}),
                rdescript="DragonflyDev: Automatically Create a Command to Click at the Current Mouse Position with Given Spec"),


 # Caster Development: commands uses the caster standard format with the R and rdescript.
        # Use Editors 'find and replace' to edit 'MyGrammar' to application or grammar name.
        # maybe somebody knows how to make it so that you can tab through the relevant places
        "commander [<spec>] key":
            R(Text('"%(spec)s": R(Key(""), rdescript="MyGrammar: "') + Key("right, comma") +
              Key("left:18"),
              rdescript="CasterDev: Automatically Create Key Command with Given Spec"),
        "commander [<spec>] key repeat":
            R(Text('"%(spec)s [<n>]": R(Key(""), rdescript="MyGrammar: "') + Key("right") +
              Text(" * Repeat(extra='n'),") + Key("left:38"),
              rdescript="CasterDev: Automatically Create Repeatable Key Command with Given Spec"),
        "commander [<spec>] text":
            R(Text('"%(spec)s": R(Text(""), rdescript="MyGrammar: "') + Key("right, comma") +
              Key("left:18"),
              rdescript="CasterDev: Automatically Create Text Command with Given Spec"),
        "commander [<spec>] [bring] app":
            R(Text('"%(spec)s": R(BringApp(), rdescript="MyGrammar: "') + Key("right, comma") +
              Key("left:17"),
              rdescript="CasterDev: Automatically Create Bing App Command with Given Spec"),
        "commander [<spec>] function":
            R(Text('"%(spec)s": R(Function(), rdescript="MyGrammar: "') + Key("right, comma") +
              Key("left:17"),
              rdescript="CasterDev: Automatically Create Function Command with Given Spec"),
        "commander [<spec>] mimic [<text>]":
            R(Text('"%(spec)s": R(') + Function(type_mimic) + Text(', rdescript="MyGrammar: "') +
              Key("right, comma, left:3"),
              rdescript="CasterDev: Automatically Create Mimic Command with Given Spec"),
        "commander [<spec>] mouse [<mouse_button>]":
            R(Text('"%(spec)s": R(') + Function(type_mouse_current_position_button,
              extra={"mouse_button"}) + Key("right") + Text(', rdescript=""') + Key("right, comma, left:3"),
              rdescript="CasterDev: Automatically Create Command to Click at Current Mouse Position with Given Spec"),
        # I couldn't get "commander [<spec>] playback [<text>]" to work
            # "commander [<spec>] playback [<text>]": Text('"%(spec)s": R(')
            #   + Function(type_playback) + Key("down:2") + Text(", rdescript=''") + Key("right, comma, left:3"),
    }

    extras = [
        new_modifier_choice_object,
        Choice("button_dictionary_1", Keyboard.button_dictionary_1),
        Dictation("text"),
        Dictation("dict"),
        Dictation("spec"),
        Choice("mouse_button", {
            "left": "left",
            "right": "right",
            "middle": "middle",
        }),
        Choice("left_right", {
            "left": "left",
            "right": "right",
        }),
        Choice("up_down", {
            "up": "up",
            "down": "down",
        }),
        IntegerRefST("distance_1", 1, 500),
        IntegerRefST("distance_2", 1, 500),
    ]
    defaults = {"spec": "", "dict": "", "text": "", "mouse_button": ""}


def get_rule():
    return VoiceDevCommands, RuleDetails(ccrtype=CCRType.GLOBAL)
