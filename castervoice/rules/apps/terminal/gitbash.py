from dragonfly import Mimic, Function, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key, Text

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


def _apply(n):
    if n != 0:
        Text("stash@{" + str(int(n)) + "}").execute()


class GitBashRule(MappingRule):
    GIT_ADD_ALL = "g, i, t, space, a, d, d, space, minus, A"
    GIT_COMMIT = "g, i, t, space, c, o, m, m, i, t, space, minus, m, space, quote, quote, left"
    mapping = {
        "(git|get) base":
            Text("git "),
        "(git|get) (initialize repository|init)":
            Text("git init"),
        "(git|get) add":
            R(Key("g, i, t, space, a, d, d, space, dot")),
        "(git|get) add all":
            R(Key(GIT_ADD_ALL)),
        "(git|get) commit all":
            R(Key("%s, ;, space, %s" % (GIT_ADD_ALL, GIT_COMMIT))),
        "(git|get) status":
            R(Key("g, i, t, space, s, t, a, t, u, s")),
        "(git|get) commit":
            R(Key(GIT_COMMIT)),
        "(git|get) bug fix commit <n>":
            R(Mimic("get", "commit") + Text("fixes #%(n)d ") + Key("backspace")),
        "(git|get) reference commit <n>":
            R(Mimic("get", "commit") + Text("refs #%(n)d ") + Key("backspace")),
        "(git|get) checkout":
            R(Text("git checkout ")),
        "(git|get) branch":
            R(Text("git branch ")),
        "(git|get) remote":
            R(Text("git remote ")),
        "(git|get) merge":
            R(Text("git merge ")),
        "(git|get) merge tool":
            R(Text("git mergetool")),
        "(git|get) fetch":
            R(Text("git fetch ")),
        "(git|get) push":
            R(Text("git push ")),
        "(git|get) pull":
            R(Text("git pull ")),
        "CD up":
            R(Text("cd ..")),
        "CD":
            R(Text("cd ")),
        "list":
            R(Text("ls")),
        "make directory":
            R(Text("mkdir ")),
        "undo [last] commit | (git|get) reset soft head":
            R(Text("git reset --soft HEAD~1")),
        "(undo changes | (git|get) reset hard)":
            R(Text("git reset --hard")),
        "stop tracking [file] | (git|get) remove":
            R(Text("git rm --cached ")),
        "preview remove untracked | (git|get) clean preview":
            R(Text("git clean -nd")),
        "remove untracked | (git|get) clean untracked":
            R(Text("git clean -fd")),
        "(git|get) visualize":
            R(Text("gitk")),
        "(git|get) visualize file":
            R(Text("gitk -- PATH")),
        "(git|get) visualize all":
            R(Text("gitk --all")),
        "(git|get) stash":
            R(Text("git stash")),
        "(git|get) stash apply [<n>]":
            R(Text("git stash apply") + Function(_apply)),
        "(git|get) stash list":
            R(Text("git stash list")),
        "(git|get) stash branch":
            R(Text("git stash branch NAME")),
        "(git|get) cherry pick":
            R(Text("git cherry-pick ")),
        "(git|get) (abort cherry pick | cherry pick abort)":
            R(Text("git cherry-pick --abort")),
        "(git|get) (GUI | gooey)":
            R(Text("git gui")),
        "(git|get) blame":
            R(Text("git blame PATH -L FIRSTLINE,LASTLINE")),
        "(git|get) gooey blame":
            R(Text("git gui blame PATH")),
        "search recursive":
            R(Text("grep -rinH \"PATTERN\" *")),
        "search recursive count":
            R(Text("grep -rinH \"PATTERN\" * | wc -l")),
        "search recursive file type":
            R(Text("find . -name \"*.java\" -exec grep -rinH \"PATTERN\" {} \\;")),
        "to file":
            R(Text(" > FILENAME")),
    }
    extras = [
        ShortIntegerRef("n", 1, 10000),
    ]
    defaults = {"n": 0}


_executables = [
    "\\sh.exe",
    "\\bash.exe",
    "\\cmd.exe",
    "\\mintty.exe",
    "\\powershell.exe",
    "idea",
    "idea64",
    "studio64",
    "pycharm"
]


def get_rule():
    return GitBashRule, RuleDetails(name="git bash", executable=_executables)

