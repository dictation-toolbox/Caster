from dragonfly import (Grammar, Dictation, Repeat)

import IDE
from castervoice.apps.gitbash import GitBashRule
from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class JetbrainsRule(MergeRule):
    pronunciation = "jet brains"

    def merge_dictionaries(x, y):
        z = x.copy()  # start with x's keys and values
        z.update(y)  # modifies z with y's keys and values & returns None
        return z

    def command_list_to_dictionary(commands):
        dictionary = {}
        for command in commands:
            dictionary[command.phrase] = command.registered_action
        return dictionary


    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]

    DELAY = "20"

    mapping = {
        IDE.QUICK_FIX: R(Key("a-enter")),
        IDE.DUPLICATE_LINE_DOWN: R(Key("c-d")),
        "auto complete": R(Key("cs-a")),
        IDE.FORMAT_ALL_CODE: R(Key("ca-l")),
        "show doc": R(Key("c-q")),
        "show param": R(Key("c-p")),
        IDE.GENERATE_CODE: R(Key("a-insert")),
        IDE.NEW_FILE: R(Key("a-insert")),
        "jump to source": R(Key("f4")),
        IDE.DELETE_LINE: R(Key("c-y")),
        IDE.SEARCH_FOR_SYMBOL_IN_ALL_FILES: R(Key("cas-n")),
        IDE.SEARCH_FOR_FILE_IN_ALL_FILES: R(Key("c-n")),
        IDE.SEARCH_FOR_CLASS_IN_ALL_FILES: R(Key("c-n")),
        IDE.BUILD_PROJECT: R(Key("c-f9")),
        IDE.BUILD_AND_RUN_PROJECT: R(Key("s-f10")),
        IDE.NEXT_TAB: R(Key("a-right/%s" % DELAY)) * Repeat(extra="n"),
        IDE.PREVIOUS_TAB: R(Key("a-left/%s" % DELAY)) * Repeat(extra="n"),
        IDE.COMMENT_LINE: R(Key("c-slash")),
        IDE.UNCOMMENT_LINE: R(Key("cs-slash")),
        "select ex" : R(Key("c-w")),
        "select ex down" : R(Key("cs-w")),
        IDE.SEARCH_FOR_ALL_IN_ALL_FILES: R(Key("shift, shift")),
        IDE.FIND_IN_CURRENT_FILE: R(Key("c-f")),
        IDE.FIND_NEXT_MATCH: R(Key("enter")),
        IDE.FIND_PREVIOUS_MATCH: R(Key("s-enter")),
        IDE.REPLACE_IN_CURRENT_FILE: R(Key("c-r")),
        IDE.FIND_IN_ALL_FILES: R(Key("cs-f")),
        IDE.REPLACE_IN_ALL_FILES: R(Key("cs-r")),
        IDE.GO_TO_LINE: R(Key("c-g/%s" % DELAY) + Text("%(n)s") + Key("enter")),
        IDE.IMPLEMENT_METHODS: R(Key("c-i")),
        IDE.OVERRIDE_METHOD: R(Key("c-o")),
        "run config": R(Key("as-f10")),
        IDE.FIND_USAGE: R(Key("a-f7")),
        IDE.GO_TO_DECLARATION: R(Key("c-b")),
        IDE.SMART_AUTO_COMPLETE: R(Key("cs-space")),
        IDE.NAVIGATE_BACKWARD: R(Key("ca-left")) * Repeat(extra="n"),
        IDE.NAVIGATE_FORWARD: R(Key("ca-left")) * Repeat(extra="n"),
        IDE.METHOD_FORWARD: R(Key("a-down")) * Repeat(extra="n"),
        IDE.METHOD_BACKWARD: R(Key("a-up")) * Repeat(extra="n"),
        IDE.NEXT_ERROR: R(Key("f2")) * Repeat(extra="n"),
        IDE.PREVIOUS_ERROR: R(Key("s-f2")) * Repeat(extra="n"),
        IDE.OPTIMIZE_IMPORTS: R(Key("ca-o")) * Repeat(extra="n"),
        IDE.MOVE_LINE_UP: R(Key("as-up")) * Repeat(extra="n"),
        IDE.MOVE_LINE_DOWN: R(Key("as-down")) * Repeat(extra="n"),
        IDE.EXPAND_SELECTION: R(Key("c-w")) * Repeat(extra="n"),
        IDE.AUTO_INDENT: R(Key("ca-i")),
        IDE.CLOSE_TAB_N_TIMES: R(Key("c-f4/%s" % DELAY)) * Repeat(extra="n"),
        IDE.RUN_PROJECT: R(Key("cs-f10")),
        "settings": R(Key("ca-s")),

        # refactoring
        IDE.REFACTOR: R(Key("cas-t")),
        IDE.RENAME: R(Key("s-f6")),
        IDE.INLINE: R(Key("ca-n")),
        IDE.EXTRACT_METHOD: R(Key("ca-m")),
        IDE.EXTRACT_VARIABLE: R(Key("ca-v")) * Repeat(extra="n"),
        IDE.EXTRACT_FIELD: R(Key("ca-f")) * Repeat(extra="n"),
        IDE.EXTRACT_CONSTANT: R(Key("ca-c")) * Repeat(extra="n"),
        IDE.EXTRACT_PARAMETER: R(Key("ca-p")) * Repeat(extra="n"),

        # window navigation
        IDE.GO_TO_EDITOR: R(Key("escape")),
        IDE.GO_TO_PROJECT_EXPLORER: R(Key("a-1")),
        IDE.TOGGLE_TERMINAL: R(Key("a-f12")),

        # must be bound manually below this point
        IDE.DELETE_TO_LINE_START: R(Key("a-d,0")),
        IDE.DELETE_TO_LINE_END: R(Key("a-d,$")),
        # jet brains can only split horizontally or vertically
        IDE.SPLIT_WINDOW_UP: R(Key("cs-s,h")),
        IDE.SPLIT_WINDOW_DOWN: R(Key("cs-s,h")),
        IDE.SPLIT_WINDOW_RIGHT: R(Key("cs-s,v")),
        IDE.SPLIT_WINDOW_LEFT: R(Key("cs-s,v")),
        IDE.SPLIT_MOVE_UP: R(Key("cs-s,up"))* Repeat(extra="n"),
        IDE.SPLIT_MOVE_DOWN: R(Key("cs-s,down"))* Repeat(extra="n"),
        IDE.SPLIT_MOVE_RIGHT: R(Key("cs-s,right"))* Repeat(extra="n"),
        IDE.SPLIT_MOVE_LEFT: R(Key("cs-s,left"))* Repeat(extra="n"),
    }
    defaults = {"n": 1, "mim": ""}


# ---------------------------------------------------------------------------

context = AppContext(executable="idea", title="IntelliJ") \
          | AppContext(executable="idea64", title="IntelliJ") \
          | AppContext(executable="studio64") \
          | AppContext(executable="pycharm")
grammar = Grammar("IntelliJ + Android Studio + PyCharm", context=context)

if settings.SETTINGS["apps"]["jetbrains"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(JetbrainsRule())
    else:
        jet_brains_rule = JetbrainsRule(name="jet brains")
        gfilter.run_on(jet_brains_rule)
        grammar.add_rule(jet_brains_rule)

        # You will need to change your terminal to bash under settings->tools
        # C:\Program Files\Git\bin\bash.exe
        git_rule = GitBashRule()
        gfilter.run_on(git_rule)
        grammar.add_rule(git_rule)

        grammar.load()
