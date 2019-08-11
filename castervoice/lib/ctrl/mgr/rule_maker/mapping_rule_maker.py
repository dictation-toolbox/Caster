from dragonfly import Grammar, AppContext
from castervoice.lib.ctrl.mgr.rule_maker.base_rule_maker import BaseRuleMaker


class MappingRuleMaker(BaseRuleMaker):
    """
    Creates a MappingRule instance from the rule's class and a RuleDetails
    object, then runs all transformers over it.
    """

    def __init__(self, smr_configurer):
        self._transformers = []
        self._smr_configurer = smr_configurer

    def add_transformer(self, transformer):
        self._transformers.append(transformer)

    def create_non_ccr_grammar(self, rule_class, details):
        rule_instance = rule_class(name=details.name)
        if not details.transformer_exclusion:
            for transformer in self._transformers:
                rule_instance = transformer.get_transformed_rule(rule_instance)

        self._smr_configurer.configure(rule_instance)

        context = None
        if details.executable is not None:
            context = AppContext(executable=details.executable, title=details.title)
        grammar = Grammar(details.grammar_name, context=context)
        grammar.add_rule(rule_instance)
        return grammar
