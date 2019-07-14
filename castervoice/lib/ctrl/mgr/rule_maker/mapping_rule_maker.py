from dragonfly import Grammar, AppContext
from castervoice.lib.ctrl.mgr.rule_maker.base_rule_maker import BaseRuleMaker


class MappingRuleMaker(BaseRuleMaker):

    def __init__(self, gdef_transformer):
        self._gdef_transformer = gdef_transformer

    def create_non_ccr_grammar(self, rule_class, details):
        rule_instance = rule_class(name=details.name)
        rule_instance = self._gdef_transformer.get_transformed_rule(rule_instance)

        context = None
        if details.executable is not None:
            context = AppContext(executable=details.executable)
        grammar = Grammar(details.grammar_name, context=context)
        grammar.add_rule(rule_instance)
        return grammar
