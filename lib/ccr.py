try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from lib import paths, settings, utilities
import io, sys
from dragonfly import *


# this stuff shouldn't be called here
unified_grammar = None

def change_CCR(enable_disable, ccr_mode):
    enable = True if str(enable_disable) == "enable" else False
    ccrm = str(ccr_mode)
    # Make the combined file
    compatibility_success = combine_CCR_files(enable, ccrm)
    if not compatibility_success[0]:
        utilities.report("INCOMPATIBILITY: "+compatibility_success[1])
        return
    
    # If compatibility success failed, no need to worry about writing the config file wrong
    config_settings = settings.get_settings()
    config_settings[ccrm] = enable
    settings.save_config()
    # Now, toss the old grammar and make a new one
    unload()
    refresh()
    utilities.report(str(enable_disable).capitalize() + "d " + ccr_mode, speak=True)



def combine_CCR_files(enable, a, b="", c="", d=""):
    # enable is a Boolean
    # a,b,c,d are all the same dynamically generated choice, some may be blank-- that should be determined here
#     utilities.remote_debug()
    try:
        str_a = str(a)
        str_b = str(b)
        str_c = str(c)
        str_d = str(d)
        chosen_modes = []
        for s in [str_a, str_b, str_c, str_d]:
            if not s == "":
                chosen_modes.append(s)
        
        config_settings = settings.get_settings()  # this is a dictionary of settings.json
        backup = []
        def reset_settings():
            for setting in config_settings:
                if setting in backup:
                    config_settings[setting] = True
                else:
                    config_settings[setting] = False
        
        if enable:
            # in case there is a compatibility problem, save what was active before changing the settings
            for s in config_settings:
                if config_settings[s] == True:
                    backup.append(s)
            # now change the settings 
            for cm in chosen_modes:
                config_settings[cm] = True
        else:
            for cm in chosen_modes:
                config_settings[cm] = False

        # now, using the settings, scan in all the appropriate files and check for compatibility
        relevant_configs = {}
        relevant_configs["non_cmd"] = []
        relevant_configs["mapping"] = []
        relevant_configs["extras"] = []
        relevant_configs["defaults"] = []
        for m in config_settings:
            if config_settings[m] == True:
                with open(paths.get_generic_config_path() + "\\config" + m + ".txt", "r") as f:
                    # these three Booleans will determine where a line gets put in the big dictionary
                    mapping = False
                    extras = False
                    defaults = False
                    lines = f.readlines()
                    for line in lines:
                        no_whitespace = line.strip()
                        
                        if line.startswith("cmd.map"):
                            mapping = True
                            continue
                        elif line.startswith("cmd.extras"):
                            extras = True
                            continue
                        elif line.startswith("cmd.defaults"):
                            defaults = True
                            continue
                        elif (no_whitespace.startswith("}") or no_whitespace.startswith("]")) and len(no_whitespace) == 1:
                            mapping = False
                            extras = False
                            defaults = False
                            continue
                        
                        if no_whitespace == "" or no_whitespace.startswith("#"):
                            continue
                        
                        if mapping:
                            if not line in relevant_configs["mapping"]:
                                relevant_configs["mapping"].append(line)
                            elif not line == "\n":
                                reset_settings()
                                return (False, line)
                        elif extras:
                            if not line in relevant_configs["extras"] or no_whitespace == "}),":
                                relevant_configs["extras"].append(line)
                            elif not line == "\n":
                                reset_settings()
                                return (False, line)
                        elif defaults:
                            if not line in relevant_configs["defaults"]:
                                relevant_configs["defaults"].append(line)
                            elif not line == "\n":
                                reset_settings()
                                return (False, line)
                        else:
                            if not line in relevant_configs["non_cmd"]:
                                relevant_configs["non_cmd"].append(line)

        # At this point, either we have all the lines or the function is returned False
        with open(paths.get_unified_config_path(), "w") as fw:
            for lnc in relevant_configs["non_cmd"]:
                fw.write(lnc)
            fw.write("cmd.map= {\n")
            for lm in relevant_configs["mapping"]:
                fw.write(lm)
            fw.write("}\n")
            fw.write("cmd.extras= [\n")
            for le in relevant_configs["extras"]:
                fw.write(le)
            fw.write("]\n")
            fw.write("cmd.defaults= {\n")
            for ld in relevant_configs["defaults"]:
                fw.write(ld)
            fw.write("}\n")
        
        return (True,"")
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))
    

"""
Continuous command recognition for programmers
============================================================================

This module allows the user switch quickly between programming languages
and use continuous command  recognition with each. It is based on the work
of many others, including people that I haven't listed here.
Thanks Christo Butcher, davitenio, poppe1219, ccowan


"""
def generate_language_rule(path):
    #---------------------------------------------------------------------------
    # Each of the following steps needs to be done per programming language
    
    language = "unified"  # path.split('config', 1)[-1].split(".", 1)[0]
    
    # STEP 1: create the config object
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
    namespace = configuration.load(path)
    
    #---------------------------------------------------------------------------
    # STEP 2: formatting functions
    # Here we prepare the list of formatting functions from the config file.
    
    # Retrieve text-formatting functions from this module's config file.
    #  Each of these functions must have a name that starts with "format_".
    format_functions = {}
    if namespace:
        for name, function in namespace.items():
            if name.startswith("format_") and callable(function):
                spoken_form = function.__doc__.strip()
        
                # We wrap generation of the Function action in a function so
                #  that its *function* element will be local.  Otherwise it
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
    
            mapping = format_functions
            extras = [Dictation("dictation")]
    
    else:
        FormatRule = None
    
    
    #---------------------------------------------------------------------------
    # Here we define the keystroke rule.
    
    class KeystrokeRule(MappingRule):
        exported = False
        mapping = configuration.cmd.map
        extras = configuration.cmd.extras
        defaults = configuration.cmd.defaults
    
    
    
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
    sequence_name = "sequence_" + language
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
    grammar = Grammar(language)  # Create this module's grammar .
    grammar.add_rule(RepeatRule())  # Add the top-level rule.
    
    return grammar    
    
def refresh():
    global unified_grammar
    unified_grammar = generate_language_rule(paths.get_unified_config_path())
    unified_grammar.load()  # Load the grammar.
    utilities.report("refreshing CCR")

# Unload function which will be called at unload time.
def unload():
    global unified_grammar 
    if unified_grammar: 
        unified_grammar.disable()
        unified_grammar.unload()
    unified_grammar = None

def camel_case(text):
    t = str(text)
    words = t.split(" ")
    Text(words[0] + "".join(w.capitalize() for w in words[1:]))._execute()
    
def score(text):
    """ score <dictation> """  # Docstring defining spoken-form.
    t = str(text)  # Get written-form of dictated text.
    Text("_".join(t.split(" ")))._execute()
