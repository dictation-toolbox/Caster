#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Firefox

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, Dictation, Repeat, Mouse, Pause)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
import Browser


class FirefoxRule(MergeRule):
    pronunciation = "fire fox"

    mapping = {
        Browser.OPEN_NEW_WINDOW:
            R(Key("c-n")),
        Browser.OPEN_NEW_INCOGNITO_WINDOW:
            R(Key("cs-p")),
        Browser.NEW_TAB_N_TIMES:
            R(Key("c-t") * Repeat(extra="n")),
        Browser.REOPEN_TAB_N_TIMES:
            R(Key("cs-t")) * Repeat(extra="n"),
        Browser.CLOSE_TAB_N_TIMES:
            R(Key("c-w")) * Repeat(extra='n'),
        Browser.CLOSE_ALL_TABS:
            R(Key("cs-w")),
        Browser.NEXT_TAB_N_TIMES:
            R(Key("c-tab")) * Repeat(extra="n"),
        Browser.PREVIOUS_TAB_N_TIMES:
            # control shift tab doesn't work and this appears to be an undocumented work new tab that new tab that around
            R(Key("c-tab/30")) * Repeat(extra="n"),
        Browser.OPEN_NEW_TAB_BASED_ON_CURSOR:
            R(Mouse("middle") + Pause("20") + Key("c-tab")),
        Browser.SWITCH_TO_NTH_TAB:
            R(Key("c-%(nth)")),
        Browser.GO_BACK_N_TIMES:
            R(Key("a-left/20")) * Repeat(extra="n"),
        Browser.GO_FORWARD_N_TIMES:
            R(Key("a-right/20")) * Repeat(extra="n"),
        Browser.ZOOM_IN_N_TIMES:
            R(Key("c-plus/20")) * Repeat(extra="n"),
        Browser.ZOOM_OUT_N_TIMES:
            R(Key("c-minus/20")) * Repeat(extra="n"),
        Browser.ZOOM_RESET_DEFAULT:
            R(Key("c-0")),
        Browser.FORCE_HARD_REFRESH:
            R(Key("c-f5")),
        Browser.FIND_NEXT_MATCH:
            R(Key("c-g/20")) * Repeat(extra="n"),
        Browser.FIND_PREVIOUS_MATCH:
            R(Key("cs-g/20")) * Repeat(extra="n"),
        Browser.TOGGLE_CARET_BROWSING:
            R(Key("f7")),
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
            R(Key("c-b")),
        Browser.SHOW_BOOKMARKS:
            R(Key("cs-o")),
        Browser.TOGGLE_FULL_SCREEN:
            R(Key("f11")),
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
        Browser.DUPLICATE_TAB:
            R(Key("a-d,a-c,c-t/15,c-v/15, enter")),
        Browser.DUPLICATE_WINDOW:
            R(Key("a-d,a-c,c-n/15,c-v/15, enter")),
        Browser.SHOW_EXTENSIONS:
            R(Key("as-a, l, e/15, enter")),
        Browser.SHOW_SETTINGS:
            R(Key("a-t/5, o, enter")),
        Browser.CLEAR_BROWSING_DATA:
            R(Key("cs-del")),
        Browser.SHOW_DEVELOPER_TOOLS:
            R(Key("cs-i")),
        "IRC identify":
            R(Text("/msg NickServ identify PASSWORD"),
              rdescript="FireFox: IRC Chat Channel Identify"),
    }
    extras = Browser.EXTRAS
    defaults = {"n": 1, "dict": "nothing"}


#---------------------------------------------------------------------------

context = AppContext(executable="firefox")
grammar = Grammar("firefox", context=context)

if settings.SETTINGS["apps"]["firefox"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(FirefoxRule())
    else:
        rule = FirefoxRule(name="firefox")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
