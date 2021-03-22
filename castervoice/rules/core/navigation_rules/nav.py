from dragonfly import Function, Repeat, Dictation, Choice, ContextAction, ShortIntegerRef
from castervoice.lib.context import AppContext

from castervoice.lib import navigation, context, textformat, text_utils
from castervoice.rules.core.navigation_rules import navigation_support
from dragonfly.actions.action_mimic import Mimic

from castervoice.lib.actions import Key, Mouse
from castervoice.rules.ccr.standard import SymbolSpecs

try:  # Try first loading from caster user directory
    from punctuation_rules.punctuation_support import double_text_punc_dict, text_punc_dict
except ImportError:
    try:  # Try  first loading from caster user directory top level
        from punctuation_support import double_text_punc_dict, text_punc_dict
    except ImportError:
        from castervoice.rules.core.punctuation_rules.punctuation_support import double_text_punc_dict, text_punc_dict

try:
    from keyboard_rules import keyboard_support
except ImportError: 
    try:
        from keyboard_support import keyboard_support
    except ImportError: 
        from castervoice.rules.core.keyboard_rules import keyboard_support

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.actions import AsynchronousAction, ContextSeeker
from castervoice.lib.merge.state.actions2 import UntilCancelled
from castervoice.lib.merge.state.short import S, L, R

_tpd = text_punc_dict()
_dtpd = double_text_punc_dict()


for key, value in _dtpd.items():
    if len(value) == 2:
        _dtpd[key] = value[0] + "~" + value[1]
    elif len(value) == 4:
        _dtpd[key] = value[0:1] + "~" + value[2:3]
    else:
        msg = "Need to deal with nonstandard pair length in double_text_punc_dict: {}"
        raise Exception(msg.format(str(value)))


