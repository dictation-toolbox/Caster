

"""
Continuous command recognition for programmers
============================================================================

This module allows the user switch quickly between programming languages
and use continuous command  recognition with each. It is based on the work
of many others, including people that I haven't listed here.
Thanks Christo Butcher, davitenio, poppe1219, ccowan


"""

from dragonfly import *

from caster.lib import control
from caster.lib import settings, utilities


try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

grammar = None
grammarN = None
current_combined_rule_ccr = None
current_combined_rule_nonccr = None
rule_pairs = {}

MODULE_MARKERS=["#<ccr>","#</ccr>","#<non>","#</non>",]
MODULE_SHELL=["from dragonfly import *", 
              "cmd.map = {", MODULE_MARKERS[0],  "'default command text A':Text('')", MODULE_MARKERS[1], "}", 
              "cmd.extras = [", "]", "cmd.defaults = {", "}", 
              "cmd.ncactive=True", 
              "cmd.ncmap = {", MODULE_MARKERS[2], "'default command text B':Text('')", MODULE_MARKERS[3], "}", 
              "cmd.ncextras = [", "]", "cmd.ncdefaults = {", "}"
              ]


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
    if rule1 == None or rule2 == None:
        return True
    
    result = True
    
    for key in rule1._mapping:
        if key in rule2._mapping:
            result = False
    return result

def _merge_node_compatible_check(node_rule):
    global current_combined_rule_ccr
    for spec in node_rule.master_node.all_possibilities():
        if spec in current_combined_rule_ccr._mapping.keys():
            utilities.report("The spec '"+spec+"' from the "+node_rule.master_node.text \
                             + " node is incompatible with one of the following CCR modules: " \
                             + ", ".join([x for x in settings.SETTINGS["ccr"]["modes"] if settings.SETTINGS["ccr"]["modes"][x]]) \
                             + " --disabling "+node_rule.master_node.text +" node")
            node_rule.master_node.active = False
            return

def _merge_node_compatibility():
    global current_combined_rule_ccr
    if current_combined_rule_ccr==None:
        return
    for node_rule in control.nexus().noderules:
        if node_rule.master_node.active:
            _merge_node_compatible_check(node_rule)
                

class ConfigCCR(Config):
    def __init__(self, name):
        Config.__init__(self, name)
        self.cmd = Section("Language section")
        self.cmd.map = Item(
            {"mimic <text>": Mimic(extra="text"), },
            namespace={"Key": Key, "Text":  Text, }
        )
        self.cmd.extras = Item([Dictation("text")])
        self.cmd.defaults = Item({})
        self.cmd.ncmap = Item(
            {"mimic <text>": Mimic(extra="text"), },
            namespace={"Key": Key, "Text":  Text, }
        )
        self.cmd.ncextras = Item([Dictation("text")])
        self.cmd.ncdefaults = Item({})
        self.cmd.ncactive = Item(False)   

def generate_language_rule_pair(path):
    ''' creates a CCR subsection from a text file, also optionally a non-CCR subsection '''
    #---------------------------------------------------------------------------
    language = path.split("/")[-1].split(".")[-2]
    
    configuration = ConfigCCR("CCR " + language)
    configuration.load(path)
    #---------------------------------------------------------------------------
    ccr = MappingRule(exported=False,
        mapping=configuration.cmd.map,
        extras=configuration.cmd.extras,
        defaults=configuration.cmd.defaults)
    nonccr = None
    if configuration.cmd.ncactive:  # .get_value():
        nonccr = MappingRule(exported=True,
            mapping=configuration.cmd.ncmap,
            extras=configuration.cmd.ncextras,
            defaults=configuration.cmd.ncdefaults,
            name="nonccr")
    #---------------------------------------------------------------------------
    return (ccr, nonccr)
#     return ccr

def create_repeat_rule(language_rule):
    
    alts = [RuleRef(rule=language_rule)]
    for noderule in control.nexus().noderules:
        if noderule.master_node.active:
            alts.append(RuleRef(rule=noderule))
    single_action = Alternative(alts)
    sequence_name = "sequence_" + "language"
    sequence = Repetition(single_action, min=1, max=16, name=sequence_name)
    original = Alternative(alts, name="original")
    terminal = Alternative(alts, name="terminal")
    
    #---------------------------------------------------------------------------
    # Here we define the top-level rule which the user can say.
    class RepeatRule(CompoundRule):
        # Here we define this rule's spoken-form and special elements.
        spec = "[<original> original] [<" + sequence_name + ">] [terminal <terminal>]"# 
        extras = [ sequence, original, terminal ] # Sequence of actions defined above.
                   
        def _process_recognition(self, node, extras):
            original = None
            terminal = None
            sequence = None
            if "original" in extras:
                original = extras["original"]
            if sequence_name in extras:
                sequence = extras[sequence_name]
            if "terminal" in extras:
                terminal = extras["terminal"]
            print original, "\n\n", sequence, "\n\n", terminal
            if original!=None:
                original.execute()
