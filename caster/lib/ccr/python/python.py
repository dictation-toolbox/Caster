'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import Key, Text, Dictation, MappingRule

from caster.lib import control
from caster.lib.dfplus.merge.mergerule import MergeRule, TokenSet
from caster.lib.dfplus.state.short import R


class PythonNon(MappingRule):
    mapping = {
        "with":                         R(Text("with "), rdescript="Python: With"),
        "open file":                    R(Text("open('filename','r') as f:"), rdescript="Python: Open File"),
        "read lines":                   R(Text("content = f.readlines()"), rdescript="Python: Read Lines"),
        "try catch":                    R(Text("try:")+Key("enter:2/10, backspace")+Text("except Exception:")
                                          +Key("enter"), rdescript="Python: Try Catch"),
        }

class Python(MergeRule):
    auto = [".py"]
    non = PythonNon
    
    mapping = {        
        # CCR PROGRAMMING STANDARD
        #
        "iffae":                        R(Key("i,f,space,colon,left"), rdescript="Python: If"),
        "shells":                       R(Text("else:")+Key("enter"), rdescript="Python: Else"),        
        #
        # (no switch in Python)
        "breaker":                      R(Text("break"), rdescript="Python: Break"),
        #
        "for each":                     R(Text("for  in :")+ Key("left:5"), rdescript="Python: For Each Loop"),
        "for loop":                     R(Text("for i in range(0, ):")+ Key("left:2"), rdescript="Python: For i Loop"),
        "while loop":                   R(Text("while :")+ Key("left"), rdescript="Python: While"),
        # (no do-while in Python)
        #
        "convert to string":            R(Text("str()")+ Key("left"), rdescript="Python: Convert To String"),
        "convert to integer":           R(Text("int()")+ Key("left"), rdescript="Python: Convert To Integer"),
        "convert to floating point":    R(Text("float()")+ Key("left"), rdescript="Python: Convert To Floating-Point"),
        #
        "lodge and":                    R(Text(" and "), rdescript="Python: And"),
        "lodge or":                     R(Text(" or "), rdescript="Python: Or"),
        "lodge not":                    R(Text("!"), rdescript="Python: Not"),
        #
        "print to console":             R(Text("print()")+Key("left"), rdescript="Python: Print"),
        #
        "import":                       R(Text( "import " ), rdescript="Python: Import"),
        #
        "function":                     R(Text("def "), rdescript="Python: Function"),        
        "class":                        R(Text("class "), rdescript="Python: Class"),
        #
        "add comment":                  R(Text( "#" ), rdescript="Python: Add Comment"),
        "long comment":                 R(Text("''''''") + Key("left:3"), rdescript="Python: Long Comment"),
        #                
        "value not":                    R(Text("None"), rdescript="Python: Null"),
        #
        "return":                       R(Text("return "), rdescript="Python: Return"),
        #
        "value true":                   R(Text("True"), rdescript="Python: True"),
        "value false":                  R(Text("False"), rdescript="Python: False"),
                
         
        # Python specific           
         
        "sue iffae":                    R(Text("if "), rdescript="Python: Short If"), 
        "sue shells":                   R(Text("else "), rdescript="Python: Short Else"),
          
         
        "from":                         R(Text( "from " ), rdescript="Python: From"),
        "self":                         R(Text("self"), rdescript="Python: Self"),
        "long not":                     R(Text(" not "), rdescript="Python: Long Not"),
        "it are in":                    R(Text(" in "), rdescript="Python: In"),          #supposed to sound like "iter in"
        
        "shell iffae | LFA":            R(Key("e,l,i,f,space,colon,left"), rdescript="Python: Else If"),
        "convert to character":         R(Text("chr()")+ Key("left"), rdescript="Python: Convert To Character"),
        "length of":                    R(Text("len()")+ Key("left"), rdescript="Python: Length"),
         
        "global":                       R(Text("global "), rdescript="Python: Global"),
                        
        "make assertion":               R(Text("assert "), rdescript="Python: Assert"),
        "list comprehension":           R(Text("[x for x in LIST if CONDITION]"), rdescript="Python: List Comprehension"),
       
        "[dot] (pie | pi)":             R(Text(".py"), rdescript="Python: .py"),
        "jason":                        R(Text("json"), rdescript="Python: json"),
          
         
        }

    extras   = [Dictation("text"),]
    defaults = {}
    
    token_set = TokenSet(["and", "del", "from", "not", "while", "as", "elif",
                 "global", "or", "with", "assert", "else", "if", "pass",
                 "yield", "break", "except", "import", "print", "class",
                 "exec", "in", "raise", "continue", "finally", "is",
                 "return", "def", "for", "lambda", "try"], 
                         "#", 
                         ["'''", '"""'])

control.nexus().merger.add_global_rule(Python(ID=100))