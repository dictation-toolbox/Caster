# pylint: skip-file
from dragonfly import Repeat, MappingRule

import browser_shared
from castervoice.lib.actions import Key
from castervoice.rules.apps.browser.browser_shared_commands import BrowserSharedCommands
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class FirefoxRule(MappingRule):
    _mapping = {
        browser_shared.PREVIOUS_TAB_N_TIMES:
            # control shift tab doesn't work and this appears to be an undocumented workaround
            R(Key("c-tab/30")) * Repeat(extra="n"),
        browser_shared.FIND_NEXT_MATCH:
            R(Key("c-g/20")) * Repeat(extra="n"),
        browser_shared.TOGGLE_BOOKMARK_TOOLBAR:
            R(Key("c-b")),
        browser_shared.SHOW_EXTENSIONS:
            R(Key("a-a, l, e/15, enter")),
    }
    mapping = BrowserSharedCommands.merge_dictionaries(_mapping, BrowserSharedCommands.chromeAndFirefoxMapping)
    extras = browser_shared.get_extras()
    defaults = browser_shared.get_defaults()


#def get_rule():
#    return FirefoxRule, RuleDetails(name="fire fox", executable="firefox")
