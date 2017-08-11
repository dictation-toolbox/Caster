'''
Created on Sep 2, 2015

@author: synkarius
'''
from dragonfly import Key, Text, Dictation, Function, Choice

from caster.lib import control, textformat
from caster.lib.ccr.standard import SymbolSpecs
from caster.lib.dfplus.additions import SelectiveAction
from caster.lib.dfplus.merge.mergerule import MergeRule, TokenSet
from caster.lib.dfplus.state.short import R

# Helper methods
def import_from(imported_from):
    Text(textformat.master_format_text(5, 2, str(imported_from)))

class Javascript(MergeRule):
    auto = [".js"]
        
    mapping = {
        
        # CCR PROGRAMMING STANDARD
        SymbolSpecs.IF:                 R(Text("if ") + Key("lparen"), rdescript="Javascript: If"),
        SymbolSpecs.ELSE:               R(Text("else ") + Key("lbrace, enter"), rdescript="Javascript: Else"),
        SymbolSpecs.ELIF:               R(Text("else if ") + Key("lparen"), rdescript="JS: Elif"),
        #
        SymbolSpecs.SWITCH:             R(Text("switch") + Key("lparen, rparen, space, lbrace, enter"), rdescript="Javascript: Switch"),
        SymbolSpecs.CASE:               R(Text("case :") + Key("left"), rdescript="Javascript: Case"),
        SymbolSpecs.BREAK:              R(Text("break;"), rdescript="Break"),
        SymbolSpecs.DEFAULT:            R(Text("default: "), rdescript="Javascript: Default"),
        #
        SymbolSpecs.DO_LOOP:            R(Text("do ") + Key("lbrace, enter"), rdescript="Javascript: Do Loop"),
        SymbolSpecs.WHILE_LOOP:         R(Text("while ") + Key("lparen, enter"), rdescript="Javascript: While"),
        SymbolSpecs.FOR_LOOP:           R(Text("for (var i=0; i<; i++)") + Key("left:5"), rdescript="Javascript: For i Loop"),
        SymbolSpecs.FOR_EACH_LOOP:      R(Text("for (in)") + Key("left:3"), rdescript="Javascript: For Each Loop"),
        #
        SymbolSpecs.TO_INTEGER:         R(Text("parseInt()") + Key("left"), rdescript="Javascript: Convert To Integer"),
        SymbolSpecs.TO_FLOAT:           R(Text("parseFloat()") + Key("left"), rdescript="Javascript: Convert To Floating-Point"),
        SymbolSpecs.TO_STRING:          R(Key("dquote, dquote, plus"), rdescript="Javascript: Convert To String"),
        #
        SymbolSpecs.AND:                R(Text(" && "), rdescript="Javascript: And"),
        SymbolSpecs.OR:                 R(Text(" || "), rdescript="Javascript: Or"),
        SymbolSpecs.NOT:                R(Text("!"), rdescript="Javascript: Not"),
        
        #
        SymbolSpecs.SYSOUT:             R(Text("console.log") + Key("lparen"), rdescript="JS: log"),
        
        # Imports
        ## if we use just SymbolSpecs.IMPORT, then the next rule fails to recognize
        "em" + SymbolSpecs.IMPORT:      R(Text("import  from ''") + Key("left:8"), rdescript="JS: import"),
        "embraced" + SymbolSpecs.IMPORT:
                                        R(Text("import {  } from ''") + Key("left:10"), rdescript="JS: import"),
        SymbolSpecs.IMPORT + " [<is_method>] <textnv> [from <imported_from>]":
                                        R(Text("import ") + Function(textformat.js_format)
                                            + Text(" from ") + Key("apostrophe") + Function(import_from),
                                            rdescript="ES6 import <x> from"),
        "braced" + SymbolSpecs.IMPORT + " [<is_method>] <textnv> [from <imported_from>]":
                                        R(Text("import { ") + Function(textformat.js_format)
                                            + Text(" } from ") + Key("apostrophe") + Function(import_from),
                                            rdescript="ES6 import <x> from"),

        # 
        SymbolSpecs.FUNCTION:           R(Text("function () {};") + Key("left:6, enter"), rdescript="Javascript: Function"),
        # FIXME: add classes
        #
        SymbolSpecs.COMMENT:            R(Text("//"), rdescript="Javascript: Add Comment"),
        SymbolSpecs.LONG_COMMENT:       R(Text("/**/") + Key("left,left"), rdescript="Javascript: Long Comment"),
        #
        SymbolSpecs.NULL:               R(Text("null"), rdescript="Javascript: Null"),
        #
        SymbolSpecs.RETURN:             R(Text("return "), rdescript="Javascript: Return"),
        #
        SymbolSpecs.TRUE:               R(Text("true"), rdescript="Javascript: True"),
        SymbolSpecs.FALSE:              R(Text("false"), rdescript="Javascript: False"),
        #
        SymbolSpecs.ARROW:              R(Text(" => "), rdescript="JS: Arrow"),

        # JavaScript specific
        "anon funk":                    R(Text("function () ") + Key("lbrace, enter"), rdescript="Javascript: Anonymous Function"),
        "inner HTML":                   R(Text("innerHTML"), rdescript="Javascript: InnerHTML"),
        "new new":                      R(Text("new "), rdescript="Javascript: New"),
        "continue":                     R(Text("continue"), rdescript="Javascript: Continue"),

        "this":                         R(Text("this"), rdescript="Javascript: This"),
        "try":                          R(Text("try ") + Key("lbrace, enter"), rdescript="Javascript: Try"),
        "catch":                        R(Text("catch(e) ") + Key("lbrace, enter"), rdescript="Javascript: Catch"),
        
        "throw":                        R(Text("throw "), rdescript="Javascript: Throw"),
        "instance of":                  R(Text("instanceof "), rdescript="Javascript: Instance Of"),
        

        "(far | variable)":             R(Text("var "), rdescript="Javascript: Variable"),
        

        "(met | med) <textnv>":         R(Text(".")
                                            + Function(textformat.camel_format)
                                            + Key("lparen"), rdescript="JS: method call"),
        "part <textnv>":                R(Text(".")
                                            + Function(textformat.camel_format), rdescript="js: object property"),

        #ES6 stuff
        "(cons | const)":               R(Text("const "), rdescript="es6 const"),
        "lambda":                       R(Text("() => ") + Key("left:5"), rdescript="es6 arrow function"),
        "lambda <text>":                R(Key("lparen") + Text("%(text)s") + Key("rparen") + Text(" => "),
                                            rdescript="es6 arrow func w/ arg"),

        # flow
        "using flow":                   R(Text("// @flow") + Key("enter, backspace:3"), rdescript="enable flow"),
        "maybe":                        R(Text(": ?"), rdescript="maybe type"),
        "optional":                     R(Text("?: "), rdescript="optional property"),

        #atom/nuclide
        "tag wrap":                     R(Key("as-w"), rdescript="tag wrap"),
          }

    extras = [
        Dictation("text"),
        Dictation("textnv"),
        Dictation("imported_from"),
        Choice("is_method", {
            "met": 3,
            "ob": 2
            })
        ]

    defaults = {
        "is_method": 2,
        "imported_from": ""
    }
    
    token_set = TokenSet(["abstract", "arguments", "boolean", "break", "byte",
                 "case", "catch", "char", "class", "const", "continue",
                 "debugger", "default", "delete", "do", "double", "else",
                 "enum", "eval", "export", "extends", "false", "final",
                 "finally", "float", "for", "function", "goto", "if",
                 "implements", "import", "in", "instanceof", "int",
                 "interface", "let", "long", "native", "new", "null",
                 "package", "private", "protected", "public", "return",
                 "short", "static", "super", "switch", "synchronized",
                 "this", "throw", "throws", "transient", "true", "try",
                 "typeof", "var", "void", "volatile", "while", "with",
                 "yield"],
                         "//",
                         ["/*", "*/"])


control.nexus().merger.add_global_rule(Javascript(ID=200))
