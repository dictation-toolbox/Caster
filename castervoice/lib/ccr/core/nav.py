'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import Repeat, Function, Dictation, Choice, MappingRule

from castervoice.lib import context, navigation, alphanumeric, textformat, text_utils
from castervoice.lib import control, utilities
from castervoice.lib.actions import Key, Mouse
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.actions import AsynchronousAction, ContextSeeker
from castervoice.lib.dfplus.state.actions2 import UntilCancelled
from castervoice.lib.dfplus.state.short import L, S, R
from dragonfly.actions.action_mimic import Mimic
from castervoice.lib.ccr.standard import SymbolSpecs

from inspect           import getargspec
# from action_base      import ActionBase, ActionError
from dragonfly.actions.action_base import ActionBase, ActionError

# tweaked version of function action for dealing with the case when the argument names
# from the extras don't match the argument names in the function signature
class RemapArgsFunction(ActionBase):
    # def __init__(self, function, remap_data=None, **defaults):
    def __init__(self, function, defaults=None, remap_data=None):
    
        ActionBase.__init__(self)
        self._function = function
        self._defaults = defaults or {}
        self._remap_data = remap_data or {}
        self._str = function.__name__

        # TODO Use inspect.signature instead; getargspec is deprecated.
        (args, varargs, varkw, defaults) = getargspec(self._function)
        if varkw:  self._filter_keywords = False
        else:      self._filter_keywords = True
        self._valid_keywords = set(args)

    def _execute(self, data=None):
        arguments = dict(self._defaults)
        if isinstance(data, dict):
            arguments.update(data)

        # Remap specified names.
        if arguments and self._remap_data:
            for old_name, new_name in self._remap_data.items():
                if old_name in data:
                    arguments[new_name] = arguments.pop(old_name)

        if self._filter_keywords:
            invalid_keywords = set(arguments.keys()) - self._valid_keywords
            for key in invalid_keywords:
                del arguments[key]

        try:
            self._function(**arguments)
        except Exception as e:
            self._log.exception("Exception from function %s:"
                                % self._function.__name__)
            raise ActionError("%s: %s" % (self, e))


_NEXUS = control.nexus()


