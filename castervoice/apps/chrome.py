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
from castervoice.lib.temporary import Store, Retrieve
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class ChromeRule(MergeRule):
    pronunciation = "google chrome"
    mapping = {
        "new window":
            R(Key("c-n")),
        "(new incognito window | incognito)":
            R(Key("cs-n")),
        "new tab [<n>]":
            R(Key("c-t")*Repeat(extra="n")),
        "reopen tab [<n>]":
            R(Key("cs-t"))*Repeat(extra="n"),
        "close tab [<n>]":
            R(Key("c-w"))*Repeat(extra='n'),
        "close all tabs":
            R(Key("cs-w")),
        "next tab [<n>]":
            R(Key("c-tab"))*Repeat(extra="n"),
        "previous tab [<n>]":
            R(Key("cs-tab"))*Repeat(extra="n"),
        "new tab that":
            R(Mouse("middle") + Pause("20") + Key("c-tab")),
        "<nth> tab":
            R(Key("c-%(nth)s") ),
        "last tab":
            R(Key("c-9")),
        "second last tab":
            R(Key("c-9, cs-tab")),
        "go back [<n>]":
            R(Key("a-left/20"))*Repeat(extra="n"),
        "go forward [<n>]":
            R(Key("a-right/20"))*Repeat(extra="n"),
        "zoom in [<n>]":
            R(Key("c-plus/20"))*Repeat(extra="n"),
        "zoom out [<n>]":
            R(Key("c-minus/20"))*Repeat(extra="n"),
        "zoom reset":
            R(Key("c-0")),
        "super refresh":
            R(Key("c-f5")),
        "switch focus [<n>]":
            R(Key("f6/20"))*Repeat(extra="n"),
        "[find] next match [<n>]":
            R(Key("c-g/20"))*Repeat(extra="n"),
        "[find] prior match [<n>]":
            R(Key("cs-g/20"))*Repeat(extra="n"),
        "[toggle] caret browsing":
            R(Key("f7")),
              # now available through an add on, was a standard feature
        "home page":
            R(Key("a-home")),
        "[show] history":
            R(Key("c-h")),
        "address bar":
            R(Key("c-l")),
        "show downloads":
            R(Key("c-j")),
        "add bookmark":
            R(Key("c-d")),
        "bookmark all tabs":
            R(Key("cs-d")),
        "[toggle] bookmark bar":
            R(Key("cs-b")),
        "[show] bookmarks":
            R(Key("cs-o")),
        "switch user":
            R(Key("cs-m")),
        "chrome task manager":
            R(Key("s-escape")),
        "[toggle] full-screen":
            R(Key("f11")),
        "focus notification":
            R(Key("a-n")),
        "allow notification":
            R(Key("as-a")),
        "deny notification":
            R(Key("as-a")),
        "developer tools":
            R(Key("f12")),
        "view [page] source":
            R(Key("c-u")),
        "resume":
            R(Key("f8")),
        "step over":
            R(Key("f10")),
        "step into":
            R(Key("f11")),
        "step out":
            R(Key("s-f11")),

        "IRC identify":
            R(Text("/msg NickServ identify PASSWORD")),

        "google that":
            R(Store(remove_cr=True) + Key("c-t") + Retrieve() + Key("enter")),

        "wikipedia that":
            R(Store(space="+", remove_cr=True) + Key("c-t") + Text("https://en.wikipedia.org/w/index.php?search=") + Retrieve() + Key("enter")),

        "duplicate tab":
            R(Key("a-d,a-c,c-t/15,c-v/15, enter")),
        "duplicate window":
            R(Key("a-d,a-c,c-n/15,c-v/15, enter")),
        "extensions":
            R(Key("a-f/20, l, e/15, enter")),
        "(menu | three dots)":
            R(Key("a-f")),
        "settings":
            R(Key("a-f/5, s")),
        "downloads":
            R(Key("c-j")),
        "chrome task manager":
            R(Key("s-escape")),
        "clear browsing data":
            R(Key("cs-del")),
        "developer tools":
            R(Key("cs-i")),
        "more tools":
            R(Key("a-f/5, l")),
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
