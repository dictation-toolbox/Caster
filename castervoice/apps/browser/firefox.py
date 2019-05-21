#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Firefox

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, Repeat)

import browser
from castervoice.apps.browser.chrome_and_firefox import ChromeAndFirefox
from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.state.short import R


class FirefoxRule(ChromeAndFirefox):
    pronunciation = "fire fox"

    _mapping = {
        browser.PREVIOUS_TAB_N_TIMES:
            # control shift tab doesn't work and this appears to be an undocumented work new tab that new tab that around
            R(Key("c-tab/30")) * Repeat(extra="n"),
        browser.SWITCH_TO_NTH_TAB:
            R(Key("c-%(nth)")),
        browser.FIND_NEXT_MATCH:
            R(Key("c-g/20")) * Repeat(extra="n"),
        browser.TOGGLE_BOOKMARK_TOOLBAR:
            R(Key("c-b")),
        browser.SHOW_EXTENSIONS:
            R(Key("a-a, l, e/15, enter")),
    }
    mapping = ChromeAndFirefox.merge_dictionaries(_mapping, ChromeAndFirefox.chromeAndFirefoxMapping)
    extras = ChromeAndFirefox.EXTRAS
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
