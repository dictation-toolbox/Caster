'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import Dictation, MappingRule, Choice, Pause

from castervoice.lib import control
from castervoice.lib.actions import Key, Text
from castervoice.lib.ccr.standard import SymbolSpecs
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class PythonNon(MappingRule):
    mapping = {
        "with":
            R(Text("with "), rdescript="Python: With"),
        "open file":
            R(Text("open('filename','r') as f:"), rdescript="Python: Open File"),
        "read lines":
            R(Text("content = f.readlines()"), rdescript="Python: Read Lines"),
        "try catch":
            R(Text("try:") + Key("enter:2/10, backspace") + Text("except Exception:") +
              Key("enter"),
              rdescript="Python: Try Catch"),
        
    }


class Python(MergeRule):
    non = PythonNon

    mapping = {
        SymbolSpecs.IF:
            R(Key("i,f,space,colon,left"), rdescript="Python: If"),
        SymbolSpecs.ELSE:
            R(Text("else:") + Key("enter"), rdescript="Python: Else"),
        #
        # (no switch in Python)
        SymbolSpecs.BREAK:
            R(Text("break"), rdescript="Python: Break"),
        #
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for  in :") + Key("left:5"), rdescript="Python: For Each Loop"),
        SymbolSpecs.FOR_LOOP:
            R(Text("for i in range(0, ):") + Key("left:2"),
              rdescript="Python: For i Loop"),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while :") + Key("left"), rdescript="Python: While"),
        # (no do-while in Python)
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("int()") + Key("left"), rdescript="Python: Convert To Integer"),
        SymbolSpecs.TO_FLOAT:
            R(Text("float()") + Key("left"),
              rdescript="Python: Convert To Floating-Point"),
        SymbolSpecs.TO_STRING:
            R(Text("str()") + Key("left"), rdescript="Python: Convert To String"),
        #
        SymbolSpecs.AND:
            R(Text(" and "), rdescript="Python: And"),
        SymbolSpecs.OR:
            R(Text(" or "), rdescript="Python: Or"),
        SymbolSpecs.NOT:
            R(Text("!"), rdescript="Python: Not"),
        #
        SymbolSpecs.SYSOUT:
            R(Text("print()") + Key("left"), rdescript="Python: Print"),
        #
        SymbolSpecs.IMPORT:
            R(Text("import "), rdescript="Python: Import"),
        #
        SymbolSpecs.FUNCTION:
            R(Text("def ():") + Key("left:3"), rdescript="Python: Function"),
        SymbolSpecs.CLASS:
            R(Text("class :") + Key("left"), rdescript="Python: Class"),
        
        

        #
        SymbolSpecs.COMMENT:
            R(Text("#"), rdescript="Python: Add Comment"),
        SymbolSpecs.LONG_COMMENT:
            R(Text("''''''") + Key("left:3"), rdescript="Python: Long Comment"),
        #
        SymbolSpecs.NULL:
            R(Text("None"), rdescript="Python: Null"),
        #
        SymbolSpecs.RETURN:
            R(Text("return "), rdescript="Python: Return"),
        #
        SymbolSpecs.TRUE:
            R(Text("True"), rdescript="Python: True"),
        SymbolSpecs.FALSE:
            R(Text("False"), rdescript="Python: False"),

        # Python specific
        "sue iffae":
            R(Text("if "), rdescript="Python: Short If"),
        "sue shells":
            R(Text("else "), rdescript="Python: Short Else"),
        "from":
            R(Text("from "), rdescript="Python: From"),
        "self":
            R(Text("self"), rdescript="Python: Self"),
        "long not":
            R(Text(" not "), rdescript="Python: Long Not"),
        "it are in":
            R(Text(" in "), rdescript="Python: In"),  #supposed to sound like "iter in"
        "shell iffae | LFA":
            R(Key("e,l,i,f,space,colon,left"), rdescript="Python: Else If"),
        "convert to character":
            R(Text("chr()") + Key("left"), rdescript="Python: Convert To Character"),
        "length of":
            R(Text("len()") + Key("left"), rdescript="Python: Length"),
        "global":
            R(Text("global "), rdescript="Python: Global"),
        "make assertion":
            R(Text("assert "), rdescript="Python: Assert"),
        "list (comprehension | comp)":
            R(Text("[x for x in TOKEN if TOKEN]"),
              rdescript="Python: List Comprehension"),
        
        "[dot] (pie | pi)":
            R(Text(".py"), rdescript="Python: .py"),
        "toml":
            R(Text("toml"), rdescript="Python: toml"),
        "jason":
            R(Text("toml"), rdescript="Python: json"),
        "identity is":
            R(Text(" is "), rdescript="Python: is"),
        "yield":
            R(Text("yield "), rdescript="Python: Yield"),
        
        # essentially an improved version of the try catch command above
            # probably a better option than this is to use snippets with tab stops 
            # VS code has the extension Python-snippets. these are activated by 
            # going into the command pallet (cs-p) and typing in "insert snippet"
            # then press enter and then you have choices of snippets show up in the drop-down list.
            # you can also make your own snippets.
        "try [<exception>]": 
            R(Text("try : ") + Pause("10") + Key("enter/2") 
            + Text("except %(exception)s:") + Pause("10") + Key("enter/2"),
                rdescript="create 'try catch' block with given exception"),
        "try [<exception>] as": 
            R(Text("try :") + Pause("10") + Key("enter/2") + Text("except %(exception)s as :")
            + Pause("10") + Key("enter/2"),  rdescript="create 'try catch as' block with given exception"),

        
        # class and class methods
        "subclass": R(Text("class ():") + Key("left:3"), rdescript="Python: subclass"),
        "dunder": R(Text("____()") + Key("left:4"),  rdescript="Python special method"),
        "init": Text("__init__()") + Key("left"),
        "meth [<binary_meth>]": R(Text("__%(binary_meth)s__(self, other):"), 
            rdescript="Python: binary special method"),     
        "meth [<unary_meth>]": R(Text("__%(unary_meth)s__(self):"), 
            rdescript="Python: unary special method"),     
        
        



    }

    extras = [
        Dictation("text"),
        Choice("unary_meth", {
                "reper": "reper",
                "stir": "str",
                "len": "len",
        }),
        Choice("binary_meth", {
                "add": "add",
                "subtract": "sub",
        }),
        Choice("exception", {
            "exception": "Exception",
            "stop iteration": "StopIteration",
            "system exit": "SystemExit",
            "standard": "StandardError",
            "arithmetic": "ArithmeticError",
            "overflow": "OverflowError",
            "floating-point": "FloatingPointError",
            "zero division": "ZeroDivisionError",
            "assertion": "AssertionError",
            "EOF": "EOFError",
            "import": "ImportError",
            "keyboard interrupt": "KeyboardInterrupt",
            "lookup": "LookupError",
            "index": "IndexError",
            "key": "KeyError",
            "name": "NameError",
            "unbound local": "UnboundLocalError",
            "environment": "EnvironmentError",
            "IO": "IOError",
            "OS": "OSError",
            "syntax": "SyntaxError",
            "system exit": "SystemExit",
            "type": "TypeError",
            "value": "ValueError",
            "runtime": "RuntimeError",
            "not implemented": "NotImplementedError",
            



        })
    ]
    defaults = {"unary_meth": "", "binary_meth": "", "exception": ""}


control.nexus().merger.add_global_rule(Python(ID=100))
