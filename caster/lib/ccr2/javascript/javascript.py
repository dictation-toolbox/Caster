'''
Created on Sep 2, 2015

@author: synkarius
'''
from dragonfly import Key, Text

from caster.lib import control
from caster.lib.dfplus.additions import SelectiveAction
from caster.lib.dfplus.merge.mergerule import MergeRule, TokenSet
from caster.lib.dfplus.state.short import R


class Javascript(MergeRule):
    auto = [(".js", "javascript")]
        
    mapping = {
        
        # CCR PROGRAMMING STANDARD
        "iffae":                        R(Text("if () {}")+Key("left, enter:2, up"), rdescript="Javascript: If"),
        "shells":                       R(Text("else {}")+Key("left, enter:2, up"), rdescript="Javascript: Else"),
        #
        "switch":                       R(Text("switch() {}")+Key("left, enter:2, up"), rdescript="Javascript: Switch"),
        "case of":                      R(Text("case :")+Key("left"), rdescript="Javascript: Case"),
        "breaker":                      R(Text("break;"), rdescript="Break"),
        "default":                      R(Text("default: "), rdescript="Javascript: Default"),
        #
        "do loop":                      R(Text("do {}")+Key("left, enter:2"), rdescript="Javascript: Do Loop"),
        "while loop":                   R(Text("while ()")+Key("left"), rdescript="Javascript: While"),
        "for loop":                     R(Text("for (var i=0; i<VALUE; i++)"), rdescript="Javascript: For i Loop"),
        "for each":                     R(Text("for (VARIABLE in OBJECT)"), rdescript="Javascript: For Each Loop"), 
        #
        "convert to string":            R(Key("dquote, dquote, plus"), rdescript="Javascript: Convert To String"),
        "convert to integer":           R(Text("parseInt()")+Key("left"), rdescript="Javascript: Convert To Integer"),
        "convert to floating point":    R(Text("parseFloat()")+Key("left"), rdescript="Javascript: Convert To Floating-Point"),
        #
        "lodge and":                    R(Text(" && "), rdescript="Javascript: And"),
        "lodge or":                     R(Text(" || "), rdescript="Javascript: Or"),
        "lodge not":                    R(Text("!"), rdescript="Javascript: Not"),
        #
        "print to console":             R(Text("console.log()")+Key("left"), rdescript="Javascript: Print"),
        #
        # (no imports in javascript)
        # 
        "function":                     R(Text("function NAME() {};")+Key("left:2, enter")
                                     +SelectiveAction(Key("enter, up"), ["AptanaStudio3.exe"]), 
                                     rdescript="Javascript: Function"),
        # (no classes in javascript)
        #
        "add comment":                  R(Text("//"), rdescript="Javascript: Add Comment"),
        "long comment":                 R(Text("/**/")+Key("left,left"), rdescript="Javascript: Long Comment"),
        #
        "value not":                    R(Text("null"), rdescript="Javascript: Null"),
        #
        "return":                       R(Text("return "), rdescript="Javascript: Return"),
        #
        "value true":                   R(Text("true"), rdescript="Javascript: True"),
        "value false":                  R(Text("false"), rdescript="Javascript: False"),
        
        
        # JavaScript specific
        "anon funk":                    R(Text("function () {}")+Key("left:1, enter")
                                     +SelectiveAction(Key("enter, up"), ["AptanaStudio3.exe"]), 
                                     rdescript="Javascript: Anonymous Function"),
        "timer":                        R(Text("setInterval()")+Key("left"), rdescript="Javascript: Timer"),
        "timeout":                      R(Text("setTimeout()")+Key("left"), rdescript="Javascript: Timeout"),
        "sue iffae":                    R(Text("if()")+Key("left"), rdescript="Javascript: Short If"),
        "document":                     R(Text("document"), rdescript="Javascript: Document"),
        "index of":                     R(Text("indexOf()")+Key("left"), rdescript="Javascript: Index Of"),
        "has own property":             R(Text("hasOwnProperty()")+Key("left"), rdescript="Javascript: Has Own Property"),
        "length":                       R(Text("length"), rdescript="Javascript: Length"),
        "self":                         R(Text("self"), rdescript="Javascript: Self"),
        "push":                         R(Text("push"), rdescript="Javascript: Push"),
        "inner HTML":                   R(Text("innerHTML"), rdescript="Javascript: InnerHTML"),
        "new new":                      R(Text("new "), rdescript="Javascript: New"),
        "continue":                     R(Text("continue"), rdescript="Javascript: Continue"),

        "this":                         R(Text("this"), rdescript="Javascript: This"),
        "try":                          R(Text("try {}")+Key("left, enter:2, up"), rdescript="Javascript: Try"),
        "catch":                        R(Text("catch(e) {}")+Key("left, enter:2, up"), rdescript="Javascript: Catch"),
        
        "throw":                        R(Text("throw "), rdescript="Javascript: Throw"),
        "instance of":                  R(Text("instanceof "), rdescript="Javascript: Instance Of"), 
        
        "(far | variable)":             R(Text("var "), rdescript="Javascript: Variable"),
        "sue iffae":                    R(Text("if ()")+Key("left"), rdescript="Javascript: Short If"),
        "sue shells":                   R(Text("else")+Key("enter"), rdescript="Javascript: Short Else"),
         
        "shell iffae":                  R(Text("else if ()")+Key("left"), rdescript="Javascript: Else If"),
       
          }

    extras = []
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
    
    
    
    
    
    
    
    
control.nexus().merger.add_global_rule(Javascript())