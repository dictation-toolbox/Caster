'''
Created on Sep 12, 2015

@author: synkarius
'''
import inspect

from dragonfly.grammar.elements import RuleRef, Alternative, Repetition
from dragonfly.grammar.rule_compound import CompoundRule

from caster.lib import utilities, settings
from caster.lib.dfplus.merge.mergerule import MergeRule


class Inf(object):
    TYPE = "type"
    GLOBAL = 0
    APP = 1
    SELFMOD = 2
    #
    TIME = "time"
    BOOT = 3
    RUN = 4
    

class MergePair(object):
    def __init__(self, type, time,  rule1, rule2, check_compatibility):
        self.type = type
        self.time = time
        self.rule1 = rule1
        self.rule2 = rule2
        self.changed = False
        self.check_compatibility = check_compatibility

class CCRMerger(object):
    CORE = ["alphabet", "navigation", "numbers", "punctuation"]
    _GLOBAL = "global"
    _APP = "app"
    _SELFMOD = "selfmod"
    
    def __init__(self):
        # original copies of rules
        self._global_rules = {}
        self._app_rules = {}
        # self modifying rules (don't make copies)
        self._self_modifying_rules = {}
        # filter functions
        self._filters = []
        # active rules
        self._base_global = None
        self._global_with_apps = []
        # config
        self.load_config()
    
    '''config file stuff'''
    def save_config(self):
        utilities.save_json_file(self._config, settings.SETTINGS["paths"]["CCR_CONFIG_PATH"])
    def load_config(self):
        self._config = utilities.load_json_file(settings.SETTINGS["paths"]["CCR_CONFIG_PATH"])
    def update_config(self, merge=False):
        '''call this after all rules have been added'''
        changed = False
        if not CCRMerger._GLOBAL in self._config:
            self._config[CCRMerger._GLOBAL] = {}
        for name in self.global_rule_names():
            if not name in self._config[CCRMerger._GLOBAL]:
                self._config[CCRMerger._GLOBAL][name] = name in CCRMerger.CORE
                utilities.report(name+" global CCR module added")
                changed = True
        if not CCRMerger._APP in self._config:
            self._config[CCRMerger._APP] = {}
        for name in self.global_rule_names():
            if not name in self._config[CCRMerger._APP]:
                self._config[CCRMerger._APP][name] = name in CCRMerger.CORE
                utilities.report(name+" app CCR module added")
                changed = True
        if not CCRMerger._SELFMOD in self._config:
            self._config[CCRMerger._SELFMOD] = {}
        for name in self.selfmod_rule_names():
            if not name in self._config[CCRMerger._SELFMOD]:
                self._config[CCRMerger._SELFMOD][name] = name in CCRMerger.CORE
                utilities.report(name+" selfmod CCR module added")
                changed = True
        if changed: self.save_config()
        if merge: self.merge()
    
    '''setup: adding rules and filters'''
    def add_global_rule(self, rule):
        assert rule.context==None, "global rules may not have contexts, "+rule.get_name()+" has a context"
        self._add_to(rule, self._global_rules)
    def add_app_rule(self, rule, context=None):
        if context!=None and rule.context==None: rule.context=context
        assert rule.context!=None, "app rules must have contexts, "+rule.get_name()+" has no context"
        self._add_to(rule, self._app_rules)
    def add_selfmodrule(self, rule, name, context=None):
        rule.context = context
        self._self_modifying_rules[name] = rule        
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
    def selfmod_rule_names(self):
        return self._self_modifying_rules.keys()
    
    '''merging'''
    def _get_rules_by_composite(self, composite):
        return [rule.copy() for name, rule in self._global_rules if rule.ID in composite]
    def _compatibility_checks(self, merge_pair, base, rule):
        if merge_pair.check_compatibility==False or \
        base.check_compatibility(rule):
            base = base.merge(rule)
        else:
            # figure out which MergeRules aren't compatible
            composite = base.composite.copy() # composite is a set of the ids of the rules which make up this rule
            for ID in rule.compatible:
                if not rule.compatible[ID]: composite.discard(ID)
            # rebuild a base from remaining MergeRules
            base = None
            for rule in self._get_rules_by_composite(composite): 
                base = rule if base is None else base.merge(rule)
            # merge in the new rule
            base = base.merge(rule)
        return base
    
    def merge(self, time, name=None, enable=True, save=False):
        base = self._base_global
        named_rule = self._global_rules[name].copy() if name is not None else None
