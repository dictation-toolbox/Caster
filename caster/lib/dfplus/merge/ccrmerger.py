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
    def __init__(self, time, type, rule1, rule2, check_compatibility):
        self.time = time
        self.type = type
        self.rule1 = rule1
        self.rule2 = rule2
        self.changed = False # presently unused
        self.check_compatibility = check_compatibility

class CCRMerger(object):
    CORE = ["alphabet", "navigation", "numbers", "punctuation"]
    _GLOBAL = "global"
    _APP = "app"
    _SELFMOD = "selfmod"
    
    def __init__(self, use_real_config=True):
        self._grammars = [] # cannot put multiple large rules in a single grammar despite context separation
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
        self.use_real_config = use_real_config
        self.load_config()
        self.update_config() # this call prepares the config to receive new modules
    
    '''config file stuff'''
    def save_config(self):
        if self.use_real_config:
            utilities.save_json_file(self._config, settings.SETTINGS["paths"]["CCR_CONFIG_PATH"])
    def load_config(self):
        if self.use_real_config:
            self._config = utilities.load_json_file(settings.SETTINGS["paths"]["CCR_CONFIG_PATH"])
        else:
            self._config  = {}
    def update_config(self):
        '''call this after all rules have been added'''
        changed = False
        '''global rules'''
        if not CCRMerger._GLOBAL in self._config:
            self._config[CCRMerger._GLOBAL] = {}
        for name in self.global_rule_names():
            if not name in self._config[CCRMerger._GLOBAL]:
                self._config[CCRMerger._GLOBAL][name] = name in CCRMerger.CORE
                changed = True
        '''app rules'''
        if not CCRMerger._APP in self._config:
            self._config[CCRMerger._APP] = {}
        for name in self.app_rule_names():
            if not name in self._config[CCRMerger._APP]:
                self._config[CCRMerger._APP][name] = True
                changed = True
        '''self modifying rules'''
        if not CCRMerger._SELFMOD in self._config:
            self._config[CCRMerger._SELFMOD] = {}
        for name in self.selfmod_rule_names():
            if not name in self._config[CCRMerger._SELFMOD]:
                self._config[CCRMerger._SELFMOD][name] = False
                changed = True
        
        if changed: self.save_config()
    
    '''setup: adding rules and filters'''
    def add_global_rule(self, rule):
        assert rule.get_context() is None, "global rules may not have contexts, "+rule.get_name()+" has a context: "+str(rule.get_context())
        assert isinstance(rule, MergeRule) and not hasattr(rule, "set_merger"), \
            "only MergeRules may be added as global rules; use add_selfmodrule() or add_app_rule()"
        self._add_to(rule, self._global_rules)
    def add_app_rule(self, rule, context=None):
        if context is not None and rule.get_context() is None: rule.set_context(context)
        assert rule.get_context() is not None, "app rules must have contexts, "+rule.get_name()+" has no context"
        self._add_to(rule, self._app_rules)
    def add_selfmodrule(self, rule):
        assert hasattr(rule, "set_merger"), "only SelfModifyingRules may be added by add_selfmodrule()"
        rule.set_merger(self)
        self._add_to(rule, self._self_modifying_rules)
    def add_filter(self, filter):
        if not filter in self._filters:
            self._filters.append(filter)
    def _add_to(self, rule, group):
        if rule.get_name() in \
        self.global_rule_names()+\
        self.app_rule_names()+\
        self.selfmod_rule_names():
            raise Exception("Rule Naming Conflict: "+rule.get_name())
        if isinstance(rule, MergeRule):
            for name in group.keys(): 
                group[name].compatibility_check(rule) # calculate compatibility for uncombined rules at boot time
            group[rule.get_name()] = rule
    
    '''getters'''
    def global_rule_names(self):
        return self._global_rules.keys()
    def app_rule_names(self):
        return self._app_rules.keys()
    def selfmod_rule_names(self):
        return self._self_modifying_rules.keys()
    def language_autos(self):
        autos = {}
        for rule in self._global_rules.values():
            if rule.__class__.auto is not None:
                for extension in rule.__class__.auto:
                    autos[extension] = [rule.get_name()]
                # right here check for language groups, add them into autos
        return autos
    
    '''rule change functions'''
    def global_rule_changer(self):
        def _(name, enable, save):
            self._config[CCRMerger._GLOBAL][name] = enable
            self.merge(Inf.RUN, name, enable, save)
        return _
    def selfmod_rule_changer(self):
        def _(name2, enable, save):
            self._config[CCRMerger._SELFMOD][name2] = enable
            self.merge(Inf.SELFMOD, name2, enable, save)
        return _
    
    '''merging'''
    def _get_rules_by_composite(self, composite, original=False):
        return [rule if original else rule.copy()  \
                for rule in self._global_rules.values() \
                if rule.ID in composite]
    def _compatibility_merge(self, merge_pair, base, rule):
        '''MergeRule.merge always returns a copy, so there's
        no need to worry about the originals getting modified'''
        if merge_pair.check_compatibility==False or \
        base is None or \
        base.compatibility_check(rule):
            base = rule if base is None else base.merge(rule)
        else:
            # figure out which MergeRules aren't compatible
            composite = base.composite.copy() # composite is a set of the ids of the rules which make up this rule
            for ID in rule.compatible:
                if not rule.compatible[ID]: composite.discard(ID)
            # rebuild a base from remaining MergeRules
            base = None
            for _rule in self._get_rules_by_composite(composite): 
                base = _rule if base is None else base.merge(_rule)
            # merge in the new rule
            if base is not None:
                base = base.merge(rule)
            else:
                base = rule
        return base
        
    def _add_grammar(self, rule, ccr=False, context=None):
        name = str(rule)
        grammar = Grammar(name, context=context)
        self._grammars.append(grammar)
        if ccr:
            repeater = self._create_repeat_rule(rule)
            grammar.add_rule(repeater)
        else:
            grammar.add_rule(rule)
    
    def wipe(self):
        while len(self._grammars) > 0: 
            grammar = self._grammars.pop()
            for rule in grammar.rules: rule.disable()
            grammar.disable()
            del grammar
    
    def merge(self, time, name=None, enable=True, save=False):
        '''combines MergeRules, SelfModifyingRules;
        handles CCR for apps;
        instantiates affiliated rules;
        adds everything to its grammar
        ;
        assumptions made: 
        * SelfModifyingRules have already made changes to themselves
        * the appropriate activation boolean(s) in the appropriate map has already been set'''
        
        self.wipe()
        base = self._base_global
        named_rule = None
        
        '''get base CCR rule'''
        if time == Inf.BOOT: # rebuild via config
            for name, rule in self._global_rules.iteritems():
                if self._config[CCRMerger._GLOBAL][name]:
                    mp = MergePair(time, Inf.GLOBAL, base, rule, False) # copies not made at boot time, allows user to make permanent changes
                    self._run_filters(mp)
                    if base is None: base = rule
                    else: base = self._compatibility_merge(mp, base, rule)
        else: # rebuild via composite
            composite = base.composite.copy()# IDs of all rules that the composite rule is made of
            if time != Inf.SELFMOD:
                named_rule = self._global_rules[name] if name is not None else None
                if enable == False:
                    composite.discard(named_rule.ID) # throw out rule getting disabled
            base = None
            for rule in self._get_rules_by_composite(composite): 
                mp = MergePair(time, Inf.GLOBAL, base, rule.copy(), False)
                self._run_filters(mp)
                if base is None: base = rule
                else: base = self._compatibility_merge(mp, base, mp.rule2) # mp.rule2 because named_rule got copied
            if time != Inf.SELFMOD and enable == True:
                mp = MergePair(time, Inf.GLOBAL, base, named_rule.copy(), True)
                self._run_filters(mp)
                base = self._compatibility_merge(mp, base, mp.rule2) # mp.rule2 because named_rule got copied
                
        '''compatibility check and filter function active selfmodrules'''
        for name2, rule in self._self_modifying_rules.iteritems():
            '''no need to make copies of selfmod rules because even if
            filter functions trash their mapping, they'll just regenerate
            it next time they modify themselves; 
            furthermore, they need to preserve state'''
            if self._config[CCRMerger._SELFMOD][name2]:
                mp = MergePair(time, Inf.SELFMOD, base, rule, False)
                self._run_filters(mp)
                base = self._compatibility_merge(mp, base, rule)
        if time == Inf.SELFMOD and name is not None \
        and not self._config[CCRMerger._SELFMOD][name]:
            try: # reset deactivated NodeRule
                if rule.master_node.spec != rule.node.spec:
                    rule.reset_node()
            except AttributeError: pass
        
        '''have base, make copies, merge in apps'''
        active_apps = []
        for rule in self._app_rules.values():
            context = rule.get_context()
            mp = MergePair(time, Inf.APP, base, rule.copy(), False)
            self._run_filters(mp)
            rule = self._compatibility_merge(mp, base, mp.rule2) # mp.rule2 because named_rule got copied
            rule.set_context(context)
            active_apps.append(rule)
            
        
        '''negation context for appless version of base rule'''
        contexts = [rule.get_context() for rule in self._app_rules.values() \
                    if rule.get_context() is not None]# get all contexts
        negation_context = None
        for context in contexts:
            negate = ~context
            if negation_context is None: negation_context = negate
            else: negation_context & negate
        
        
        '''handle empty merge'''
        if base is None:
            base = MergeRule()
        
        ''' save results for next merge '''
        self._base_global = base.copy() 
        
        '''instantiate non-ccr rules affiliated with rules in the base CCR rule'''
        active_global  = self._get_rules_by_composite(base.composite, True)
        global_non_ccr = [rule.non() for rule in active_global \
                         if rule.non is not None]
        
        '''update grammars'''
        self._add_grammar(base, True, negation_context)
        for rule in global_non_ccr: self._add_grammar(rule)
        for rule in active_apps: self._add_grammar(rule, True, rule.get_context())
        for grammar in self._grammars: grammar.load()
        
        
        '''save if necessary'''
        if time in [Inf.RUN, Inf.SELFMOD] and save:
            # everything in base composite is active, everything in selfmod is active, update the config as such
            active_global_names = [rule.get_name() for rule in active_global]
            for rule_name in self._global_rules:
                self._config[CCRMerger._GLOBAL][rule_name] = rule_name in active_global_names
            active_selfmod_names = [name3 for name3 in self._config[CCRMerger._SELFMOD] if self._config[CCRMerger._SELFMOD][name3]]#[rule.get_name() for rule in selfmod]
            for rule_name in self._self_modifying_rules:
                self._config[CCRMerger._SELFMOD][rule_name] = rule_name in active_selfmod_names
            self.save_config()
        
    def _run_filters(self, merge_pair):
        for filter_fn in self._filters:
            try: filter_fn(merge_pair)
            except Exception: 
                utilities.simple_log()
                print("Filter function '"+filter_fn.__name__+"' failed.")
        
    def _create_repeat_rule(self, rule):
        ORIGINAL, SEQ, TERMINAL = "original", "caster_base_sequence", "terminal"
        alts = [RuleRef(rule=rule)]#+[RuleRef(rule=sm) for sm in selfmod]
        single_action = Alternative(alts)
        max = settings.SETTINGS["miscellaneous"]["max_ccr_repetitions"]
        sequence = Repetition(single_action, min=1, max=max, name=SEQ)
        original = Alternative(alts, name=ORIGINAL)
        terminal = Alternative(alts, name=TERMINAL)
        class RepeatRule(CompoundRule):
            spec = "[<"+ORIGINAL+"> original] [<" + SEQ + ">] [terminal <"+TERMINAL+">]"
            extras = [ sequence, original, terminal ] 
            def _process_recognition(self, node, extras):
                original = extras[ORIGINAL] if ORIGINAL in extras else None
                sequence = extras[SEQ] if SEQ in extras else None
                terminal = extras[TERMINAL] if TERMINAL in extras else None
                if original is not None: original.execute()
                if sequence is not None:
                    for action in sequence:
                        action.execute()
                if terminal is not None: terminal.execute()
        return RepeatRule(name="Repeater"+MergeRule.get_merge_name())
