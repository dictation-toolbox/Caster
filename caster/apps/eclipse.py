''' line ops functions '''

from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, Key, Text, Repeat, Pause)
from dragonfly.actions.action_function import Function
from dragonfly.actions.action_mimic import Mimic
from dragonfly.grammar.elements import Choice

from caster.lib import control, utilities
from caster.lib import settings
from caster.lib.ccr.core.nav import Navigation
from caster.lib.dfplus.additions import IntegerRefST, Boolean
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R, L, S
from caster.lib import context as CONTEXT
from dragonfly.actions.action_paste import Paste


class EclipseController(object):
    def __init__(self):
        self.regex = False
        self.analysis_chars = r"\]"
    def regex_on(self):
        if not self.regex:
            Key("a-x").execute() # turn on regex
        self.regex = True
    def regex_off(self):
        if self.regex:
            Key("a-x").execute() # turn off regex
        self.regex = False
    def analyze_for_configure(self):
        '''solves the problem of the editor not being smart about toggles by using text
        to see which toggles are active'''
        
        '''regex toggle check'''
        Key("escape").execute() # get out of Find
        result = CONTEXT.read_nmax_tries(10)
        if result == self.analysis_chars:
            self.regex = False
            Key("backspace").execute()
        elif result == self.analysis_chars[1]:
            self.regex = True
            Key("delete, backspace").execute()
        else:
            control.nexus().intermediary.text("Eclipse configuration failed ("+result+")")
        
        
    def lines_relative(self, back, n):
        if back: #backward
            try:
                num = CONTEXT.read_nmax_tries(10)
                txt = str(int(num)-int(n)+1) # +1 to include current line
                Text(txt).execute()
            except ValueError:
                utilities.simple_log()
                return
            Key("enter").execute()
        else: #forward
            Key("escape, end, home, home").execute() # end-home-home to include all of current line
        
        # forward or backward
        Key("s-down:"+str(int(n))+"/5, s-left").execute()
    
#     def process_text_for_search(self, text, regex, rtog):
#         text = str(text)
#         if int(regex) == 1:
#             text = text[0] + "?".join(list(text[1:])) + "?"
#         if int(rtog) == 1:
#             Key("a-x").execute() # turn on regex
#         Text(text).execute()
#     def set_direction(self, direction):
#         key = "o" # forward
#         if int(direction) == 0:
#             key = "b" #backward
#         Key("a-"+key).execute()

    
        
    
ec_con = EclipseController()

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
            
            
        }
    extras = [
            Dictation("text"),
            Dictation("mim"),
            IntegerRefST("n", 1, 3000),
            
            
             ]
    defaults = {"n": 1, "mim":""}#, "regex": 0, "rtog":0s

class EclipseCCR(MergeRule):
    pronunciation = "eclipse"
    
    mwith = [Navigation().get_name()]
    
    mapping = {
            #Line Ops
            "configure":                                R(Paste(ec_con.analysis_chars)+Key("left:2/5, c-f/20, backslash, rbracket, enter") + \
                                                          Function(ec_con.analyze_for_configure), rdescript="Eclipse: Configure"),
            "jump in [<n>]":                            R(Key("c-f, a-o")+Paste(r"[\(\[\{\<]")+Function(ec_con.regex_on)+ \
                                                          Key("enter:%(n)d/5, escape, right") , rdescript="Eclipse: Jump In"),
            "jump out [<n>]":                           R(Key("c-f, a-o")+Paste(r"[\)\] \}\>]")+Function(ec_con.regex_on)+ \
                                                          Key("enter:%(n)d/5, escape, right") , rdescript="Eclipse: Jump Out"),
            "jump back [<n>]":                          R(Key("c-f/5, a-b")+Paste(r"[\)\]\}\>]")+Function(ec_con.regex_on)+ \
                                                          Key("enter:%(n)d/5, escape, left") , rdescript="Eclipse: Jump Back"),
            "[go to] line <n>":                         R(Key("c-l") + Pause("50") + Text("%(n)d") + Key("enter")+ Pause("50")+
                                                          Mimic(extra="mim"), rdescript="Eclipse: Go To Line"),
            "shackle <n> [<back>]":                     R(Key("c-l")+Key("right, cs-left")+ \
                                                          Function(ec_con.lines_relative), rdescript="Eclipse: Select Relative Lines"),
            
        }
    extras = [
              Dictation("text"),
              IntegerRefST("n", 1, 1000),
              Boolean("back"),
             ]
    defaults = {"n": 1, "back": False}
#---------------------------------------------------------------------------

context = AppContext(executable="javaw", title="Eclipse") | AppContext(executable="eclipse", title="Eclipse") | AppContext(executable="AptanaStudio3")
grammar = Grammar("Eclipse", context=context)
grammar.add_rule(CommandRule(name="eclipse"))
if settings.SETTINGS["apps"]["eclipse"]:
    grammar.load()
    control.nexus().merger.add_app_rule(EclipseCCR(), context)
