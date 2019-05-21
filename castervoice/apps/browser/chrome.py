#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Chrome

"""
# ---------------------------------------------------------------------------

from dragonfly import (Grammar, Repeat,
                       Mouse, Pause)

import Browser
from castervoice.apps.browser.ChromeAndFirefox import ChromeAndFirefox
from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.temporary import Store, Retrieve


class ChromeRule(ChromeAndFirefox):
    pronunciation = "google chrome"

    _mapping = {
        Browser.OPEN_NEW_WINDOW:
            R(Key("c-n")),
        Browser.OPEN_NEW_INCOGNITO_WINDOW:
            R(Key("cs-n")),
        Browser.PREVIOUS_TAB_N_TIMES:
            R(Key("cs-tab")) * Repeat(extra="n"),
        Browser.SWITCH_TO_NTH_TAB:
            R(Key("c-%(nth)s")),
        Browser.SWITCH_TO_LAST_TAB:
            R(Key("c-9")),
        Browser.SWITCH_TO_SECOND_TO_LAST_TAB:
            R(Key("c-9, cs-tab")),
        "switch focus [<n>]":
            R(Key("f6/20")) * Repeat(extra="n"),
        Browser.TOGGLE_BOOKMARK_TOOLBAR:
            R(Key("cs-b")),
        "switch user":
            R(Key("cs-m")),
        "focus notification":
            R(Key("a-n")),
        "allow notification":
            R(Key("as-a")),
        "deny notification":
            R(Key("as-a")),
        "google that":
            R(Store(remove_cr=True) + Key("c-t") + Retrieve() + Key("enter")),
        "wikipedia that":
            R(Store(space="+", remove_cr=True) + Key("c-t") + Text(
                "https://en.wikipedia.org/w/index.php?search=") + Retrieve() + Key("enter")),
        Browser.SHOW_EXTENSIONS:
            R(Key("a-f/20, l, e/15, enter")),
        "more tools":
            R(Key("a-f/5, l")),
    }
    mapping = ChromeAndFirefox.merge_dictionaries(_mapping, ChromeAndFirefox.chromeAndFirefoxMapping)
    extras = Browser.EXTRAS
    defaults = {"n": 1, "dict": "", "click_by_voice_options": "c"}


# ---------------------------------------------------------------------------

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
