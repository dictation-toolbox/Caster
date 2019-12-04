import traceback

from dragonfly import Function, MappingRule

from castervoice.lib import printer
from castervoice.lib.ctrl.mgr.errors.invalid_transformation_error import InvalidTransformationError, ITMessage
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.ccrmerging2.activation_rule_generator import ActivationRuleGenerator
from castervoice.lib.merge.mergerule import MergeRule


class TransformersRunner(ActivationRuleGenerator):

    def __init__(self, config):
        self._transformers_config = config
        self._transformers = []

    def add_transformer(self, transformer_class):
        transformer = None

        # test instantiation
        try:
            transformer = transformer_class()
        except:
            err = "Error instantiating {}.".format(transformer_class.__name__)
            printer.out(err)
            return

        # register it
        if transformer.get_class_name() not in self._transformers_config:
            self._transformers_config.set_transformer_active(transformer.get_class_name(), False)
            self._transformers_config.save()
            printer.out("New transformer added: {}".format(transformer.get_class_name()))

        if self._transformers_config.is_transformer_active(transformer.get_class_name()):
            self._transformers.append(transformer)

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

    def transform_rule(self, rule_instance):
        r = rule_instance
        orig_class = TransformersRunner._get_rule_class(r)
        for transformer in self._transformers:
            try:
                r = transformer.get_transformed_rule(r)
                TransformersRunner._post_transform_validate(orig_class, r)
            except:
                err = "Error while running transformer {} with {} rule."
                printer.out(err.format(transformer, r))
                traceback.print_exc()
        return r

    @staticmethod
    def _get_rule_class(rule):
        return rule.__class__

    @staticmethod
    def _post_transform_validate(orig_class, rule):
        """
        There are only two changes you're not allowed to make to a rule.
        1. You're not allowed to change it into something which is not still its original class
           or a child class of its original class.
        2. You're not allowed to change the name of its class.
        """
        orig_rcn = orig_class.__name__
        current_class = TransformersRunner._get_rule_class(rule)

        no_class_change = orig_class == current_class
        maintains_mapping_rule = issubclass(orig_class, MappingRule) and issubclass(current_class, MappingRule)
        maintains_merge_rule = issubclass(orig_class, MergeRule) and issubclass(current_class, MergeRule)
        maintains = no_class_change or maintains_mapping_rule or maintains_merge_rule
        if not maintains:
            raise InvalidTransformationError(ITMessage.BAD_TYPE, orig_rcn)
        if orig_rcn != current_class.__name__:
            raise InvalidTransformationError(ITMessage.CLASS_KEY, orig_rcn)
