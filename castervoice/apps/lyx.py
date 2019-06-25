from castervoice.lib.imports import *

class LyxRule(MergeRule):
    pronunciation = "lyx"

    mapping = {
        "new file": R(Key("c-n"), rdescript="LyX: new file"),
        "open file": R(Key("c-o"), rdescript="LyX: open file"),
        "save as": R(Key("cs-s"), rdescript="LyX: save as"),

        "math mode": R(Key("c-m"), rdescript="LyX: math mode"),
        "display mode": R(Key("cs-m"), rdescript="LyX: display mode"),

        "view PDF": R(Key("c-r"), rdescript="LyX: view PDF"),
        "update PDF": R(Key("cs-r"), rdescript="LyX: update PDF"),

        "move line up [<n>]": R(Key("a-up"), rdescript="LyX: move line up")*Repeat(extra="n"),
        "move line down [<n>]": R(Key("a-down"), rdescript="LyX: move line down")*Repeat(extra="n"),

        "insert <environment>": R(Key("a-i, h, %(environment)s"), rdescript="LyX: insert environment"),
        }
    extras = [
        IntegerRefST("n", 1, 10),
        Choice("environment", {
            "(in line formula | in line)": "i",
            "(display formula | display)": "d",
            "(equation array environment | equation array)": "e",
            "(AMS align environment | AMS align)": "a",
            "AMS align at [environment]": "t",
            "AMS flalign [environment]": "f",
            "(AMS gathered environment | AMS gather)": "g",
            "(AMS multline [environment]| multiline)": "m",
            "array [environment]": "y",
            "(cases [environment] | piecewise)": "c",
            "(aligned [environment] | align)": "l",
            "aligned at [environment]": "v",
            "gathered [environment]": "h",
            "split [environment]": "s",
            "delimiters": "r",
            "matrix": "x",
            "macro": "o",
            }),
    ]
    defaults = {
        "n": 1,
    }


context = AppContext(executable="lyx")
control.non_ccr_app_rule(LyxRule(), context=context)