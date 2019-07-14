from dragonfly import MappingRule, Function
from dragonfly.grammar.grammar_base import Grammar


class TooEarlyGrammarActivatorError(Exception):
    def __init__(self):
        super("Do not attempt to build the activation rule before setting the de/activator functions.")


class GrammarActivator(object):

    """
    It is the responsibility of the Activator to manage a grammar for activating
    and deactivating rules. It is stateful.
    """
    def __init__(self, merge_rule_class):
        self._class_name_to_trigger = {}
        self._rule = None
        self._grammar = None
        self._activation_fn = self._construction_error
        self._merge_rule_class = merge_rule_class

    """
    De/activator function is injected from somewhere else.
    It is a function which takes:
    trigger: string representing what to call the rule
    active: boolean to set active or inactive
    """
    def set_activation_fn(self, activation_fn):
        self._activation_fn = activation_fn

    """
    register or re-register a rule;
    the "trigger" is what the rule is called when you say "enabled X" or "disable X"
    """
    def register_rule(self, managed_rule):
        trigger = self._get_best_trigger(managed_rule)
        self._class_name_to_trigger[managed_rule.rule_class.__name__] = trigger

    """
    Ideally we're dealing with a MergeRule and the trigger is its pronunciation. But since
    GrammarManager also manages pure Dragonfly rules, we might need to derive the name otherwise.
    """
    def _get_best_trigger(self, managed_rule):
        rule_instance = managed_rule.rule_class()
        if isinstance(rule_instance, self._merge_rule_class):
            return rule_instance.get_pronunciation()
        if managed_rule.details.name is not None:
            return managed_rule.details.name
        if managed_rule.details.grammar_name is not None:
            return managed_rule.details.grammar_name
        return managed_rule.rule_class.__name__

    def reconstruct_activation_rule(self):
        """construct new rule and grammar"""
        mapping = {}
        for class_name in self._class_name_to_trigger.keys():
            trigger = self._class_name_to_trigger[class_name]
            mapping["enable " + trigger] = Function(lambda: self._activation_fn(class_name, True))
            mapping["disable " + trigger] = Function(lambda: self._activation_fn(class_name, False))
        rule = MappingRule(mapping, [], {})
        grammar = Grammar("grammar_activator_grammar")
        grammar.add_rule(rule)

        '''destroy prior mapping'''
        if self._rule is not None:
            self._rule.disable()
            self._grammar.disable()
            del self._grammar

        '''set references and activate'''
        self._rule = rule
        self._grammar = grammar
        self._grammar.enable()

    def _construction_error(self, _1, _2):
        raise TooEarlyGrammarActivatorError()