class NavigationNon(MappingRule):
    mapping = {
        "<direction> <time_in_seconds>":
            AsynchronousAction(
                [L(S(["cancel"], Key("%(direction)s"), consume=False))],
                repetitions=1000,
                blocking=False),
        "erase multi clipboard":
            R(Function(navigation.erase_multi_clipboard, nexus=_NEXUS),
              rdescript="Core: Erase Multi Clipboard"),
        "find":
            R(Key("c-f"), rdescript="Core: Find"),
        "find next [<n>]":
            R(Key("f3"), rdescript="Core: Find Next")*Repeat(extra="n"),
        "find prior [<n>]":
            R(Key("s-f3"), rdescript="Core: Find Prior")*Repeat(extra="n"),
        "find everywhere":
            R(Key("cs-f"), rdescript="Core: Find Everywhere"),
        "replace":
            R(Key("c-h"), rdescript="Core: Replace"),
        "(F to | F2)":
            R(Key("f2"), rdescript="Core: Key: F2"),
        "(F six | F6)":
            R(Key("f6"), rdescript="Core: Key: F6"),
        "(F nine | F9)":
            R(Key("f9"), rdescript="Core: Key: F9"),
        "[show] context menu":
            R(Key("s-f10"), rdescript="Core: Context Menu"),
        "shift right click":
            R(Key("shift:down") + Mouse("right") + Key("shift:up"),
              rdescript="Core-Mouse: Shift + Right Click"),
        "curse <direction> [<direction2>] [<nnavi500>] [<dokick>]":
            R(Function(navigation.curse), rdescript="Core: Curse"),
        "scree <direction> [<nnavi500>]":
            R(Function(navigation.wheel_scroll), rdescript="Core: Wheel Scroll"),
        "colic":
            R(Key("control:down") + Mouse("left") + Key("control:up"),
              rdescript="Core-Mouse: Ctrl + Left Click"),
        "garb [<nnavi500>]":
            R(Mouse("left") + Mouse("left") + Function(
                navigation.stoosh_keep_clipboard,
                nexus=_NEXUS),
              rdescript="Core: Highlight @ Mouse + Copy"),
        "drop [<nnavi500>]":
            R(Mouse("left") + Mouse("left") + Function(
                navigation.drop_keep_clipboard,
                nexus=_NEXUS,
                capitalization=0,
                spacing=0),
              rdescript="Core: Highlight @ Mouse + Paste"),
        "sure stoosh":
            R(Key("c-c"), rdescript="Core: Simple Copy"),
        "sure cut":
            R(Key("c-x"), rdescript="Core: Simple Cut"),
        "sure spark":
            R(Key("c-v"), rdescript="Core: Simple Paste"),
        "refresh":
            R(Key("c-r"), rdescript="Core: Refresh"),
        "maxiwin":
            R(Key("w-up"), rdescript="Core: Maximize Window"),
        "move window":
            R(Key("a-space, r, a-space, m"), rdescript="Core: Move Window"),
        "window (left | lease) [<n>]":
            R(Key("w-left"), rdescript="Core: Window Left")*Repeat(extra="n"),
        "window (right | ross) [<n>]":
            R(Key("w-right"), rdescript="Core: Window Right")*Repeat(extra="n"),
        "monitor (left | lease) [<n>]":
            R(Key("sw-left"), rdescript="Core: Monitor Left")*Repeat(extra="n"),
        "monitor (right | ross) [<n>]":
            R(Key("sw-right"), rdescript="Core: Monitor Right")*Repeat(extra="n"),
        "(next | prior) window":
            R(Key("ca-tab, enter"), rdescript="Core: Next Window"),
        "switch (window | windows)":
            R(Key("ca-tab"), rdescript="Core: Switch Window")*Repeat(extra="n"),
        "next tab [<n>]":
            R(Key("c-pgdown"), rdescript="Core: Next Tab")*Repeat(extra="n"),
        "prior tab [<n>]":
            R(Key("c-pgup"), rdescript="Core: Previous Tab")*Repeat(extra="n"),
        "close tab [<n>]":
            R(Key("c-w/20"), rdescript="Core: Close Tab")*Repeat(extra="n"),
        "elite translation <text>":
            R(Function(alphanumeric.elite_text), rdescript="Core: 1337 Text"),

        # Workspace management
        "show work [spaces]":
            R(Key("w-tab"), rdescript="Core: Show Workspaces"),
        "(create | new) work [space]":
            R(Key("wc-d"), rdescript="Core: Create Workspace"),
        "close work [space]":
            R(Key("wc-f4"), rdescript="Core: Close Workspace"),
        "close all work [spaces]":
            R(Function(utilities.close_all_workspaces),
                rdescript="Core: Close All Work Spaces"),
        "next work [space] [<n>]":
            R(Key("wc-right"), rdescript="Core: Next Workspace")*Repeat(extra="n"),
        "(previous | prior) work [space] [<n>]":
            R(Key("wc-left"), rdescript="Core: Prior Workspace")*Repeat(extra="n"),

        "go work [space] <n>":
            R(Function(lambda n: utilities.go_to_desktop_number(n)),
                rdescript="Core: Go to Workspace N"),
        "send work [space] <n>":
            R(Function(lambda n: utilities.move_current_window_to_desktop(n)),
                rdescript="Core: Send Current Window to Workspace N"),
        "move work [space] <n>":
            R(Function(lambda n: utilities.move_current_window_to_desktop(n, True)),
                rdescript="Core: Move Current Window to Workspace N"),
    }

    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 50),
        IntegerRefST("nnavi500", 1, 500),
        Choice("time_in_seconds", {
            "super slow": 5,
            "slow": 2,
            "normal": 0.6,
            "fast": 0.1,
            "superfast": 0.05
        }),
        navigation.get_direction_choice("direction"),
        navigation.get_direction_choice("direction2"),
        navigation.TARGET_CHOICE,
        Choice("dokick", {
            "kick": 1,
            "psychic": 2
        }),
        Choice("wm", {
            "ex": 1,
            "tie": 2
        }),
    ]
    defaults = {
        "n": 1,
        "mim": "",
        "nnavi500": 1,
        "direction2": "",
        "dokick": 0,
        "text": "",
        "wm": 2
    }


def move_until_character_sequence(left_right, character_sequence):
    if left_right == "left":
        Key("s-home, c-c/2").execute()
        Key("right").execute()
    if left_right == "right":
        Key("s-end, c-c/2").execute()
        Key("left").execute()

    character_sequence = str(character_sequence).lower()
    text = pyperclip.paste()    
    # don't distinguish between upper and lowercase
    text = text.lower()
    if left_right == "left":
        if text.rfind(character_sequence) == -1:
            raise IndexError("character_sequence not found")
        else:
            character_sequence_start_position = text.rfind(character_sequence) + len(character_sequence)
            offset = len(text) - character_sequence_start_position 
            Key("left:%d" %offset).execute()
    if left_right == "right":
        if text.find(character_sequence) == -1:
            raise IndexError("character_sequence not found")
        else:
            character_sequence_start_position = text.find(character_sequence) 
            offset = character_sequence_start_position 
            Key("right:%d" %offset).execute()
        


