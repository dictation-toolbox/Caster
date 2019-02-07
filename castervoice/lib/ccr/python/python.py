'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import Dictation, MappingRule

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
            R(Text("def "), rdescript="Python: Function"),
        SymbolSpecs.CLASS:
            R(Text("class "), rdescript="Python: Class"),
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
        "list comprehension":
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
    }

    extras = [
        Dictation("text"),
    ]
    defaults = {}


control.nexus().merger.add_global_rule(Python(ID=100))
