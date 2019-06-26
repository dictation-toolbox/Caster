from castervoice.lib.imports import *
import ide

class JetbrainsRule(MergeRule):
    pronunciation = "jet brains"

    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]

    DELAY = "20"

    mapping = {
        ide.QUICK_FIX: R(Key("a-enter")),
        ide.DUPLICATE_LINE_DOWN: R(Key("c-d")),
        "auto complete": R(Key("cs-a")),
        ide.FORMAT_ALL_CODE: R(Key("ca-l")),
        "show doc": R(Key("c-q")),
        "show param": R(Key("c-p")),
        ide.GENERATE_CODE: R(Key("a-insert")),
        ide.NEW_FILE: R(Key("a-insert")),
        "jump to source": R(Key("f4")),
        ide.DELETE_LINE: R(Key("c-y")),
        ide.SEARCH_FOR_SYMBOL_IN_ALL_FILES: R(Key("cas-n")),
        ide.SEARCH_FOR_FILE_IN_ALL_FILES: R(Key("c-n")),
        ide.SEARCH_FOR_CLASS_IN_ALL_FILES: R(Key("c-n")),
        ide.BUILD_PROJECT: R(Key("c-f9")),
        ide.BUILD_AND_RUN_PROJECT: R(Key("s-f10")),
        ide.NEXT_TAB: R(Key("a-right/%s" % DELAY)) * Repeat(extra="n"),
        ide.PREVIOUS_TAB: R(Key("a-left/%s" % DELAY)) * Repeat(extra="n"),
        ide.COMMENT_LINE: R(Key("c-slash")),
        ide.UNCOMMENT_LINE: R(Key("cs-slash")),
        "select ex" : R(Key("c-w")),
        "select ex down" : R(Key("cs-w")),
        ide.SEARCH_FOR_ALL_IN_ALL_FILES: R(Key("shift, shift")),
        ide.FIND_IN_CURRENT_FILE: R(Key("c-f")),
        ide.FIND_NEXT_MATCH: R(Key("enter"))  * Repeat(extra="n"),
        ide.FIND_PREVIOUS_MATCH: R(Key("s-enter"))  * Repeat(extra="n"),
        ide.REPLACE_IN_CURRENT_FILE: R(Key("c-r")),
        ide.FIND_IN_ALL_FILES: R(Key("cs-f")),
        ide.REPLACE_IN_ALL_FILES: R(Key("cs-r")),
        ide.GO_TO_LINE: R(Key("c-g/%s" % DELAY) + Text("%(n)s") + Key("enter")),
        ide.IMPLEMENT_METHODS: R(Key("c-i")),
        ide.OVERRIDE_METHOD: R(Key("c-o")),
        "run config": R(Key("as-f10")),
        ide.FIND_USAGE: R(Key("a-f7")),
        ide.GO_TO_DECLARATION: R(Key("c-b")),
        ide.SMART_AUTO_COMPLETE: R(Key("cs-space")),
        ide.NAVIGATE_BACKWARD: R(Key("ca-left")) * Repeat(extra="n"),
        ide.NAVIGATE_FORWARD: R(Key("ca-right")) * Repeat(extra="n"),
        ide.METHOD_FORWARD: R(Key("a-down")) * Repeat(extra="n"),
        ide.METHOD_BACKWARD: R(Key("a-up")) * Repeat(extra="n"),
        ide.NEXT_ERROR: R(Key("f2")) * Repeat(extra="n"),
        ide.PREVIOUS_ERROR: R(Key("s-f2")) * Repeat(extra="n"),
        ide.OPTIMIZE_IMPORTS: R(Key("ca-o")) * Repeat(extra="n"),
        ide.MOVE_LINE_UP: R(Key("as-up")) * Repeat(extra="n"),
        ide.MOVE_LINE_DOWN: R(Key("as-down")) * Repeat(extra="n"),
        ide.EXPAND_SELECTION: R(Key("c-w")) * Repeat(extra="n"),
        ide.SHRINK_SELECTION: R(Key("cs-w")) * Repeat(extra="n"),
        ide.AUTO_INDENT: R(Key("ca-i")),
        ide.CLOSE_TAB_N_TIMES: R(Key("c-f4/%s" % DELAY)) * Repeat(extra="n"),
        ide.RUN_PROJECT: R(Key("s-f10")),
        ide.DEBUG_PROJECT: R(Key("s-f9")),
        ide.REDO: R(Key("cs-z")) * Repeat(extra="n"),
        ide.SHOW_SETTINGS: R(Key("ca-s")),
        # only works if you disable tabs.
        ide.CLOSE_PANE_N_TIMES: R(Key("c-f4/%s" % DELAY)) * Repeat(extra="n"),

        # refactoring
        ide.REFACTOR: R(Key("cas-t")),
        ide.RENAME: R(Key("s-f6")),
        ide.INLINE: R(Key("ca-n")),
        ide.EXTRACT_METHOD: R(Key("ca-m")),
        ide.EXTRACT_VARIABLE: R(Key("ca-v")) * Repeat(extra="n"),
        ide.EXTRACT_FIELD: R(Key("ca-f")) * Repeat(extra="n"),
        ide.EXTRACT_CONSTANT: R(Key("ca-c")) * Repeat(extra="n"),
        ide.EXTRACT_PARAMETER: R(Key("ca-p")) * Repeat(extra="n"),

        # window navigation
        ide.GO_TO_EDITOR: R(Key("escape")),
        ide.GO_TO_PROJECT_EXPLORER: R(Key("a-1")),
        ide.TOGGLE_TERMINAL: R(Key("a-f12")),

        # must be bound manually below this point
        ide.DELETE_TO_LINE_START: R(Key("a-d,0")),
        ide.DELETE_TO_LINE_END: R(Key("a-d,$")),
        # jet brains can only split horizontally or vertically
        ide.SPLIT_WINDOW_UP: R(Key("cs-s,h")),
        ide.SPLIT_WINDOW_DOWN: R(Key("cs-s,h")),
        ide.SPLIT_WINDOW_RIGHT: R(Key("cs-s,v")),
        ide.SPLIT_WINDOW_LEFT: R(Key("cs-s,v")),
        ide.SPLIT_MOVE_UP: R(Key("cs-s,up")) * Repeat(extra="n"),
        ide.SPLIT_MOVE_DOWN: R(Key("cs-s,down")) * Repeat(extra="n"),
        ide.SPLIT_MOVE_RIGHT: R(Key("cs-s,right")) * Repeat(extra="n"),
        ide.SPLIT_MOVE_LEFT: R(Key("cs-s,left")) * Repeat(extra="n"),
        ide.RENAME_CURRENT_FILE: R(Key("cas-r")),
    }

    defaults = {"n": 1, "mim": ""}


context = AppContext(executable="idea", title="IntelliJ") \
          | AppContext(executable="idea64", title="IntelliJ") \
          | AppContext(executable="studio64") \
          | AppContext(executable="pycharm")
control.non_ccr_app_rule(JetbrainsRule(), context=context)
