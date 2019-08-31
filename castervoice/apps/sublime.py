from castervoice.lib.imports import *


class SublimeRule(MergeRule):
    pronunciation = "sublime"

    mapping = {
        "new file":
            R(Key("c-n")),
        "new window":
            R(Key("cs-n")),
        "open file":
            R(Key("c-o")),
        "open folder":
            R(Key("f10, f, down:2, enter")),
        "open recent":
            R(Key("f10, f, down:3, enter")),
        "save as":
            R(Key("cs-s")),
        #
        "comment line":
            R(Key("c-slash")),
        "comment block":
            R(Key("cs-slash")),
        "outdent lines":
            R(Key("c-lbracket")),
        "join lines":
            R(Key("c-j")),
        "match bracket":
            R(Key("c-m")),
        #
        "(select | sell) all":
            R(Key("c-a")),
        "(select | sell) scope [<n2>]":
            R(Key("cs-space")),
        "(select | sell) brackets [<n2>]":
            R(Key("cs-m")),
        "(select | sell) indent":
            R(Key("cs-j")),
        #
        "find":
            R(Key("c-f")),
        "get all":
            R(Key("a-enter")),
        "replace":
            R(Key("c-h")),
        "edit lines":
            R(Key("cs-l")),
        "edit next [<n3>]":
            R(Key("c-d/10")),
        "edit up [<n3>]":
            R(Key("ac-up")),
        "edit down [<n3>]":
            R(Key("ac-down")),
        "edit all":
            R(Key("a-f3")),
        #
        "transform upper":
            R(Key("c-k, c-u")),
        "transform lower":
            R(Key("c-k, c-l")),
        #
        "line <ln1>":
            R(Key("c-g/10") + Text("%(ln1)s") + Key("enter")),
        "<action> [line] <ln1> [by <ln2>]":
            R(Function(navigation.action_lines)),
        "go to file":
            R(Key("c-p")),
        "go to <dict> [<filetype>]":
            R(Key("c-p") + Text("%(dict)s" + "%(filetype)s") + Key("enter")),
        "go to word":
            R(Key("c-semicolon")),
        "go to symbol":
            R(Key("c-r")),
        "go to [symbol in] project":
            R(Key("cs-r")),
        "go to that":
            R(Store() + Key("cs-r") + Retrieve() + Key("enter")),
        "find that in project":
            R(Store() + Key("cs-f") + Retrieve() + Key("enter")),
        "find that":
            R(Store() + Key("c-f") + Retrieve() + Key("enter")),
        "command pallette":
            R(Key("cs-p")),
        #
        "fold":
            R(Key("cs-lbracket")),
        "unfold":
            R(Key("cs-rbracket")),
        "unfold all":
            R(Key("c-k, c-j")),
        "fold [level] <n2>":
            R(Key("c-k, c-%(n2)s")),
        #
        "full screen":
            R(Key("f11")),
        "toggle side bar":
            R(Key("c-k, c-b")),
        "show key bindings":
            R(Key("f10, p, right, k")),
        "zoom in [<n2>]":
            R(Key("c-equal")),
        "zoom out [<n2>]":
            R(Key("c-minus")),
        #
        "(set | add) bookmark":
            R(Key("c-f2")),
        "next bookmark":
            R(Key("f2")),
        "previous bookmark":
            R(Key("s-f2")),
        "clear bookmarks":
            R(Key("cs-f2")),
        #
        "build it":
            R(Key("c-b")),
        #
        "record macro":
            R(Key("c-q")),
        "play [back] macro [<n3>]":
            R(Key("cs-q/10")),
        "(new | create) snippet":
            R(Key("ac-n")),
        #
        "close tab":
            R(Key("c-w")),
        "next tab":
            R(Key("c-pgdown")),
        "previous tab":
            R(Key("c-pgup")),
        "<nth> tab":
            R(Key("a-%(nth)s")),
        "column <cols>":
            R(Key("as-%(cols)s")),
        "focus <panel>":
            R(Key("c-%(panel)s")),
        "move <panel>":
            R(Key("cs-%(panel)s")),
        #
        "open terminal":
            R(Key("cs-t")),
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("ln1", 1, 1000),
        IntegerRefST("ln2", 1, 1000),
        IntegerRefST("n2", 1, 9),
        IntegerRefST("n3", 1, 21),
        Choice("action", navigation.actions),
        Choice(
            "nth", {
                "first": "1",
                "second": "2",
                "third": "3",
                "fourth": "4",
                "fifth": "5",
                "sixth": "6",
                "seventh": "7",
                "eighth": "8",
                "ninth": "9",
            }),
        Choice("cols", {
            "one": "1",
            "two": "2",
            "three": "3",
            "grid": "5",
        }),
        Choice("panel", {
            "one": "1",
            "left": "1",
            "two": "2",
            "right": "2",
        }),
        Choice("filetype", {
            "pie | python": "py",
            "mark [down]": "md",
            "tech": "tex",
            "tommel": "toml",
        }),
    ]
    defaults = {
        "ln2": "",
        "n2": 1,
        "n3": 1,
        "file type": "",
    }


context = AppContext(executable="sublime_text", title="Sublime Text")
control.non_ccr_app_rule(SublimeRule(), context=context)
