'''
Created on Sep 1, 2015

@author: synkarius
'''
import random
import re

from dragonfly import MappingRule, Pause, Context

from caster.lib import utilities


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
    @staticmethod
    def get_merge_name(): # returns unique str(int) for procedural rule names 
        return str(MergeRule._get_next_id())
    
    mapping = {"hello world default macro": Pause("10")}
    
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
                 exported=None, context=None, ID=None, composite=None, compatible=None):
        self.ID = ID if ID is not None else MergeRule._get_next_id()
        self.compatible = {} if compatible is None else compatible
        if composite is not None: self.composite = composite # the IDs of the rules which this MergeRule is composed of
        else: self.composite = set([self.ID])
        MappingRule.__init__(self, name, mapping, extras, 
                             defaults, exported, context)
    def __eq__(self, other):
        if not isinstance(other, MergeRule):
            return False
        return self.ID == other.ID
    
    def mapping_copy(self):
        return self._mapping.copy()
    def extras_copy(self):
        return self._extras.copy()
    def defaults_copy(self):
        return self._defaults
    def merge(self, other, context=None):
        mapping = self.mapping_copy()
        mapping.update(other.mapping_copy())
        extras_dict = self.extras_copy()
        extras_dict.update(other.extras_copy()) # not just combining lists avoids duplicates
        extras = extras_dict.values()
        defaults = self.defaults_copy()
        defaults.update(other.defaults_copy())
        return MergeRule("Merged"+MergeRule.get_merge_name()+self.get_name()[0]+other.get_name()[0], 
                         mapping, extras, defaults, self.exported and other.exported, context, # no ID
                         composite=self.composite.union(other.composite))
                
    def get_name(self):
        return self.name if self.pronunciation==None else self.pronunciation
    def copy(self):
        return MergeRule(self.name, self._mapping, self._extras.values(), self._defaults, 
                         self._exported, self._context, self.ID, self.composite, self.compatible)
    def compatibility_check(self, other, debug=False):
        if other.ID in self.compatible:
            return self.compatible[other.ID] # lazily
        compatible = True
        for key in self._mapping.keys():
            if key in other._mapping.keys():
                compatible = False
                break
        self.compatible[other.ID] = compatible
        other.compatible[self.ID] = compatible
        return compatible
    def incompatible_IDs(self):
        return [ID for ID in self.compatible if not self.compatible[ID]]
            
        