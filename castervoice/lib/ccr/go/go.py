'''
Created November 2018

@author: Mike Roberts
'''
from dragonfly import Choice, Key, Text

from castervoice.lib import control
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.ccr.standard import SymbolSpecs


class Go(MergeRule):

    mapping = {
        SymbolSpecs.IF:
            R(Text("if  {}") + Key("left, enter, up, end, left:2"), rdescript="Go: if"),
        SymbolSpecs.ELSE:
            R(Text("else {}") + Key("left, enter, up"), rdescript="Go: else"),
        #
        SymbolSpecs.SWITCH:
            R(Text("switch  {}") + Key("left, enter, up, end, left:2"),
              rdescript="Go: switch"),
        SymbolSpecs.CASE:
            R(Text("case :") + Key("left"), rdescript="Go: case"),
        SymbolSpecs.DEFAULT:
            R(Text("default:") + Key("enter"), rdescript="Go: default"),
        SymbolSpecs.BREAK:
            R(Text("break"), rdescript="Go: break"),
        #
        SymbolSpecs.WHILE_LOOP:
            R(Text("for  {}") + Key("left, enter, up, end, left:2"),
              rdescript="Go: while loop"),
        SymbolSpecs.FOR_LOOP:
            R(Text("for i := 0; i<; i++ {}") + Key("left, enter, up, end, left:7"),
              rdescript="Go: for loop"),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for  := range  {}") + Key("left, enter, up, home, right:4"),
              rdescript="Go: for each"),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("strconv.Atoi()") + Key("left"), rdescript="Go: convert to integer"),
        SymbolSpecs.TO_STRING:
            R(Text("strconv.Itoa()") + Key("left"), rdescript="Go: convert to string"),
        #
        SymbolSpecs.AND:
            R(Text(" && "), rdescript="Go: and"),
        SymbolSpecs.OR:
            R(Text(" || "), rdescript="Go: or"),
        SymbolSpecs.NOT:
            R(Text("!"), rdescript="Go: not"),
        #
        SymbolSpecs.SYSOUT:
            R(Text("fmt.Println()") + Key("left"), rdescript="Go: sysout"),
        #
        SymbolSpecs.IMPORT:
            R(Text("import ()") + Key("left, enter"), rdescript="Go: import"),
        #
        SymbolSpecs.FUNCTION:
            R(Text("func "), rdescript="Go: function"),
        SymbolSpecs.CLASS:
            R(Text("type  struct {}") + Key("left, enter, up, home, right:5"),
              rdescript="Go: class"),
        #
        SymbolSpecs.COMMENT:
            R(Text("//"), rdescript="Go: comment"),
        SymbolSpecs.LONG_COMMENT:
            R(Text("/**/") + Key("left, left"), rdescript="Go: long comment"),
        #
        SymbolSpecs.NULL:
            R(Text("nil"), rdescript="Go: nil"),
        #
        SymbolSpecs.RETURN:
            R(Text("return "), rdescript="Go: return"),
        #
        SymbolSpecs.TRUE:
            R(Text("true"), rdescript="Go: true"),
        SymbolSpecs.FALSE:
            R(Text("false"), rdescript="Go: false"),
        #
        "[type] (inter | integer)":
            R(Text("int"), rdescript="Go: integer"),
        "[type] boolean":
            R(Text("bool"), rdescript="Go: boolean"),
        "[type] string":
            R(Text("string"), rdescript="Go: string"),
        "assign":
            R(Text(" := "), rdescript="Go: assign"),
        "(function | funk) main":
            R(Text("func main() {}") + Key("left, enter"), rdescript="Go: main function"),
        "make map":
            R(Text("make(map[])") + Key("left:2"), rdescript="Go: create a map"),
        "package":
            R(Text("package "), rdescript="Go: package"),
    }

    extras = []
    defaults = {}


control.nexus().merger.add_global_rule(Go())
