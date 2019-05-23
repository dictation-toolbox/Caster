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

import browser
from castervoice.apps.browser.browser_shared_commands import BrowserSharedCommands
from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.temporary import Store, Retrieve


class ChromeRule(BrowserSharedCommands):
    pronunciation = "google chrome"

    _mapping = {
        browser.OPEN_NEW_WINDOW:
            R(Key("c-n")),
        browser.OPEN_NEW_INCOGNITO_WINDOW:
            R(Key("cs-n")),
        browser.PREVIOUS_TAB_N_TIMES:
            R(Key("cs-tab")) * Repeat(extra="n"),
        browser.SWITCH_TO_TAB_N:
            R(Key("c-%(m)s%(nth)s")),
        browser.SWITCH_TO_LAST_TAB:
            R(Key("c-9")),
        browser.SWITCH_TO_SECOND_TO_LAST_TAB:
            R(Key("c-9, cs-tab")),
        "switch focus [<n>]":
            R(Key("f6/20")) * Repeat(extra="n"),
        browser.TOGGLE_BOOKMARK_TOOLBAR:
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
        browser.SHOW_EXTENSIONS:
            R(Key("a-f/20, l, e/15, enter")),
        "more tools":
            R(Key("a-f/5, l")),
    }
    mapping = BrowserSharedCommands.merge_dictionaries(_mapping, BrowserSharedCommands.chromeAndFirefoxMapping)
    extras = browser.EXTRAS
    defaults = browser.DEFAULTS


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