def copypaste_delete_until_character_sequence(left_right, character_sequence):
        if left_right == "left":
            Key("s-home, c-c/2").execute()
        if left_right == "right":
            Key("s-end, c-c/2").execute()
        character_sequence = str(character_sequence).lower()
        text = pyperclip.paste()
        # don't distinguish between upper and lowercase
        text = text.lower()
        new_text = delete_until_character_sequence(text, character_sequence, left_right)
        offset = len(new_text)
        pyperclip.copy(new_text)
        Key("c-v/2").execute()
        # move cursor back into the right spot. only necessary for left_right = "right"
        if left_right == "right":
            Key("left:%d" %offset).execute()
        

def delete_until_character_sequence(text, character_sequence, left_right):
    if left_right == "left":
        if text.rfind(character_sequence) == -1:
            raise IndexError("character_sequence not found")
        else:
            character_sequence_start_position = text.rfind(character_sequence)
            new_text_start_position = character_sequence_start_position 
            new_text = text[:new_text_start_position]
            return new_text
    if left_right == "right":
        if text.find(character_sequence) == -1:
            raise IndexError("character_sequence not found")
        else:
            character_sequence_start_position = text.find(character_sequence)
            new_text_start_position = character_sequence_start_position + len(character_sequence)
            new_text = text[new_text_start_position:]
            return new_text

