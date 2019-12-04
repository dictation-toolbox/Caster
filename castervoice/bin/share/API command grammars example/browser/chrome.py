# pylint: skip-file
from dragonfly import Repeat, MappingRule

import browser_shared
from castervoice.lib.actions import Key
from castervoice.rules.apps.browser.browser_shared_commands import BrowserSharedCommands
from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R
from castervoice.lib.temporary import Store, Retrieve


class ChromeRule(MappingRule):
    _mapping = {
        browser_shared.PREVIOUS_TAB_N_TIMES:
            R(Key("cs-tab")) * Repeat(extra="n"),
        browser_shared.SWITCH_TO_TAB_N:
            R(Key("c-%(m)s%(nth)s")),
        browser_shared.SWITCH_TO_LAST_TAB:
            R(Key("c-9")),
        browser_shared.SWITCH_TO_SECOND_TO_LAST_TAB:
            R(Key("c-9, cs-tab")),
        "switch focus [<n>]":
            R(Key("f6/20")) * Repeat(extra="n"),
        browser_shared.TOGGLE_BOOKMARK_TOOLBAR:
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
        browser_shared.SHOW_EXTENSIONS:
            R(Key("a-f/20, l, e/15, enter")),
        "more tools":
            R(Key("a-f/5, l")),
    }
    mapping = BrowserSharedCommands.merge_dictionaries(_mapping, BrowserSharedCommands.chromeAndFirefoxMapping)
    extras = browser_shared.get_extras()
    defaults = browser_shared.get_defaults()


#def get_rule():
#    return ChromeRule, RuleDetails(name="google chrome", executable="chrome")
