''' line ops functions '''

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, Key, Text, Repeat, Pause)
from dragonfly.actions.action_function import Function
from dragonfly.actions.action_mimic import Mimic
from dragonfly.grammar.elements import Choice

from caster.lib import control, utilities
from caster.lib import settings
from caster.lib.ccr.core.nav import Navigation
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.actions import AsynchronousAction
from caster.lib.dfplus.state.short import R, L, S
from caster.lib import context as CONTEXT

def process_text_for_search(text, regex, rtog):
    text = str(text)
    if int(regex) == 1:
        text = text[0] + "?".join(list(text[1:])) + "?"
    if int(rtog) == 1:
        Key("a-x").execute() # turn on regex
    Text(text).execute()
def set_direction(direction):
    key = "o" # forward
    if int(direction) == 0:
        key = "b" #backward
    Key("a-"+key).execute()
def lines_relative(direction, n):
    if int(direction) == 0: #backward
        try:
            num = CONTEXT.read_selected_without_altering_clipboard(True)[1]
            txt = str(int(num)-int(n))
            Text(txt).execute()
        except ValueError:
            utilities.simple_log()
            return
        Key("enter").execute()
    else: #forward
        Key("escape").execute()
    
    # forward or backward
    Pause("50").execute()
    Key("s-down:"+str(int(n))+"/5").execute()
    
        
    


class CommandRule(MappingRule):

    mapping = {
                    
            "prior tab [<n>]":                          R(Key("cs-f6"), rdescript="Eclipse: Previous Tab") * Repeat(extra="n"),  # these two must be set up in the eclipse preferences
            "next tab [<n>]":                           R(Key("c-f6"), rdescript="Eclipse: Next Tab") * Repeat(extra="n"),
            "open resource":                            R(Key("cs-r"), rdescript="Eclipse: Open Resource"),
            "open type":                                R(Key("cs-t"), rdescript="Eclipse: Open Type"),

            "jump to source":                           R(Key("f3"), rdescript="Eclipse: Jump To Source"),
            "editor select":                            R(Key("c-e"), rdescript="Eclipse: Editor Select"),
            
            "step over [<n>]":                          R(Key("f6/50") * Repeat(extra="n"), rdescript="Eclipse: Step Over"),
            "step into":                                R(Key("f5"), rdescript="Eclipse: Step Into"),
            "step out [of]":                            R(Key("f7"), rdescript="Eclipse: Step Out"),
            "resume":                                   R(Key("f8"), rdescript="Eclipse: Resume"),
            "(debug | run) last":                       R(Key("f11"), rdescript="Eclipse: Run Last"),
            "mark occurrences":                         R(Key("as-o"), rdescript="Eclipse: Mark Occurrences"),

            # "terminate" changes to the settings for this hotkey: (when: in dialogs and windows)
            "terminate":                                R(Key("c-f2"), rdescript="Eclipse: Terminate Running Program"),
            
            "find everywhere":                          R(Key("ca-g"), rdescript="Eclipse: Search Project"),
            "refractor symbol":                         R(Key("sa-r"), rdescript="Eclipse: Re-Factor Symbol"),
            
            "symbol next [<n>]":                        R(Key("c-k"), rdescript="Eclipse: Symbol Next") * Repeat(extra="n"),
            "symbol prior [<n>]":                       R(Key("cs-k"), rdescript="Eclipse: Symbol Prior") * Repeat(extra="n"),            
            
            "format code":                              R(Key("cs-f"), rdescript="Eclipse: Format Code"),
            "do imports":                               R(Key("cs-o"), rdescript="Eclipse: Do Imports"),
            "comment line":                             R(Key("c-slash"), rdescript="Eclipse: Comment Line"),
            
            "build it":                                 R(Key("c-b"), rdescript="Eclipse: Build"), 
            
            "split view horizontal":                    R(Key("cs-underscore"), rdescript="Eclipse: Split View (H)"), 
            "split view vertical":                      R(Key("cs-lbrace"), rdescript="Eclipse: Split View (V)"),
            
            #Line Ops
            "search [<regex>] [<rtog>] [<direction>] <text>": R(Key("c-f") + Pause("50") + \
                                                          Function(process_text_for_search) + \
                                                          Function(set_direction), rdescript="Eclipse: Search")  + \
                                                        AsynchronousAction([L(S(["cancel"], Key("enter")))], 1, 50, "...", False),
            "lines <n> [<direction>]":                  R(Key("c-l")+Pause("50")+Key("right, cs-left")+Pause("50")+Function(lines_relative), \
                                                          rdescript="Eclipse: Select Relative Lines"),
        }
    extras = [
            Dictation("text"),
            Dictation("mim"),
            IntegerRefST("n", 1, 3000),
            
            # line ops
            Choice("direction", {"back" : 0}),
            Choice("regex", {"reg" : 1}),
            Choice("rtog", {"toggle" : 1}),
            
             ]
    defaults = {"n": 1, "mim":"", "direction": 1, "regex": 0, "rtog":0}

class EclipseCCR(MergeRule):
    pronunciation = "eclipse"
    
    mwith = [Navigation().get_name()]
    
    mapping = {
            "[go to] line <n>":                         R(Key("c-l") + Pause("50") + Text("%(n)d") + Key("enter")+ Pause("50")+
                                                          Mimic(extra="mim"), rdescript="Eclipse: Go To Line"),
        }
    extras = [
              Dictation("text"),
              IntegerRefST("n", 1, 1000),
             ]
    defaults = {"n": 1}
#---------------------------------------------------------------------------

context = AppContext(executable="javaw", title="Eclipse") | AppContext(executable="eclipse", title="Eclipse") | AppContext(executable="AptanaStudio3")
grammar = Grammar("Eclipse", context=context)
grammar.add_rule(CommandRule(name="eclipse"))
if settings.SETTINGS["apps"]["eclipse"]:
    grammar.load()
    control.nexus().merger.add_app_rule(EclipseCCR(), context)
