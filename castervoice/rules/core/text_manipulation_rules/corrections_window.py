from dragonfly import MappingRule, Function, Choice
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.asynch.corrections.manager import send_choice, cancel, choice_grammar_enabled



class CorrectionsWindowRule(MappingRule):
    """
    Rules to be invoked when the corrections window is displayed.
    They are forwarded into the process that is met and edging the corrections window
    so that it can respond appropriately.
    """

    mapping = {
        "cancel": R(Function(cancel)),
        "choose <choice>": R(Function(send_choice)),
    }
    extras = [
        IntegerRefST("choice", 0, 100),
    ]


def get_rule():
    details = RuleDetails(name="corrections window", function_context=choice_grammar_enabled)
    return CorrectionsWindowRule, details
