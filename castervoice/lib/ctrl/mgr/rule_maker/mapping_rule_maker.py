from dragonfly import Grammar, AppContext
from castervoice.lib.ctrl.mgr.rule_maker.base_rule_maker import BaseRuleMaker


class MappingRuleMaker(BaseRuleMaker):
    """
    Creates a MappingRule instance from the rule's class and a RuleDetails
    object, then runs the "words.txt" transformer over it.
    """

    def __init__(self, gdef_transformer, smr_configurer):
        self._gdef_transformer = gdef_transformer
        self._smr_configurer = smr_configurer

    def create_non_ccr_grammar(self, rule_class, details):
        rule_instance = rule_class(name=details.name)
        rule_instance = self._gdef_transformer.get_transformed_rule(rule_instance)

        self._smr_configurer.configure(rule_instance)

        context = None
        if details.executable is not None:
            context = AppContext(executable=details.executable)
        grammar = Grammar(details.grammar_name, context=context)
        grammar.add_rule(rule_instance)
        return grammar
