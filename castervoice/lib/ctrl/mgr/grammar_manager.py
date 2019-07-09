class _PreInstantiatedGrammarManager(object):
    '''a stand-in for the real grammar manager for until the real singleton is instantiated
    -- it holds the rules which are to be loaded and then when the singleton is instantiated,
    passes them off to it'''

    def __init__(self):
        self._pending_rules = []
    
    def register_rule(self, rule_class, details):
        self._pending_rules.append((rule_class, details))

        
_PRE = _PreInstantiatedGrammarManager()
_INSTANCE = None


class _ManagedRule(object):

    def __init__(self, rule_class, details, grammar=None):
        self.rule_class = rule_class
        self.details = details
        self.grammar = grammar


'''
Jobs of the grammar manager:
1. Keep a copy of the latest stable version of a rule.
2. Know when a rule has changed (make an observer class to compose with this?)
3. Be in charge of loading/unloading via an internal loading grammar 
        -- this also applies to non-CCR grammars
        MappingRules should be enabled with 'enable' + (their name, else their Grammar's 'name', else executable)
'''
class GrammarManager(object):
    
    @staticmethod
    def get_instance():
        return _INSTANCE if _INSTANCE is not None else _PRE
    
    '''should be used by Nexus or other suitable controller'''

    @staticmethod
    def set_instance(merger, settings_module, appcontext_class, grammar_class, transformers,
                     delegating_validator, rule_sets, reload_observable):
        global _INSTANCE, _PRE
        if _INSTANCE is None:
            _INSTANCE = GrammarManager(merger, settings_module, appcontext_class,
                                       grammar_class, transformers, delegating_validator,
                                       rule_sets, reload_observable)
            _INSTANCE._convert(_PRE)
            _PRE = None
    
    def __init__(self, merger, settings_module, appcontext_class, grammar_class, transformers,
                 validator, rule_sets, reload_observable):
        # merger is necessary to unload ccr rules and their nons
        self._merger = merger
        # DI AppContext class, instantiated later
        self._appcontext_class = appcontext_class
        # DI Grammar class, instantiated later
        self._grammar_class = grammar_class
        # DI filter method, used later (default impl = castervoice.lib.dfplus.merge.gfilter.run_on)
        self._filter_method = filter_method
        # DI settings module
        self._settings_module = settings_module
        # DI validator
        self._validator = validator
        # rules: (class name : _ManagedRule}
        self._managed_rules = {}
        # companion rules -- when a rule is activated, it can have 0-n companion rules auto activated with it
        self._companion_rules = {}
        # 
        self._reload_observable = reload_observable
        self._reload_observable.register_listener(self)
        [self._register_rules_from_content_manager(rs) for rs in rule_sets]
        
    '''
    Do not call this manually. Should only be called by the reload observable.
    '''
    def receive(self, file_path_changed):
        '''
        TODO: this
        '''
        pass
    
    def _register_rules_from_content_manager(self, rule_set):
        for rd in rule_set:
            rule_class = rd[0]
            rule_details = rd[1]
            self.register_rule(rule_class, rule_details)
            self._reload_observable.register_watched_file(rule_details.path)
    
    def load(self, rule_class_name):
        '''defer to loaders
        '''
        pass
    
    def unload(self, rule_class_name):
        '''defer to loaders
        
        '''
        pass
    
    '''
    If a rule is registered a second time, 
    A. The new version should be attempted to be loaded.
    B. If it loads, the old version should
        1. have its grammar unloaded if there is a grammar
        2. be deleted from the _managed_rules map
    
    TODO:
    Okay, so instantiation errors are one thing, but what if we never make it to
    the "register" call? That is going to have to be handled, maybe in the "loading"
    package.
    -- can't recover if it fails on reboot
    -- can recover afterwards -- if it fails importlib, the crash will not deregister the old version
    '''
    def register_rule(self, rule_class, details):
        name = rule_class.__name__
        
        '''attempt to instantiate the rule'''
        test_instance = None 
        try:
            test_instance = rule_class()
        except:
            print(name + " rejected due to instantiation errors")
            return
        
        '''if ccr, validate the rule'''
        if details.declared_ccrtype is not None:
            error = self._validator.validate(test_instance, details.declared_ccrtype)
            if error is not None:
                print(name + " rejected due to validation errors: " + error)
                return
        
        '''if already registered, unregister it'''
        if name in self._managed_rules:
            self._unregister(name)
        
        '''
        rule should be safe for loading at this point: register it
        but do not load here -- this method only registers
        '''
        managed_rule = _ManagedRule(rule_class, details)
        self._managed_rules[name] = managed_rule

    
    '''
    Both rules must be registered before registering the companion.
        self._companion_rules is {rule: [companions]}
    '''
    def register_companion_rule(self, rule_class, companion_rule_class):
        rule_class_name = rule_class.__name__
        companion_rule_class_name = companion_rule_class.__name__
        
        if rule_class_name in self._managed_rules and \
            companion_rule_class_name in self._managed_rules:
            companions_list = [] if not rule_class_name in self._companion_rules \
                else self._companion_rules[rule_class_name]
            companions_list.append(companion_rule_class_name)
            self._companion_rules[rule_class_name] = companions_list
    
    def _unregister(self, rule_class_name):
        managed_rule = self._managed_rules[rule_class_name]
        if managed_rule.grammar is not None:
            managed_rule.grammar.unload()
        del self._managed_rules[rule_class_name]
            
            
    def _convert(self, pre):
        for t in pre._pending_rules:
            self.register(t[0], t[1])
    
    def _load_dragonfly_style(self, rule_class, details):
        if details.enabled:
            if self._settings_module["miscellaneous"]["rdp_mode"]:
                self._load_via_merger(rule_class(), details)
            else:
                rule_instance = rule_class(name=details.name)
                self._filter_method(rule_instance)
                
                context = self._appcontext_class(executable=details.executable)
                grammar = self._grammar_class(details.grammar_name, context=context)
                grammar.add_rule(rule_instance)
                grammar.load()
    
    def _load_via_merger(self, rule, details):
        self._merger.add_global_rule(rule)
    
    
