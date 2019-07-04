'''
Created on Jun 23, 2019

@author: synkarius
'''


class _PreInstantiatedGrammarManager(object):
    '''a stand-in for the real grammar manager for until the real singleton is instantiated
    -- it holds the rules which are to be loaded and then when the singleton is instantiated,
    passes them off to it'''

    def __init__(self):
        self._pending_rules = []
    
    def load(self, rule_class, details):
        self._pending_rules.append((rule_class, details))

        
_PRE = _PreInstantiatedGrammarManager()
_INSTANCE = None


class _LoadedRule(object):

    def __init__(self, rule, grammar, details):
        self.rule = rule
        self.grammar = grammar
        self.details = details


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
                 global_validator, app_validator, selfmod_validator):
        # rule path to loaded rule
        self._rule_map = {}
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
        # DI validators
        self._global_validator = global_validator
        self._app_validator = app_validator
        self._selfmod_validator = selfmod_validator
    
    def load(self, rule_class, details):
        if details.ccr:
            self._load_via_merger(rule_class(), details)
        else:
            self._load_dragonfly_style(rule_class, details)
        '''TODO: get the grammar back from merger for unload??'''
            
    def unload(self, rule_class):
        '''TODO'''
            
    def _convert(self, pre):
        for t in pre._pending_rules:
            self.load(t[0], t[1])
    
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
    
    def _add_to_map(self, rule, grammar, details):    
        self._rule_map[str(rule)] = _LoadedRule(rule, grammar, details) 
    
