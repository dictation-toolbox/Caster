from castervoice.lib.imports import *

import browser
from castervoice.apps.browser.browser_shared_commands import BrowserSharedCommands


class ChromeRule(BrowserSharedCommands):
    pronunciation = "google chrome"

    _mapping = {
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


context = AppContext(executable="chrome")
control.non_ccr_app_rule(ChromeRule(), context=context)