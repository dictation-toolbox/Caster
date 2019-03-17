#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Chrome

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat,
                       Function, Choice, Mouse, Pause)

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
        "new window":
            Key("c-n"),
        "(new incognito window | incognito)":
            Key("cs-n"),
        "new tab [<n>]":
            R(Key("c-t"), rdescript="Chrome: New Tab")*Repeat(extra="n"),
        "reopen tab [<n>]":
            R(Key("cs-t"), rdescript="Chrome: Reopen Tab")*Repeat(extra="n"),
        "close tab [<n>]":
            R(Key("c-w"))*Repeat(extra='n'),
        "close all tabs":
            R(Key("cs-w"), rdescript="Chrome: Close All Tabs"),
        "next tab [<n>]":
            R(Key("c-tab"))*Repeat(extra="n"),
        "previous tab [<n>]":
            R(Key("cs-tab"))*Repeat(extra="n"),
        "new tab that":
            R(Mouse("middle") + Pause("20") + Key("c-tab"),
              rdescript=
              "Browser: when the mouse is hovering over a link open that link in a new tab and then go to that new tab "
              ),
        "<nth> tab":
            R(Key("c-%(nth)s"), rdescript="Chrome: nth tab" ),
        "last tab":
            R(Key("c-1, cs-tab"), rdescript="Chrome: Last tab"),
        "second last tab":
            R(Key("c-1, cs-tab:2"), rdescript="Chrome: Second last tab"),
        "go back [<n>]":
            R(Key("a-left/20"), rdescript="Chrome: Navigate History Backward")*
            Repeat(extra="n"),
        "go forward [<n>]":
            R(Key("a-right/20"), rdescript="Chrome: Navigate History Forward")*
            Repeat(extra="n"),
        "zoom in [<n>]":
            R(Key("c-plus/20"), rdescript="Chrome: Zoom In")*Repeat(extra="n"),
        "zoom out [<n>]":
            R(Key("c-minus/20"), rdescript="Chrome: Zoom")*Repeat(extra="n"),
        "zoom reset":
            R(Key("c-0"), rdescript="Chrome: Reset Zoom"),
        "super refresh":
            R(Key("c-f5"), rdescript="Chrome: Super Refresh"),
        "switch focus [<n>]":
            R(Key("f6/20"), rdescript="Chrome: Switch Focus")*Repeat(extra="n"),
        "[find] next match [<n>]":
            R(Key("c-g/20"), rdescript="Chrome: Next Match")*Repeat(extra="n"),
        "[find] prior match [<n>]":
            R(Key("cs-g/20"), rdescript="Chrome: Prior Match")*Repeat(extra="n"),
        "[toggle] caret browsing":
            R(Key("f7"), rdescript="Chrome: Caret Browsing"
              ),  # now available through an add on, was a standard feature
        "home page":
            R(Key("a-home"), rdescript="Chrome: Home Page"),
        "[show] history":
            R(Key("c-h"), rdescript="Chrome: Show History"),
        "address bar":
            R(Key("c-l"), rdescript="Chrome: Address Bar"),
        "show downloads":
            R(Key("c-j"), rdescript="Chrome: Show Downloads"),
        "add bookmark":
            R(Key("c-d"), rdescript="Chrome: Add Bookmark"),
        "bookmark all tabs":
            R(Key("cs-d"), rdescript="Chrome: Bookmark All Tabs"),
        "[toggle] bookmark bar":
            R(Key("cs-b"), rdescript="Chrome: Toggle Bookmark Bar"),
        "[show] bookmarks":
            R(Key("cs-o"), rdescript="Chrome: Show Bookmarks"),
        "switch user":
            R(Key("cs-m"), rdescript="Chrome: Switch User"),
        "chrome task manager":
            R(Key("s-escape"), rdescript="Chrome: Chrome Task Manager"),
        "[toggle] full-screen":
            R(Key("f11"), rdescript="Chrome: Toggle Fullscreen Mode"),
        "focus notification":
            R(Key("a-n"), rdescript="Chrome: Focus Notification"),
        "allow notification":
            R(Key("as-a"), rdescript="Chrome: Allow Notification"),
        "deny notification":
            R(Key("as-a"), rdescript="Chrome: Deny Notification"),
        "developer tools":
            R(Key("f12"), rdescript="Chrome: Developer Tools"),
        "view [page] source":
            R(Key("c-u"), rdescript="Chrome: View Page Source"),
        "resume":
            R(Key("f8"), rdescript="Chrome: Resume"),
        "step over":
            R(Key("f10"), rdescript="Chrome: Step Over"),
        "step into":
            R(Key("f11"), rdescript="Chrome: Step Into"),
        "step out":
            R(Key("s-f11"), rdescript="Chrome: Step Out"),

        "IRC identify":
            R(Text("/msg NickServ identify PASSWORD"),
              rdescript="IRC Chat Channel Identify"),

        "google that":
            R(Key("c-c, c-t, c-v, enter"), rdescript="googles highlighted text"),
        "duplicate tab":
            R(Key("a-d,a-c,c-t/15,c-v/15, enter"), rdescript="duplicate the current tab"),
        "duplicate window":
            R(Key("a-d,a-c,c-n/15,c-v/15, enter"),
              rdescript="duplicate the current tab in a new window"),
        "extensions":
            R(Key("a-f/20, l, e/15, enter"), rdescript="chrome extensions"),
        "(menu | three dots)":
            R(Key("a-f"),
              rdescript="go to the three dots menu at the top right of chrome"),
        "settings":
            R(Key("a-f/5, s"), rdescript="chrome settings"),
        "downloads":
            R(Key("c-j"), rdescript="show downloads"),
        "chrome task manager":
            R(Key("s-escape"), rdescript="chrome task manager"),
        "clear browsing data":
            R(Key("cs-del"), rdescript="clear browsing data"),
        "developer tools":
            R(Key("cs-i"), rdescript="developer tools"),
        "more tools":
            R(Key("a-f/5, l"), rdescript="more tools"),

        # click by voice chrome extension commands
        # these require the click by voice Chrome extension
        # these allow you to browse Google Chrome hands-free
        #  (I haven't tried surfer keys yet, but apparently that's another good option)
        "<numbers> <dictation>":
            R(Key("cs-space/30") + Text("%(numbers)d:%(click_by_voice_options)s") +
              Key("enter/30") + Text("%(dictation)s"),
              rdescript="input dictation into numbered text field"),
        "go <numbers> <dictation>":
            R(Key("cs-space/30") + Text("%(numbers)d:%(click_by_voice_options)s") +
              Key("enter/30") + Text("%(dictation)s") + Key("enter"),
              rdescript="input dictation into numbered text field then press enter"),
        "next <numbers> <dictation>":
            R(Key("cs-space/30") + Text("%(numbers)d:%(click_by_voice_options)s") +
              Key("enter/30") + Text("%(dictation)s") + Key("tab"),
              rdescript="input dictation into numbered text field then press tab"),
        "<numbers> [<click_by_voice_options>]":
            R(Key("cs-space/30") + Text("%(numbers)d:%(click_by_voice_options)s") +
              Key("enter"),
              rdescript="click link with click by voice options"),
        "hide hints":
            R(Key("cs-space/30") + Text(":-") + Key("enter"),
              rdescript="hide click by voice hints (i.e. numbers)"),
        "show hints":
            R(Key("cs-space/30") + Text(":+") + Key("enter"),
              rdescript="show click by voice hints (i.e. numbers)"),
    }
    extras = [
        Choice(
            "click_by_voice_options",
            {
                "go": "f",
                "click": "c",
                "push": "b",  # open as new tab but don't go to it
                "tab": "t",  # open as new tab and go to it
                "window": "w",
                "hover": "h",
                "link": "k",
                "copy": "s",
            }),
        Choice("nth", {
            "first": "1",
            "second": "2",
            "third": "3",
            "fourth": "4",
            "fifth": "5",
            "sixth": "6",
            "seventh": "7",
            "eighth": "8",
            "ninth": "9",
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