#             sequence = extras[sequence_name]  # A sequence of actions.
            if sequence!=None:
                for action in sequence:
                    action.execute()
            if terminal!=None:
                terminal.execute()

    #---------------------------------------------------------------------------
    
    return RepeatRule()

# Create and load this module's grammar.
def refresh():
    global grammar, grammarN, current_combined_rule_ccr, current_combined_rule_nonccr
    unload()
    grammar = Grammar("multi edit ccr")
    grammarN = Grammar("nccr")
    if current_combined_rule_ccr != None:
        _merge_node_compatibility()
        grammar.add_rule(create_repeat_rule(current_combined_rule_ccr))
        grammar.load()
    if current_combined_rule_nonccr != None:
        ccrn = merge_copy(current_combined_rule_nonccr, None, None)
        grammarN.add_rule(ccrn)
        grammarN.load()

def initialize_ccr():
    try:
        for r in settings.SETTINGS["ccr"]["modes"]:
            if settings.SETTINGS["ccr"]["modes"][r]:
                set_active(r)
        refresh()
    except Exception:
        utilities.simple_log()
    
    
def set_active(ccr_mode=None):
    global rule_pairs, current_combined_rule_ccr, current_combined_rule_nonccr
    new_rule_ccr = None
    new_rule_nonccr = None
    incompatibility_found = False
    
    
    
    if ccr_mode != None:
        # add mode
        ccr_mode = str(ccr_mode)
        # obtain rule: either retrieve it or generate it
        
        target_rule_pair = None
        for rule_name in rule_pairs:
            if rule_name == ccr_mode:
                target_rule_pair = rule_pairs[rule_name]
        if target_rule_pair == None or settings.SETTINGS["ccr"]:
            target_rule_pair = generate_language_rule_pair(settings.SETTINGS["paths"]["GENERIC_CONFIG_PATH"] + "/config" + ccr_mode + ".txt")
            rule_pairs[ccr_mode] = target_rule_pair
         
        # determine compatibility
        if merge_copy_compatible(target_rule_pair[0], current_combined_rule_ccr):
            new_rule_ccr = merge_copy(target_rule_pair[0], current_combined_rule_ccr, None)
            if target_rule_pair[1] != None and merge_copy_compatible(target_rule_pair[01], current_combined_rule_nonccr):
                new_rule_nonccr = merge_copy(target_rule_pair[1], current_combined_rule_nonccr, None)
        else:
            # handling incompatibility
            for r in settings.SETTINGS["ccr"]["modes"]:
                if settings.SETTINGS["ccr"]["modes"][r] and not merge_copy_compatible(target_rule_pair[0], rule_pairs[r][0]):
                    settings.SETTINGS["ccr"]["modes"][r] = False
                    incompatibility_found = True
                    # add disabled rule to common section of settings
                    
        settings.SETTINGS["ccr"]["modes"][ccr_mode] = True
    
    if ccr_mode == None or incompatibility_found:
        # delete mode or incompatibility_found
        current_combined_rule_nonccr = None
        for r in settings.SETTINGS["ccr"]["modes"]:
            if settings.SETTINGS["ccr"]["modes"][r]:
                new_rule_ccr = merge_copy(rule_pairs[r][0], new_rule_ccr, None)
                if rule_pairs[r][1] != None:
                    new_rule_nonccr = merge_copy(rule_pairs[r][1], new_rule_nonccr, None)
    
    current_combined_rule_ccr = new_rule_ccr
    # 
    if new_rule_nonccr != None:
        current_combined_rule_nonccr = new_rule_nonccr
        
def set_active_command(enable_disable, ccr_mode):
    ccr_mode = str(ccr_mode)
    if int(enable_disable) == 1:
        set_active(ccr_mode)
    else:
        settings.SETTINGS["ccr"]["modes"][ccr_mode] = False
        set_active()
        
    # activate and save
    settings.save_config()
    refresh()

def refresh_from_files(ccr_mode=None):
    global rule_pairs
    for r in settings.SETTINGS["ccr"]["modes"]:
        if settings.SETTINGS["ccr"]["modes"][r]:
            rule_pairs[r] = generate_language_rule_pair(settings.SETTINGS["paths"]["GENERIC_CONFIG_PATH"] + "/config" + r + ".txt")
    if ccr_mode!=None:
        set_active_command(0, ccr_mode)
        set_active_command(1, ccr_mode)

# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
    global grammarN
    if grammarN: grammarN.unload()
    grammarN = None
