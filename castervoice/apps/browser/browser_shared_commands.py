#
# __author__ = "lexxish"
#
from castervoice.lib.imports import *

from castervoice.apps.browser import browser
from castervoice.lib import github_automation


class BrowserSharedCommands(MergeRule):

    @staticmethod
    def merge_dictionaries(x, y):
        z = x.copy()
        z.update(y)
        return z

    chromeAndFirefoxMapping = {
        browser.OPEN_NEW_WINDOW:
            R(Key("c-n")),
        browser.OPEN_NEW_INCOGNITO_WINDOW:
            R(Key("cs-n")),
        browser.NEW_TAB_N_TIMES:
            R(Key("c-t") * Repeat(extra="n")),
        browser.REOPEN_TAB_N_TIMES:
            R(Key("cs-t")) * Repeat(extra="n"),
        browser.CLOSE_TAB_N_TIMES:
            R(Key("c-w")) * Repeat(extra='n'),
        browser.CLOSE_WINDOW:
            R(Key("cs-w")),
        browser.NEXT_TAB_N_TIMES:
            R(Key("c-tab")) * Repeat(extra="n"),
        browser.OPEN_NEW_TAB_BASED_ON_CURSOR:
            R(Mouse("middle") + Pause("20") + Key("c-tab")),
        browser.GO_BACK_N_TIMES:
            R(Key("a-left/20")) * Repeat(extra="n"),
        browser.GO_FORWARD_N_TIMES:
            R(Key("a-right/20")) * Repeat(extra="n"),
        browser.ZOOM_IN_N_TIMES:
            R(Key("c-plus/20")) * Repeat(extra="n"),
        browser.ZOOM_OUT_N_TIMES:
            R(Key("c-minus/20")) * Repeat(extra="n"),
        browser.ZOOM_RESET_DEFAULT:
            R(Key("c-0")),
        browser.FORCE_HARD_REFRESH:
            R(Key("c-f5")),
        browser.FIND_NEXT_MATCH:
            R(Key("c-g/20")) * Repeat(extra="n"),
        browser.FIND_PREVIOUS_MATCH:
            R(Key("cs-g/20")) * Repeat(extra="n"),
        # requires an extension in some browsers such as chrome
        browser.TOGGLE_CARET_BROWSING:
            R(Key("f7")),
        browser.GO_TO_HOMEPAGE:
            R(Key("a-home")),
        browser.SHOW_HISTORY:
            R(Key("c-h")),
        browser.SELECT_ADDRESS_BAR:
            R(Key("c-l")),
        browser.SHOW_DOWNLOADS:
            R(Key("c-j")),
        browser.ADD_BOOKMARK:
            R(Key("c-d")),
        browser.BOOKMARK_ALL_TABS:
            R(Key("cs-d")),
        browser.SHOW_BOOKMARKS:
            R(Key("cs-o")),
        browser.TOGGLE_FULL_SCREEN:
            R(Key("f11")),
        browser.SHOW_PAGE_SOURCE:
            R(Key("c-u")),
        browser.DEBUG_RESUME:
            R(Key("f8")),
        browser.DEBUG_STEP_OVER:
            R(Key("f10")),
        browser.DEBUG_STEP_INTO:
            R(Key("f11")),
        browser.DEBUG_STEP_OUT:
            R(Key("s-f11")),
        browser.DUPLICATE_TAB:
            R(Key("a-d,a-c,c-t/15,c-v/15, enter")),
        browser.DUPLICATE_WINDOW:
            R(Key("a-d,a-c,c-n/15,c-v/15, enter")),
        browser.SHOW_MENU:
            R(Key("a-f")),
        browser.SHOW_SETTINGS:
            R(Key("a-f/5, s")),
        browser.SHOW_TASK_MANAGER:
            R(Key("s-escape")),
        browser.CLEAR_BROWSING_DATA:
            R(Key("cs-del")),
        browser.SHOW_DEVELOPER_TOOLS:
            R(Key("cs-i")),
        browser.CHECKOUT_PR:
            R(Function(github_automation.github_checkoutupdate_pull_request, new=True)),
        browser.UPDATE_PR:
            R(Function(github_automation.github_checkoutupdate_pull_request, new=False)),
        "IRC identify":
            R(Text("/msg NickServ identify PASSWORD")),
    }
