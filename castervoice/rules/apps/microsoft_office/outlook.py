from dragonfly import Function, Repeat, Dictation, Choice, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


def capitalize(text):
    output = str(text).title()
    Text(output).execute()


class OutlookRule(MappingRule):
    mapping = {
        # create new thing
        "new (appointment | event)": R(Key("sc-a")),
        "new contact": R(Key("cs-c")),
        "new folder": R(Key("cs-e")),
        "advanced (search| find)": R(Key("cs-f")),
        "new office document": R(Key("cs-h")),
        "(inbox | go to inbox)": R(Key("cs-i")),
        "new journal entry": R(Key("cs-j")),
        "new task": R(Key("cs-k")),
        "new contact group": R(Key("cs-l")),
        "(new message| new mail)": R(Key("cs-m")),
        "new note": R(Key("cs-n")),
        "open the new search folder window": R(Key("cs-p")),
        "new meeting request": R(Key("cs-q")),
        "new task request": R(Key("cs-u")),

        # new message window
        "to field": R(Key("a-dot")),
        "c c field": R(Key("a-c")),
        "subject [field]": R(Key("a-u")),
        "subject <text>": R(Key("a-u") + Function(capitalize) + Key("tab")),
        "attach file": R(Key("n, a, f")),
        "add to dictionary": R(Key("s-f10/2, a")),
        "click send message": R(Key("a-s")),  # be careful
        "find and replace": R(Key("c-h")),
        "check names": R(Key("c-k")),
        "spell check": R(Key("f7")),
        "save as": R(Key("f12")),  # only in mail view

        # folders pane
        "expand [that]": R(Key("asterisk")),
        "collapse [that]": R(Key("minus")),

        # folders navigation
        # some of these may be user dependent, depends on the order of your folders
        # which you can inspect by pressing control y
        # also I think some of these are built into Dragon
        "[go to] sent mail": R(Key("c-y/10, s, enter")),
        "go to drafts": R(Key("c-y/10, d, enter")),
        "go to trash": R(Key("c-y/10, t, enter")),
        "go to spam": R(Key("c-y/10, s:2, enter")),
        "go to starred": R(Key("c-y/10, s:3, enter")),
        "go to important": R(Key("c-y/10, i:2, enter")),
        "go to outbox": R(Key("cs-o")),

        # center pane
        "sort by [<sort_by>]": R(Key("a-v/5, a, b/5, %(sort_by)s")),
        "reverse sort": R(Key("a-v, r, s")),
        "block sender": R(Key("a-h/3, j/3, b")),
        "search [bar] [<dict>]": R(Key("c-e") + Text("%(dict)s")),
        "(message list | messages)": R(Key("tab:3")),
        "(empty | clear) search [bar]": R(Key("c-e, c-a, del/3, escape")),
        # from the search bar to get the focus into the messages is three tabs
        # pressing escape also seems to work.
        "refresh [mail]": R(Key("f9")),

        # reading pane
        "open attachment": R(Key("s-tab, enter")),
        "[open] attachment menu": R(Key("s-tab, right")),
        "next message [<n>]": R(Key("s-f6/10, down"))*Repeat(extra='n'),
        "(prior | previous) message [<n>]": R(Key("s-f6/20, up"))*Repeat(extra='n'),
        "[select] next link": R(Key("tab")),
        "[select] (previous | prior) link": R(Key("s-tab")),

        # calendar
        "workweek [view]": R(Key("ca-2")),
        "full week [view]": R(Key("ca-3")),
        "month view": R(Key("ca-4")),

        # message shortcuts
        "reply [<dict>]": R(Key("c-r") + Text("%(dict)s")),
        "reply all [<dict>]": R(Key("cs-r") + Text("%(dict)s")),
        "forward": R(Key("c-f")),
        "Mark as read": R(Key("c-q")),
        "Mark as unread": R(Key("c-u")),
        "(folder | go to folder)": R(Key("c-y")),

        # navigation
        "next pane [<n>]": R(Key("f6"))*Repeat(extra='n'),
        "(un|prior|previous) pane [<n>]": R(Key("s-f6"))*Repeat(extra='n'),
        "mail view": R(Key("c-1")),
        "calendar": R(Key("c-2")),
        "contacts": R(Key("c-3")),
        "tasks": R(Key("c-4")),
        "go to notes": R(Key("c-5")),
        "folder list": R(Key("c-6")),
        "find contact": R(Key("f11")),
        "address book": R(Key("cs-a")),
        "next open message": R(Key("c-dot")),
        "(prior | previous) open message": R(Key("c-comma")),
        "previous view": R(Key("a-left")),
        "next view": R(Key("a-right")),

        # misc
        "[go] back": R(Key("a-left")),
    }
    extras = [
        Dictation("dict"),
        Dictation("text"),
        ShortIntegerRef("n", 1, 100),
        Choice(
            "sort_by", {
                "date": "d",
                "from": "f",
                "to": "t",
                "size": "s",
                "subject": "j",
                "type": "t",
                "attachments": "c",
                "account": "o",
            }),
    ]
    defaults = {"n": 1, "dict": "", "text": "", "sort_by": ""}


def get_rule():
    return OutlookRule, RuleDetails(name="outlook", executable="outlook")
