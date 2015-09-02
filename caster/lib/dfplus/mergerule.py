'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly.grammar.rule_mapping import MappingRule


class MergeRule(MappingRule):
    @staticmethod
    def _get_next_id():
        if not hasattr(MergeRule._get_next_id, "id"):
            MergeRule._get_next_id.id = 0  
        MergeRule._get_next_id.id += 1
        return MergeRule._get_next_id.id
    def __init__(self, name=None, mapping=None, extras=None, defaults=None,
                 exported=None, context=None):
        self.ID = MergeRule._get_next_id()
        self.incompatible = []
        MappingRule.__init__(self, name, mapping, extras, defaults, exported, context)
    def __eq__(self, other):
        return self.ID == other.ID
    def merge(self, other, context=None):
        mapping = other.mapping.copy()
        mapping.update(self._mapping)
        extras_dict = other.extras.copy()
        extras_dict.update(self.extras)
        extras = extras_dict.values()
        defaults = other.defaults.copy()
        defaults.update(self.defaults)
        return MergeRule(self.name + "+" + other.name, mapping, extras, defaults, self.exported and other.exported, context)
    def compatibility_check(self, other):
        if self.ID in other.incompatible:
            return False
        compatible = True
        for key in self.mapping:
            if key in other.mapping:
                compatible = False
        if not compatible:
            self.incompatible.append(other.ID)
            other.incompatible.append(self.ID)
        return compatible