class Navigation(MergeRule):
    non = NavigationNon
    pronunciation = CCRMerger.CORE[1]

    mapping = {
    # "periodic" repeats whatever comes next at 1-second intervals until "cancel" is spoken or 100 tries occur
        "periodic":
            ContextSeeker(forward=[L(S(["cancel"], lambda: None),
            S(["*"], lambda fnparams: UntilCancelled(Mimic(*filter(lambda s: s != "periodic", fnparams)), 1).execute(),
            use_spoken=True))]),
    # VoiceCoder-inspired -- these should be done at the IDE level
        "fill <target>":
            R(Key("escape, escape, end"), show=False) +
            AsynchronousAction([L(S(["cancel"], Function(context.fill_within_line, nexus=_NEXUS)))],
            time_in_seconds=0.2, repetitions=50, rdescript="Core: Fill" ),
        "jump in":
            AsynchronousAction([L(S(["cancel"], context.nav, ["right", "(~[~{~<"]))],
            time_in_seconds=0.1, repetitions=50, rdescript="Core: Jump: In"),
        "jump out":
            AsynchronousAction([L(S(["cancel"], context.nav, ["right", ")~]~}~>"]))],
            time_in_seconds=0.1, repetitions=50, rdescript="Core: Jump: Out"),
        "jump back":
            AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))],
            time_in_seconds=0.1, repetitions=50, rdescript="Core: Jump: Back"),
        "jump back in":
            AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))],
            finisher=Key("right"), time_in_seconds=0.1, repetitions=50, rdescript="Core: Jump: Back In" ),

    # keyboard shortcuts
        'save':
            R(Key("c-s"), rspec="save", rdescript="Core: Save"),
        'shock [<nnavi50>]':
            R(Key("enter"), rspec="shock", rdescript="Core: Enter")* Repeat(extra="nnavi50"),
        'shin shock [<nnavi50>]':
            R(Key("s-enter"), rspec="shift shock", rdescript="Core: Shift Enter")* Repeat(extra="nnavi50"),

        "(<mtn_dir> | <mtn_mode> [<mtn_dir>]) [(<nnavi500> | <extreme>)]":
            R(Function(text_utils.master_text_nav), rdescript="Core: Keyboard Text Navigation"),

        "shift click":
            R(Key("shift:down") + Mouse("left") + Key("shift:up"),
              rdescript="Core-Mouse: Shift Click"),

        "stoosh [<nnavi500>]":
            R(Function(navigation.stoosh_keep_clipboard, nexus=_NEXUS), rspec="stoosh", rdescript="Core: Copy"),
        "cut [<nnavi500>]":
            R(Function(navigation.cut_keep_clipboard, nexus=_NEXUS), rspec="cut", rdescript="Core: Cut"),
        "spark [<nnavi500>] [(<capitalization> <spacing> | <capitalization> | <spacing>) (bow|bowel)]":
            R(Function(navigation.drop_keep_clipboard, nexus=_NEXUS), rspec="spark", rdescript="Core: Paste"),

        "splat [<splatdir>] [<nnavi10>]":
            R(Key("c-%(splatdir)s"), rspec="splat", rdescript="Core: Splat") * Repeat(extra="nnavi10"),
        "deli [<nnavi50>]":
            R(Key("del/5"), rspec="deli", rdescript="Core: Delete") * Repeat(extra="nnavi50"),
        "shin deli [<nnavi50>]":
            R(Key("s-del/5"), rspec="shift deli", rdescript="Core:hard Delete") * Repeat(extra="nnavi50"),
        "shin tabby [<nnavi50>]":
            R(Key("s-tab/5"), rspec="shift tabby", rdescript="Core: shift tab") * Repeat(extra="nnavi50"),
        "clear [<nnavi50>]":
            R(Key("backspace/5:%(nnavi50)d"), rspec="clear", rdescript="Core: Backspace"),
        SymbolSpecs.CANCEL:
            R(Key("escape"), rspec="cancel", rdescript="Core: Cancel Action"),


        "shackle":
            R(Key("home/5, s-end"), rspec="shackle", rdescript="Core: Select Line"),
        "(tell | tau) <semi>":
            R(Function(navigation.next_line), rspec="tell dock", rdescript="Core: Complete Line"),
        "duple [<nnavi50>]":
            R(Function(navigation.duple_keep_clipboard), rspec="duple", rdescript="Core: Duplicate Line"),
        "Kraken":
            R(Key("c-space"), rspec="Kraken", rdescript="Core: Control Space"),
        
        
        "ecker":
            R(Key("escape"), rspec= "ecker",  rdescript="Core: escape"),
        "smack [<n>]":
            R(Key("cs-left, del"), rspec="smack",  rdescript="Core: delete words to left") * Repeat(extra='n'),
        "tack [<n>]":
            R(Key("cs-right, del"), rspec="tack",  rdescript="Core: delete words to right") * Repeat(extra='n'),
        "smack wally":
            R(Key("s-left, del"), rspec="smack wally",  rdescript="Core: delete all words to left"),
        "tack wally":
            R(Key("s-right, del"), rspec="tack wally",  rdescript="Core: delete all words to right"),
        "dropdown list": 
            R(Key("a-down"), rspec="dropdown list", rdescript="Core: drop down a drop down list"),

    # moved from non- CCR rule
        "undo [<n>]":
            R(Key("c-z"), rdescript="Core: Undo")*Repeat(extra="n"),
        "redo [<n>]":
            R(Key("c-y"), rdescript="Core: Redo")*Repeat(extra="n"),
        "squat":
            R(Function(navigation.left_down, nexus=_NEXUS), rdescript="Core-Mouse: Left Down"),
        "bench":
            R(Function(navigation.left_up, nexus=_NEXUS), rdescript="Core-Mouse: Left Up"),
        "kick":
            R(Function(navigation.left_click, nexus=_NEXUS),
              rdescript="Core-Mouse: Left Click"),
        "kick mid":
            R(Function(navigation.middle_click, nexus=_NEXUS),
              rdescript="Core-Mouse: Middle Click"),
        "psychic":
            R(Function(navigation.right_click, nexus=_NEXUS),
              rdescript="Core-Mouse: Right Click"),
        "(kick double|double kick)":
            R(Function(navigation.left_click, nexus=_NEXUS)*Repeat(2),
              rdescript="Core-Mouse: Double Click"),
        
    # text formatting
        "set [<big>] format (<capitalization> <spacing> | <capitalization> | <spacing>) (bow|bowel)":
            R(Function(textformat.set_text_format), rdescript="Core: Set Text Format"),
        "clear castervoice [<big>] formatting":
            R(Function(textformat.clear_text_format), rdescript="Core: Clear Caster Formatting"),
        "peek [<big>] format":
            R(Function(textformat.peek_text_format), rdescript="Core: Peek Format"),
        "(<capitalization> <spacing> | <capitalization> | <spacing>) (bow|bowel) <textnv> [brunt]":
            R(Function(textformat.master_format_text), rdescript="Core: Text Format"),
        "[<big>] format <textnv>":
            R(Function(textformat.prior_text_format), rdescript="Core: Last Text Format"),
        "<word_limit> [<big>] format <textnv>":
            R(Function(textformat.partial_format_text), rdescript="Core: Partial Text Format"),

        "hug <enclosure>":
            R(Function(text_utils.enclose_selected), rdescript="Core: Enclose text "),
        "dredge":
            R(Key("a-tab"), rdescript="Core: Alt-Tab"),
        

        # "delete until" commands
        "kill ross <right_character>": 
            RemapArgsFunction(copypaste_delete_until_character_sequence, dict(left_right="right"), dict(right_character='character_sequence')),
        "kill ross <dictation>": 
            RemapArgsFunction(copypaste_delete_until_character_sequence, dict(left_right="right"), dict(dictation='character_sequence')),
        "kill leese <left_character>": 
            RemapArgsFunction(copypaste_delete_until_character_sequence, dict(left_right="left"), dict(left_character="character_sequence")),
        "kill leese <dictation>": 
            RemapArgsFunction(copypaste_delete_until_character_sequence, dict(left_right="left"), dict(dictation='character_sequence')),
            
        # "move until" commands
        "leeser <left_character>": RemapArgsFunction(move_until_character_sequence, dict(left_right = "left"), dict(left_character="character_sequence")),
        "rosser <right_character>": RemapArgsFunction(move_until_character_sequence, dict(left_right = "right"), dict(right_character="character_sequence")),
        "leeser <dictation>": RemapArgsFunction(move_until_character_sequence, dict(left_right = "left"), dict(dictation="character_sequence")),
        "rosser <dictation>": RemapArgsFunction(move_until_character_sequence, dict(left_right = "right"), dict(dictation="character_sequence")),
        


    }

    extras = [
        IntegerRefST("n", 1, 11),
        IntegerRefST("nnavi10", 1, 11),
        IntegerRefST("nnavi50", 1, 50),
        IntegerRefST("nnavi500", 1, 500),
        Dictation("textnv"),
        Dictation("dictation"),
        Choice(
            "enclosure", {
                "prekris": "(~)",
                "angle": "<~>",
                "curly": "{~}",
                "brax": "[~]",
                "thin quotes": "'~'",
                'quotes': '"~"',
            }),
        Choice("capitalization", {
            "yell": 1,
            "tie": 2,
            "Gerrish": 3,
            "sing": 4,
            "laws": 5
        }),
        Choice(
            "spacing", {
                "gum": 1,
                "gun": 1,
                "spine": 2,
                "snake": 3,
                "pebble": 4,
                "incline": 5,
                "dissent": 6,
                "descent": 6
            }),
        Choice("semi", {
            "dock": ";",
            "doc": ";",
            "sink": ""
        }),
        Choice("word_limit", {
            "single": 1,
            "double": 2,
            "triple": 3,
            "Quadra": 4
        }),
        navigation.TARGET_CHOICE,
        navigation.get_direction_choice("mtn_dir"),
        Choice("mtn_mode", {
            "shin": "s",
            "queue": "cs",
            "fly": "c",
        }),
        Choice("extreme", {
            "Wally": "way",
        }),
        Choice("big", {
            "big": True,
        }),
        Choice("splatdir", {
            "lease": "backspace",
            "ross": "delete",
        }),
           Choice("left_character", {
            "prekris": "(",
            "right prekris": ")",
            "brax": "[",
            "right brax": "]",
            "angle": "<",
            "right angle": ">",
            "curly": "{",
            "right curly": "}"
            "quotes": '"',
            "single quote": "'",
            "comma": ",",
            "period": ".",
            "questo": "?",
            "backtick": "`",
        }),
        Choice("right_character", {
            "prekris": ")",
            "left prekris": "(",
            "brax": "]",
            "left brax": "[",
            "angle": ">",
            "lefty angle": "<"
            "curly": "}",
            "left curly": "{",
            "quotes": '"',
            "single quote": "'",
            "comma": ",",
            "period": ".",
            "questo": "?",
            "backtick": "`",
        }),
 
    ]

    defaults = {
        "nnavi500": 1,
        "nnavi50": 1,
        "nnavi10": 1,
        "textnv": "",
        "capitalization": 0,
        "spacing": 0,
        "mtn_mode": None,
        "mtn_dir": "right",
        "extreme": None,
        "big": False,
        "splatdir": "backspace",
    }


control.nexus().merger.add_global_rule(Navigation())
