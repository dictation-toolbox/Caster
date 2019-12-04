from dragonfly import Function, MappingRule
import traceback

from castervoice.lib import printer
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.ccrmerging2.activation_rule_generator import ActivationRuleGenerator


class HooksRunner(ActivationRuleGenerator):
    def __init__(self, config):
        self._hooks = []
        self._hooks_config = config

    def add_hook(self, hook_class):
        hook = None

        # test instantiation
        try:
            hook = hook_class()
            self._hooks.append(hook)
        except:
            err = "Error instantiating {}.".format(hook_class.__name__)
            traceback.print_exc()
            printer.out(err)
            return

        # register it
        if hook.get_class_name() not in self._hooks_config:
            self._hooks_config.set_hook_active(hook.get_class_name(), False)
            self._hooks_config.save()
            printer.out("New hook added: {}".format(hook.get_class_name()))

    def construct_activation_rule(self):
        m = {}
        for hook in self._hooks:
            enable_action = Function(lambda: self._hooks_config.set_hook_active(hook.get_class_name(), True))
            disable_action = Function(lambda: self._hooks_config.set_hook_active(hook.get_class_name(), False))
            m["enable {} hook".format(hook.get_pronunciation())] = enable_action
            m["disable {} hook".format(hook.get_pronunciation())] = disable_action

        class HooksActivationRule(MappingRule):
            mapping = m
        details = RuleDetails(name="hooks runner hooks activator rule",
                              watch_exclusion=True)

        return HooksActivationRule, details

    def execute(self, event):
        for hook in self._hooks:
            if not self._hooks_config.is_hook_active(hook.get_class_name()):
                continue
            if hook.match(event.get_type()):
                try:
                    hook.run(event)
                except:
                    err = "Error while running hook {} with {} event."
                    printer.out(err.format(hook, event.get_type()))
