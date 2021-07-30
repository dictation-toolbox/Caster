# pylint: skip-file
#
# __author__ = "lexxish"
#
from dragonfly import Choice, ShortIntegerRef

from castervoice.rules.apps.shared.directions import FORWARD, RIGHT, BACK, LEFT

OPEN_NEW_WINDOW = "(new window|win new)"
OPEN_NEW_INCOGNITO_WINDOW = "(new incognito window | incognito)"
CLOSE_WINDOW = "win close|close all tabs"
NEW_TAB_N_TIMES = "new tab [<n>]|tab new [<n>]"
REOPEN_TAB_N_TIMES = "reopen tab [<n>]|tab reopen [<n>]"
CLOSE_TAB_N_TIMES = "close tab [<n>]|tab close [<n>]"
NEXT_TAB_N_TIMES = "%s tab [<n>]|tab %s [<n>]" % (FORWARD, RIGHT)
PREVIOUS_TAB_N_TIMES = "%s tab [<n>]|tab %s [<n>]" % (BACK, LEFT)
OPEN_NEW_TAB_BASED_ON_CURSOR = "new tab that"
SWITCH_TO_TAB_N = "tab <m>|<nth> tab"
SWITCH_TO_LAST_TAB = "last tab"
SWITCH_TO_SECOND_TO_LAST_TAB = "second last tab"
GO_FORWARD_N_TIMES = "go %s [<n>]" % FORWARD
GO_BACK_N_TIMES = "go %s [<n>]" % BACK
ZOOM_IN_N_TIMES = "zoom in [<n>]"
ZOOM_OUT_N_TIMES = "zoom out [<n>]"
ZOOM_RESET_DEFAULT = "zoom reset"
FORCE_HARD_REFRESH = "(hard refresh|super refresh)"
FIND_NEXT_MATCH = "find %s [match] [<n>]" % FORWARD
FIND_PREVIOUS_MATCH = "find %s [match] [<n>]" % BACK
TOGGLE_CARET_BROWSING = "[toggle] caret browsing"
GO_TO_HOMEPAGE = "[go] home [page]"
SHOW_HISTORY = "[show] history"
SELECT_ADDRESS_BAR = "address bar"
SHOW_DOWNLOADS = "[show] downloads"
ADD_BOOKMARK = "[add] bookmark"
BOOKMARK_ALL_TABS = "bookmark all [tabs]"
TOGGLE_BOOKMARK_TOOLBAR = "[toggle] bookmark bar"
SHOW_BOOKMARKS = "[show] bookmarks"
TOGGLE_FULL_SCREEN = "[toggle] full screen"
SHOW_PAGE_SOURCE = "(show|view) page source"
DEBUG_RESUME = "resume"
DEBUG_STEP_OVER = "step over"
DEBUG_STEP_INTO = "step into"
DEBUG_STEP_OUT = "step out"
DUPLICATE_TAB = "(duplicate tab|tab duple)"
DUPLICATE_WINDOW = "(duplicate window|win duple)"
SHOW_EXTENSIONS = "[show] (extensions|plugins)"
SHOW_MENU = "[show] (menu | three dots)"
SHOW_SETTINGS = "[show] settings"
SHOW_TASK_MANAGER = "[show chrome] task manager"
CLEAR_BROWSING_DATA = "(clear history|clear browsing data)"
SHOW_DEVELOPER_TOOLS = "[show] developer tools"
CHECKOUT_PR = "checkout [this] pull request [locally]"
UPDATE_PR = "update [this] pull request [locally]"


def get_defaults():
    return {"n": 1, "m":"", "nth": ""}


def get_extras():
    return [
        Choice("nth", {
            "first": "1",
            "second": "2",
            "third": "3",
            "fourth": "4",
            "fifth": "5",
            "sixth": "6",
            "seventh": "7",
            "eighth": "8",
        }),
        ShortIntegerRef("n", 1, 100),
        ShortIntegerRef("m", 1, 10)
    ]
