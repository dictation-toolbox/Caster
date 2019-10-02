from dragonfly import Function, MappingRule

from castervoice.lib import printer
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.ccrmerging2.activation_rule_generator import ActivationRuleGenerator


class TransformersRunner(ActivationRuleGenerator):

    def __init__(self, config):
        self._transformers_config = config
        self._transformers = []

    def add_transformer(self, transformer_class):
        transformer = None

        # test instantiation
        try:
            transformer = transformer_class()
            self._transformers.append(transformer)
        except:
            err = "Error instantiating {}.".format(transformer_class.__name__)
            printer.out(err)
            return

        # register it
        if transformer.get_class_name() not in self._transformers_config:
            self._transformers_config.set_transformer_active(transformer.get_class_name(), False)
            self._transformers_config.save()
            printer.out("New transformer added: {}".format(transformer.get_class_name()))

    def construct_activation_rule(self):
        m = {}
        for t in self._transformers:
            enable_action = \
                Function(lambda: self._transformers_config.set_transformer_active(t.get_class_name(), True))
            disable_action = \
                Function(lambda: self._transformers_config.set_transformer_active(t.get_class_name(), False))
            m["enable {} transformer".format(t.get_pronunciation())] = enable_action
            m["disable {} transformer".format(t.get_pronunciation())] = disable_action

        class TransformersActivationRule(MappingRule):
            mapping = m
        details = RuleDetails(name="transformers runner transformers activator rule",
                              watch_exclusion=True)

        return TransformersActivationRule, details

    def transform_rule(self, rule):
        for transformer in self._transformers:
            if not self._transformers_config.is_transformer_active(transformer.get_class_name()):
                continue
            try:
                rule = transformer.get_transformed_rule(rule)
            except:
                err = "Error while running transformer {} with {} rule."
                printer.out(err.format(transformer, rule))
        return rule
