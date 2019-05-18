from dragonfly import (Grammar, AppContext, Dictation, Key, Repeat)

from castervoice.apps.gitbash import GitBashRule
from castervoice.apps.ide.Command import Command
from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
import IDE as IDE


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

    mapping = {
        IDE.quick_fix : R(Key("a-enter")),
        IDE.duplicate: R(Key("c-d")),
        IDE.auto_complete: R(Key("cs-a")),
        IDE.code: R(Key("ca-l")),
        IDE.show_documentation: R(Key("c-q")),
        IDE.generate_code: R(Key("a-insert")),
        IDE.new_file: R(Key("a-insert")),
        IDE.source: R(Key("f4")),
        IDE.delete_line: R(Key("c-y")),
        IDE.symbol: R(Key("cas-n")),
        IDE.build: R(Key("c-f9")),
        IDE.build_and_run: R(Key("s-f10")),
        IDE.tab: R(Key("a-right")),
        IDE.prior_tab: R(Key("a-left")),
        IDE.comment_line: R(Key("c-slash")),
        IDE.uncomment_line: R(Key("cs-slash")),
        "select ex" : R(Key("c-w")),
        "select ex down" : R(Key("cs-w")),
        IDE.search: R(Key("shift, shift")),
        IDE.find: R(Key("c-f")),
        IDE.replace: R(Key("c-r")),
        IDE.find_in_files: R(Key("cs-f")),
        IDE.replace_in_files: R(Key("cs-r")),
        IDE.go_to_line: R(Key("c-g/10") + Text("%(n)s") + Key("enter")),
        IDE.methods: R(Key("c-i")),
        IDE.override_methods: R(Key("c-o")),
        IDE.config: R(Key("as-f10")),
        IDE.usages: R(Key("a-f7")),
        IDE.declaration: R(Key("c-b")),
        IDE.kraken: R(Key("cs-space")),
        IDE.back: R(Key("ca-left")) * Repeat(extra="n"),
        IDE.forward: R(Key("ca-left")) * Repeat(extra="n"),
        IDE.kill_the_rest_of_line: R(Key("c-y")),
        IDE.method_forward: R(Key("a-down")) * Repeat(extra="n"),
        IDE.method_back: R(Key("a-up")) * Repeat(extra="n"),
        IDE.imports: R(Key("ca-o")) * Repeat(extra="n"),
        IDE.line_up: R(Key("as-up")) * Repeat(extra="n"),
        IDE.line_down: R(Key("as-down")) * Repeat(extra="n"),
        IDE.expand: R(Key("c-w")) * Repeat(extra="n"),
        IDE.indent: R(Key("ca-i")),
        "[<n>] before" : R(Key("c-left")) * Repeat(extra="n"),
        "[<n>] after" : R(Key("c-right")) * Repeat(extra="n"),
        "[<n>] befores": R(Key("cs-left")) * Repeat(extra="n"),
        "[<n>] afters" : R(Key("cs-right")) * Repeat(extra="n"),
        IDE.close_tab: R(Key("c-f4")) * Repeat(extra="n"),
        # Refactoring
        IDE.refactor: R(Key("cas-t")),
        IDE.rename: R(Key("s-f6")),
        IDE.inline: R(Key("ca-n")),
        IDE.extract_method: R(Key("ca-m")),
        IDE.variable: R(Key("ca-v")) * Repeat(extra="n"),
        IDE.field: R(Key("ca-f")) * Repeat(extra="n"),
        IDE.constant: R(Key("ca-c")) * Repeat(extra="n"),
        IDE.extract_param: R(Key("ca-p")) * Repeat(extra="n"),
        IDE.go_to_editor: R(Key("escape")),
        IDE.go_to_project_explorer: R(Key("a-1")),
        IDE.go_to_terminal: R(Key("a-f12")),
        IDE.run: R(Key("cs-f10"))
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
