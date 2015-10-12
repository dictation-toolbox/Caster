'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import Repeat, Function, Key, Dictation, Choice, Mouse, MappingRule

from caster.lib import context, navigation
from caster.lib import control
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.ccrmerger import CCRMerger
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.actions import AsynchronousAction
from caster.lib.dfplus.state.actions2 import FuzzyMatchAction
from caster.lib.dfplus.state.short import L, S, R
from caster.lib.pita import fnfz


class NavigationNon(MappingRule):
    mapping = {
        "<direction> <time_in_seconds>":    AsynchronousAction([L(S(["cancel"], Key("%(direction)s")))], 
                                                               repetitions=1000, blocking=False ),
        "erase multi clipboard":            R(Function(navigation.erase_multi_clipboard), 
                                              rdescript="Erase Multi Clipboard"),
        "find":                             R(Key("c-f"), rdescript="Find"),
        "find next [<n>]":                  R(Key("f3"), rdescript="Find Next") * Repeat(extra="n"),
        "find prior [<n>]":                 R(Key("s-f3"), rdescript="Find Prior") * Repeat(extra="n"),
        "find everywhere":                  R(Key("cs-f"), rdescript="Find Everywhere"),
        "replace":                          R(Key("c-h"), rdescript="Replace"),
        "(F to | F2)":                      R(Key("f2"), rdescript="Key: F2"),
        "(F six | F6)":                     R(Key("f6"), rdescript="Key: F6"),
        "(F nine | F9)":                    R(Key("f9"), rdescript="Key: F9"),
        
        'kick':                             R(Function(navigation.kick), rdescript="Mouse: Left Click"),
        'kick mid':                         R(Function(navigation.kick_middle), rdescript="Mouse: Middle Click"),
        'psychic':                          R(Function(navigation.kick_right), rdescript="Mouse: Right Click"),
        '(kick double|double kick)':        R(Function(navigation.kick) * Repeat(2), rdescript="Mouse: Double Click"),
        "shift right click":                R(Key("shift:down") + Mouse("right") + Key("shift:up"), rdescript="Mouse: Shift + Right Click"),
        "curse <direction> [<direction2>] [<nnavi500>] [<dokick>]": R(Function(navigation.curse), rdescript="Curse"),
      
        "colic":                            R(Key("control:down") + Mouse("left") + Key("control:up"), rdescript="Mouse: Ctrl + Left Click"),
        "garb [<nnavi500>]":                R(Mouse("left")+Mouse("left")+Key("c-c")+Function(navigation.clipboard_to_file), rdescript="Highlight @ Mouse + Copy"),
        "drop [<nnavi500>]":                R(Mouse("left")+Mouse("left")+Function(navigation.drop), rdescript="Highlight @ Mouse + Paste"),
        
        "sure stoosh":                      R(Key("c-c"), rdescript="Simple Copy"),
        "sure cut":                         R(Key("c-x"), rdescript="Simple Cut"),
        "sure spark":                       R(Key("c-v"), rdescript="Simple Paste"),
        
        "undo [<n>]":                       R(Key("c-z"), rdescript="Undo") * Repeat(extra="n"),
        "redo [<n>]":                       R(Key("c-y"), rdescript="Redo") * Repeat(extra="n"),

        "refresh":                          R(Key("c-r"), rdescript="Refresh"),
        
        "next tab [<n>]":                   R(Key("c-pgdown"), rdescript="Next Tab") * Repeat(extra="n"),
        "prior tab [<n>]":                  R(Key("c-pgup"), rdescript="Previous Tab") * Repeat(extra="n"),
        "close tab [<n>]":                  R(Key("c-w/20"), rdescript="Close Tab") * Repeat(extra="n"),
        
        "symbol match <text>":              FuzzyMatchAction(fnfz.pita_list_provider, fnfz.pita_filter, 
                                                         fnfz.pita_selection, rdescript="Fuzzy Symbol Matcher"),
        "ex match <text>":                  FuzzyMatchAction(fnfz.dredge_ex_list_provider, fnfz.dredge_ex_filter, 
                                                         fnfz.dredge_ex_selection, rdescript="Fuzzy Executable Matcher"),
        "tie match <text>":                 FuzzyMatchAction(fnfz.dredge_tie_list_provider, fnfz.dredge_tie_filter, 
                                                         fnfz.dredge_tie_selection, rdescript="Fuzzy Window Matcher"),
        
        "elite translation <text>":         R(Function(navigation.elite_text), rdescript="1337 Text"),
        
          }

    extras   = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRefST("n", 1, 50),
              IntegerRefST("nnavi500", 1, 500),
              Choice("time_in_seconds",
                {"super slow": 5, "slow": 2, "normal": 0.6, "fast": 0.1, "superfast": 0.05
                }),
              navigation.get_direction_choice("direction"),
              navigation.get_direction_choice("direction2"),
              navigation.TARGET_CHOICE, 
              Choice("dokick",
                {"kick": 1, "psychic": 2
                }),
              Choice("wm",
                {"ex": 1, "tie": 2
                }),
           ]
    defaults = {
            "n": 1, "mim":"", "nnavi500": 1, "direction2":"", "dokick": 0, "text": "", "wm": 2
           }

