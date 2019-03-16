#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Chrome and Firefox

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, Dictation, Repeat)

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

    mapping = { # most keybinds are taken from https://support.google.com/chrome/answer/157179?hl=en
        "[new] incognito window":       R(Key("cs-n"), rdescript="Chrome: New Incognito Window"),
        "new tab [<n>]":                R(Key("c-t"), rdescript="Chrome: New Tab") * Repeat(extra="n"),
        "reopen tab [<n>]":             R(Key("cs-t"), rdescript="Chrome: Reopen Tab") * Repeat(extra="n"),
        "close all tabs":               R(Key("cs-w"), rdescript="Chrome: Close All Tabs"),

        "go back [<n>]":                R(Key("a-left/20"), rdescript="Chrome: Navigate History Backward") * Repeat(extra="n"),
        "go forward [<n>]":             R(Key("a-right/20"), rdescript="Chrome: Navigate History Forward") * Repeat(extra="n"),
        "zoom in [<n>]":                R(Key("c-plus/20"), rdescript="Chrome: Zoom In") * Repeat(extra="n"),
        "zoom out [<n>]":               R(Key("c-minus/20"), rdescript="Chrome: Zoom") * Repeat(extra="n"),
        "zoom reset":                   R(Key("c-0"), rdescript="Chrome: Reset Zoom"),
        "super refresh":                R(Key("c-f5"), rdescript="Chrome: Super Refresh"),
        "switch focus [<n>]":           R(Key("f6/20"), rdescript="Chrome: Switch Focus") * Repeat(extra="n"),
        "[find] next match [<n>]":      R(Key("c-g/20"), rdescript="Chrome: Next Match") * Repeat(extra="n"),
        "[find] prior match [<n>]":     R(Key("cs-g/20"), rdescript="Chrome: Prior Match") * Repeat(extra="n"),
        "[toggle] caret browsing":      R(Key("f7"), rdescript="Chrome: Caret Browsing"), # now available through an add on, was a standard feature

        "home page":                    R(Key("a-home"), rdescript="Chrome: Home Page"),
        "show history":                 R(Key("c-h"), rdescript="Chrome: Show History"),
        "address bar":                  R(Key("c-l"), rdescript="Chrome: Address Bar"),
        "show downloads":               R(Key("c-j"), rdescript="Chrome: Show Downloads"),
        "[add] bookmark":               R(Key("c-d"), rdescript="Chrome: Add Bookmark"),
        "bookmark all tabs":            R(Key("cs-d"), rdescript="Chrome: Bookmark All Tabs"),
        "[toggle] bookmark bar":        R(Key("cs-b"), rdescript="Chrome: Toggle Bookmark Bar"),
        "show bookmarks":               R(Key("cs-o"), rdescript="Chrome: Show Bookmarks"),
        "switch user":                  R(Key("cs-m"), rdescript="Chrome: Switch User"),
        "chrome task manager":          R(Key("s-escape"), rdescript="Chrome: Chrome Task Manager"),
        "[toggle] full-screen":         R(Key("f11"), rdescript="Chrome: Toggle Fullscreen Mode"),
        "focus notification":           R(Key("a-n"), rdescript="Chrome: Focus Notification"),
        "allow notification":           R(Key("as-a"), rdescript="Chrome: Allow Notification"),
        "deny notification":            R(Key("as-a"), rdescript="Chrome: Deny Notification"),

        "developer tools":              R(Key("f12"), rdescript="Chrome: Developer Tools"),
        "view [page] source":           R(Key("c-u"), rdescript="Chrome: View Page Source"),
        "resume":                       R(Key("f8"), rdescript="Chrome: Resume"),
        "step over":                    R(Key("f10"), rdescript="Chrome: Step Over"),
        "step into":                    R(Key("f11"), rdescript="Chrome: Step Into"),
        "step out":                     R(Key("s-f11"), rdescript="Chrome: Step Out"),

        "IRC identify":                 R(Text("/msg NickServ identify PASSWORD"), rdescript="Chrome: IRC Chat Channel Identify"),
        }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 10),
    ]
    defaults = {"n": 1, "dict": "nothing"}


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
