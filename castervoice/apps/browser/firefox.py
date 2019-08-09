from dragonfly import Key, Repeat

import browser
from castervoice.apps.browser.browser_shared_commands import BrowserSharedCommands
from castervoice.lib.ctrl.mgr import rdcommon
from castervoice.lib.merge.state.short import R


class FirefoxRule(BrowserSharedCommands):
    pronunciation = "fire fox"

    _mapping = {
        browser.PREVIOUS_TAB_N_TIMES:
            # control shift tab doesn't work and this appears to be an undocumented workaround
            R(Key("c-tab/30")) * Repeat(extra="n"),
        browser.FIND_NEXT_MATCH:
            R(Key("c-g/20")) * Repeat(extra="n"),
        browser.TOGGLE_BOOKMARK_TOOLBAR:
            R(Key("c-b")),
        browser.SHOW_EXTENSIONS:
            R(Key("a-a, l, e/15, enter")),
    }
    mapping = BrowserSharedCommands.merge_dictionaries(_mapping, BrowserSharedCommands.chromeAndFirefoxMapping)
    extras = browser.EXTRAS
    defaults = browser.DEFAULTS


def get_rule():
    return FirefoxRule, rdcommon.app_executable("firefox")
