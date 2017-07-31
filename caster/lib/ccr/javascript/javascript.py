'''
Created on Sep 2, 2015

@author: synkarius
'''
from dragonfly import Key, Text, Dictation

from caster.lib import control
from caster.lib.ccr.standard import SymbolSpecs
from caster.lib.dfplus.additions import SelectiveAction
from caster.lib.dfplus.merge.mergerule import MergeRule, TokenSet
from caster.lib.dfplus.state.short import R


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
        SymbolSpecs.SYSOUT:             R(Text("console.log()") + Key("left"), rdescript="Javascript: Print"),
        #
        # (no imports in javascript)
        # 
        SymbolSpecs.FUNCTION:           R(Text("function () {};") + Key("left:6, enter"), rdescript="Javascript: Function"),
        # TODO: add classes
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
        "timer":                        R(Text("setInterval") + Key("lbrace"), rdescript="Javascript: Timer"),
        "timeout":                      R(Text("setTimeout") + Key("lbrace"), rdescript="Javascript: Timeout"),
        "document":                     R(Text("document"), rdescript="Javascript: Document"),
        "index of":                     R(Text("indexOf") + Key("lbrace"), rdescript="Javascript: Index Of"),
        "has own property":             R(Text("hasOwnProperty") + Key("lbrace"), rdescript="Javascript: Has Own Property"),
        "length":                       R(Text("length"), rdescript="Javascript: Length"),
        "self":                         R(Text("self"), rdescript="Javascript: Self"),
        "push":                         R(Text("push"), rdescript="Javascript: Push"),
        "inner HTML":                   R(Text("innerHTML"), rdescript="Javascript: InnerHTML"),
        "new new":                      R(Text("new "), rdescript="Javascript: New"),
        "continue":                     R(Text("continue"), rdescript="Javascript: Continue"),

        "this":                         R(Text("this"), rdescript="Javascript: This"),
        "try":                          R(Text("try ") + Key("lbrace, enter"), rdescript="Javascript: Try"),
        "catch":                        R(Text("catch(e) ") + Key("lbrace, enter"), rdescript="Javascript: Catch"),
        
        "throw":                        R(Text("throw "), rdescript="Javascript: Throw"),
        "instance of":                  R(Text("instanceof "), rdescript="Javascript: Instance Of"),
        
        "(far | variable)":             R(Text("var "), rdescript="Javascript: Variable"),

        #ES6 stuff
        "(cons | const)":               R(Text("const "), rdescript="es6 const"),
        "lambda funk":                  R(Text("() => ") + Key("left:5"), rdescript="es6 arrow function"),
        "lambda funk <text>":           R(Key("lparen") + Text("%(text)s")
                                            + Key("rparen") + Text(" => ") + Key("end"),
                                            rdescript="es6 arrow func w/ arg"),

        # React stuff
        "my props":                     R(Text("this.props."), rdescript="React props"),
        "my state":                     R(Text("this.state."), rdescript="React state"),
        "set state":                    R(Text("this.setState") + Key("lparen, lbrace"), rdescript="React setState"),
          }

    extras = [Dictation("text"),]
    defaults = {}
    
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
