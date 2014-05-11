
"""
Continuous command recognition for programmers
============================================================================

This module allows the user switch quickly between programming languages
and use continuous command  recognition with each. It is based on the work
of many others, including people that I haven't listed here.
Thanks Christo Butcher, davitenio, poppe1219


"""

try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import *
import natlink

import config
config_settings = config.get_config()
JAVAPATH = "C:\NatLink\NatLink\MacroSystem\languages\configjava.txt"

#---------------------------------------------------------------------------
# Each of the following steps needs to be done per programming language

config_java           = Config("eclipse Java")
config_java.cmd        = Section("Language section")
config_java.cmd.map    = Item(
    {
     "mimic <text>":                     Mimic(extra="text"),
    },
    namespace={
     "Key":   Key,
     "Text":  Text,
    }
)
namespace_java = config_java.load(JAVAPATH)

#---------------------------------------------------------------------------
# Here we prepare the list of formatting functions from the config file.

# Retrieve text-formatting functions from this module's config file.
#  Each of these functions must have a name that starts with "format_".
format_functions_java = {}
if namespace_java:
    for name, function in namespace_java.items():
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
        format_functions_java[spoken_form] = action


# Here we define the text formatting rule.
# The contents of this rule were built up from the "format_*"
#  functions in this module's config file.
if format_functions_java:
    class FormatRuleJava(MappingRule):

        mapping  = format_functions_java
        extras   = [Dictation("dictation")]

else:
    FormatRuleJava = None


#---------------------------------------------------------------------------
# Here we define the keystroke rule.

class KeystrokeRule(MappingRule):

    exported = False

    mapping  = config_java.cmd.map
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
alternatives_java = []
alternatives_java.append(RuleRef(rule=KeystrokeRule()))
if FormatRuleJava:
    alternatives_java.append(RuleRef(rule=FormatRuleJava()))
single_action_java = Alternative(alternatives_java)

# Second we create a repetition of keystroke elements.
# Note that we give this element the name "sequence" so that it can be used as an extra in the rule definition below.
sequence_java = Repetition(single_action_java, min=1, max=16, name="sequence_java")


#---------------------------------------------------------------------------
# Here we define the top-level rule which the user can say.
class RepeatRuleJava(CompoundRule):
    # Here we define this rule's spoken-form and special elements.
    spec     = "<sequence_java> [[[and] repeat [that]] <n> times]"
    extras   = [
                sequence_java,                 # Sequence of actions defined above.
                IntegerRef("n", 1, 100),  # Times to repeat the sequence.
               ]
    defaults = {
                "n": 1,                   # Default repeat count.
               }
    def _process_recognition(self, node, extras):
        sequence_java = extras["sequence_java"]   # A sequence of actions.
        count = extras["n"]             # An integer repeat count.
        for i in range(count):
            for action in sequence_java:
                action.execute()
        #release.execute()


#---------------------------------------------------------------------------
# Create and load this module's grammar.
context = AppContext(executable="eclipse")


class JavaEnabler(CompoundRule):
    spec = "Enable Java"                  # Spoken command to enable the Java grammar.
    
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        javaBootstrap.disable()
        grammarJava.enable()
        natlink.execScript ("TTSPlayString \"" +"Java grammar enabled"+ "\"")

class JavaDisabler(CompoundRule):
    spec = "switch language"                  # spoken command to disable the Java grammar.
    
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        grammarJava.disable()
        javaBootstrap.enable()
        natlink.execScript ("TTSPlayString \"" +"Java grammar disabled"+ "\"")

# The main Python grammar rules are activated here
javaBootstrap = Grammar("java bootstrap", context=context)                
javaBootstrap.add_rule(JavaEnabler())
javaBootstrap.load()

grammarJava = Grammar("Eclipse Java", context=context)   # Create this module's grammar.
grammarJava.add_rule(RepeatRuleJava())    # Add the top-level rule.
grammarJava.add_rule(JavaDisabler())
grammarJava.load()                    # Load the grammar.
grammarJava.disable()

# Unload function which will be called at unload time.
def unload():
    global javaBootstrap
    if javaBootstrap: javaBootstrap.unload()
    javaBootstrap = None
    global grammarJava
    if grammarJava: grammarJava.unload()
    grammarJava = None
