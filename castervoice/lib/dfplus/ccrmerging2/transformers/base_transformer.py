'''
Transformers are the successor to legacy Caster's
"filter functions". The main differences between
them are that:
1. transformers operate on single rules instead of rule pairs
2. transformers assume that the rules passed to them are non-null
3. transformers enforce immutability
4. transformers have no concept of "time" or "order"
'''
from castervoice.lib import utilities


class BaseRuleTransformer(object):
    '''do not override'''

    def get_transformed_rule(self, rule):
        if self._is_applicable(rule):
            rule_copy = None
            if hasattr(rule, "copy"):
                rule_copy = rule.copy()
            else:
                rule_copy = utilities.copy_dragonfly_mapping_rule(rule)
            return self._transform(rule_copy)
        return rule

    '''override this'''

    def _transform(self, mergerule):
        return mergerule

    '''override this'''

    def _is_applicable(self, mergerule):
        return False
