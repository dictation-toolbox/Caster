import io, sys
import time

from dragonfly import *

from lib import paths, settings, utilities


try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass



# this stuff shouldn't be called here
unified_grammar = None

class CCRFile:
    # representation of a text file, used for compatibility so we don't have to read the text file multiple times
    def __init__(self):
        self.name = None
        self.mapping = []
        self.extras = []
        self.defaults = []
        self.other = []

def change_CCR(enable_disable, ccr_mode):
    enable = True if str(enable_disable) == "enable" else False
    mode = str(ccr_mode)
    
    # get models of all relevant CCR files
    models = get_models(mode if enable else "")
    
    active_modes = get_active_modes()
    master_model = CCRFile()
    override_mode = True
    report = False
    
    if len(models[1]) > 1:
        raise Exception("you need to go back into the compatibility section and check the incoming modes against themselves")
    
    
    if enable:
        # check for compatibility
        incompatibilities = []
        for current in models[0]:  # current is one of the currently enabled CCR files
            for incoming in models[1]:
                for line in incoming.mapping:
                    if line in current.mapping:
                        if report:
                            utilities.report("CCR incompatibility found (mapping): " + line)
                        incompatibilities.append((current.name, incoming.name))
                        break
                for line in incoming.defaults:
                    if line in current.defaults and line.strip() != "}),":
                        if report:
                            utilities.report("CCR incompatibility found (defaults): " + line)
                        incompatibilities.append((current.name, incoming.name))
                        break
                for line in incoming.extras:
                    if line in current.extras:
                        if report:
                            utilities.report("CCR incompatibility found (extras): " + line)
                        incompatibilities.append((current.name, incoming.name))
                        break
#                 for line in incoming.other:
#                     if line in current.other:
#                         if report:
#                             utilities.report("CCR incompatibility found (others): " + line)
#                         incompatibilities.append((current.name, incoming.name))
                        
        if override_mode:  # remove current mode(s) which is(/are) incompatible with new mode(s)
            if len(incompatibilities) > 0:
                for incompatibility in incompatibilities:
                    if incompatibility[0] in active_modes:
                        active_modes.remove(incompatibility[0])
        
        active_modes.append(mode)  # active_modes is now the master list of stuff that should go in
        
    
    else:
        if mode in active_modes:
            active_modes.remove(mode)
    all_models = models[0] + models[1]
    for m in all_models:
        if not m.name in active_modes:
            all_models.remove(m)
    for model in all_models:
        master_model.mapping += model.mapping
        master_model.extras += model.extras
        master_model.defaults += model.defaults
        master_model.other += model.other    
            
    # Make the combined file
    success = combine_CCR_files(master_model)
    
    
    # If compatibility success failed, no need to worry about writing the config file wrong
    if success:
        config_settings = settings.SETTINGS["ccr"]
        for s in config_settings:
            config_settings[s] = s in active_modes
        settings.save_config()
        # Now, toss the old grammar and make a new one
        unload()
        refresh()
        utilities.report(str(enable_disable).capitalize() + "d " + ccr_mode, speak=True)
    else:
        utilities.report("failed to initialize " + ccr_mode, speak=True)

def get_active_modes():
    config_settings = settings.SETTINGS["ccr"]
    results = []
    for s in config_settings:
        if config_settings[s] == True:
            results.append(s)
    return results

def get_models(mode_1="", mode_2="", mode_3="", mode_4=""):
    # all four parameters are strings,
    # if mode_1 is null, then we are disabling
    old_ccr_files = []
    new_ccr_file = []
    
    for m in get_active_modes():
        old_ccr_files.append(get_ccr_file(m))
    for n in [mode_1, mode_2, mode_3, mode_4]:
        if n != "":
            new_ccr_file.append(get_ccr_file(str(n)))
    return (old_ccr_files, new_ccr_file)
            
def get_ccr_file(mode):
    ccr_file = CCRFile()
    ccr_file.name = mode
    with open(paths.GENERIC_CONFIG_PATH + "\\config" + mode + ".txt", "r") as f:
        
        mapping = False
        extras = False
        defaults = False
        lines = f.readlines()
        for line in lines:
            no_whitespace = line.strip()
            
            # parse the file
            # first, either change the mode or skip the line if appropriate
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
            elif no_whitespace in ["", "\n"] or no_whitespace.startswith("#"):
                continue
            
            
            if mapping:
                ccr_file.mapping.append(line)
            elif extras:
                ccr_file.extras.append(line)
#                         if not line in relevant_configs["extras"] or no_whitespace == "}),":
            elif defaults:
                ccr_file.defaults.append(line)
            else:
                ccr_file.other.append(line)
    return ccr_file

def combine_CCR_files(master_model):
    try:
        with open(paths.UNIFIED_CONFIG_PATH, "w") as fw:
            for lnc in master_model.other:
                fw.write(lnc)
            fw.write("cmd.map= {\n")
            for lm in master_model.mapping:
                fw.write(lm)
            fw.write("}\n")
            fw.write("cmd.extras= [\n")
            for le in master_model.extras:
                fw.write(le)
            fw.write("]\n")
            fw.write("cmd.defaults= {\n")
            for ld in master_model.defaults:
                fw.write(ld)
            fw.write("}\n")
        
        return True
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))
        return False
    

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
    unified_grammar = generate_language_rule(paths.UNIFIED_CONFIG_PATH)
    unified_grammar.load()  # Load the grammar.

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

def format_ecma_loop(looptype, text, condition, increment):
    lt = str(looptype)
    # to do: check settings to find which language is active
    letter = str(text)
    if not letter == "":
        letter = letter[0].lower()
    else:
        letter = "i"
    print lt
        
    if lt == "letter":
        c = str(condition)
        if c == "":
            c = "<"
        i = str(increment)
        if i == "":
            i = "++"
        Text("for (var " + letter + " = PARAMETER; " + letter + " " + c + " PARAMETER; " + letter + i + "){}")._execute()
        Key("left, enter/5:2, up")._execute()
        time.sleep(0.05)
    elif lt == "each":
        language_dependent = None
        config_settings = settings.SETTINGS["ccr"]
        if config_settings["java"]:
            language_dependent = "for (PARAMETER " + letter + " : PARAMETER){}"
        elif config_settings["javascript"]:
            language_dependent = "for (var " + letter + " in PARAMETER){}"
        else:
            language_dependent = "please_configure_language"
        Text(language_dependent)._execute()
        Key("left, enter/5:2, up")._execute()
        time.sleep(0.05)
