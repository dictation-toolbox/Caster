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
import Browser as Browser

class ChromeRule(MergeRule):
    pronunciation = "google chrome"

    mapping = {
        Browser.OPEN_NEW_WINDOW:
            R(Key("c-n")),
        Browser.OPEN_NEW_INCOGNITO_WINDOW:
            R(Key("cs-n")),
        Browser.NEW_TAB_N_TIMES:
            R(Key("c-t")*Repeat(extra="n")),
        Browser.REOPEN_TAB_N_TIMES:
            R(Key("cs-t"))*Repeat(extra="n"),
        Browser.CLOSE_TAB_N_TIMES:
            R(Key("c-w"))*Repeat(extra='n'),
        Browser.CLOSE_ALL_TABS:
            R(Key("cs-w")),
        Browser.NEXT_TAB_N_TIMES:
            R(Key("c-tab"))*Repeat(extra="n"),
        Browser.PREVIOUS_TAB_N_TIMES:
            R(Key("cs-tab"))*Repeat(extra="n"),
        Browser.OPEN_NEW_TAB_BASED_ON_CURSOR:
            R(Mouse("middle") + Pause("20") + Key("c-tab")),
        Browser.SWITCH_TO_NTH_TAB:
            R(Key("c-%(nth)s") ),
        Browser.SWITCH_TO_LAST_TAB:
            R(Key("c-9")),
        Browser.SWITCH_TO_SECOND_TO_LAST_TAB:
            R(Key("c-9, cs-tab")),
        Browser.GO_BACK_N_TIMES:
            R(Key("a-left/20"))*Repeat(extra="n"),
        Browser.GO_FORWARD_N_TIMES:
            R(Key("a-right/20"))*Repeat(extra="n"),
        Browser.ZOOM_IN_N_TIMES:
            R(Key("c-plus/20"))*Repeat(extra="n"),
        Browser.ZOOM_OUT_N_TIMES:
            R(Key("c-minus/20"))*Repeat(extra="n"),
        Browser.ZOOM_RESET_DEFAULT:
            R(Key("c-0")),
        Browser.FORCE_HARD_REFRESH:
            R(Key("c-f5")),
        "switch focus [<n>]":
            R(Key("f6/20"))*Repeat(extra="n"),
        Browser.FIND_NEXT_MATCH:
            R(Key("c-g/20"))*Repeat(extra="n"),
        Browser.FIND_PREVIOUS_MATCH:
            R(Key("cs-g/20"))*Repeat(extra="n"),
        Browser.TOGGLE_CARET_BROWSING:
            R(Key("f7")),
              # now available through an add on, was a standard feature
        Browser.GO_TO_HOMEPAGE:
            R(Key("a-home")),
        Browser.SHOW_HISTORY:
            R(Key("c-h")),
        Browser.SELECT_ADDRESS_BAR:
            R(Key("c-l")),
        Browser.SHOW_DOWNLOADS:
            R(Key("c-j")),
        Browser.ADD_BOOKMARK:
            R(Key("c-d")),
        Browser.BOOKMARK_ALL_TABS:
            R(Key("cs-d")),
        Browser.TOGGLE_BOOKMARK_TOOLBAR:
            R(Key("cs-b")),
        Browser.SHOW_BOOKMARKS:
            R(Key("cs-o")),
        "switch user":
            R(Key("cs-m")),
        Browser.TOGGLE_FULL_SCREEN:
            R(Key("f11")),
        "focus notification":
            R(Key("a-n")),
        "allow notification":
            R(Key("as-a")),
        "deny notification":
            R(Key("as-a")),
        Browser.SHOW_PAGE_SOURCE:
            R(Key("c-u")),
        Browser.DEBUG_RESUME:
            R(Key("f8")),
        Browser.DEBUG_STEP_OVER:
            R(Key("f10")),
        Browser.DEBUG_STEP_INTO:
            R(Key("f11")),
        Browser.DEBUG_STEP_OUT:
            R(Key("s-f11")),

        "IRC identify":
            R(Text("/msg NickServ identify PASSWORD")),

        "google that":
            R(Store(remove_cr=True) + Key("c-t") + Retrieve() + Key("enter")),

        "wikipedia that":
            R(Store(space="+", remove_cr=True) + Key("c-t") + Text("https://en.wikipedia.org/w/index.php?search=") + Retrieve() + Key("enter")),

        Browser.DUPLICATE_TAB:
            R(Key("a-d,a-c,c-t/15,c-v/15, enter")),
        Browser.DUPLICATE_WINDOW:
            R(Key("a-d,a-c,c-n/15,c-v/15, enter")),
        Browser.SHOW_EXTENSIONS:
            R(Key("a-f/20, l, e/15, enter")),
        Browser.SHOW_MENU:
            R(Key("a-f")),
        Browser.SHOW_SETTINGS:
            R(Key("a-f/5, s")),
        Browser.SHOW_TASK_MANAGER:
            R(Key("s-escape")),
        Browser.CLEAR_BROWSING_DATA:
            R(Key("cs-del")),
        Browser.SHOW_DEVELOPER_TOOLS:
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
