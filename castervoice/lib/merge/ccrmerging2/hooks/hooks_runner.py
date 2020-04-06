from dragonfly import Function, MappingRule
import traceback

from castervoice.lib import printer
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.ccrmerging2.activation_rule_generator import ActivationRuleGenerator
from castervoice.lib import settings
from castervoice.lib.merge.state.short import R


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

        # register new hook and enables default hooks
        default_hooks = settings.SETTINGS["hooks"]["default_hooks"]
        if hook.get_class_name() not in self._hooks_config:
            if hook.get_class_name() in default_hooks:
                self._hooks_config.set_hook_active(hook.get_class_name(), True)
                printer.out("Default hook added and enabled: {}".format(hook.get_class_name()))
            else:
                self._hooks_config.set_hook_active(hook.get_class_name(), False)
                printer.out("New hook added: {}".format(hook.get_class_name()))
        self._hooks_config.save()

    def construct_activation_rule(self):
        m = {}
        for hook in self._hooks:
            enable_action = R(Function(lambda: self._hooks_config.set_hook_active(hook.get_class_name(), True)) + Function(hook._run_on_enable))
            disable_action = R(Function(lambda: self._hooks_config.set_hook_active(hook.get_class_name(), False)) + Function(hook._run_on_disable))
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
                    err = "Error while running hook {} with {} event.\n"
                    printer.out(err.format(hook, event.get_type()))
                    traceback.print_exc()