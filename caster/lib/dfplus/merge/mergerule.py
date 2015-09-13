'''
Created on Sep 1, 2015

@author: synkarius
'''
import re

from dragonfly import MappingRule


class TokenSet(object):
    SYMBOL_PATTERN = re.compile("([A-Za-z0-9_]+)")
    def __init__(self, keywords, line_comment, long_comment):
        self.keywords = keywords
        self.line_comment = line_comment
        self.long_comment = long_comment

class MergeRule(MappingRule):
    @staticmethod
    def _get_next_id():
        if not hasattr(MergeRule._get_next_id, "id"):
            MergeRule._get_next_id.id = 0  
        MergeRule._get_next_id.id += 1
        return MergeRule._get_next_id.id
    
    '''MergeRules which define `auto` (array of tuples, 
    first value file extension to recognize, second value 
    programming language) will work with auto command 
    and language mode'''
    auto = None
    
    '''MergeRules which define `pronunciation` will use
    the pronunciation string rather than their class name
    for their respective enable/disable commands'''
    pronunciation = None
    
    '''MergeRules which define `non` will instantiate
    their paired non-CCR MergeRule and activate it 
    alongside themselves'''
    non = None
    
    '''MergeRules which define `token_set` will enable
    scanning of directories for use with the 
    "symbol match" command in their language'''
    token_set = None
    
    '''MergeRules which define `context` with a 
    Dragonfly AppContext become non-global; this
    is the same as adding a context to a Grammar'''
    context = None
    
    def __init__(self, name=None, mapping=None, extras=None, defaults=None,
                 exported=None, context=None):
        self.ID = MergeRule._get_next_id()
        self.incompatible = []
        MappingRule.__init__(self, name, mapping, extras, defaults, exported, context)
    def __eq__(self, other):
        if not isinstance(other, MergeRule):
            return False
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
    def get_name(self):
        return self.name if self.pronunciation==None else self.pronunciation
    def copy(self):
        return MergeRule(self.name, self.mapping, self.extras.values(), self.defaults, self.exported)
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
    