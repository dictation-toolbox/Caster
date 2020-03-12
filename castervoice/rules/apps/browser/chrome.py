from dragonfly import Repeat, Pause, Function, Choice, MappingRule

from castervoice.lib.actions import Key, Mouse, Text

from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve

class ChromeRule(MappingRule):
    mapping = {
        "(new window|win new)":
            R(Key("c-n")),
        "(new incognito window | incognito)":
            R(Key("cs-n")),
        "new tab [<n>]|tab new [<n>]":
            R(Key("c-t") * Repeat(extra="n")),
        "reopen tab [<n>]|tab reopen [<n>]":
            R(Key("cs-t")) * Repeat(extra="n"),
        "close tab [<n>]|tab close [<n>]":
            R(Key("c-w")) * Repeat(extra='n'),
        "win close|close all tabs":
            R(Key("cs-w")),
        "(next|forward) tab [<n>]|tab (right|sauce) [<n>]":
            R(Key("c-tab")) * Repeat(extra="n"),
        "(back|previous) tab [<n>]|tab (left|lease) [<n>]":
            R(Key("cs-tab")) * Repeat(extra="n"),    
        "new tab that":
            R(Mouse("middle") + Pause("20") + Key("c-tab")),
        "go (back|prev|prior|previous) [<n>]":
            R(Key("a-left/20")) * Repeat(extra="n"),
        "go (next|forward) [<n>]":
            R(Key("a-right/20")) * Repeat(extra="n"),
        "zoom in [<n>]":
            R(Key("c-plus/20")) * Repeat(extra="n"),
        "zoom out [<n>]":
            R(Key("c-minus/20")) * Repeat(extra="n"),
        "zoom reset":
            R(Key("c-0")),
        "(hard refresh|super refresh)":
            R(Key("c-f5")),
        "find (next|forward) [match] [<n>]":
            R(Key("c-g/20")) * Repeat(extra="n"),
        "find (back|prev|prior|previous) [match] [<n>]":
            R(Key("cs-g/20")) * Repeat(extra="n"),
        # requires an extension in some browsers such as chrome
        "[toggle] caret browsing":
            R(Key("f7")),
        "[go] home [page]":
            R(Key("a-home")),
        "[show] history":
            R(Key("c-h")),
        "address bar":
            R(Key("c-l")),
        "[show] downloads":
            R(Key("c-j")),
        "[add] bookmark":
            R(Key("c-d")),
        "bookmark all [tabs]":
            R(Key("cs-d")),
       "[show] bookmarks":
            R(Key("cs-o")),
        "[toggle] full screen":
            R(Key("f11")),
        "(show|view) page source":
            R(Key("c-u")),
        "resume":
            R(Key("f8")),
        "step over":
            R(Key("f10")),
        "step into":
            R(Key("f11")),
        "step out":
            R(Key("s-f11")),
        "(duplicate tab|tab duple)":
            R(Key("a-d,a-c,c-t/15,c-v/15, enter")),
        "(duplicate window|win duple)":
            R(Key("a-d,a-c,c-n/15,c-v/15, enter")),
        "[show] (menu | three dots)":
            R(Key("a-f")),
        "[show] settings":
            R(Key("a-f/5, s")),
        "[show chrome] task manager":
            R(Key("s-escape")),
        "(clear history|clear browsing data)":
            R(Key("cs-del")),
        "[show] developer tools":
            R(Key("cs-i")),
        "checkout [this] pull request [locally]":
            R(Function(github_automation.github_checkoutupdate_pull_request, new=True)),
        "update [this] pull request [locally]":
            R(Function(github_automation.github_checkoutupdate_pull_request, new=False)),
        "IRC identify":
            R(Text("/msg NickServ identify PASSWORD")),
        "tab <m>|<nth> tab":
            R(Key("c-%(m)s%(nth)s")),
        "last tab":
            R(Key("c-9")),
        "second last tab":
            R(Key("c-9, cs-tab")),
        "switch focus [<n>]":
            R(Key("f6/20")) * Repeat(extra="n"),
        "[toggle] bookmark bar":
            R(Key("cs-b")),
        "switch user":
            R(Key("cs-m")),
        "focus notification":
            R(Key("a-n")),
        "allow notification":
            R(Key("as-a")),
        "deny notification":
            R(Key("as-a")),
        "google that":
            R(Store(remove_cr=True) + Key("c-t") + Retrieve() + Key("enter")),
        "wikipedia that":
            R(Store(space="+", remove_cr=True) + Key("c-t") + Text(
                "https://en.wikipedia.org/w/index.php?search=") + Retrieve() + Key("enter")),
        "[show] (extensions|plugins)":
            R(Key("a-f/20, l, e/15, enter")),
        "more tools":
            R(Key("a-f/5, l")),
    }
    extras = [
        Choice("nth", {
                "first": "1",
                "second": "2",
                "third": "3",
                "fourth": "4",
                "fifth": "5",
                "sixth": "6",
                "seventh": "7",
                "eighth": "8",
            }),
        IntegerRefST("n", 1, 100),
        IntegerRefST("m", 1, 10)
    ]
    defaults = {"n": 1, "m":"", "nth": ""}


def get_rule():
    return ChromeRule, RuleDetails(name="google chrome", executable="chrome")