class Navigation(MergeRule):
    pronunciation = "navigation"

    mapping = {
        # "periodic" repeats whatever comes next at 1-second intervals until "terminate"
        # or "escape" (or your SymbolSpecs.CANCEL) is spoken or 100 tries occur
        "periodic":
            ContextSeeker(forward=[
                L(
                    S(["cancel"], lambda: None),
                    S(["*"],
                      lambda fnparams: UntilCancelled(
                          Mimic(*filter(lambda s: s != "periodic", fnparams)), 1).execute(
                          ),
                      use_spoken=True))
            ]),
        # VoiceCoder-inspired -- these should be done at the IDE level
        "fill <target>":
            R(Key("escape, escape, end"), show=False) +
            AsynchronousAction([L(S(["cancel"], Function(context.fill_within_line)))],
            time_in_seconds=0.2, repetitions=50 ),
        "jump in":
            AsynchronousAction([L(S(["cancel"], context.nav, ["right", "(~[~{~<"]))],
                               time_in_seconds=0.1,
                               repetitions=50),
        "jump out":
            AsynchronousAction([L(S(["cancel"], context.nav, ["right", ")~]~}~>"]))],
                               time_in_seconds=0.1,
                               repetitions=50),
        "jump back":
            AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))],
                               time_in_seconds=0.1,
                               repetitions=50),
        "jump back in":
            AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))],
                               finisher=Key("right"),
                               time_in_seconds=0.1,
                               repetitions=50),

        # keyboard shortcuts
        'save':
            R(Key("c-s"), rspec="save"),
        "shift click":
            R(Key("shift:down") + Mouse("left") + Key("shift:up")),
        "stoosh [<nnavi500>]":
            R(Function(navigation.stoosh_keep_clipboard), rspec="stoosh"),
        "cut [<nnavi500>]":
            R(Function(navigation.cut_keep_clipboard), rspec="cut"),
        "spark [<nnavi500>] [(<capitalization> <spacing> | <capitalization> | <spacing>) [(bow|bowel)]]":
            R(Function(navigation.drop_keep_clipboard), rspec="spark"),
        "splat [<splatdir>] [<nnavi10>]":
            R(Key("c-%(splatdir)s"), rspec="splat")*Repeat(extra="nnavi10"),
        SymbolSpecs.CANCEL:
            R(Key("escape"), rspec="cancel"),
        "shackle":
            R(Key("home/5, s-end"), rspec="shackle"),
        "(tell | tau) <semi>":
            R(Function(navigation.next_line), rspec="tell dock"),
        "(hark | heart) <semi>":
            R(Function(navigation.previous_line), rspec="hark dock"),
        "duple [<nnavi50>]":
            R(Function(navigation.duple_keep_clipboard), rspec="duple"),
        "Kraken":
            R(Key("c-space"), rspec="Kraken"),
        "undo [<nnavi10>]":
            R(Key("c-z"))*Repeat(extra="nnavi10"),
        "redo [<nnavi10>]":
            R(
                ContextAction(default=Key("c-y")*Repeat(extra="nnavi10"),
                              actions=[
                                  (AppContext(executable=["rstudio", "foxitreader"]),
                                   Key("cs-z")*Repeat(extra="nnavi10")),
                              ])),

        # text formatting
        "set [<big>] format (<capitalization> <spacing> | <capitalization> | <spacing>) [(bow|bowel)]":
            R(Function(textformat.set_text_format)),
        "clear castervoice [<big>] formatting":
            R(Function(textformat.clear_text_format)),
        "peek [<big>] format":
            R(Function(textformat.peek_text_format)),
        "(<capitalization> <spacing> | <capitalization> | <spacing>) [(bow|bowel)] <textnv> [brunt]":
            R(Function(textformat.master_format_text)),
        "[<big>] format <textnv>":
            R(Function(textformat.prior_text_format)),
        "<word_limit> [<big>] format <textnv>":
            R(Function(textformat.partial_format_text)),
        "hug <enclosure>":
            R(Function(text_utils.enclose_selected)),
        "dredge [<nnavi10>]":
            R(Key("alt:down, tab/20:%(nnavi10)d, alt:up"),
              rdescript="Core: switch to most recent Windows"),

        # Ccr Mouse Commands
        "kick [<nnavi3>]":
            R(Function(navigation.left_click))*Repeat(extra="nnavi3"),
        "psychic":
            R(Function(navigation.right_click)),
        "(kick double|double kick)":
            R(Function(navigation.left_click)*Repeat(2)),
        "squat":
            R(Function(navigation.left_down)),
        "bench":
            R(Function(navigation.left_up)),

        # special keystroke commands
        "(lease wally | latch) [<nnavi10>]":
            R(Key("home:%(nnavi10)s")),
        "(ross wally | ratch) [<nnavi10>]":
            R(Key("end:%(nnavi10)s")),
        "sauce wally [<nnavi10>]":
            R(Key("c-home:%(nnavi10)s")),
        "dunce wally [<nnavi10>]":
            R(Key("c-end:%(nnavi10)s")),
        "bird [<nnavi500>]":
            R(Key("c-left:%(nnavi500)s")),
        "firch [<nnavi500>]":
            R(Key("c-right:%(nnavi500)s")),
        "brick [<nnavi500>]":
            R(Key("s-left:%(nnavi500)s")),
        "frick [<nnavi500>]":
            R(Key("s-right:%(nnavi500)s")),
        "blitch [<nnavi500>]":
            R(Key("cs-left:%(nnavi500)s")),
        "flitch [<nnavi500>]":
            R(Key("cs-right:%(nnavi500)s")),
        "<button_dictionary_500_no_prefix_no_modifier> [<nnavi500>]":
            R(Key("%(button_dictionary_500_no_prefix_no_modifier)s")*Repeat(extra='nnavi500'),
              rdescript="press buttons from button_dictionary_500_no_prefix_no_modifier"),
        "<modifier> <button_dictionary_500_modifier> [<nnavi500>]":
            R(Key("%(modifier)s-%(button_dictionary_500_modifier)s")*Repeat(extra='nnavi500'),
              rdescript="press modifiers plus buttons from button_dictionary_500_modifier"),
        "<modifier> <button_dictionary_1_modifier>":
            R(Key("%(modifier)s-%(button_dictionary_1_modifier)s"),
              rdescript="press modifiers plus buttons from button_dictionary_1_modifier"),              
    }
    
    tell_commands_dict = {"dock": ";", "doc": ";", "sink": "", "com": ",", "deck": ":"}
    tell_commands_dict.update(_tpd)
    button_dictionary_500_no_prefix_no_modifier = {
        "tabby": "tab",
        "clear": "backspace",
        "deli": "del",
        "shock": "enter",
        "lease": "left",
        "ross": "right",
        "sauce": "up",
        "dunce": "down",
        "page (down | dunce)": "pgdown",
        "page (up | sauce)": "pgup",
    }
    button_dictionary_500_modifier = { 
        key:value for key, value in keyboard_support.button_dictionary_1.items() if value in [
            "backspace", "del", "enter", "left", "right", "up", "down", "pgdown", "pgup"
            ]
    }
    button_dictionary_1_modifier = { 
        key:value for key, value in keyboard_support.button_dictionary_1.items() if value in [
            "home", "end"
            ]
    }    
    extras = [
        ShortIntegerRef("nnavi10", 1, 11),
        ShortIntegerRef("nnavi3", 1, 4),
        ShortIntegerRef("nnavi50", 1, 50),
        ShortIntegerRef("nnavi500", 1, 500),
        Dictation("textnv"),
        Choice("enclosure", _dtpd),
        
        Choice("capitalization", {
            "yell": 1,
            "tie": 2,
            "gerrish": 3,
            "sing": 4,
            "laws": 5,
            "say": 6,
            "cop": 7,
            "slip": 8,
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
                "descent": 6,
            }),
        Choice("semi", tell_commands_dict),
        Choice("word_limit", {
            "single": 1,
            "double": 2,
            "triple": 3,
            "Quadra": 4
        }),
        navigation_support.TARGET_CHOICE,
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
        keyboard_support.modifier_choice_object,
        Choice("button_dictionary_500_no_prefix_no_modifier", button_dictionary_500_no_prefix_no_modifier),
        Choice("button_dictionary_500_modifier", button_dictionary_500_modifier),
        Choice("button_dictionary_1_modifier", button_dictionary_1_modifier)        
    ]

    defaults = {
        "nnavi500": 1,
        "nnavi50": 1,
        "nnavi10": 1,
        "nnavi3": 1,
        "textnv": "",
        "capitalization": 0,
        "spacing": 0,
        "extreme": None,
        "big": False,
        "splatdir": "backspace",
    }


def get_rule():
    return Navigation, RuleDetails(ccrtype=CCRType.GLOBAL)
