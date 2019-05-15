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

_NEXUS = control.nexus()


class NavigationNon(MergeRule):
    mapping = {
        "<direction> <time_in_seconds>":
            AsynchronousAction(
                [L(S(["cancel"], Key("%(direction)s"), consume=False))],
                repetitions=1000,
                blocking=False),
        "erase multi clipboard":
            R(Function(navigation.erase_multi_clipboard, nexus=_NEXUS)),
        "find":
            R(Key("c-f")),
        "find next [<n>]":
            R(Key("f3"))*Repeat(extra="n"),
        "find prior [<n>]":
            R(Key("s-f3"))*Repeat(extra="n"),
        "find everywhere":
            R(Key("cs-f")),
        "replace":
            R(Key("c-h")),
        "(F to | F2)":
            R(Key("f2")),
        "(F six | F6)":
            R(Key("f6")),
        "(F nine | F9)":
            R(Key("f9")),
        "[show] context menu":
            R(Key("s-f10")),
        "squat":
            R(Function(navigation.left_down, nexus=_NEXUS)),
        "bench":
            R(Function(navigation.left_up, nexus=_NEXUS)),
        "kick":
            R(Function(navigation.left_click, nexus=_NEXUS)),
        "kick mid":
            R(Function(navigation.middle_click, nexus=_NEXUS)),
        "psychic":
            R(Function(navigation.right_click, nexus=_NEXUS)),
        "(kick double|double kick)":
            R(Function(navigation.left_click, nexus=_NEXUS)*Repeat(2)),
        "shift right click":
            R(Key("shift:down") + Mouse("right") + Key("shift:up")),
        "curse <direction> [<direction2>] [<nnavi500>] [<dokick>]":
            R(Function(navigation.curse)),
        "scree <direction> [<nnavi500>]":
            R(Function(navigation.wheel_scroll)),
        "colic":
            R(Key("control:down") + Mouse("left") + Key("control:up")),
        "garb [<nnavi500>]":
            R(Mouse("left") + Mouse("left") + Function(
                navigation.stoosh_keep_clipboard,
                nexus=_NEXUS)),
        "drop [<nnavi500>]":
            R(Mouse("left") + Mouse("left") + Function(
                navigation.drop_keep_clipboard,
                nexus=_NEXUS,
                capitalization=0,
                spacing=0)),
        "sure stoosh":
            R(Key("c-c")),
        "sure cut":
            R(Key("c-x")),
        "sure spark":
            R(Key("c-v")),
        "undo [<n>]":
            R(Key("c-z"))*Repeat(extra="n"),
        "redo [<n>]":
            R(Key("c-y"))*Repeat(extra="n"),
        "refresh":
            R(Key("c-r")),
        "maxiwin":
            R(Key("w-up")),
        "move window":
            R(Key("a-space, r, a-space, m")),
        "window (left | lease) [<n>]":
            R(Key("w-left"))*Repeat(extra="n"),
        "window (right | ross) [<n>]":
            R(Key("w-right"))*Repeat(extra="n"),
        "monitor (left | lease) [<n>]":
            R(Key("sw-left"))*Repeat(extra="n"),
        "monitor (right | ross) [<n>]":
            R(Key("sw-right"))*Repeat(extra="n"),
        "(next | prior) window":
            R(Key("ca-tab, enter")),
        "switch (window | windows)":
            R(Key("ca-tab"))*Repeat(extra="n"),
        "next tab [<n>]":
            R(Key("c-pgdown"))*Repeat(extra="n"),
        "prior tab [<n>]":
            R(Key("c-pgup"))*Repeat(extra="n"),
        "close tab [<n>]":
            R(Key("c-w/20"))*Repeat(extra="n"),
        "elite translation <text>":
            R(Function(alphanumeric.elite_text)),

        # Workspace management
        "show work [spaces]":
            R(Key("w-tab")),
        "(create | new) work [space]":
            R(Key("wc-d")),
        "close work [space]":
            R(Key("wc-f4")),
        "close all work [spaces]":
            R(Function(utilities.close_all_workspaces)),
        "next work [space] [<n>]":
            R(Key("wc-right"))*Repeat(extra="n"),
        "(previous | prior) work [space] [<n>]":
            R(Key("wc-left"))*Repeat(extra="n"),

        "go work [space] <n>":
            R(Function(lambda n: utilities.go_to_desktop_number(n))),
        "send work [space] <n>":
            R(Function(lambda n: utilities.move_current_window_to_desktop(n))),
        "move work [space] <n>":
            R(Function(lambda n: utilities.move_current_window_to_desktop(n, True))),
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


class Navigation(MergeRule):
    non = NavigationNon
    pronunciation = CCRMerger.CORE[1]

    mapping = {
    # "periodic" repeats whatever comes next at 1-second intervals until "terminate" 
    # or "escape" (or your SymbolSpecs.CANCEL) is spoken or 100 tries occur
        "periodic":
            ContextSeeker(forward=[L(S(["cancel"], lambda: None),
            S(["*"], lambda fnparams: UntilCancelled(Mimic(*filter(lambda s: s != "periodic", fnparams)), 1).execute(),
            use_spoken=True))]),
    # VoiceCoder-inspired -- these should be done at the IDE level
        "fill <target>":
            R(Key("escape, escape, end"), show=False) +
            AsynchronousAction([L(S(["cancel"], Function(context.fill_within_line, nexus=_NEXUS)))],
            time_in_seconds=0.2, repetitions=50 ),
        "jump in":
            AsynchronousAction([L(S(["cancel"], context.nav, ["right", "(~[~{~<"]))],
            time_in_seconds=0.1, repetitions=50),
        "jump out":
            AsynchronousAction([L(S(["cancel"], context.nav, ["right", ")~]~}~>"]))],
            time_in_seconds=0.1, repetitions=50),
        "jump back":
            AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))],
            time_in_seconds=0.1, repetitions=50),
        "jump back in":
            AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))],
            finisher=Key("right"), time_in_seconds=0.1, repetitions=50 ),

    # keyboard shortcuts
        'save':
            R(Key("c-s"), rspec="save"),
        'shock [<nnavi50>]':
            R(Key("enter"), rspec="shock")* Repeat(extra="nnavi50"),

        "(<mtn_dir> | <mtn_mode> [<mtn_dir>]) [(<nnavi500> | <extreme>)]":
            R(Function(text_utils.master_text_nav)),

        "shift click":
            R(Key("shift:down") + Mouse("left") + Key("shift:up")),

        "stoosh [<nnavi500>]":
            R(Function(navigation.stoosh_keep_clipboard, nexus=_NEXUS), rspec="stoosh"),
        "cut [<nnavi500>]":
            R(Function(navigation.cut_keep_clipboard, nexus=_NEXUS), rspec="cut"),
        "spark [<nnavi500>] [(<capitalization> <spacing> | <capitalization> | <spacing>) (bow|bowel)]":
            R(Function(navigation.drop_keep_clipboard, nexus=_NEXUS), rspec="spark"),

        "splat [<splatdir>] [<nnavi10>]":
            R(Key("c-%(splatdir)s"), rspec="splat") * Repeat(extra="nnavi10"),
        "deli [<nnavi50>]":
            R(Key("del/5"), rspec="deli") * Repeat(extra="nnavi50"),
        "clear [<nnavi50>]":
            R(Key("backspace/5:%(nnavi50)d"), rspec="clear"),
        SymbolSpecs.CANCEL:
            R(Key("escape"), rspec="cancel"),


        "shackle":
            R(Key("home/5, s-end"), rspec="shackle"),
        "(tell | tau) <semi>":
            R(Function(navigation.next_line), rspec="tell dock"),
        "duple [<nnavi50>]":
            R(Function(navigation.duple_keep_clipboard), rspec="duple"),
        "Kraken":
            R(Key("c-space"), rspec="Kraken"),

    # text formatting
        "set [<big>] format (<capitalization> <spacing> | <capitalization> | <spacing>) (bow|bowel)":
            R(Function(textformat.set_text_format)),
        "clear castervoice [<big>] formatting":
            R(Function(textformat.clear_text_format)),
        "peek [<big>] format":
            R(Function(textformat.peek_text_format)),
        "(<capitalization> <spacing> | <capitalization> | <spacing>) (bow|bowel) <textnv> [brunt]":
            R(Function(textformat.master_format_text)),
        "[<big>] format <textnv>":
            R(Function(textformat.prior_text_format)),
        "<word_limit> [<big>] format <textnv>":
            R(Function(textformat.partial_format_text)),

        "hug <enclosure>":
            R(Function(text_utils.enclose_selected)),
        "dredge":
            R(Key("a-tab")),
    

        
        
        # the following text manipulation commands currently only work on text
            # that is on the same line as the cursor, though this could be expanded.
        # requires the latest version of dragonfly because of her recent modification of the Function action
            # I think dragonfly2-0.13.0
        # The alphabet should probably be added into the choice dictionaries.
        # the keypress waittime should probably be made higher for these commands.
        # the wait times in the functions could also be reduced.
        # the functions should probably be adjusted to avoid inappropriately recognizing substrings
        # these work in most applications not all (e.g. doesn't work in Microsoft Word),
        # probably something to do with the wait times within paste_string_without_altering_clipboard
        
        "change [<lease_ross>] <dictation> to <dictation2>":
            R(Function(navigation.copypaste_replace_phrase_with_phrase,
                       dict(dictation="replaced_phrase", dictation2="replacement_phrase", lease_ross="left_right")),
              rdescript="Core: replace text to the left or right of the cursor"),
        
        "remove [<lease_ross>] <dictation>":
            R(Function(navigation.copypaste_remove_phrase_from_text,
                       dict(dictation="phrase", lease_ross="left_right")),
              rdescript="remove chosen phrase to the left or right of the cursor"),
        "remove [lease] <left_character>":
            R(Function(navigation.copypaste_remove_phrase_from_text,
                       dict(left_character="phrase"),
                       left_right="left"),
              rdescript="remove chosen character to the left of the cursor"),
        "remove ross <right_character>":
            R(Function(navigation.copypaste_remove_phrase_from_text,
                       dict(right_character="phrase"),
                       left_right="right"),
              rdescript="remove chosen character to the right of the cursor"),
        "go [lease] <left_character>":
            R(Function(navigation.move_until_phrase,
                       dict(left_character="phrase"),
                       left_right="left"),
              rdescript="move to chosen character to the left of the cursor"),
        "go [<lease_ross>] <dictation>":
            R(Function(navigation.move_until_phrase,
                       dict(dictation="phrase", lease_ross="left_right")),
              rdescript="move to chosen phrase to the left or right of the cursor"),
        "go ross <right_character>":
            R(Function(navigation.move_until_phrase,
                       dict(right_character="phrase"),
                       left_right="right"),
              rdescript="move to chosen character to the right of the cursor"),
        "grab [<lease_ross>] <dictation> ":
            R(Function(navigation.select_until_phrase, dict(dictation="phrase", lease_ross="left_right")),
                 rdescript="select until chosen phrase (inclusive)"),
        "grab [lease] <left_character>":
            R(Function(navigation.select_until_phrase, dict(left_character="phrase"), left_right="left"),
            rdescript="select left until chosen character"),
        "grab ross <right_character>":
            R(Function(navigation.select_until_phrase, dict(right_character="phrase"), left_right="right"),
            rdescript="select right until chosen character"),
        "wipe [<lease_ross>] <dictation>":
            R(Function(navigation.copypaste_delete_until_phrase,
                       dict(dictation="phrase", lease_ross="left_right")),
              rdescript="delete left until chosen phrase (exclusive)"),
        "wipe [lease] <left_character>":
            R(Function(navigation.copypaste_delete_until_phrase,
                       dict(left_character="phrase"),
                       left_right="left"),
              rdescript="delete left until chosen character (exclusive)"),
        "wipe ross <right_character>":
            R(Function(navigation.copypaste_delete_until_phrase,
                       dict(right_character="phrase"), 
                       left_right="right"),
              rdescript="delete left until chosen character"),
        


    }

    extras = [
        IntegerRefST("nnavi10", 1, 11),
        IntegerRefST("nnavi50", 1, 50),
        IntegerRefST("nnavi500", 1, 500),
        Dictation("textnv"),
        Dictation("dictation"),
        Dictation("dictation2"),
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
        Choice("lease_ross", {
            "lease": "left",
            "ross": "right",
        }),
        Choice(
            "left_character", {
                "[left] prekris": "(",
                "right prekris": ")",
                "[left] brax": "[",
                "right brax": "]",
                "[left] angle": "<",
                "right angle": ">",
                "[left] curly": "{",
                "right curly": "}",
                "quotes": '"',
                "single quote": "'",
                "comma": ",",
                "period": ".",
                "questo": "?",
                "backtick": "`",
                "equals": "=",
                "dolly": "$",
                "slash": "/",
                "backslash": "\\",
                "minus": "-",
                "plus": "+",
                "starling": "*",
                "x-ray": "x",

            }),
        Choice(
            "right_character", {
                "[right] prekris": ")",
                "left prekris": "(",
                "[right] brax": "]",
                "left brax": "[",
                "[right] angle": ">",
                "left angle": "<",
                "[right] curly": "}",
                "left curly": "{",
                "quotes": '"',
                "single quote": "'",
                "comma": ",",
                "period": ".",
                "questo": "?",
                "backtick": "`",
                "equals": "=",
                "dolly": "$",
                "slash": "/",
                "backslash": "\\",
                "minus": "-",
                "plus": "+",
                "starling": "*",
                "x-ray": "x",
                
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
        "lease_ross": "left",
    }


control.nexus().merger.add_global_rule(Navigation())
