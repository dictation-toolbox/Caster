#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Adobe Acrobat

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, Dictation, Repeat, Choice, Mouse, Pause)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


ShowHideMenu = Key("a-v, s")
class AcrobatRule(MergeRule):
    pronunciation = "acrobat"

    mapping = {

        
        "[go to] page <n>": R(Key("a-v, n, g/15") + Text("%(n)s") + Key("enter"),
            rdescript="go to page acrobat)"),
        "set zoom <n>": R(Key("c-y/40") + Text("%(n)s") + Key("enter"), rdescript="set zoom level"),
        
        "open": R(Key("c-o"), rdescript="open"),
        "duplicate tab":R(Key("a-w,n/40,ws-left"), rdescript="duplicate tab in new window"),
        "enable scrolling": R(Key("a-v, p, c"), rdescript="enable scrolling as opposed to single page mode"),
        "(disable scrolling | single page mode)": R(Key("a-v, p, s"),
             rdescript="single page mode, you can scroll one page at a time"),
        "(nab | next tab) [<n>]": R(Key("c-tab"),
             rdescript="next tab") * Repeat(extra="n"),
        "(lab | prior tab) [<n>]": R(Key("cs-tab")),
             rdescript="prior tab") * Repeat(extra="n"),
        
        "(home button|homer)": R(Mouse("[100, 101], left"),
             rdescript="click home button on top left"), # coordinates may be user dependent

 # Sticky Note Commands
            # must have the cursor over the location where you want the sticky note
        "add note [<dict>]": R(Mouse("right") + Key("t/5") + Text("%(dict)s"),
             rdescript="add sticky note with dictation"),
        "fast [add] note [<dict>]":
            R(Mouse("right") + Key("t/5") + Text("%(dict)s") + Pause("10") + Key("escape/5, c-s"),
             rdescript="add sticky note with dictation then close it and save"),
        "open blank note":
            R(Mouse("right") + Key("t/5"), rdescript="open sticky note"),
        "add blank note":
            R(Mouse("right") + Key("t/5, escape/5, c-s"),
                rdescript="open sticky note, close it, and then save"),
        "delete note":
            R(Mouse("right") + Key("l, c-s"), rdescript="close sticky note then save"),
              
        
        "(go | go back) [<n>]": Key("a-left"),
             rdescript="go back to previous location") * Repeat(extra='n'),
        "save as": R(Key("a-f, a"), rdescript="save as"),

        # when you open up a document that you have previously saved, and then click save,
            # Adobe will sometimes make you go back into the save dialogbox
            # and choose the location you want to save it in and then make you say that you want 
            # to overwrite the file. This is annoying, but this command "fast save" will automatically 
            # do all that for you.
        "fast save": R(Key("c-s/10, enter/10, enter/10, left, enter"),
             rdescript="fast save"),

        # if page down goes too far down then try this command
        "down it [<n>]": R(Key("pgdown:%(n)s, up:4"), rdescript="page down and then go up a little bit"),
        "up it [<n>]": R(Key("pgup:%(n)s, down:4"), rdescript="page up and then go down a little bit"),

        "tools pane": R(ShowHideMenu + Key("t"), rdescript="tools pane"),
        "menu bar": R(ShowHideMenu + Key("m"), rdescript="menu bar"),
        "model tree": R(ShowHideMenu + Key("n, e"),  rdescript="model tree"),
        "bookmarks": R(ShowHideMenu + Key("n, b"), rdescript="bookmarks"),
        "[page] thumbnails": R(ShowHideMenu + Key("n, b"), rdescript="page thumbnails"),
               
        "rotate [<n>]": R(Key("c-plus"),  rdescript="rotate page clockwise" * Repeat(extra='n'),

        # Scrolling Commands
            # Acrobat has a built-in scrolling function with nine speeds. 
            # Unfortunately, there are not separate commands for our scrolling up and down
            # You have to start by scrolling in the most recently used direction and then reverse the direction
        "scroll <speed_one_to_nine>": Key("cs-h/2, %(speed_one_to_nine)s"),
        "scroll": Key("cs-h/2, 6"),
        "change speed <speed_one_to_nine>": Key("%(speed_one_to_nine)s, %(speed_one_to_nine)s"),
        "reverse [direction]": R(Key("minus"), rdescript="reverse scrolling direction while scrolling"),
        "stop [scrolling]": R(Key("escape"), rdescript="stop scrolling"),

        # cursor commands 
            # (must enable "you single key accelerators to access tools" by going to: edit -> preferences -> general)
        "highlight": R(Key("u"), rdescript=""),
        "hand tool": R(Key("h"), rdescript=""),
        "select tool": R(Key("v"), rdescript=""),

    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 1000),
        IntegerRefST("m", 1, 9),
        IntegerRefST("speed_one_to_nine", 1, 9),
    ]
    defaults = {"n": 1, "dict": "nothing"}


#---------------------------------------------------------------------------

context = AppContext(executable="acrobat")
grammar = Grammar("acrobat", context=context)

if settings.SETTINGS["apps"]["acrobat"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(AcrobatRule())
    else:
        rule = AcrobatRule(name="acrobat")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
