'''
Created on Sep 12, 2015

@author: synkarius
'''
from dragonfly.grammar.elements import RuleRef, Alternative, Repetition
from dragonfly.grammar.grammar_base import Grammar
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
        self._grammar = Grammar("CCR Master")
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
        self.update_config() # this call prepares the config to receive new modules
    
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
                changed = True
        if not CCRMerger._APP in self._config:
            self._config[CCRMerger._APP] = {}
        for name in self.app_rule_names():
            if not name in self._config[CCRMerger._APP]:
                self._config[CCRMerger._APP][name] = True
                changed = True
        if not CCRMerger._SELFMOD in self._config:
            self._config[CCRMerger._SELFMOD] = {}
        for name in self.selfmod_rule_names():
            if not name in self._config[CCRMerger._SELFMOD]:
                self._config[CCRMerger._SELFMOD][name] = False
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
        rule.merger = self
        self._self_modifying_rules[name] = rule        
    def add_filter(self, filter):
        if not filter in self._filters:
            self._filters.append(filter)
    def _add_to(self, rule, group):
        if rule.get_name() in \
        self.global_rule_names()+\
        self.app_rule_names()+\
        self.selfmod_rule_names():
            raise "Rule Naming Conflict: "+rule.get_name()
        if isinstance(rule, MergeRule):
            for name in group: 
                group[name].compatibility_check(rule) # calculate compatibility for uncombined rules at boot time
            group[rule.get_name()] = rule
    
    '''getters'''
    def global_rule_names(self):
        return self._global_rules.keys()
    def app_rule_names(self):
        return self._app_rules.keys()
    def selfmod_rule_names(self):
        return self._self_modifying_rules.keys()
    
    '''rule change functions'''
    def global_rule_changer(self):
        def _(name, enable, save):
            self._config[CCRMerger._GLOBAL][name] = enable
            self.merge(Inf.RUN, name, enable, save)
        return _
    
    '''merging'''
    def _get_rules_by_composite(self, composite, original=False):
        return [rule if original else rule.copy()  \
                for name, rule in self._global_rules.iteritems() \
                if rule.ID in composite]
    def _compatibility_merge(self, merge_pair, base, rule):
        '''MergeRule.merge always returns a copy, so there's
        no need to worry about the originals getting modified'''
        if merge_pair.check_compatibility==False or \
        base.compatibility_check(rule, True):
            base = base.merge(rule, rule.context)
        else:
            # figure out which MergeRules aren't compatible
            composite = base.composite.copy() # composite is a set of the ids of the rules which make up this rule
            for ID in rule.compatible:
                if not rule.compatible[ID]: composite.discard(ID)
            # rebuild a base from remaining MergeRules
            base = None
            for _rule in self._get_rules_by_composite(composite): 
                base = _rule if base is None else base.merge(_rule, _rule.context)
            # merge in the new rule
            base = base.merge(rule, rule.context)
        return base
    
    def merge(self, time, name=None, enable=True, save=False):
        '''combines MergeRules, SelfModifyingRules;
        handles CCR for apps;
        instantiates affiliated rules;
        adds everything to its grammar
        ;
        assumptions made: 
        * SelfModifyingRules have already made changes to themselves
        * the appropriate activation boolean(s) in the appropriate map has already been set'''
        self._grammar.unload()
        base = self._base_global
        
        '''get base CCR rule'''
        if time != Inf.SELFMOD: # SelfModifyingRule changes don't alter the base rule
            named_rule = self._global_rules[name] if name is not None else None
            if enable:
                if time == Inf.BOOT:
                    for name, rule in self._global_rules.iteritems():
                        if self._config[CCRMerger._GLOBAL][name]:
                            mp = MergePair(time, Inf.GLOBAL, base, rule, False) # copies not made at boot time, allows user to make permanent changes
                            self._run_filters(mp)
                            if base is None: base = rule
                            else: base = self._compatibility_merge(mp, base, rule)
                else:#runtime-enable
                    mp = MergePair(time, Inf.GLOBAL, base, named_rule.copy(), True)
                    self._run_filters(mp)
                    base = self._compatibility_merge(mp, base, mp.rule2) # mp.rule2 because named_rule got copied
            else:#disable
                composite = base.composite.copy()# IDs of all rules that the composite rule is made of
                composite.discard(named_rule.ID)
                base = None
                for rule in self._get_rules_by_composite(composite): 
                    mp = MergePair(time, Inf.GLOBAL, base, rule.copy(), False)
                    self._run_filters(mp)
                    if base is None: base = rule
                    else: base = self._compatibility_merge(mp, base, mp.rule2) # mp.rule2 because named_rule got copied
                
        '''compatibility check and filter function active 
        selfmodrules, but do not merge them in; they will
        become parts of the Alternative in _create_repeat_rule()'''
        selfmod = []
        for name, rule in self._self_modifying_rules.iteritems():
            '''no need to make copies of selfmod rules because even if
            filter functions trash their mapping, they'll just regenerate
            it next time they modify themselves; 
            furthermore, they need to preserve state'''
            if self._config[CCRMerger._SELFMOD][name]:
                use_rule = True
                mp = MergePair(time, Inf.SELFMOD, base, rule, False)
                self._run_filters(mp)
                if mp.check_compatibility: use_rule &= base.compatibility_check(rule)
                if use_rule:
                    for smrule in selfmod: # also have to check against other active selfmodrules
                        mp_ = MergePair(time, Inf.SELFMOD, smrule, rule, False)
                        self._run_filters(mp_)
                        if mp_.check_compatibility: use_rule &= rule.compatibility_check(smrule)
                        if not use_rule: break
                    if use_rule: selfmod.append(rule)
        
        
        '''have base, make copies, merge in apps'''
        active_apps = []
        for rule in self._app_rules.values():
            mp = MergePair(time, Inf.APP, base, rule.copy(), False)
            self._run_filters(mp)
            rule = self._compatibility_merge(mp, base, mp.rule2) # mp.rule2 because named_rule got copied
            active_apps.append(rule)
           
        
        '''negation context for appless version of base rule'''
        contexts = [rule.context for rule in self._app_rules.values() \
                    if rule.context is not None]# get all contexts
        master_context = None
        for context in contexts:
            negate = ~context
            if master_context is None: master_context = negate
            else: master_context | negate
        base = base.merge(base, master_context) # sets context through constructor
        
        '''instantiate non-ccr rules affiliated with rules in the base CCR rule'''
        active_global  = self._get_rules_by_composite(base.composite, True)
        global_non_ccr = [rule.non() for rule in active_global \
                         if rule.non is not None]
        
        '''modify grammar'''
        while len(self._grammar.rules) > 0: self._grammar.remove_rule(self._grammar.rules[0])
        for rule in [base]+active_apps: self._grammar.add_rule(self._create_repeat_rule(rule, selfmod))
        for rule in global_non_ccr: self._grammar.add_rule(rule)
        
        '''save if necessary'''
        if time == Inf.RUN and save: 
            # everything in base composite is active, everything in selfmod is active, update the config as such
            active_global_names = [rule.get_name() for rule in active_global]
            for rule_name in self._global_rules:
                self._config[CCRMerger._GLOBAL][rule_name] = rule_name in active_global_names
            active_selfmod_names = [rule.get_name() for rule in selfmod]
            for rule_name in self._self_modifying_rules:
                self._config[CCRMerger._SELFMOD][rule_name] = rule_name in active_selfmod_names
            self.save_config()
        
        self._base_global = base
        self._grammar.load()
        
    def _run_filters(self, merge_pair):
        for filter_fn in self._filters: filter_fn(merge_pair)
    def _create_repeat_rule(self, rule, selfmod):
        ORIGINAL, SEQ, TERMINAL = "original", "caster_base_sequence", "terminal"
        alts = [RuleRef(rule=rule)]+[RuleRef(rule=sm) for sm in selfmod]
        single_action = Alternative(alts)
        sequence = Repetition(single_action, min=1, max=16, name=SEQ)
        original = Alternative(alts, name=ORIGINAL)
        terminal = Alternative(alts, name=TERMINAL)
        class RepeatRule(CompoundRule):
            spec = "[<"+ORIGINAL+"> original] [<" + SEQ + ">] [terminal <"+TERMINAL+">]"
            extras = [ sequence, original, terminal ] 
            def _process_recognition(self, node, extras):
                original = extras[ORIGINAL] if ORIGINAL in extras else None
                sequence = extras[SEQ] if SEQ in extras else None
                terminal = extras[TERMINAL] if TERMINAL in extras else None
                if original!=None: original.execute()
                if sequence!=None:
                    for action in sequence:
                        action.execute()
                if terminal!=None: terminal.execute()
        return RepeatRule(name=rule.get_name()+str(rule.context))
