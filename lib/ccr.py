

"""
Continuous command recognition for programmers
============================================================================

This module allows the user switch quickly between programming languages
and use continuous command  recognition with each. It is based on the work
of many others, including people that I haven't listed here.
Thanks Christo Butcher, davitenio, poppe1219, ccowan


"""
from dragonfly import *

from lib import settings, utilities


try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

grammar = None
current_combined_rule = None
rules = {}

def merge_copy(rule1, rule2, context):
    if rule1 == None:
        raise Exception("first parameter can't be null")
    if rule2 != None:
        mapping = rule1._mapping.copy()
        mapping.update(rule2._mapping)
        extras_dict = rule1._extras.copy()
        extras_dict.update(rule2._extras)
        extras = extras_dict.values()
        defaults = rule1._defaults.copy()
        defaults.update(rule2._defaults)
        return MappingRule(rule1._name + "+" + rule2._name, mapping, extras, defaults, rule1._exported, context)
    else:
        return MappingRule(rule1._name, rule1._mapping, rule1._extras.values(), rule1._defaults, rule1._exported, context)

def merge_copy_compatible(rule1, rule2):
    '''
    ccrc: another CCR_Container
    '''
    if rule1 == None:
        raise Exception("first parameter can't be null")
    if rule2 == None:
        return True
    for key in rule1._mapping:
        if key in rule2._mapping:
            return False
    return True

def generate_language_rule(path):
    ''' Turns the original _multiedit.py into a rule factory '''

    #---------------------------------------------------------------------------
    language = path.split("/")[-1].split(".")[-2]
    
    configuration = Config("CCR " + language)
    configuration.cmd = Section("Language section")
    configuration.cmd.map = Item(
        {
         "mimic <text>":                     Mimic(extra="text"),
        },
        namespace={
         "Key":   Key,
         "Text":  Text,
        }
    )
    configuration.cmd.extras = Item([Dictation("text")])
    configuration.cmd.defaults = Item({})
    configuration.load(path)
    #---------------------------------------------------------------------------
    
    class KeystrokeRule(MappingRule):
        exported = False
        mapping = configuration.cmd.map
        extras = configuration.cmd.extras
        defaults = configuration.cmd.defaults
    #---------------------------------------------------------------------------
    return KeystrokeRule()

def create_repeat_rule(ks_rule):

    alternatives = []
    alternatives.append(RuleRef(rule=ks_rule))
    single_action = Alternative(alternatives)
    
    sequence_name = "sequence_" + "language"
    sequence = Repetition(single_action, min=1, max=16, name=sequence_name)
    
    
    #---------------------------------------------------------------------------
    # Here we define the top-level rule which the user can say.
    class RepeatRule(CompoundRule):
        # Here we define this rule's spoken-form and special elements.
        spec = "<" + sequence_name + "> [[[and] repeat [that]] <n> times]"
        extras = [
                    sequence,  # Sequence of actions defined above.
                    IntegerRef("n", 1, 100),  # Times to repeat the sequence.
                   ]
        defaults = {
                    "n": 1,  # Default repeat count.
                   }
        def _process_recognition(self, node, extras):
            sequence = extras[sequence_name]  # A sequence of actions.
            count = extras["n"]  # An integer repeat count.
            for i in range(count):
                for action in sequence:
                    action.execute()

    #---------------------------------------------------------------------------
    
    return RepeatRule()
# Create and load this module's grammar.
def refresh():
    global grammar
    unload()
    grammar = Grammar("multi edit")
    if current_combined_rule!=None:
        grammar.add_rule(create_repeat_rule(current_combined_rule))
        grammar.load()

def initialize_ccr():
    global current_combined_rule
    
    # read from file if active, standard or common
    for r in settings.SETTINGS["ccr"]["modes"]:
        if settings.SETTINGS["ccr"]["modes"][r] or r in settings.SETTINGS["ccr"]["common"] or r in settings.SETTINGS["ccr"]["standard"]:
            rules[r] = generate_language_rule(settings.SETTINGS["paths"]["GENERIC_CONFIG_PATH"] + "/config" + r + ".txt")
    
    # activate if marked as active
    for r in settings.SETTINGS["ccr"]["modes"]:
        if settings.SETTINGS["ccr"]["modes"][r]:
            current_combined_rule = merge_copy(rules[r], current_combined_rule, None)
    refresh()
    
    

def set_active(enable_disable, ccr_mode):
    ccr_mode = str(ccr_mode)
    enable_disable = int(enable_disable)
    global rules
    global current_combined_rule
    new_rule = None
    if enable_disable == -1:
        return
    elif enable_disable == 0:
        settings.SETTINGS["ccr"]["modes"][ccr_mode] = False
    elif enable_disable == 1:
        # obtain rule: either retrieve it or generate it
        
        target_rule = None
        for rule_name in rules:
            if rule_name == ccr_mode:
                target_rule = rules[rule_name]
        if target_rule == None:
            target_rule = generate_language_rule(settings.SETTINGS["paths"]["GENERIC_CONFIG_PATH"] + "/config" + ccr_mode + ".txt")
            rules[ccr_mode] = target_rule
        
        # determine compatibility
        if merge_copy_compatible(target_rule,current_combined_rule):
            new_rule = merge_copy(target_rule,current_combined_rule, None)
        else:
            for r in settings.SETTINGS["ccr"]["modes"]:
                if settings.SETTINGS["ccr"]["modes"][r] and not merge_copy_compatible(target_rule, rules[r]):
                    settings.SETTINGS["ccr"]["modes"][r] = False
                    print "setting "+r+" to False"
                    # add disabled rule to common section of settings
                    
        settings.SETTINGS["ccr"]["modes"][ccr_mode] = True
        print "setting "+ccr_mode+" to True"
    
    # rebuild if necessary
    if new_rule == None:
        for r in settings.SETTINGS["ccr"]["modes"]:
            if settings.SETTINGS["ccr"]["modes"][r]:
                new_rule = merge_copy(rules[r], new_rule, None)
        
    
    # activate and save
    settings.save_config()
    current_combined_rule = new_rule
    refresh()  

# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None

def camel_case(text):
    t = str(text)
    words = t.split(" ")
    Text(words[0] + "".join(w.capitalize() for w in words[1:]))._execute()
    
def score(text):
    """ score <dictation> """  # Docstring defining spoken-form.
    t = str(text)  # Get written-form of dictated text.
    Text("_".join(t.split(" ")))._execute()
