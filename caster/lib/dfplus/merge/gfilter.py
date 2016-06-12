################################# Global Filter Functions From File module  ############################################
'''GlobalFilterDefs overrides ALL instances of some word(s) in all rules'''

import os

from dragonfly.grammar.elements import Choice

from caster.lib import settings


class GlobalFilterDefs(object):
    '''parsing modes'''
    MODES = {
             "<<<ANY>>>":       0,
             "<<<SPEC>>>":      1,
             "<<<EXTRA>>>":     2,
             "<<<DEFAULT>>>":   3,
             "<<<NOT_SPECS>>>": 4
            }
    
    def __init__(self, lines):
        self.specs = {}
        self.extras = {}
        self.defaults = {}
        mode = 0
        
        for line in lines:
            
            if line.startswith("#") or not line.strip(): # ignore comments and empty lines
                continue
            
            pair = line.split("->")
            original = pair[0].strip()
            
            if original in GlobalFilterDefs.MODES:
                mode = GlobalFilterDefs.MODES[original]
                continue
            
            new = pair[1].strip()
            
            '''only handles mode 1 for now'''
            if mode == 0:
                self.specs[original] = new
                self.extras[original] = new
                self.defaults[original] = new
            elif mode == 1:
                self.specs[original] = new
            elif mode == 2:
                self.extras[original] = new
            elif mode == 3:
                self.defaults[original] = new
            elif mode == 4:
                self.extras[original] = new
                self.defaults[original] = new

DEFS = None

if os.path.isfile(settings.SETTINGS["paths"]["FILTER_DEFS_PATH"]):
    '''user must create caster/user/fdefs.txt for it to get picked up here'''
    with open(settings.SETTINGS["paths"]["FILTER_DEFS_PATH"]) as f:
        lines = f.readlines()
        try:
            DEFS = GlobalFilterDefs(lines)
        except Exception:
            print("Unable to parse fdefs.txt")

def spec_override_from_config(mp):
    '''run at boot time only: changes are permanent'''
    if mp.time != 3: # 3 == Inf.BOOT
        return
    '''redundant safety check'''
    if DEFS is None:
        return
    
    for rule in [mp.rule1, mp.rule2]:
        if rule is not None:
            '''SPECS'''
            for spec in rule.mapping_actual().keys():
                action = rule.mapping_actual()[spec]
                nspec = spec # new spec
                for original in DEFS.specs.keys():
                    if original in spec:
                        new = DEFS.specs[original]
                        nspec = spec.replace(original, new)
                        
                if spec == nspec:
                    continue;
                
                del rule.mapping_actual()[spec]
                rule.mapping_actual()[nspec] = action
            
            '''EXTRAS'''
            extras = rule.extras_copy().values()
            extras_changed = False
            if len(extras) > 0:
                replacements = {}
                for extra in extras:
                    if isinstance(extra, Choice): # IntegerRefSTs will be dealt with elsewhere
                        choices = extra._choices
                        replace = False
                        for s in choices.keys(): #ex: "dunce make" is key, some int or whatever is the value
                            for ns in DEFS.extras.keys(): #ex: "dunce" is key, "down" is the value
                                if ns in s: # ex: "dunce" is in "dunce make"
                                    replace = True
                                    val = choices[s] 
                                    del choices[s]
                                    s = s.replace(ns, DEFS.extras[ns])
                                    choices[s] = val
                        if replace:
                            new_choice = Choice(extra.name, choices)
                            replacements[extra] = new_choice
                for old_choice in replacements:
                    new_choice = replacements[old_choice]
                    extras.remove(old_choice)
                    extras.append(new_choice)
                if len(replacements) > 0:
                    extras_changed = True
            
            '''DEFAULTS'''
            defaults = rule.defaults_copy()
            defaults_changed = False
            if len(defaults) > 0:
                replacements = {}
                for default_key in defaults.keys(): # 
                    value = defaults[default_key]
                    if isinstance(value, basestring):
                        '''only replace strings; also,
                        only replace values, not keys:
                        default_key should not be changed - it will never be spoken'''
                        nvalue = value # new value
                        replace = False
                        for old in DEFS.defaults.keys(): # 'old' is the target word(s) in the old 'value'
                            new = DEFS.defaults[old]
                            if old in nvalue:
                                nvalue = nvalue.replace(old, new)
                                replace = True
                        if replace:
                            defaults[default_key] = nvalue
                            defaults_changed = True
            
            if extras_changed or defaults_changed:
                rule.__init__(rule._name, rule.mapping_actual(), extras, defaults, rule._exported,
                              rule.ID, rule.composite, rule.compatible, rule._mcontext, rule._mwith)
                        

if DEFS is not None:
    print("Global rule filter from file 'words.txt' activated ...")
    

    
    
    
