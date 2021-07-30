from dragonfly import Repeat, Dictation, MappingRule, ShortIntegerRef
from castervoice.lib.actions import Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class MSVCRule(MappingRule):
    mapping = {
        "cursor prior": R(Key("c-minus")),
        "cursor next": R(Key("cs-minus")),
        "toggle full screen": R(Key("sa-enter")),
        "resolve": R(Key("c-dot")),
        "jump to source": R(Key("f12")),
        "snippet": R(Key("tab")),
        "step over [<n>]": R(Key("f10/50")*Repeat(extra="n")),
        "step into": R(Key("f11")),
        "step out [of]": R(Key("s-f11")),
        "resume": R(Key("f8")),
        "build [last]": R(Key("ca-f7")),
        "debug [last]": R(Key("f5")),
        "comment out": R(Key("c-k/50, c-c")),
        "on comment out": R(Key("c-k/50, c-u")),
        "set bookmark": R(Key("c-k, c-k")),
        "next bookmark": R(Key("c-k, c-n")),
        "break point": R(Key("f9")),
        "format code": R(Key("cs-f")),
        "(do imports | import all)": R(Key("cs-o")),
        "comment line": R(Key("c-slash")),
        "go to line": R(Key("c-g")),
    }
    extras = [
        Dictation("text"),
        ShortIntegerRef("n", 1, 1000),
    ]
    defaults = {"n": 1}


def get_rule():
    return MSVCRule, RuleDetails(name="Microsoft visual studio", executable="WDExpress")
