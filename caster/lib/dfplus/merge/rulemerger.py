'''
Created on Sep 12, 2015

@author: synkarius
'''
import inspect
from caster.lib.dfplus.merge.mergerule import MergeRule

class CCRMerger(object):
    def __init__(self):
        self._global_rules = {}
        self._app_rules = {}
        self._user_rules = {}
        self._filters = []
    
    '''setup: adding rules and filters'''
    def add_global_rule(self, rule):
        assert rule.context==None, "global rules may not have contexts, "+rule.get_name()+" has a context"
        self._add_to(rule, self._global_rules)
    def add_app_rule(self, rule, context=None):
        if context!=None and rule.context==None: rule.context=context
        assert rule.context!=None, "app rules must have contexts, "+rule.get_name()+" has no context"
        self._add_to(rule, self._app_rules)
    def add_user_rule(self, rule, context=None):
        if context!=None and rule.context==None: rule.context=context
        self._add_to(rule, self._user_rules)
    def add_filter(self, filter):
        if not filter in self._filters:
            self._filters.append(filter)
    def _add_to(self, rule, group):
        if isinstance(rule, MergeRule) and not rule.get_name() in group:
            group[rule.get_name()] = rule
    
    
    '''unused code to get ccr modules automatically like they were in the previous system'''
    def _extends(self, member, rule_type):
        return inspect.isclass(member) and member!=rule_type and issubclass(member, rule_type)
    def _get_caster_objects(self, module):
        '''gets instances of all MergeRules in a module'''
        _map = {}
        for name, obj in inspect.getmembers(module):
            if self._extends(obj, MergeRule):
                rule = obj()
                _map[rule.get_name()] = rule
        return _map
