'''
Created on 2018-05-27 from javascript.py

@author: comodoro
'''

from caster.lib import control
from caster.lib.actions import Key, Text
from caster.ccr.standard import SymbolSpecs
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class Dart(MergeRule):

    mapping = {

        # CCR PROGRAMMING STANDARD
        SymbolSpecs.IF:
            R(Text("if () {}") + Key("left, enter:2, up"), rdescript="Dart: If"),
        SymbolSpecs.ELSE:
            R(Text("else {}") + Key("left, enter:2, up"), rdescript="Dart: Else"),
        #
        SymbolSpecs.SWITCH:
            R(Text("switch () {}") + Key("left, enter:2, up"),
              rdescript="Dart: Switch"),
        SymbolSpecs.CASE:
            R(Text("case :") + Key("left"), rdescript="Dart: Case"),
        SymbolSpecs.BREAK:
            R(Text("break;"), rdescript="Dart: Break"),
        SymbolSpecs.DEFAULT:
            R(Text("default: "), rdescript="Dart: Default"),
        #
        SymbolSpecs.DO_LOOP:
            R(Text("do {}") + Key("left, enter:2"), rdescript="Dart: Do Loop"),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while ()") + Key("left"), rdescript="Dart: While"),
        SymbolSpecs.FOR_LOOP:
            R(Text("for (var i = 0; i < TOKEN; i++)"), rdescript="Dart: For i Loop"),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for (TOKEN in TOKEN)"), rdescript="Dart: For Each Loop"),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("int.parse()") + Key("left"),
              rdescript="Dart: Convert To Integer"),
        SymbolSpecs.TO_FLOAT:
            R(Text("double.parse()") + Key("left"),
              rdescript="Dart: Convert To Floating-Point (double)"),
        SymbolSpecs.TO_STRING:
            R(Text(".toString()"), rdescript="Dart: Convert To String"),
        #
        SymbolSpecs.AND:
            R(Text(" && "), rdescript="Dart: And"),
        SymbolSpecs.OR:
            R(Text(" || "), rdescript="Dart: Or"),
        SymbolSpecs.NOT:
            R(Text("!"), rdescript="Dart: Not"),
        #
        SymbolSpecs.SYSOUT:
            R(Text("print()") + Key("left"), rdescript="Dart: Print"),

        SymbolSpecs.IMPORT:
            R(Text("import ''") + Key("left"), rdescript="Dart: Import"),

        SymbolSpecs.FUNCTION:
            R(Text("TOKEN() {}") + Key("left, enter"), rdescript="Dart: Function"),

        SymbolSpecs.CLASS:
            R(Text("class {}") + Key("left/5:2"), rdescript="Dart: Class"),
        #
        SymbolSpecs.COMMENT:
            R(Text("//"), rdescript="Dart: Add Comment"),
        SymbolSpecs.LONG_COMMENT:
            R(Text("/**/") + Key("left,left"), rdescript="Dart: Long Comment"),
        #
        SymbolSpecs.NULL:
            R(Text("null"), rdescript="Dart: Null"),
        #
        SymbolSpecs.RETURN:
            R(Text("return "), rdescript="Dart: Return"),
        #
        SymbolSpecs.TRUE:
            R(Text("true"), rdescript="Dart: True"),
        SymbolSpecs.FALSE:
            R(Text("false"), rdescript="Dart: False"),

        # Dart specific
        "anon funk":
            R(Text("() => {}") + Key("left:1, enter"),
              rdescript="Dart: Anonymous Function"),
        "length":
            R(Text("length"), rdescript="Dart: Length"),
        "self":
            R(Text("self"), rdescript="Dart: Self"),
        "new new":
            R(Text("new "), rdescript="Dart: New"),
        "continue":
            R(Text("continue"), rdescript="Dart: Continue"),
        "this":
            R(Text("this"), rdescript="Dart: This"),
        "try":
            R(Text("try {}") + Key("left, enter:2, up"), rdescript="Dart: Try"),
        "catch":
            R(Text("catch(e) {}") + Key("left, enter:2, up"),
              rdescript="Dart: Catch"),
        "throw":
            R(Text("throw "), rdescript="Dart: Throw"),
        "instance of":
            R(Text("instanceof "), rdescript="Dart: Instance Of"),
        "const":
            R(Text("const "), rdescript=" Dart: Const"),
        "equals if null":
            R(Text(" ??= "), rdescript=" Dart: Assign if null"),
        "a sink":
            R(Text("async "), rdescript="Dart: Async"),
        "await":
            R(Text("await "), rdescript="Dart: Await"),
        "yield":
            R(Text("yield "), rdescript="Dart: Yield"),
        "cascade":
            R(Key("enter") + Text(".."), rdescript="Dart: Cascade operator"),
        "dock string":
            R(Text("/// "), rdescript="Dart: Docomentation string"),
        "var":
            R(Text("var TOKEN = "), rdescript="Dart: Var"),
    }

    extras = []
    defaults = {}


control.nexus().merger.add_global_rule(Dart())
