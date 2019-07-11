from castervoice.lib.imports import *


class FileDialogueRule(MergeRule):
    pronunciation = "file dialogue"

    mapping = {
        "up [<n>]": R(Key("a-up"))*Repeat(extra="n"),
        "back [<n>]": R(Key("a-left"))*Repeat(extra="n"),
        "forward [<n>]": R(Key("a-right"))*Repeat(extra="n"),
        "search [<text>]": R(Key("c-l, tab") + Text("%(text)s")),
        "organize": R(Key("c-l, tab:2")),
        "(left | navigation) pane": R(Key("c-l, tab:3")),
        "(center|file|files|folder) (list | pane)": R(Key("c-l, tab:4")),
        "sort [headings]": R(Key("c-l, tab:5")),
        "[file] name": R(Key("a-n")),
        "file type": R(Key("c-l, tab:7")),

    }
    extras = [IntegerRefST("n", 1, 10),
    Dictation("text"),]
    defaults = {
        "n": 1,
    }


dialogue_context = AppContext(title=[
        "open",
        "save",
        "select",
    ])
control.non_ccr_app_rule(FileDialogueRule(), context=dialogue_context)
