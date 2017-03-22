'''
Created on Feb 6, 2017

@author: 2
'''
from dragonfly.actions.action_base import Repeat
from dragonfly.actions.action_key import Key
from dragonfly.actions.action_text import Text

from caster.lib import control
from caster.lib.ccr.standard import SymbolSpecs
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R
from caster.lib.dfplus.additions import IntegerRefST

class ColdFusion(MergeRule):
    pronunciation = "cold fusion"
    
    mapping = { 
        
        # CCR PROGRAMMING STANDARD
        SymbolSpecs.IF:                             R(Text("if (){}") + Key("left:3"), rdescript="ColdFusion: If"),
        SymbolSpecs.ELSE:                           R(Text("else {}") + Key("left, enter"), rdescript="ColdFusion: Else"),
        #
        SymbolSpecs.SWITCH:                         R(Text("switch() {}") + Key("left, enter, up"), rdescript="ColdFusion: Switch"),
        SymbolSpecs.CASE:                           R(Text("case :") + Key("left"), rdescript="ColdFusion: Case"),
        SymbolSpecs.BREAK:                          R(Text("break;"), rdescript="Break"),
        SymbolSpecs.DEFAULT:                        R(Text("default: "), rdescript="ColdFusion: Default"),
        #
        SymbolSpecs.DO_LOOP:                        R(Text("do {}") + Key("left, enter"), rdescript="ColdFusion: Do Loop"),
        SymbolSpecs.WHILE_LOOP:                     R(Text("while ()") + Key("left") + Text("  ") + Key("left:1"), rdescript="ColdFusion: While"),
        SymbolSpecs.FOR_LOOP:                       R(Text("for (var i = 0; i < ; i++){}") + Key("left, enter, up, right:12"), rdescript="ColdFusion: For i Loop"),
        SymbolSpecs.FOR_EACH_LOOP:                  R(Text("for (  in  ){}") + Key("left:8"), rdescript="ColdFusion: For Each Loop"),
        #
        SymbolSpecs.TO_INTEGER:                     R(Text("parseInt()") + Key("left"), rdescript="ColdFusion: Convert To Integer"),
        SymbolSpecs.TO_FLOAT:                       R(Text("parseFloat()") + Key("left"), rdescript="ColdFusion: Convert To Floating-Point"),
        SymbolSpecs.TO_STRING:                      R(Key("dquote, dquote, plus"), rdescript="ColdFusion: Convert To String"),
        #
        SymbolSpecs.AND:                            R(Text(" && "), rdescript="ColdFusion: And"),
        SymbolSpecs.OR:                             R(Text(" || "), rdescript="ColdFusion: Or"),
        SymbolSpecs.NOT:                            R(Text("!"), rdescript="ColdFusion: Not"),
        #
        SymbolSpecs.SYSOUT:                         R(Text("writeOutput();") + Key("left:2"), rdescript="ColdFusion: Print"),
        #
        SymbolSpecs.IMPORT:                         R(Text("import ;") + Key("left"), rdescript="ColdFusion: Import"),
        # 
        SymbolSpecs.FUNCTION:                       R(Text("function (){}") + Key("left, enter, up, right:5"), rdescript="ColdFusion: Function"),
        #
        SymbolSpecs.COMMENT:                        R(Text("//"), rdescript="ColdFusion: Add Comment"),
        SymbolSpecs.LONG_COMMENT:                   R(Text("/**/") + Key("left:2"), rdescript="ColdFusion: Long Comment"),
        #
        SymbolSpecs.NULL:                           R(Text("null"), rdescript="ColdFusion: Null"),
        #
        SymbolSpecs.RETURN:                         R(Text("return ;") + Key("left"), rdescript="ColdFusion: Return"),
        #
        SymbolSpecs.TRUE:                           R(Text("true"), rdescript="ColdFusion: True"),
        SymbolSpecs.FALSE:                          R(Text("false"), rdescript="ColdFusion: False"),

        # ColdFusion specific 

        "(far | variable)":                         R(Text("var ;") + Key("left"), rdescript="ColdFusion: Variable"), 
        "new":                                      R(Text("new ();") + Key("left:3"), rdescript="ColdFusion: This"),
        "try":                                      R(Text("try {}") + Key("left, enter"), rdescript="ColdFusion: Try"),
        "catch":                                    R(Text("catch(e) {}") + Key("left, enter"), rdescript="ColdFusion: Catch"),
        "throw":                                    R(Text("throw "), rdescript="ColdFusion: Throw"),
        "dump":                                     R(Text("dump();") + Key("left:2"), rdescript="ColdFusion: dump"),

        # ColdFusion specific functions
        "length":                                   R(Text("len()") + Key("left"), rdescript="ColdFusion: Length"),
        "struct key exists":                        R(Text("structKeyExists()") + Key("left:1"), rdescript="ColdFusion: StructKeyExists"),
        "number format":                            R(Text("numberFormat()") + Key("left:1"), rdescript="ColdFusion: NumberFormat"),
        "date format":                              R(Text("dateFormat()") + Key("left:1"), rdescript="ColdFusion: NumberFormat"),
        "date compare":                             R(Text("dateCompare()") + Key("left:1"), rdescript="ColdFusion: NumberFormat"),

        "assert equals":                            R(Text("assertEquals()") + Key("left"), rdescript="ColdFusion: Assert Equals"),
        
        # ColdFusion specific scopes
        "arguments":                                R(Text("arguments."), rdescript="ColdFusion: Variable"), 
        "session":                                  R(Text("session."), rdescript="ColdFusion: Variable"), 
        "attributes":                               R(Text("attributes."), rdescript="ColdFusion: Variable"), 
        "application":                              R(Text("application."), rdescript="ColdFusion: Application Scope"), 
        "this":                                     R(Text("this"), rdescript="ColdFusion: This"),

        # ColdFusion statically typed
        "public any function":                      R(Text("public any function (){}") + Key("left, enter, up, right:21"), rdescript="ColdFusion: Public Any Function"),
        "public void function":                     R(Text("public void function (){}") + Key("left, enter, up, right:22"), rdescript="ColdFusion: Public Void Function"),
        "public struct function":                   R(Text("public struct function (){}") + Key("left, enter, up, right:24"), rdescript="ColdFusion: Public Void Function"),
       
    }

    extras = [
            IntegerRefST("npunc", 0, 10),
    ]
    defaults = {
            "npunc": 1,
    }


control.nexus().merger.add_global_rule(ColdFusion())
