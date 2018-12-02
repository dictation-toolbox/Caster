'''
Created on Sep 1, 2015

@author: synkarius
'''

from caster.lib import control
from caster.lib.actions import Key, Text
from caster.ccr.standard import SymbolSpecs
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class Bash(MergeRule):
    mapping = {
        SymbolSpecs.IF:
            R(Text("if [[  ]]; ") + Key("left/5:5"), rdescript="Bash: If"),
        SymbolSpecs.ELSE:
            R(Text("else"), rdescript="Bash: Else"),
        #
        SymbolSpecs.SWITCH:
            R(Text("case TOKEN in"), rdescript="Bash: Switch"),
        SymbolSpecs.CASE:
            R(Text("TOKEN)  ;;") + Key("left/5:2"), rdescript="Bash: Case"),
        SymbolSpecs.BREAK:
            R(Text("break"), rdescript="Bash: Break"),
        SymbolSpecs.DEFAULT:
            R(Text("*)  ;;"), rdescript="Bash: Default"),
        #
        SymbolSpecs.DO_LOOP:
            R(Text("until [  ]; do") + Key("left/5:7"), rdescript="Bash: Do Loop"),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while [  ]; do") + Key("left/5:7"), rdescript="Bash: While"),
        SymbolSpecs.FOR_LOOP:
            R(Text("for (( i=0; i<=TOKEN; i++ )); do"), rdescript="Bash: For i Loop"),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for TOKEN in TOKEN; do"), rdescript="Bash: For Each Loop"),
        #
        # integers?
        # strings?
        # floats?
        #
        SymbolSpecs.AND:
            R(Text(" && "), rdescript="Bash: And"),
        SymbolSpecs.OR:
            R(Text(" || "), rdescript="Bash: Or"),
        SymbolSpecs.NOT:
            R(Text("!"), rdescript="Bash: Not"),
        #
        SymbolSpecs.SYSOUT:
            R(Text("echo "), rdescript="Bash: Print"),
        #
        SymbolSpecs.IMPORT:
            R(Text(". /path/to/functions"),
              rdescript="Bash: Import"),  # (top of file, under #!/bin/bash)
        #
        SymbolSpecs.FUNCTION:
            R(Text("TOKEN(){}") + Key("left, enter/5:2"), rdescript="Bash: Function"),
        # classes?
        #
        SymbolSpecs.COMMENT:
            R(Text("# "), rdescript="Bash: Add Comment"),
        # no multiline comment in bash
        #
        SymbolSpecs.NULL:
            R(Text('-z "$var"') + Key("left/5:1"), rdescript="Bash: Null"),
        #
        SymbolSpecs.RETURN:
            R(Text("return "), rdescript="Bash: Return"),
        #
        SymbolSpecs.TRUE:
            R(Text("true"), rdescript="Bash: True"),
        SymbolSpecs.FALSE:
            R(Text("false"), rdescript="Bash: False"),

        # Bash specific
        "key do":
            R(Text("do"), rdescript="Bash: Do"),
        "key done":
            R(Text("done"), rdescript="Bash: Done"),
        "key fee":
            R(Text("fi"), rdescript="Bash: End If"),
        "shell iffae":
            R(Text("elif [[  ]]; ") + Key("left/5:5"), rdescript="Bash: Else If"),
        "sue iffae":
            R(Text("[[  ]]") + Key("left/5:3"), rdescript="Bash: Short If"),
        "length of":
            R(Text("${#TOKEN[@]}"), rdescript="Bash: Length"),
        "push":
            R(Text("TOKEN+=()"), rdescript="Bash: Push"),
        "continue":
            R(Text("continue"), rdescript="Bash: Continue"),
        "she bang":
            R(Text("#!/bin/bash"), rdescript="Bash: Shebang"),
        "end switch":
            R(Text("esac"), rdescript="Bash: End Switch"),
    }

    extras = []
    defaults = {}


control.nexus().merger.add_global_rule(Bash())
