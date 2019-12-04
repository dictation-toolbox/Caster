#
# __author__ = "lexxish"
#
# pylint: skip-file
from dragonfly import Repeat, Pause, Function

from castervoice.lib.actions import Key, Mouse
from castervoice.rules.apps.browser import browser_shared
from castervoice.lib import github_automation
from castervoice.lib.actions import Text
from castervoice.lib.merge.state.short import R


class BrowserSharedCommands(object):

    @staticmethod
    def merge_dictionaries(x, y):
        z = x.copy()
        z.update(y)
        return z

    chromeAndFirefoxMapping = {
        browser_shared.OPEN_NEW_WINDOW:
            R(Key("c-n")),
        browser_shared.OPEN_NEW_INCOGNITO_WINDOW:
            R(Key("cs-n")),
        browser_shared.NEW_TAB_N_TIMES:
            R(Key("c-t") * Repeat(extra="n")),
        browser_shared.REOPEN_TAB_N_TIMES:
            R(Key("cs-t")) * Repeat(extra="n"),
        browser_shared.CLOSE_TAB_N_TIMES:
            R(Key("c-w")) * Repeat(extra='n'),
        browser_shared.CLOSE_WINDOW:
            R(Key("cs-w")),
        browser_shared.NEXT_TAB_N_TIMES:
            R(Key("c-tab")) * Repeat(extra="n"),
        browser_shared.OPEN_NEW_TAB_BASED_ON_CURSOR:
            R(Mouse("middle") + Pause("20") + Key("c-tab")),
        browser_shared.GO_BACK_N_TIMES:
            R(Key("a-left/20")) * Repeat(extra="n"),
        browser_shared.GO_FORWARD_N_TIMES:
            R(Key("a-right/20")) * Repeat(extra="n"),
        browser_shared.ZOOM_IN_N_TIMES:
            R(Key("c-plus/20")) * Repeat(extra="n"),
        browser_shared.ZOOM_OUT_N_TIMES:
            R(Key("c-minus/20")) * Repeat(extra="n"),
        browser_shared.ZOOM_RESET_DEFAULT:
            R(Key("c-0")),
        browser_shared.FORCE_HARD_REFRESH:
            R(Key("c-f5")),
        browser_shared.FIND_NEXT_MATCH:
            R(Key("c-g/20")) * Repeat(extra="n"),
        browser_shared.FIND_PREVIOUS_MATCH:
            R(Key("cs-g/20")) * Repeat(extra="n"),
        # requires an extension in some browsers such as chrome
        browser_shared.TOGGLE_CARET_BROWSING:
            R(Key("f7")),
        browser_shared.GO_TO_HOMEPAGE:
            R(Key("a-home")),
        browser_shared.SHOW_HISTORY:
            R(Key("c-h")),
        browser_shared.SELECT_ADDRESS_BAR:
            R(Key("c-l")),
        browser_shared.SHOW_DOWNLOADS:
            R(Key("c-j")),
        browser_shared.ADD_BOOKMARK:
            R(Key("c-d")),
        browser_shared.BOOKMARK_ALL_TABS:
            R(Key("cs-d")),
        browser_shared.SHOW_BOOKMARKS:
            R(Key("cs-o")),
        browser_shared.TOGGLE_FULL_SCREEN:
            R(Key("f11")),
        browser_shared.SHOW_PAGE_SOURCE:
            R(Key("c-u")),
        browser_shared.DEBUG_RESUME:
            R(Key("f8")),
        browser_shared.DEBUG_STEP_OVER:
            R(Key("f10")),
        browser_shared.DEBUG_STEP_INTO:
            R(Key("f11")),
        browser_shared.DEBUG_STEP_OUT:
            R(Key("s-f11")),
        browser_shared.DUPLICATE_TAB:
            R(Key("a-d,a-c,c-t/15,c-v/15, enter")),
        browser_shared.DUPLICATE_WINDOW:
            R(Key("a-d,a-c,c-n/15,c-v/15, enter")),
        browser_shared.SHOW_MENU:
            R(Key("a-f")),
        browser_shared.SHOW_SETTINGS:
            R(Key("a-f/5, s")),
        browser_shared.SHOW_TASK_MANAGER:
            R(Key("s-escape")),
        browser_shared.CLEAR_BROWSING_DATA:
            R(Key("cs-del")),
        browser_shared.SHOW_DEVELOPER_TOOLS:
            R(Key("cs-i")),
        browser_shared.CHECKOUT_PR:
            R(Function(github_automation.github_checkoutupdate_pull_request, new=True)),
        browser_shared.UPDATE_PR:
            R(Function(github_automation.github_checkoutupdate_pull_request, new=False)),
        "IRC identify":
            R(Text("/msg NickServ identify PASSWORD")),
    }
