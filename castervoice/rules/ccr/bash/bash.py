'''
Created on Sep 1, 2015
@author: synkarius
'''
from castervoice.lib.actions import Text, Key
from castervoice.rules.ccr.standard import SymbolSpecs
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R



class Bash(MergeRule):
    pronunciation = "bash"

    mapping = {
        SymbolSpecs.IF:
            R(Text("if [[  ]]; ") + Key("left/5:5")),
        SymbolSpecs.ELSE:
            R(Text("else")),
        #
        SymbolSpecs.SWITCH:
            R(Text("case TOKEN in")),
        SymbolSpecs.CASE:
            R(Text("TOKEN)  ;;") + Key("left/5:2")),
        SymbolSpecs.BREAK:
            R(Text("break")),
        SymbolSpecs.DEFAULT:
            R(Text("*)  ;;")),
        #
        SymbolSpecs.DO_LOOP:
            R(Text("until [  ]; do") + Key("left/5:7")),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while [  ]; do") + Key("left/5:7")),
        SymbolSpecs.FOR_LOOP:
            R(Text("for (( i=0; i<=TOKEN; i++ )); do")),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for TOKEN in TOKEN; do")),
        #
        # integers?
        # strings?
        # floats?
        #
        SymbolSpecs.AND:
            R(Text(" && ")),
        SymbolSpecs.OR:
            R(Text(" || ")),
        SymbolSpecs.NOT:
            R(Text("!")),
        #
        SymbolSpecs.SYSOUT:
            R(Text("echo ")),
        #
        SymbolSpecs.IMPORT:
            R(Text(". /path/to/functions")),  # (top of file, under #!/bin/bash)
        #
        SymbolSpecs.FUNCTION:
            R(Text("TOKEN(){}") + Key("left, enter/5:2")),
        # classes?
        #
        SymbolSpecs.COMMENT:
            R(Text("# ")),
        # no multiline comment in bash
        #
        SymbolSpecs.NULL:
            R(Text('-z "$var"') + Key("left/5:1")),
        #
        SymbolSpecs.RETURN:
            R(Text("return ")),
        #
        SymbolSpecs.TRUE:
            R(Text("true")),
        SymbolSpecs.FALSE:
            R(Text("false")),

        # Bash specific
        "key do":
            R(Text("do")),
        "key done":
            R(Text("done")),
        "key fee":
            R(Text("fi")),
        "shell iffae":
            R(Text("elif [[  ]]; ") + Key("left/5:5")),
        "sue iffae":
            R(Text("[[  ]]") + Key("left/5:3")),
        "length of":
            R(Text("${#TOKEN[@]}")),
        "push":
            R(Text("TOKEN+=()")),
        "continue":
            R(Text("continue")),
        "she bang":
            R(Text("#!/bin/bash")),
        "end switch":
            R(Text("esac")),
    }

    extras = []
    defaults = {}


def get_rule():
    return Bash, RuleDetails(ccrtype=CCRType.GLOBAL)
