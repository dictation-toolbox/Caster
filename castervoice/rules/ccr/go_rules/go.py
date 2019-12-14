'''
Created November 2018
@author: Mike Roberts
'''
from dragonfly import Key

from castervoice.lib.actions import Text
from castervoice.rules.ccr.standard import SymbolSpecs
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Go(MergeRule):

    mapping = {
        SymbolSpecs.IF:
            R(Text("if  {}") + Key("left, enter, up, end, left:2")),
        SymbolSpecs.ELSE:
            R(Text("else {}") + Key("left, enter, up")),
        #
        SymbolSpecs.SWITCH:
            R(Text("switch  {}") + Key("left, enter, up, end, left:2")),
        SymbolSpecs.CASE:
            R(Text("case :") + Key("left")),
        SymbolSpecs.DEFAULT:
            R(Text("default:") + Key("enter")),
        SymbolSpecs.BREAK:
            R(Text("break")),
        #
        SymbolSpecs.WHILE_LOOP:
            R(Text("for  {}") + Key("left, enter, up, end, left:2")),
        SymbolSpecs.FOR_LOOP:
            R(Text("for i := 0; i<; i++ {}") + Key("left, enter, up, end, left:7")),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for  := range  {}") + Key("left, enter, up, home, right:4")),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("strconv.Atoi()") + Key("left")),
        SymbolSpecs.TO_STRING:
            R(Text("strconv.Itoa()") + Key("left")),
        #
        SymbolSpecs.AND:
            R(Text(" && ")),
        SymbolSpecs.OR:
            R(Text(" || ")),
        SymbolSpecs.NOT:
            R(Text("!")),
        #
        SymbolSpecs.SYSOUT:
            R(Text("fmt.Println()") + Key("left")),
        #
        SymbolSpecs.IMPORT:
            R(Text("import ()") + Key("left, enter")),
        #
        SymbolSpecs.FUNCTION:
            R(Text("func ")),
        SymbolSpecs.CLASS:
            R(Text("type  struct {}") + Key("left, enter, up, home, right:5")),
        #
        SymbolSpecs.COMMENT:
            R(Text("//")),
        SymbolSpecs.LONG_COMMENT:
            R(Text("/**/") + Key("left, left")),
        #
        SymbolSpecs.NULL:
            R(Text("nil")),
        #
        SymbolSpecs.RETURN:
            R(Text("return ")),
        #
        SymbolSpecs.TRUE:
            R(Text("true")),
        SymbolSpecs.FALSE:
            R(Text("false")),
        #
        "[type] (inter | integer)":
            R(Text("int")),
        "[type] boolean":
            R(Text("bool")),
        "[type] string":
            R(Text("string")),
        "assign":
            R(Text(" := ")),
        "(function | funk) main":
            R(Text("func main() {}") + Key("left, enter")),
        "make map":
            R(Text("make(map[])") + Key("left:2")),
        "package":
            R(Text("package ")),
    }

    extras = []
    defaults = {}


def get_rule():
    return Go, RuleDetails(ccrtype=CCRType.GLOBAL)