#         _time = Inf.BOOT if base is None else Inf.RUN # Inf.RUN = not the first time
        
        if time != Inf.NODE: # NodeRule node changes needn't alter the base rule
            if enable:
                if time == Inf.BOOT:
                    for name, rule in self._global_rules:
                        if self._config[CCRMerger._GLOBAL][name]:
                            mp = MergePair(time, Inf.GLOBAL, base, rule, False)
                            self._run_filters(mp)
                            if mp.check_compatibility and base is not None: 
                                base = self._compatibility_checks(mp, base, rule)
                            base = rule if base is None else base.merge(rule)
                else:
                    mp = MergePair(time, Inf.GLOBAL, base, named_rule, True)
                    self._run_filters(mp)
                    base = self._compatibility_checks(mp, base, rule)
            else:#disable
                composite = base.composite.copy()# IDs of all rules that the composite rule is made of
                composite.discard(named_rule.ID)
                base = None
                for rule in self._get_rules_by_composite(composite): 
                    mp = MergePair(time, Inf.GLOBAL, base, rule, False)
                    self._run_filters(mp)
                    if mp.check_compatibility and base is not None: 
                        base = self._compatibility_checks(mp, base, rule)
                    base = rule if base is None else base.merge(rule)
        
        # compatibility check and filter function active noderules, but do not merge them in
        # this will require a new "time", Inf._SELFMOD 
        # if the filter functions don't wipe them, let them be added as alternatives in _create_repeat_rule()
        selfmod = []
        for name, rule in self._self_modifying_rules:
            '''no need to make copies of selfmod rules because even if
            filter functions trash their mapping, they'll just regenerate
            it next time they modify themselves'''
            if self._config[CCRMerger._SELFMOD][name]:
                self._run_filters(MergePair(time, Inf.SELFMOD, base, rule, False))
                for smrule in selfmod: # also have to check against other active noderules
                    self._run_filters(MergePair(time, Inf.SELFMOD, smrule, rule, False))
                # do we want the option to shut them off if they're incompatible??
        
        
        # instantiate non-ccr rules
        active_global  = self._get_rules_by_composite(base.composite)
        global_non_ccr = [rule.non() for rule in active_global \
                         if rule.non is not None]
        
        
        
        # have base, make copies, merge in apps
        
        
        # get all contexts
        
        
        
        
        
        
        repeat_rule = self._create_repeat_rule(base)
        
        # save if necessary
        if time == Inf.RUN and save: 
            # everything in base composite is active, everything in selfmod is active, update the config as such
            active_global_names = [rule.get_name() for rule in active_global]
            for rule_name in self._global_rules:
                self._config[CCRMerger._GLOBAL][rule_name] = rule_name in active_global_names
            active_selfmod_names = [rule.get_name() for rule in selfmod]
            for rule_name in self._self_modifying_rules:
                self._config[CCRMerger._SELFMOD][rule_name] = rule_name in active_selfmod_names
            self.save_config()
        
    def _run_filters(self, merge_pair):
        for filter_fn in self._filters: filter_fn(merge_pair)
    def _create_repeat_rule(self, base):
        ORIGINAL, SEQ, TERMINAL = "original", "caster base sequence", "terminal"
        alts = [RuleRef(rule=base)]
        single_action = Alternative(alts)
        sequence = Repetition(single_action, min=1, max=16, name=SEQ)
        original = Alternative(alts, name=ORIGINAL)
        terminal = Alternative(alts, name=TERMINAL)
        class RepeatRule(CompoundRule):
            spec = "[<"+ORIGINAL+"> original] [<" + SEQ + ">] [terminal <"+TERMINAL+">]"
            extras = [ sequence, original, terminal ] 
            def _process_recognition(self, node, extras):
                original = extras[ORIGINAL] if ORIGINAL in extras else None
                terminal = extras[SEQ] if SEQ in extras else None
                sequence = extras[TERMINAL] if TERMINAL in extras else None
                if original!=None: original.execute()
                if sequence!=None:
                    for action in sequence:
                        action.execute()
                if terminal!=None: terminal.execute()
        return RepeatRule()
    
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
