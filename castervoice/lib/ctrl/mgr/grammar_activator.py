from dragonfly import MappingRule, Function

from castervoice.lib.ctrl.mgr.errors.no_pronunciation_error import NoPronunciationError
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails


class GrammarActivator(object):
    """
    It is the responsibility of the Activator to manage a grammar for activating
    and deactivating rules. It is stateful.
    """

    def __init__(self, merge_rule_checker_fn):
        self._class_name_to_trigger = {}
        self._activation_rule_class = None
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
        trigger = self._get_trigger(managed_rule)
        self._class_name_to_trigger[managed_rule.get_rule_class_name()] = trigger

    def _get_trigger(self, managed_rule):
        """
        Ideally we're dealing with a MergeRule and the trigger is its pronunciation. But since
        GrammarManager also manages pure Dragonfly rules, we might need to derive the name otherwise.
        """
        rule_instance = managed_rule.get_rule_instance()
        if self._merge_rule_checker_fn(rule_instance):
            return rule_instance.get_pronunciation()
        if managed_rule.get_details().name is not None:
            return managed_rule.get_details().name
        raise NoPronunciationError(managed_rule.get_rule_class_name())

    def construct_activation_rule(self):
        """
        Construct new rule and for activation.
        Should be called once only, after initial content loading.
        Rule reloading does not watch for new files, so no need to ever call this again.
        """
        if self._activation_rule_class is not None:
            return None

        _mapping = {}
        for class_name, trigger in self._class_name_to_trigger.items():
            enable_spec = "enable {}".format(trigger)
            disable_spec = "disable {}".format(trigger)
            _mapping[enable_spec] = Function(lambda rcn: self._activation_fn(rcn, True), rcn=class_name)
            _mapping[disable_spec] = Function(lambda rcn: self._activation_fn(rcn, False), rcn=class_name)

        class GrammarActivatorRule(MappingRule):
            mapping = _mapping
        self._activation_rule_class = GrammarActivatorRule

        # name that should be pretty difficult to say by mistake:
        details = RuleDetails(name="grammar manager grammar activator rule",
                              watch_exclusion=True)

        return self._activation_rule_class, details
