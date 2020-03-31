from dragonfly import Mimic, MappingRule
from castervoice.lib.actions import Key


from castervoice.rules.apps.speech_engine.dragon_rules.dragon_support import extras_for_whole_file, defaults_for_whole_file
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class SpellingWindowRule(MappingRule):
    mapping = {
        # TODO: make these CCR

        "<first_second_third> word":
            R(Key("home, c-right:%(first_second_third)d, cs-right"),
              rdescript="Dragon: select the first second or third etc. word"),
        "last [word]": R(Key("right, cs-left"), rdescript="Dragon: select the last word"),
        "second [to] last word": R(Key("right, c-left:1, cs-left"), rdescript="Dragon: select the second to last word"),
        "<n10>": R(Mimic("choose", extra="n10"),
                   rdescript="Dragon: e.g. instead of having to say 'choose two' you can just say 'two'"),
        # consider making the above command global so that it works when you say something like
        # "insert before 'hello'" where there are multiple instances of 'hello'
        # personally I think it's better just to have the setting where Dragon choose is the closest instance

    }

    # see above
    extras = extras_for_whole_file()
    defaults = defaults_for_whole_file()


def get_rule():
    return SpellingWindowRule, RuleDetails(name="dragon spelling window", executable="natspeak")
