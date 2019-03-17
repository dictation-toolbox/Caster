#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Chrome 

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat, Function, Choice, Mouse, Pause)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class ChromeRule(MergeRule):
    pronunciation = "google chrome"

    mapping = { 
 
    
 
        "new [<n>]":                R(Key("c-t"), rdescript="Browser: New Tab") * Repeat(extra="n"),
        "new window": Key("c-n"),
        "(new incognito window | incognito)": Key("cs-n"),
        "new tab [<n>]":                R(Key("c-t"), rdescript="Browser: New Tab") * Repeat(extra="n"),
        "reopen tab [<n>]":             R(Key("cs-t"), rdescript="Browser: Reopen Tab") * Repeat(extra="n"),
        "close tab [<n>]":               R(Key("c-w")) * Repeat(extra='n'),
        "close all tabs":               R(Key("cs-w"), rdescript="Browser: Close All Tabs"),
        "(nab | next tab) [<n>]":                    R(Key("c-tab")) * Repeat(extra="n"),
        "(lab | previous tab) [<n>]":                    R(Key("cs-tab")) * Repeat(extra="n"),
        "(new tab | nab) that": 
            R(Mouse("middle") + Pause("20") + Key("c-tab"), 
                rdescript="Browser: when the mouse is hovering over a link open that link in a new tab and then go to that new tab "),
        
        "second tab": R(Key("c-2")),
         "first tab": R(Key("c-1")),
        "third tab": R(Key("c-3")),
        "fourth tab": R(Key("c-4")),
        "fifth tab": R(Key("c-5")),
        "sixth tab": R(Key("c-6")),
        "seventh tab": R(Key("c-7")),
        "eighth tab": R(Key("c-8")),
        "ninth tab": R(Key("c-9")),
        "last tab": R(Key("c-1, cs-tab")),
        "second last tab": R(Key("c-1, cs-tab:2")),
        
        
        "go back [<n>]":                R(Key("a-left/20"), rdescript="Browser: Navigate History Backward") * Repeat(extra="n"),
        "go forward [<n>]":             R(Key("a-right/20"), rdescript="Browser: Navigate History Forward") * Repeat(extra="n"),
        "zoom in [<n>]":                R(Key("c-plus/20"), rdescript="Browser: Zoom In") * Repeat(extra="n"),
        "zoom out [<n>]":               R(Key("c-minus/20"), rdescript="Browser: Zoom") * Repeat(extra="n"),
        "zoom reset":                   R(Key("c-0"), rdescript="Browser: Reset Zoom"),
        "super refresh":                R(Key("c-f5"), rdescript="Browser: Super Refresh"),
        "switch focus [<n>]":           R(Key("f6/20"), rdescript="Browser: Switch Focus") * Repeat(extra="n"),
        "[find] next match [<n>]":      R(Key("c-g/20"), rdescript="Browser: Next Match") * Repeat(extra="n"),
        "[find] prior match [<n>]":     R(Key("cs-g/20"), rdescript="Browser: Prior Match") * Repeat(extra="n"),
        "[toggle] caret browsing":      R(Key("f7"), rdescript="Browser: Caret Browsing"), # now available through an add on, was a standard feature

        "home page":                    R(Key("a-home"), rdescript="Browser: Home Page"),
        "[show] history":                 R(Key("c-h"), rdescript="Browser: Show History"),
        "[address] bar":                  R(Key("c-l"), rdescript="Browser: Address Bar"),
        "show downloads":               R(Key("c-j"), rdescript="Browser: Show Downloads"),
        "[add] bookmark":               R(Key("c-d"), rdescript="Browser: Add Bookmark"),
        "bookmark all tabs":            R(Key("cs-d"), rdescript="Browser: Bookmark All Tabs"),
        "[toggle] bookmark bar":        R(Key("cs-b"), rdescript="Browser: Toggle Bookmark Bar"),
        "[show] bookmarks":               R(Key("cs-o"), rdescript="Browser: Show Bookmarks"),
        "switch user":                  R(Key("cs-m"), rdescript="Browser: Switch User"),
        "chrome task manager":          R(Key("s-escape"), rdescript="Browser: Chrome Task Manager"),
        "[toggle] full-screen":         R(Key("f11"), rdescript="Browser: Toggle Fullscreen Mode"),
        "focus notification":           R(Key("a-n"), rdescript="Browser: Focus Notification"),
        "allow notification":           R(Key("as-a"), rdescript="Browser: Allow Notification"),
        "deny notification":            R(Key("as-a"), rdescript="Browser: Deny Notification"),


        "developer tools":              R(Key("f12"), rdescript="Browser: Developer Tools"),
        "view [page] source":           R(Key("c-u"), rdescript="Browser: View Page Source"),
        "resume":                       R(Key("f8"), rdescript="Browser: Resume"),
        "step over":                    R(Key("f10"), rdescript="Browser: Step Over"),
        "step into":                    R(Key("f11"), rdescript="Browser: Step Into"),
        "step out":                     R(Key("s-f11"), rdescript="Browser: Step Out"),

        "IRC identify":                 R(Text("/msg NickServ identify PASSWORD"), rdescript="IRC Chat Channel Identify"),

        "google that": R(Key("c-c, c-t, c-v, enter"), rdescript="googles highlighted text"),
        "duplicate tab":R(Key("a-d,a-c,c-t/15,c-v/15, enter"),
             rdescript="duplicate the current tab"),
        "duplicate window":R(Key("a-d,a-c,c-n/15,c-v/15, enter"),
             rdescript="duplicate the current tab in a new window"),
        "extensions": R(Key("a-f/20, l, e/15, enter"),
             rdescript="chrome extensions"),
        "(menu | three dots)": R(Key("a-f"),
             rdescript="go to the three dots menu at the top right of chrome"),
        "settings": R(Key("a-f/5, s"),
             rdescript="chrome settings"),
        "downloads": R(Key("c-j"),
             rdescript="show downloads"),
        "chrome task manager": R(Key("s-escape"), rdescript="chrome task manager"),
        "clear browsing data": R(Key("cs-del"), rdescript="clear browsing data"),
        "developer tools": R(Key("cs-i"), rdescript="developer tools"),
        "more tools": R(Key("a-f/5, l"), rdescript="more tools"),



# click by voice chrome extension commands
# these require the click by voice Chrome extension
# these allow you to browse Google Chrome hands-free
#  (I haven't tried surfer keys yet, but apparently that's another good option)
        "<numbers> <dictation>": R(Key("cs-space/30")+Text("%(numbers)d:%(click_by_voice_options)s")
            + Key("enter/30") + Text("%(dictation)s"), 
            rdescript="input dictation into numbered text field"),
        "go <numbers> <dictation>": R(Key("cs-space/30")+Text("%(numbers)d:%(click_by_voice_options)s")
            + Key("enter/30") + Text("%(dictation)s") + Key("enter"), 
            rdescript="input dictation into numbered text field then press enter"),
        "next <numbers> <dictation>": R(Key("cs-space/30")+Text("%(numbers)d:%(click_by_voice_options)s")
            + Key("enter/30") + Text("%(dictation)s") + Key("tab"), 
            rdescript="input dictation into numbered text field then press tab"),
        "<numbers> [<click_by_voice_options>]": R(Key("cs-space/30")
            + Text("%(numbers)d:%(click_by_voice_options)s") + Key("enter"), 
            rdescript="click link with click by voice options"),
        "hide hints": R(Key("cs-space/30")+Text(":-")+Key("enter"),
             rdescript="hide click by voice hints (i.e. numbers)"),
        "show hints": R(Key("cs-space/30")+Text(":+")+Key("enter"),
            rdescript="show click by voice hints (i.e. numbers)"),


        }
    extras = [
        Choice("click_by_voice_options", {
            "go": "f",
            "click": "c",
            "push": "b", # open as new tab but don't go to it
            "tab": "t", # open as new tab and go to it
            "window": "w",
            "hover": "h",
            "link": "k",
            "copy": "s",
        }),
        
        Dictation("dictation"),
        IntegerRefST("n", 1, 10),
        IntegerRefST("m", 1, 10),
        IntegerRefST("numbers", 0, 1000),
    ]
    defaults = {"n": 1, "dict": "", "click_by_voice_options": "c"}


#---------------------------------------------------------------------------

context = AppContext(executable="chrome")
grammar = Grammar("chrome", context=context)

if settings.SETTINGS["apps"]["chrome"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(ChromeRule())
    else:
        rule = ChromeRule(name="chrome")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
