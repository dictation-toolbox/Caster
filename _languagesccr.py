
"""
Continuous command recognition for programmers
============================================================================

This module allows the user switch quickly between programming languages
and use continuous command  recognition with each. It is based on the work
of many others, including people that I haven't listed here.
Thanks Christo Butcher, davitenio, poppe1219, ccowan


"""

try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import *
import natlink

import config, paths
config_settings = config.get_config()
ALL_LANGUAGE_CONFIGS=paths.get_all_language_configs()

rules = []
           
def disable_all_except(language):
    global rules
    global config_settings
    #import pydevd;pydevd.settrace()
    for holder in rules:
        if not holder.language == language:
            config_settings[holder.language] = False
            config.save_config()
            holder.grammar.disable()
            holder.bootstrap.enable()
            

class GrammarHolder():
    def __init__(self, gram, boot, lan):
        self.grammar = gram
        self.bootstrap = boot
        self.language = lan

def generate_language_rule(path):
    #---------------------------------------------------------------------------
    # Each of the following steps needs to be done per programming language
    
    language = path.split('config', 1)[-1].split(".", 1)[0]
    
    #STEP 1: create the config object
    configuration           = Config("CCR "+language)
    configuration.cmd        = Section("Language section")
    configuration.cmd.map    = Item(
        {
         "mimic <text>":                     Mimic(extra="text"),
        },
        namespace={
         "Key":   Key,
         "Text":  Text,
        }
    )
    namespace = configuration.load(path)
    
    #---------------------------------------------------------------------------
    #STEP 2: formatting functions
    # Here we prepare the list of formatting functions from the config file.
    
    # Retrieve text-formatting functions from this module's config file.
    #  Each of these functions must have a name that starts with "format_".
    format_functions = {}
    if namespace:
        for name, function in namespace.items():
            if name.startswith("format_") and callable(function):
                spoken_form = function.__doc__.strip()
        
                # We wrap generation of the Function action in a function so
                #  that its *function* variable will be local.  Otherwise it
                #  would change during the next iteration of the namespace loop.
                def wrap_function(function):
                    def _function(dictation):
                        formatted_text = function(dictation)
                        Text(formatted_text).execute()
                    return Function(_function)
        
                action = wrap_function(function)
                format_functions[spoken_form] = action
    
    
    # Here we define the text formatting rule.
    # The contents of this rule were built up from the "format_*"
    #  functions in this module's config file.
    if format_functions:
        class FormatRule(MappingRule):
    
            mapping  = format_functions
            extras   = [Dictation("dictation")]
    
    else:
        FormatRule = None
    
    
    #---------------------------------------------------------------------------
    # Here we define the keystroke rule.
    
    class KeystrokeRule(MappingRule):
        exported = False
        mapping  = configuration.cmd.map
        extras   = [
                    IntegerRef("n", 1, 100),
                    IntegerRef("n2", 1, 100),
                    IntegerRef("n3", 1, 100),
                    Dictation("text"),
                    Dictation("text2"),
                   ]
        defaults = {
                    "n": 1,
                   }
    
    
    
    #---------------------------------------------------------------------------
    # Here we create an element which is the sequence of keystrokes.
    
    # First we create an element that references the keystroke rule.
    #  Note: when processing a recognition, the *value* of this element
    #  will be the value of the referenced rule: an action.
    alternatives = []
    alternatives.append(RuleRef(rule=KeystrokeRule()))
    if FormatRule:
        alternatives.append(RuleRef(rule=FormatRule()))
    single_action = Alternative(alternatives)
    
    # Second we create a repetition of keystroke elements.
    # Note that we give this element the name "sequence" so that it can be used as an extra in the rule definition below.
    sequence_name = "sequence_"+language
    sequence = Repetition(single_action, min=1, max=16, name=sequence_name)
    
    
    #---------------------------------------------------------------------------
    # Here we define the top-level rule which the user can say.
    class RepeatRule(CompoundRule):
        # Here we define this rule's spoken-form and special elements.
        spec     = "<"+sequence_name+"> [[[and] repeat [that]] <n> times]"
        extras   = [
                    sequence,                 # Sequence of actions defined above.
                    IntegerRef("n", 1, 100),  # Times to repeat the sequence.
                   ]
        defaults = {
                    "n": 1,                   # Default repeat count.
                   }
        def _process_recognition(self, node, extras):
            sequence = extras[sequence_name]   # A sequence of actions.
            count = extras["n"]             # An integer repeat count.
            for i in range(count):
                for action in sequence:
                    action.execute()

    #---------------------------------------------------------------------------
    bootstrap = Grammar("bootstrap "+language)  # Create this module's enabler .
    grammar = Grammar(language)   # Create this module's grammar .
    
    class Enabler(CompoundRule):
        spec = "Enable "+language                  # Spoken command to enable the  grammar.
        
        def _process_recognition(self, node, extras):   # Callback when command is spoken.
            global config_settings
            config_settings[language] = True
            config.save_config()
            bootstrap.disable()
            grammar.enable()
            disable_all_except(language)
            natlink.execScript ("TTSPlayString \"" +language+" grammar enabled"+ "\"")
    
    class Disabler(CompoundRule):
        spec = "Disable " +language                 # spoken command to disable the  grammar.
        
        def _process_recognition(self, node, extras):   # Callback when command is spoken.
            global config_settings
            config_settings[language] = False
            config.save_config()
            grammar.disable()
            bootstrap.enable()
            natlink.execScript ("TTSPlayString \"" +language+" grammar disabled"+ "\"")
    
    bootstrap.add_rule(Enabler())
    bootstrap.load()
    
    grammar.add_rule(RepeatRule())    # Add the top-level rule.
    grammar.add_rule(Disabler())
    grammar.load()                    # Load the grammar.
    grammar.disable()
    
    if config_settings[language] == True:
        grammar.enable()
    
    return GrammarHolder(grammar,bootstrap,language)


#---------------------------------------------------------------------------    


for path in ALL_LANGUAGE_CONFIGS:
    rules.append(generate_language_rule(path))
    



# Unload function which will be called at unload time.
def unload():
    global rules
    for holder in rules:
        holder.grammar.unload()
        holder.grammar = None
        holder.bootstrap.unload()
        holder.bootstrap = None
    holder = None
