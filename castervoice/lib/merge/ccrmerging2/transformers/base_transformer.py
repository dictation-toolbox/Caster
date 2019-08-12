'''
Transformers are the successor to legacy Caster's
"filter functions". The main differences between
them are that:
1. transformers operate on single rules instead of rule pairs
2. transformers assume that the rules passed to them are non-null
3. transformers enforce immutability
4. transformers have no concept of "time" or "order"
'''
from castervoice.lib import utilities, printer
from castervoice.lib.ctrl.mgr.errors.base_class_error import DontUseBaseClassError
from castervoice.lib.merge.ccrmerging2.pronounceable import Pronounceable


class BaseRuleTransformer(Pronounceable):
    """
    Authors of new transformers should override the following methods:
    _transform
    _is_applicable methods
    get_pronunciation
    """

    def get_transformed_rule(self, rule):
        try:
            if self._is_applicable(rule):
                rule_copy = None
                if hasattr(rule, "copy"):
                    rule_copy = rule.copy()
                else:
                    rule_copy = utilities.copy_dragonfly_mapping_rule(rule)
                return self._transform(rule_copy)
        except:
            err = "Error while running transformer {} with {} rule."
            printer.out(err.format(self, rule))
        return rule

    def _transform(self, rule):
        raise DontUseBaseClassError(self)

    def _is_applicable(self, rule):
        raise DontUseBaseClassError(self)
