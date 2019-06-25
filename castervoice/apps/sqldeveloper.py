from castervoice.lib.imports import *

class SQLDeveloperRule(MergeRule):
    pronunciation = "sequel developer"

    mapping = {
        "run this query": R(Key("f9")),
        "format code": R(Key("c-f7")),
        "comment line": R(Key("c-slash")),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1}


context = AppContext(executable="sqldeveloper64W", title="SQL Developer")
control.non_ccr_app_rule(SQLDeveloperRule(), context=context)