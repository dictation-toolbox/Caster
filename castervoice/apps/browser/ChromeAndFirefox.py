#
# __author__ = "lexxish"
#
from dragonfly import Key, Mouse, Repeat, Pause

from castervoice.apps.browser import Browser
from castervoice.lib.actions import Text
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class ChromeAndFirefox(MergeRule):

    @staticmethod
    def merge_dictionaries(x, y):
        z = x.copy()
        z.update(y)
        return z

    chromeAndFirefoxMapping = {
        Browser.OPEN_NEW_WINDOW:
            R(Key("c-n")),
        Browser.OPEN_NEW_INCOGNITO_WINDOW:
            R(Key("cs-n")),
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
        Browser.OPEN_NEW_TAB_BASED_ON_CURSOR:
            R(Mouse("middle") + Pause("20") + Key("c-tab")),
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
        # requires an extension in some browsers such as chrome
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
        Browser.SHOW_MENU:
            R(Key("a-f")),
        Browser.SHOW_SETTINGS:
            R(Key("a-f/5, s")),
        Browser.SHOW_TASK_MANAGER:
            R(Key("s-escape")),
        Browser.CLEAR_BROWSING_DATA:
            R(Key("cs-del")),
        Browser.SHOW_DEVELOPER_TOOLS:
            R(Key("cs-i")),
        "IRC identify":
            R(Text("/msg NickServ identify PASSWORD")),
    }