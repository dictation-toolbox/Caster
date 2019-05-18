from dragonfly import (Grammar, AppContext, Dictation, Key, Repeat)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class JetbrainsRule(MergeRule):
    pronunciation = "jet brains"

    mapping = {
        "quickfix":
            R(Key("a-enter"), rdescript="JetBrains: Quick Fix"),
        "duplicate":
            R(Key("c-d"), rdescript="JetBrains: Duplicate"),
        "auto complete":
            R(Key("cs-a"), rdescript="JetBrains: Auto Complete"),
        "format code":
            R(Key("ca-l"), rdescript="JetBrains: Format Code"),
        "show doc":
            R(Key("c-q"), rdescript="JetBrains: Show Documentation"),
        "show param":
            R(Key("c-p"), rdescript="JetBrains: Show Parameters"),
        "Jen code":
            R(Key("a-insert"), rdescript="JetBrains: Generate code"),
        "new file":
            R(Key("a-insert"), rdescript="JetBrains: Generate code"),
        "jump to source":
            R(Key("f4"), rdescript="JetBrains: Jump To Source"),
        "delete line":
            R(Key("c-y"), rdescript="JetBrains: Delete Line"),
        "search symbol":
            R(Key("cas-n"), rdescript="JetBrains: Search Symbol"),
        "build":
            R(Key("c-f9"), rdescript="JetBrains: Build"),
        "build and run":
            R(Key("s-f10"), rdescript="JetBrains: Build And Run"),
        "next tab":
            R(Key("a-right"), rdescript="JetBrains: Next Tab"),
        "prior tab":
            R(Key("a-left"), rdescript="JetBrains: Previous Tab"),
        "comment line":
            R(Key("c-slash"), rdescript="JetBrains: Comment Line"),
        "uncomment line":
            R(Key("cs-slash"), rdescript="JetBrains: Uncomment Line"),
        "select ex":
            R(Key("c-w"), rdescript="JetBrains: Extended selection"),
        "select ex down":
            R(Key("cs-w"), rdescript="JetBrains: Extended selection back"),
        "search":
            R(Key("shift, shift"), rdescript="JetBrains: Search Everywhere"),
        "find":
            R(Key("cs-f"), rdescript="JetBrains: Find In Current"),
        "go to line":
            R(Key("c-g"), rdescript="JetBrains: Go To Line"),
        "implement methods":
            R(Key("c-i"), rdescript="JetBrains: Implement methods"),
        "override methods":
            R(Key("c-o"), rdescript="JetBrains: Override methods"),
        "run config":
            R(Key("as-f10"), rdescript="Jet Brains: Display run configurations dialogue"),
        "find usages":
            R(Key("a-f7"), rdescript="Jet Brains: Find usages"),
        "refactor rename":
            R(Key("s-f6"), rdescript="Jet Brains: Refactor rename"),
        "go to declaration":
            R(Key("c-b"), rdescript="Jet Brains: Go to declaration"),
        "smart kraken": #kraken is Caster default for control space
            R(Key("cs-space"), rdescript="Jet Brains: Smart completion"),
        "[<n>] back":
            R(Key("ca-left"), rdescript="Jet Brains: Navigate Back") * Repeat(extra="n"),
        "[<n>] forward":
            R(Key("cs-left"), rdescript="Jet Brains: Navigate Forward") * Repeat(extra="n"),
        "kill":
            R(Key("c-y"), rdescript="Jet Brains: Kill line at caret"),
        "[<n>] method":
            R(Key("a-down"), rdescript="Jet Brains: Navigate next method") * Repeat(extra="n"),
        "[<n>] method back":
            R(Key("a-up"), rdescript="Jet Brains: Navigate back method") * Repeat(extra="n"),
        "optimize imports":
            R(Key("ca-o"), rdescript="Jet Brains: Navigate next method") * Repeat(extra="n"),
        "[<n>] move line up":
            R(Key("as-up"), rdescript="Jet Brains: Move line up") * Repeat(extra="n"),
        "[<n>] move line down":
            R(Key("as-down"), rdescript="Jet Brains: Move line down") * Repeat(extra="n"),
        "[<n>] expand":
            R(Key("c-w"), rdescript="Jet Brains: Expand Selection") * Repeat(extra="n"),
        "auto indent":
            R(Key("ca-i"), rdescript="Jet Brains: Automatically Indent"),
        "[<n>] before":
            R(Key("c-left"), rdescript="Jet Brains: Expand Selection") * Repeat(extra="n"),
        "[<n>] after":
            R(Key("c-right"), rdescript="Jet Brains: Expand Selection") * Repeat(extra="n"),
        "[<n>] after":
            R(Key("c-right"), rdescript="Jet Brains: Expand Selection") * Repeat(extra="n"),
        "[<n>] close tab":
            R(Key("c-f4"), rdescript="Jet Brains: Expand Selection") * Repeat(extra="n"),
        # Refactoring
        "refactor":
            R(Key("cas-t"), rdescript="Jet Brains: Refactor"),
        "Rename":
            R(Key("s-f6"), rdescript="Jet Brains: Expand Selection") * Repeat(extra="n"),
        "inline":
            R(Key("ca-n"), rdescript="Jet Brains: Inline") * Repeat(extra="n"),
        "Extract Method":
            R(Key("ca-m"), rdescript="Jet Brains: Expand Selection") * Repeat(extra="n"),
        "Extract Variable":
            R(Key("ca-v"), rdescript="Jet Brains: Expand Selection") * Repeat(extra="n"),
        "Extract Field":
            R(Key("ca-f"), rdescript="Jet Brains: Expand Selection") * Repeat(extra="n"),
        "Extract Constant":
            R(Key("ca-c"), rdescript="Jet Brains: Expand Selection") * Repeat(extra="n"),
        "Extract Param":
            R(Key("ca-p"), rdescript="Jet Brains: Expand Selection") * Repeat(extra="n"),
        "go to editor":
            R(Key("escape")),
        "go to project":
            R(Key("a-1")),
        "run":
            R(Key("cs-f10"))
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


#---------------------------------------------------------------------------

context = AppContext(executable="idea", title="IntelliJ") \
          | AppContext(executable="idea64", title="IntelliJ") \
          | AppContext(executable="studio64") \
          | AppContext(executable="pycharm")
grammar = Grammar("IntelliJ + Android Studio + PyCharm", context=context)

if settings.SETTINGS["apps"]["jetbrains"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(JetbrainsRule())
    else:
        rule = JetbrainsRule(name="jet brains")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
