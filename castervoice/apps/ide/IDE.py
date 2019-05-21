#
# __author__ = "lexxish"
#

# variables
right = "(right|sauce)"
left = "(left|lease)"
up = "(up|sauce|above)"
down = "(down|dunce|below)"
forward = "(%s|next|forward)" % right
back = "(%s|back|prev|previous)" % left
method = "(meth|method)"

# general
EXPAND_SELECTION = "expand [selection] [<n>]"
SMART_AUTO_COMPLETE = "(skraken|smart kraken)"
GENERATE_CODE = "jen code"
QUICK_FIX = "quickfix"
FORMAT_ALL_CODE = "format code"
BUILD_PROJECT = "build"
RUN_PROJECT = "run"
DEBUG_PROJECT = "debug"
BUILD_AND_RUN_PROJECT = "build and run"
DEBUG_CURRENT_FILE = "debug file"
RUN_CURRENT_FILE = "run file"
NEXT_ERROR = "(%s error|error %s)" % (forward, right)
PREVIOUS_ERROR = "(%s error|error %s)" % (back, left)

# window navigation
NEXT_TAB = "%s tab [<n>]|tab %s [<n>]" % (forward, right)
PREVIOUS_TAB = "%s tab [<n>]|tab %s [<n>]" % (back, left)
CLOSE_TAB_N_TIMES = "close tab [<n>]|tab close [<n>]"
GO_TO_EDITOR = "go [to] editor"
GO_TO_PROJECT_EXPLORER = "go [to] project"
TOGGLE_TERMINAL = "[toggle] (term|terminal)"
NEW_FILE = "new file"

# editor management
SPLIT_WINDOW_UP = "split [pane] %s" % up
SPLIT_WINDOW_DOWN = "split [pane] %s" % down
SPLIT_WINDOW_RIGHT = "split [pane] %s" % right
SPLIT_WINDOW_LEFT = "split [pane] %s" % left
SPLIT_MOVE_UP = "pane %s [<n>]" % up
SPLIT_MOVE_DOWN = "pane %s [<n>]" % down
SPLIT_MOVE_RIGHT = "(pane %s|next pane) [<n>]" % right
SPLIT_MOVE_LEFT = "(pane %s|(prior|previous) pane) [<n>]" % left

# navigation
GO_TO_LINE = "go [to line] [<n>]"
METHOD_FORWARD = "%s %s [<n>]" % (method, forward)
METHOD_BACKWARD = "%s %s [<n>]" % (method, back)
NAVIGATE_FORWARD = "go %s [<n>]" % forward
NAVIGATE_BACKWARD = "go %s [<n>]" % back
GO_TO_DECLARATION = "[go to] (source|declaration)"

# search and replace
FIND_IN_CURRENT_FILE = "find"
FIND_NEXT_MATCH = "find %s" % right
FIND_PREVIOUS_MATCH = "find %s" % left
REPLACE_IN_CURRENT_FILE = "replace"
FIND_IN_ALL_FILES = "find [in] (all|files)"
REPLACE_IN_ALL_FILES = "replace [in] (all|files)"
FIND_USAGE = "[find] (usage|usages)"
SEARCH_FOR_ALL_IN_ALL_FILES = "search"
SEARCH_FOR_SYMBOL_IN_ALL_FILES = "find symbol"
SEARCH_FOR_FILE_IN_ALL_FILES = "find file"
SEARCH_FOR_CLASS_IN_ALL_FILES = "find class"

# line operations
MOVE_LINE_UP = "[move] line %s [<n>]" % up
MOVE_LINE_DOWN = "[move] line %s [<n>]" % down
DELETE_LINE = "kill [line]"
DELETE_TO_LINE_END = "kill %s" % forward
DELETE_TO_LINE_START = "kill %s" % back
COMMENT_LINE = "(comment|rem) [line]"
UNCOMMENT_LINE = "(uncomment|unrem) [line]"
DUPLICATE_LINE_UP = "(duplicate|duple) %s" % up
DUPLICATE_LINE_DOWN = "(duplicate|duple) %s" % down

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
IMPLEMENT_METHODS = "implement (%s|%ss)" % (method, method)
OVERRIDE_METHOD = "override %s" % method
AUTO_INDENT = "auto indent"


