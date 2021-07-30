'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import Pause, Dictation, Choice

from castervoice.lib.actions import Text, Key
from castervoice.rules.ccr.standard import SymbolSpecs
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R
from castervoice.lib.temporary import Store, Retrieve


class Python(MergeRule):

    mapping = {
        SymbolSpecs.IF:
            R(Key("i,f,space,colon,left")),
        SymbolSpecs.ELSE:
            R(Text("else:") + Key("enter")),
        # (no switch in Python)
        SymbolSpecs.BREAK:
            R(Text("break")),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Store() + Text("for  in :") + Key("left:5") +
              Retrieve(action_if_text="right:5")),
        SymbolSpecs.FOR_LOOP:
            R(Store() + Text("for i in range(0, ):") + Key("left:2") +
              Retrieve(action_if_text="right:2")),
        SymbolSpecs.WHILE_LOOP:
            R(Store() + Text("while :") + Key("left") + Retrieve(action_if_text="right")),
        # (no do-while in Python)
        SymbolSpecs.TO_INTEGER:
            R(Store() + Text("int()") + Key("left") + Retrieve(action_if_text="right")),
        SymbolSpecs.TO_FLOAT:
            R(Store() + Text("float()") + Key("left") + Retrieve(action_if_text="right")),
        SymbolSpecs.TO_STRING:
            R(Store() + Text("str()") + Key("left") + Retrieve(action_if_text="right")),
        SymbolSpecs.AND:
            R(Text(" and ")),
        SymbolSpecs.OR:
            R(Text(" or ")),
        SymbolSpecs.NOT:
            R(Text("!")),
        SymbolSpecs.SYSOUT:
            R(Store() + Text("print()") + Key("left") + Retrieve(action_if_text="right")),
        SymbolSpecs.IMPORT:
            R(Text("import ")),
        SymbolSpecs.FUNCTION:
            R(Store() + Text("def ():") + Key("left:3") +
              Retrieve(action_if_text="right:3")),
        SymbolSpecs.CLASS:
            R(Store() + Text("class :") + Key("left") + Retrieve(action_if_text="right")),
        SymbolSpecs.COMMENT:
            R(Store() + Text("#") + Key("space") + Retrieve(action_if_text="right")),
        SymbolSpecs.LONG_COMMENT:
            R(Store() + Text("''''''") + Key("left:3") +
              Retrieve(action_if_text="right:3")),
        SymbolSpecs.NULL:
            R(Text("None")),
        SymbolSpecs.RETURN:
            R(Text("return ")),
        SymbolSpecs.TRUE:
            R(Text("True")),
        SymbolSpecs.FALSE:
            R(Text("False")),

        # Python specific
        "sue iffae":
            R(Text("if ")),
        "sue shells":
            R(Text("else ")),
        "from":
            R(Text("from ")),
        "self":
            R(Text("self")),
        "long not":
            R(Text(" not ")),
        "it are in":
            R(Text(" in ")),
        "shell iffae | LFA":
            R(Key("e,l,i,f,space,colon,left")),
        "convert to character":
            R(Store() + Text("chr()") + Key("left") + Retrieve(action_if_text="right")),
        "length of":
            R(Store() + Text("len()") + Key("left") + Retrieve(action_if_text="right")),
        "global":
            R(Text("global ")),
        "make assertion":
            R(Text("assert ")),
        "list (comprehension | comp)":
            R(Text("[x for x in TOKEN if TOKEN]")),
        "[dot] (pie | pi)":
            R(Text(".py")),
        "toml":
            R(Text("toml")),
        "jason":
            R(Text("toml")),
        "identity is":
            R(Text(" is ")),
        "yield":
            R(Text("yield ")),

        # Essentially an improved version of the try catch command above
        # probably a better option than this is to use snippets with tab stops
        # VS code has the extension Python-snippets. these are activated by
        # going into the command pallet (cs-p) and typing in "insert snippet"
        # then press enter and then you have choices of snippets show up in the drop-down list.
        # you can also make your own snippets.
        "try [<exception>]":
            R(
                Text("try : ") + Pause("10") + Key("enter/2") +
                Text("except %(exception)s:") + Pause("10") + Key("enter/2")),
        "try [<exception>] as":
            R(
                Text("try :") + Pause("10") + Key("enter/2") +
                Text("except %(exception)s as :") + Pause("10") + Key("enter/2")),

        # class and class methods
        "sub class":
            R(Store() + Text("class ():") + Key("left:3") +
              Retrieve(action_if_text="right:3")),
        "dunder":
            R(Store() + Text("____()") + Key("left:4") +
              Retrieve(action_if_text="right:4")),
        "init":
            R(Store() + Text("__init__()") + Key("left") +
              Retrieve(action_if_text="right")),
        "meth [<binary_meth>]":
            R(Text("__%(binary_meth)s__(self, other):")),
        "meth [<unary_meth>]":
            R(Text("__%(unary_meth)s__(self):")),
    }

    extras = [
        Dictation("text"),
        Choice("unary_meth", {
            "reper": "repr",
            "stir": "str",
            "len": "len",
        }),
        Choice("binary_meth", {
            "add": "add",
            "subtract": "sub",
        }),
        Choice(
            "exception", {
                "exception": "Exception",
                "stop iteration": "StopIteration",
                "system exit": "SystemExit",
                "standard": "StandardError",
                "arithmetic": "ArithmeticError",
                "overflow": "OverflowError",
                "floating point": "FloatingPointError",
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
                "run time": "RuntimeError",
                "not implemented": "NotImplementedError",
            })
    ]
    defaults = {"unary_meth": "", "binary_meth": "", "exception": ""}


def get_rule():
    return Python, RuleDetails(ccrtype=CCRType.GLOBAL)
