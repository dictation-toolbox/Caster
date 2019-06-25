from castervoice.lib.imports import *


class GitHubDeskRule(MergeRule):
    pronunciation = "github desktop"

    mapping = {
        "new repository": R(Key("c-n")),
        "add local repository": R(Key("c-o")),
        "clone repository": R(Key("c-o")),
        "options": R(Key("c-comma")),

        "changes": R(Key("c-1")),
        "history": R(Key("c-2")),
        "(repositories | repository list)": R(Key("c-t")),
        "branches [list]": R(Key("c-b")),

        "zoom in [<n>]": R(Key("c-equals"))*Repeat(extra="n"),
        "zoom out [<n>]": R(Key("c-minus"))*Repeat(extra="n"),
        "reset zoom": R(Key("c-0")),

        "push [repository]": R(Key("c-p")),
        "pull [repository]": R(Key("cs-p")),
        "remove repository": R(Key("c-delete")),
        "view on github": R(Key("cs-g")),
        "(terminal | command prompt)": R(Key("c-backtick")),
        "explorer": R(Key("cs-f")),
        "edit": R(Key("cs-a")),

        "new branch": R(Key("cs-n")),
        "rename branch": R(Key("cs-r")),
        "delete branch": R(Key("cs-d")),

        "update from master": R(Key("cs-u")),
        "compare to branch": R(Key("cs-b")),
        "merge into current [branch]": R(Key("cs-m")),

        "compare on github": R(Key("cs-c")),
        "[create] pull request": R(Key("c-r")),
    }
    extras = [
        IntegerRefST("n", 1, 10),
    ]
    defaults = {"n": 1}


context = AppContext(executable="GitHubDesktop")
control.non_ccr_app_rule(GitHubDeskRule(), context=context)