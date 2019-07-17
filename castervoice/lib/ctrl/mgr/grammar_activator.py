from dragonfly import MappingRule, Function
from dragonfly.grammar.grammar_base import Grammar


class GrammarActivator(object):
    """
    It is the responsibility of the Activator to manage a grammar for activating
    and deactivating rules. It is stateful.
    """

    def __init__(self, merge_rule_checker_fn):
        self._class_name_to_trigger = {}
        self._activation_grammar = None
        self._activation_fn = None
        self._merge_rule_checker_fn = merge_rule_checker_fn

    def set_activation_fn(self, activation_fn):
        """
        De/activator function is injected from somewhere else.
        It is a function which takes:
        trigger: string representing what to call the rule
        active: boolean to set active or inactive
        """
        self._activation_fn = activation_fn

    def register_rule(self, managed_rule):
        """
        register or re-register a rule;
        the "trigger" is what the rule is called when you say "enabled X" or "disable X"
        """
        trigger = self._get_best_trigger(managed_rule)
        self._class_name_to_trigger[managed_rule.get_rule_class_name()] = trigger

    def _get_best_trigger(self, managed_rule):
        """
        Ideally we're dealing with a MergeRule and the trigger is its pronunciation. But since
        GrammarManager also manages pure Dragonfly rules, we might need to derive the name otherwise.
        """
        rule_instance = managed_rule.get_rule_instance()
        if self._merge_rule_checker_fn(rule_instance):
            return rule_instance.get_pronunciation()
        if managed_rule.details.name is not None:
            return managed_rule.details.name
        if managed_rule.details.grammar_name is not None:
            return managed_rule.details.grammar_name
        return managed_rule.get_rule_class_name()

    def construct_activation_rule(self):
        """
        Construct new rule and grammar for activation.
        Should be called once only, after initial content loading.
        Rule reloading does not watch for new files, so no need to ever call this again.
        """
        if self._activation_grammar is not None:
            return

        mapping = {}
        for class_name in self._class_name_to_trigger.keys():
            trigger = self._class_name_to_trigger[class_name]
            mapping["enable " + trigger] = Function(lambda: self._activation_fn(class_name, True))
            mapping["disable " + trigger] = Function(lambda: self._activation_fn(class_name, False))
        rule = MappingRule(mapping, [], {})
        grammar = Grammar("grammar_activator_grammar")
        grammar.add_rule(rule)

        '''set references and activate'''
        self._activation_grammar = grammar
        self._activation_grammar.enable()
