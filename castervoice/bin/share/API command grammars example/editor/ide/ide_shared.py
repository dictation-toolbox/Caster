# pylint: skip-file
#
# __author__ = "lexxish"
#
from castervoice.rules.apps.shared.directions import FORWARD, RIGHT, BACK, LEFT, UP, DOWN

method = "(meth|method)"
methods = "(meths|methods)"

# general
EXPAND_SELECTION = "expand [selection] [<n>]"
SHRINK_SELECTION = "shrink [selection] [<n>]"
SMART_AUTO_COMPLETE = "(skraken|smart kraken)"
GENERATE_CODE = "jen code"
QUICK_FIX = "quick fix"
FORMAT_ALL_CODE = "format [code]"
BUILD_PROJECT = "build"
RUN_PROJECT = "run"
DEBUG_PROJECT = "debug"
BUILD_AND_RUN_PROJECT = "build and run"
DEBUG_CURRENT_FILE = "debug file"
RUN_CURRENT_FILE = "run file"
NEXT_ERROR = "(%s error|error %s)" % (FORWARD, RIGHT)
PREVIOUS_ERROR = "(%s error|error %s)" % (BACK, LEFT)
REDO = "redo [<n>]"
SHOW_SETTINGS = "[show] settings"
RENAME_CURRENT_FILE = "file rename | rename file"

# window navigation
NEXT_TAB = "%s tab [<n>]|tab %s [<n>]" % (FORWARD, RIGHT)
PREVIOUS_TAB = "%s tab [<n>]|tab %s [<n>]" % (BACK, LEFT)
CLOSE_TAB_N_TIMES = "close tab [<n>]|tab close [<n>]"
GO_TO_EDITOR = "focus editor"
GO_TO_PROJECT_EXPLORER = "go [to] project"
TOGGLE_TERMINAL = "[toggle] (term|terminal)"
NEW_FILE = "new file"

# editor management
SPLIT_WINDOW_UP = "split [pane] %s" % UP
SPLIT_WINDOW_DOWN = "split [pane] %s" % DOWN
SPLIT_WINDOW_RIGHT = "split [pane] %s" % RIGHT
SPLIT_WINDOW_LEFT = "split [pane] %s" % LEFT
SPLIT_MOVE_UP = "pane %s [<n>]" % UP
SPLIT_MOVE_DOWN = "pane %s [<n>]" % DOWN
SPLIT_MOVE_RIGHT = "(pane %s|%s pane) [<n>]" % (RIGHT, RIGHT)
SPLIT_MOVE_LEFT = "(pane %s|%s pane) [<n>]" % (LEFT, LEFT)
CLOSE_PANE_N_TIMES = "close pane [<n>]|pane close [<n>]"

# navigation
GO_TO_LINE = "go [to line] [<n>]"
METHOD_FORWARD = "%s %s [<n>]" % (method, FORWARD)
METHOD_BACKWARD = "%s %s [<n>]" % (method, BACK)
NAVIGATE_FORWARD = "go %s [<n>]" % FORWARD
NAVIGATE_BACKWARD = "go %s [<n>]" % BACK
GO_TO_DECLARATION = "[go to] (source|declaration)"

# search and replace
FIND_IN_CURRENT_FILE = "find"
FIND_NEXT_MATCH = "find %s [match] [<n>]" % BACK
FIND_PREVIOUS_MATCH = "find %s [match] [<n>]" % FORWARD
REPLACE_IN_CURRENT_FILE = "replace"
FIND_IN_ALL_FILES = "find [in] (all|files)"
REPLACE_IN_ALL_FILES = "replace [in] (all|files)"
FIND_USAGE = "[find] (usage|usages)"
SEARCH_FOR_ALL_IN_ALL_FILES = "search"
SEARCH_FOR_SYMBOL_IN_ALL_FILES = "find symbol"
SEARCH_FOR_FILE_IN_ALL_FILES = "find file"
SEARCH_FOR_CLASS_IN_ALL_FILES = "find class"

# line operations
MOVE_LINE_UP = "[move] line %s [<n>]" % UP
MOVE_LINE_DOWN = "[move] line %s [<n>]" % DOWN
DELETE_LINE = "kill [line]"
DELETE_TO_LINE_END = "kill %s" % FORWARD
DELETE_TO_LINE_START = "kill %s" % BACK
COMMENT_LINE = "(comment|rem) [line]"
UNCOMMENT_LINE = "(uncomment|unrem) [line]"
DUPLICATE_LINE_UP = "(duplicate|duple) %s" % UP
DUPLICATE_LINE_DOWN = "(duplicate|duple) %s" % DOWN

# refactor
OPTIMIZE_IMPORTS = "[organize|optimize] imports"
REFACTOR = "refactor"
RENAME = "rename"
INLINE = "inline"
extract = "(pull|extract)"
EXTRACT_METHOD = "%s %s" % (extract, method)
EXTRACT_VARIABLE = "%s [variable|var]" % extract
EXTRACT_FIELD = "%s field" % extract
EXTRACT_CONSTANT = "%s constant" % extract
EXTRACT_PARAMETER = "%s (param|parameter)" % extract
IMPLEMENT_METHODS = "implement (%s|%s)" % (method, methods)
OVERRIDE_METHOD = "override %s" % method
AUTO_INDENT = "auto indent"
