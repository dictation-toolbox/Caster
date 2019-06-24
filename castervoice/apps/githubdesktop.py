from dragonfly import (Grammar, Repeat, Choice)

from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib import control, settings
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class GitHubDeskRule(MergeRule):
    pronunciation = "github desktop"

    mapping = {
            "new repository":
                R(Key("c-n"), rdescript="GitHub: New Repository"),
            "add local repository":
                R(Key("c-o"), rdescript="GitHub: Add Local Repository"),
            "clone repository":
                R(Key("c-o"), rdescript="GitHub: Clone Repository"),
            "options":
                R(Key("c-comma"), rdescript="GitHub: Options"),

            "changes":
                R(Key("c-1"), rdescript="GitHub: Changes"),
            "history":
                R(Key("c-2"), rdescript="GitHub: History"),
            "(repositories | repository list)":
                R(Key("c-t"), rdescript="GitHub: (repositories | Repository List)"),
            "branches [list]":
                R(Key("c-b"), rdescript="GitHub: Branches [list]"),

            "zoom in [<n>]":
                R(Key("c-equals"), rdescript="GitHub: Zoom In [<n>]")*Repeat(extra="n"),
            "zoom out [<n>]":
                R(Key("c-minus"), rdescript="GitHub: Zoom Out [<n>]")*Repeat(extra="n"),
            "reset zoom":
                R(Key("c-0"), rdescript="GitHub: Reset Zoom"),

            "push [repository]":
                R(Key("c-p"), rdescript="GitHub: Push [repository]"),
            "pull [repository]":
                R(Key("cs-p"), rdescript="GitHub: Pull [repository]"),
            "remove repository":
                R(Key("c-delete"), rdescript="GitHub: Remove Repository"),
            "view on github":
                R(Key("cs-g"), rdescript="GitHub: View On Github"),
            "(terminal | command prompt)":
                R(Key("c-backtick"), rdescript="GitHub: (terminal | Command Prompt)"),
            "explorer":
                R(Key("cs-f"), rdescript="GitHub: Explorer"),
            "edit":
                R(Key("cs-a"), rdescript="GitHub: Edit"),

            "new branch":
                R(Key("cs-n"), rdescript="GitHub: New Branch"),
            "rename branch":
                R(Key("cs-r"), rdescript="GitHub: Rename Branch"),
            "delete branch":
                R(Key("cs-d"), rdescript="GitHub: Delete Branch"),

            "update from master":
                R(Key("cs-u"), rdescript="GitHub: Update From Master"),
            "compare to branch":
                R(Key("cs-b"), rdescript="GitHub: Compare To Branch"),
            "merge into current [branch]":
                R(Key("cs-m"), rdescript="GitHub: Merge Into Current [branch]"),

            "compare on github":
                R(Key("cs-c"), rdescript="GitHub: Compare On Github"),
            "[create] pull request":
                R(Key("c-r"), rdescript="GitHub: [create] Pull Request"),
        }
    extras = [
        IntegerRefST("n", 1, 10),

    ]
    defaults = {"n": 1}


#---------------------------------------------------------------------------

context = AppContext(executable="GitHubDesktop")
control.non_ccr_app_rule(GitHubDeskRule(), context=context)