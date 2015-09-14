'''
Created on Sep 12, 2015

@author: synkarius
'''
import inspect
from caster.lib.dfplus.merge.mergerule import MergeRule

class Inf(object):
    TYPE = "type"
    GLOBAL = 0
    APP = 1
    #
    TIME = "time"
    BOOT = 2
    RUN = 3

class MergePair(object):
    def __init__(self, info, rule1, rule2, check_compatibility):
        self.info = info
        self.rule1 = rule1
        self.rule2 = rule2
        self.changed = False
        self.check_compatibility = check_compatibility

class CCRMerger(object):
    def __init__(self):
        self._global_rules = {}
        self._app_rules = {}
#         self._user_rules = {}
        self._filters = []
        self._base_global = None
        self._global_with_apps = []
    
    '''setup: adding rules and filters'''
    def add_global_rule(self, rule):
        assert rule.context==None, "global rules may not have contexts, "+rule.get_name()+" has a context"
        self._add_to(rule, self._global_rules)
    def add_app_rule(self, rule, context=None):
        if context!=None and rule.context==None: rule.context=context
        assert rule.context!=None, "app rules must have contexts, "+rule.get_name()+" has no context"
        self._add_to(rule, self._app_rules)
    def add_filter(self, filter):
        if not filter in self._filters:
            self._filters.append(filter)
    def _add_to(self, rule, group):
        if isinstance(rule, MergeRule) and not rule.get_name() in group:
            for name in group: group[name].compatibility_check(rule) # calculate compatibility for uncombined rules at boot time
            group[rule.get_name()] = rule
    
    '''getters'''
    def global_rule_names(self):
        return self._global_rules.keys()
    def app_rule_names(self):
        return self._app_rules.keys()
    def get_merge_function(self):
        def fn(name=None):
            self.merge(name)
        return fn
    
    '''merging'''
    def _get_rules_by_composite(self, composite):
        return [rule for name, rule in self._global_rules if rule.ID in composite]
    
    def merge(self, name=None, enable=True):
        base = self._base_global
        named_rule = self._global_rules[name].copy() if name is not None else None
        _time = Inf.BOOT if base is None else Inf.RUN # Inf.RUN = not the first time
        
        if enable:
            if _time == Inf.BOOT:
                '''base is None here'''
                #for k, v in self._global_rules:
            else:
                mp = MergePair({Inf.TIME: _time, 
                                Inf.TYPE: Inf.GLOBAL}, 
                                base, named_rule, True)
                self._run_filters(mp)
                
                # compatibility checking
                if mp.check_compatibility==False or \
                base.check_compatibility(named_rule):
                    base = base.merge(named_rule)
                else:
                    # figure out which MergeRules aren't compatible
                    composite = base.composite.copy() # composite is a set of the ids of the rules which make up this rule
                    for ID in named_rule.compatible:
                        if not named_rule.compatible[ID]: composite.discard(ID)
                    # rebuild a base from remaining MergeRules
                    base = MergeRule()
                    for rule in self._get_rules_by_composite(composite): base = base.merge(rule)
                    # merge in the new rule
                    base = base.merge(named_rule) 
        else:
            composite = base.composite.copy()
            composite.discard(named_rule.ID)
            base = MergeRule()
            for rule in self._get_rules_by_composite(composite): base = base.merge(rule)
                
        # instantiate or remove non- ccr rule
        
        
        
        # have base, make copies, merge in apps
        
    def _run_filters(self, merge_pair):
        for filter_fn in self._filters: filter_fn(merge_pair)
    
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