class Navigation(MergeRule):
    non = NavigationNon
    pronunciation = CCRMerger.CORE[1]
    
    mapping = {
    
    # VoiceCoder-inspired
    "jump in":                      AsynchronousAction([L(S(["cancel"], context.nav, ["right", "(~[~{~<"]))
                                                   ], time_in_seconds=0.1, repetitions=50, rdescript="Jump: In" ),
    "jump out":                     AsynchronousAction([L(S(["cancel"], context.nav, ["right", ")~]~}~>"]))
                                                   ], time_in_seconds=0.1, repetitions=50, rdescript="Jump: Out" ),
    "jump back":                    AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))
                                                   ], time_in_seconds=0.1, repetitions=50, rdescript="Jump: Back" ),
    "fill <target>":                R(Key("escape, escape, end"), show=False) +
                                    AsynchronousAction([L(S(["cancel"], Function(context.fill_within_line)))
                                                   ], time_in_seconds=0.2, repetitions=50, rdescript="Fill" ),
    
    # keyboard shortcuts
    'save':                         R(Key("c-s"), rspec="save", rdescript="Save"),
    'shock [<nnavi50>]':            R(Key("enter"), rspec="shock", rdescript="Enter")* Repeat(extra="nnavi50"),
    
    "(<mtn_dir> | <mtn_mode> [<mtn_dir>]) [(<nnavi500> | <extreme>)]": R(Function(navigation.master_text_nav), rdescript="Keyboard Text Navigation"),
    
    "stoosh [<nnavi500>]":          R(Key("c-c")+Function(navigation.clipboard_to_file), rspec="stoosh", rdescript="Copy"),
    "cut [<nnavi500>]":             R(Key("c-x")+Function(navigation.clipboard_to_file), rspec="cut", rdescript="Cut"),
    "spark [<nnavi500>]":           R(Function(navigation.drop), rspec="spark", rdescript="Paste"),
    
    "deli [<nnavi50>]":             R(Key("del/5"), rspec="deli", rdescript="Delete") * Repeat(extra="nnavi50"),
    "clear [<nnavi50>]":            R(Key("backspace/5:%(nnavi50)d"), rspec="cancel", rdescript="Backspace"),
    "(cancel | escape)":            R(Key("escape"), rspec="cancel", rdescript="Cancel Action"),
    
    
    "shackle":                      R(Key("home/5, s-end"), rspec="shackle", rdescript="Select Line"),
    "(tell | tau) <semi>":          R(Function(navigation.next_line), rspec="tell dock", rdescript="Complete Line"), 
    "duple [<nnavi50>]":            R(Key("escape, home, s-end, c-c, end, enter, c-v"), rspec="duple", rdescript="Duplicate Line") * Repeat(extra="nnavi50"),
    "Kraken":                       R(Key("c-space"), rspec="Kraken", rdescript="Control Space"),
         
    # text formatting
    "set format (<capitalization> <spacing> | <capitalization> | <spacing>) (bow|bowel)":  R(Function(navigation.set_text_format), rdescript="Text Format"), 
    "(<capitalization> <spacing> | <capitalization> | <spacing>) (bow|bowel) <textnv> [brunt]":  R(Function(navigation.master_format_text), rdescript="Text Format"), 
    "format [<textnv>]":            R(Function(navigation.prior_text_format), rdescript="Last Text Format"),

    }

    extras = [
        IntegerRefST("nnavi50", 1, 50),
        IntegerRefST("nnavi500", 1, 500),
        Dictation("textnv"),
        
        Choice("capitalization",
                  {"yell": 1, "tie": 2,"Gerrish": 3,"sing":4, "laws":5
                  }),
        Choice("spacing",
                  {"gum": 1, "gun": 1, "spine": 2, "snake":3
                  }),
        Choice("semi",
                    {"dock": ";", "doc": ";", "sink": ""
                    }),
          
          
          
        navigation.TARGET_CHOICE,
        navigation.get_direction_choice("mtn_dir"),
        Choice("mtn_mode",
                {"shin": "s", "queue": "cs", "fly": "c",
                }),
        Choice("extreme",
                {"Wally": "way",
                }),
    ]

    defaults ={
            "nnavi500": 1, "nnavi50": 1, "textnv": "", "capitalization": 0, "spacing":0, 
            "mtn_mode": None, "mtn_dir": "right", "extreme": None 
           }

control.nexus().merger.add_global_rule(Navigation())