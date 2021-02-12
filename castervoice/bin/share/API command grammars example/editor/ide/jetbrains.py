# pylint: skip-file
from dragonfly import Dictation, Repeat, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Text, Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
import ide_shared
from castervoice.lib.merge.state.short import R


class JetbrainsRule(MappingRule):
    extras = [
        Dictation("text"),
        Dictation("mim"),
        ShortIntegerRef("n", 1, 1000),
    ]

    DELAY = "20"

    mapping = {
        ide_shared.QUICK_FIX: R(Key("a-enter")),
        ide_shared.DUPLICATE_LINE_DOWN: R(Key("c-d")),
        "auto complete": R(Key("cs-a")),
        ide_shared.FORMAT_ALL_CODE: R(Key("ca-l")),
        "show doc": R(Key("c-q")),
        "show param": R(Key("c-p")),
        ide_shared.GENERATE_CODE: R(Key("a-insert")),
        ide_shared.NEW_FILE: R(Key("a-insert")),
        "jump to source": R(Key("f4")),
        ide_shared.DELETE_LINE: R(Key("c-y")),
        ide_shared.SEARCH_FOR_SYMBOL_IN_ALL_FILES: R(Key("cas-n")),
        ide_shared.SEARCH_FOR_FILE_IN_ALL_FILES: R(Key("c-n")),
        ide_shared.SEARCH_FOR_CLASS_IN_ALL_FILES: R(Key("c-n")),
        ide_shared.BUILD_PROJECT: R(Key("c-f9")),
        ide_shared.BUILD_AND_RUN_PROJECT: R(Key("s-f10")),
        ide_shared.NEXT_TAB: R(Key("a-right/%s" % DELAY)) * Repeat(extra="n"),
        ide_shared.PREVIOUS_TAB: R(Key("a-left/%s" % DELAY)) * Repeat(extra="n"),
        ide_shared.COMMENT_LINE: R(Key("c-slash")),
        ide_shared.UNCOMMENT_LINE: R(Key("cs-slash")),
        "select ex" : R(Key("c-w")),
        "select ex down" : R(Key("cs-w")),
        ide_shared.SEARCH_FOR_ALL_IN_ALL_FILES: R(Key("shift, shift")),
        ide_shared.FIND_IN_CURRENT_FILE: R(Key("c-f")),
        ide_shared.FIND_NEXT_MATCH: R(Key("enter")) * Repeat(extra="n"),
        ide_shared.FIND_PREVIOUS_MATCH: R(Key("s-enter")) * Repeat(extra="n"),
        ide_shared.REPLACE_IN_CURRENT_FILE: R(Key("c-r")),
        ide_shared.FIND_IN_ALL_FILES: R(Key("cs-f")),
        ide_shared.REPLACE_IN_ALL_FILES: R(Key("cs-r")),
        ide_shared.GO_TO_LINE: R(Key("c-g/%s" % DELAY) + Text("%(n)s") + Key("enter")),
        ide_shared.IMPLEMENT_METHODS: R(Key("c-i")),
        ide_shared.OVERRIDE_METHOD: R(Key("c-o")),
        "run config": R(Key("as-f10")),
        ide_shared.FIND_USAGE: R(Key("a-f7")),
        ide_shared.GO_TO_DECLARATION: R(Key("c-b")),
        ide_shared.SMART_AUTO_COMPLETE: R(Key("cs-space")),
        ide_shared.NAVIGATE_BACKWARD: R(Key("ca-left")) * Repeat(extra="n"),
        ide_shared.NAVIGATE_FORWARD: R(Key("ca-right")) * Repeat(extra="n"),
        ide_shared.METHOD_FORWARD: R(Key("a-down")) * Repeat(extra="n"),
        ide_shared.METHOD_BACKWARD: R(Key("a-up")) * Repeat(extra="n"),
        ide_shared.NEXT_ERROR: R(Key("f2")) * Repeat(extra="n"),
        ide_shared.PREVIOUS_ERROR: R(Key("s-f2")) * Repeat(extra="n"),
        ide_shared.OPTIMIZE_IMPORTS: R(Key("ca-o")) * Repeat(extra="n"),
        ide_shared.MOVE_LINE_UP: R(Key("as-up")) * Repeat(extra="n"),
        ide_shared.MOVE_LINE_DOWN: R(Key("as-down")) * Repeat(extra="n"),
        ide_shared.EXPAND_SELECTION: R(Key("c-w")) * Repeat(extra="n"),
        ide_shared.SHRINK_SELECTION: R(Key("cs-w")) * Repeat(extra="n"),
        ide_shared.AUTO_INDENT: R(Key("ca-i")),
        ide_shared.CLOSE_TAB_N_TIMES: R(Key("c-f4/%s" % DELAY)) * Repeat(extra="n"),
        ide_shared.RUN_PROJECT: R(Key("s-f10")),
        ide_shared.DEBUG_PROJECT: R(Key("s-f9")),
        ide_shared.REDO: R(Key("cs-z")) * Repeat(extra="n"),
        ide_shared.SHOW_SETTINGS: R(Key("ca-s")),
        # only works if you disable tabs.
        ide_shared.CLOSE_PANE_N_TIMES: R(Key("c-f4/%s" % DELAY)) * Repeat(extra="n"),

        # refactoring
        ide_shared.REFACTOR: R(Key("cas-t")),
        ide_shared.RENAME: R(Key("s-f6")),
        ide_shared.INLINE: R(Key("ca-n")),
        ide_shared.EXTRACT_METHOD: R(Key("ca-m")),
        ide_shared.EXTRACT_VARIABLE: R(Key("ca-v")) * Repeat(extra="n"),
        ide_shared.EXTRACT_FIELD: R(Key("ca-f")) * Repeat(extra="n"),
        ide_shared.EXTRACT_CONSTANT: R(Key("ca-c")) * Repeat(extra="n"),
        ide_shared.EXTRACT_PARAMETER: R(Key("ca-p")) * Repeat(extra="n"),

        # window navigation
        ide_shared.GO_TO_EDITOR: R(Key("escape")),
        ide_shared.GO_TO_PROJECT_EXPLORER: R(Key("a-1")),
        ide_shared.TOGGLE_TERMINAL: R(Key("a-f12")),

        # must be bound manually below this point
        ide_shared.DELETE_TO_LINE_START: R(Key("a-d,0")),
        ide_shared.DELETE_TO_LINE_END: R(Key("a-d,$")),
        # jet brains can only split horizontally or vertically
        ide_shared.SPLIT_WINDOW_UP: R(Key("cs-s,h")),
        ide_shared.SPLIT_WINDOW_DOWN: R(Key("cs-s,h")),
        ide_shared.SPLIT_WINDOW_RIGHT: R(Key("cs-s,v")),
        ide_shared.SPLIT_WINDOW_LEFT: R(Key("cs-s,v")),
        ide_shared.SPLIT_MOVE_UP: R(Key("cs-s,up")) * Repeat(extra="n"),
        ide_shared.SPLIT_MOVE_DOWN: R(Key("cs-s,down")) * Repeat(extra="n"),
        ide_shared.SPLIT_MOVE_RIGHT: R(Key("cs-s,right")) * Repeat(extra="n"),
        ide_shared.SPLIT_MOVE_LEFT: R(Key("cs-s,left")) * Repeat(extra="n"),
        ide_shared.RENAME_CURRENT_FILE: R(Key("cas-r")),
    }

    defaults = {"n": 1, "mim": ""}


def get_rule():
    details = RuleDetails(name="jet brains",
                          executable=["idea", "idea64", "studio64", "pycharm"])
    return JetbrainsRule, details
