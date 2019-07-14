from dragonfly import Grammar, AppContext
from castervoice.lib import settings
from castervoice.lib.ctrl.mgr.managed_rule import ManagedRule
from castervoice.lib.ctrl.mgr.rule_maker.base_rule_maker import BaseRuleMaker


class MappingRuleMaker(BaseRuleMaker):

    def __init__(self, gdef_transformer):
        self._gdef_transformer = gdef_transformer

    def create_managed_rule(self, rule_class, details):
        '''TODO: move this "rdp_mode" somewhere else'''
        if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
            self._load_via_merger(rule_class(), details)
        else:
            rule_instance = rule_class(name=details.name)
            rule_instance = self._gdef_transformer.get_transformed_rule(rule_instance)

            context = None
            if details.executable is not None:
                context = AppContext(executable=details.executable)
            grammar = Grammar(details.grammar_name, context=context)
            grammar.add_rule(rule_instance)
            return ManagedRule(rule_class, details, grammar)
