from dragonfly import Dictation, Repeat, MappingRule

from castervoice.lib.actions import Text, Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R

# Directional Movement

RIGHT = "(right|sauce)"
LEFT = "(left|lease)"
UP = "(up|sauce)"
DOWN = "(down|dunce)"
FORWARD = "(%s|next|forward)" % RIGHT
BACK = "(%s|back|prev|prior|previous)" % LEFT

# Miscellaneous
method = "(meth|method)"
methods = "(meths|methods)"
extract = "(pull|extract)"

# Delay Timer
DELAY = "20"


class JetbrainsRule(MappingRule):

    mapping = {
        "quick fix": R(Key("a-enter")),
        "(duplicate|duple) %s" % DOWN: R(Key("c-d")),
        "find action": R(Key("cs-a")),
        "format [code]": R(Key("ca-l")),
        "show doc": R(Key("c-q")),
        "find class": R(Key("c-n")),
        "build": R(Key("c-f9")),
        "build and run": R(Key("s-f10")),
        "%s tab [<n>]|tab %s [<n>]" % (FORWARD, RIGHT): R(Key("a-right/%s" % DELAY)) * Repeat(extra="n"),
        "%s tab [<n>]|tab %s [<n>]" % (BACK, LEFT): R(Key("a-left/%s" % DELAY)) * Repeat(extra="n"),
        "(comment|rem) [line]": R(Key("c-slash")),
        "(uncomment|unrem) [line]": R(Key("cs-slash")),
        "select ex" : R(Key("c-w")),
        "select ex down" : R(Key("cs-w")),
        "find file": R(Key("shift, shift")),
        "find": R(Key("c-f")),
        "find next": R(Key("f3")),
        "find prior": R(Key("f3")),
        "find %s [match] [<n>]" % FORWARD: R(Key("enter")) * Repeat(extra="n"),
        "find %s [match] [<n>]" % BACK: R(Key("s-enter")) * Repeat(extra="n"),
        "replace [here]": R(Key("c-r")),
        "find [in] (all|files)": R(Key("cs-f")),
        "replace [in] (all|files)": R(Key("cs-r")),
        "go [to line] [<n>]": R(Key("c-g/%s" % DELAY) + Text("%(n)s") + Key("enter")),
        "implement (%s|%s)" % (method, methods): R(Key("c-i")),
        "override %s" % method: R(Key("c-o")),
        "run config": R(Key("as-f10")),
        "[find] (usage|usages)": R(Key("a-f7")),
        "show (usage|usages)": R(Key("ca-f7")),
        "[find] (usage|usages) in file": R(Key("c-f7")),
        "[go to] (source|declaration)": R(Key("c-b")),
        "[go to] implementation": R(Key("ca-b")),
        "(skraken|smart kraken)": R(Key("cs-space")),
        "go %s [<n>]" % FORWARD: R(Key("ca-right")) * Repeat(extra="n"),
        "go %s [<n>]" % BACK: R(Key("ca-left")) * Repeat(extra="n"),
        "%s %s [<n>]" % (method, FORWARD): R(Key("a-down")) * Repeat(extra="n"),
        "%s %s [<n>]" % (method, BACK): R(Key("a-up")) * Repeat(extra="n"),
        "go block start": R(Key("c-[")),
        "go block end": R(Key("c-]")),
        "(%s error|error %s)" % (FORWARD, RIGHT): R(Key("f2")) * Repeat(extra="n"),
        "(%s error|error %s)" % (BACK, LEFT): R(Key("s-f2")) * Repeat(extra="n"),
        "[organize|optimize] imports": R(Key("ca-o")) * Repeat(extra="n"),
        "[move] line %s [<n>]" % UP: R(Key("as-up")) * Repeat(extra="n"),
        "[move] line %s [<n>]" % DOWN: R(Key("as-down")) * Repeat(extra="n"),
        "expand [selection] [<n>]": R(Key("c-w")) * Repeat(extra="n"),
        "shrink [selection] [<n>]": R(Key("cs-w")) * Repeat(extra="n"),
        "auto indent": R(Key("ca-i")),
        "close tab [<n>]|tab close [<n>]": R(Key("c-f4/%s" % DELAY)) * Repeat(extra="n"),
        "run": R(Key("s-f10")),
        "debug": R(Key("s-f9")),
        "redo [<n>]": R(Key("cs-z")) * Repeat(extra="n"),
        "[show] settings": R(Key("ca-s")),
        "collapse": R(Key("c--")),
        "uncollapse": R(Key("c-+")),
        "collapse all": R(Key("cs--")),
        "uncollapse all": R(Key("cs-+")),

        # only works if you disable tabs.
        "close pane [<n>]|pane close [<n>]": R(Key("c-f4/%s" % DELAY)) * Repeat(extra="n"),

        # refactoring
        "refactor": R(Key("cas-t")),
        "rename": R(Key("s-f6")),
        "inline": R(Key("ca-n")),
        "(pull|extract)": R(Key("ca-m")),
        "%s [variable|var]" % extract: R(Key("ca-v")) * Repeat(extra="n"),
        "%s field" % extract: R(Key("ca-f")) * Repeat(extra="n"),
        "%s constant" % extract: R(Key("ca-c")) * Repeat(extra="n"),
        "%s (param|parameter)" % extract: R(Key("ca-p")) * Repeat(extra="n"),

        # debugging
        "step over": R(Key("f8")),
        "step into": R(Key("f7")),
        "smart step over": R(Key("s-f7")),
        "step out": R(Key("s-f8")),
        "toggle breakpoint": R(Key("c-f8")),
        "view breakpoints": R(Key("cs-f8,cs-f8")),
        "continue": R(Key("f9")),

        # window navigation
        "focus editor": R(Key("escape")),
        "go tool <n>": R(Key("a-%(n)s")),
        "[toggle] (term|terminal)": R(Key("a-f12")),

        # must be bound manually below this point
        "(kill|delete) %s" % FORWARD: R(Key("a-d,0")),
        "(kill|delete) %s" % BACK: R(Key("a-d,$")),

        # jet brains can only split horizontally or vertically
        "split [pane] %s" % UP: R(Key("cs-s,h")),
        "split [pane] %s" % DOWN: R(Key("cs-s,h")),
        "split [pane] %s" % RIGHT: R(Key("cs-s,v")),
        "split [pane] %s" % LEFT: R(Key("cs-s,v")),
        "pane %s [<n>]" % UP: R(Key("cs-s,up")) * Repeat(extra="n"),
        "pane %s [<n>]" % DOWN: R(Key("cs-s,down")) * Repeat(extra="n"),
        "(pane %s|%s pane) [<n>]" % (RIGHT, RIGHT): R(Key("cs-s,right")) * Repeat(extra="n"),
        "(pane %s|%s pane) [<n>]" % (LEFT, LEFT): R(Key("cs-s,left")) * Repeat(extra="n"),
        "file rename | rename file": R(Key("cas-r")),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]

    defaults = {"n": 1, "mim": ""}


def get_rule():
    details = RuleDetails(name="jet brains",
                          executable=["idea", "idea64", "studio64", "pycharm", "rider64", "webstorm", "webstorm64"])
    return JetbrainsRule, details
