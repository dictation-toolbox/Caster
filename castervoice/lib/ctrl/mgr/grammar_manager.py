class _PreInstantiatedGrammarManager(object):
    '''a stand-in for the real grammar manager for until the real singleton is instantiated
    -- it holds the rules which are to be loaded and then when the singleton is instantiated,
    passes them off to it'''

    def __init__(self):
        self._pending_rules = []
    
    def register(self, rule_class, details):
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
                     global_validator, app_validator, selfmod_validator):
        global _INSTANCE, _PRE
        if _INSTANCE is None:
            _INSTANCE = GrammarManager(merger, settings_module, appcontext_class,
                                       grammar_class, transformers, global_validator, 
                                       app_validator, selfmod_validator)
            _INSTANCE._convert(_PRE)
            _PRE = None
    
    def __init__(self, merger, settings_module, appcontext_class, grammar_class, transformers,
                 validator):
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
    '''
    def register(self, rule_class, details):
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
    
    
