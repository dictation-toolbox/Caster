'''
Created on Sep 26, 2015

@author: synkarius
'''

from dragonfly import Key, Mimic, Text

from caster.lib import control
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

class CSharp(MergeRule):
    auto = [".cs", ".cshtml"]
    pronunciation = "C sharp"
        
    mapping = {
        # CCR PROGRAMMING STANDARD
        "iffae":                            R(Key("i, f, lparen, rparen, leftbrace, enter,up,left"), rdescript="C#: If"),
        "shells":                           R(Key("e, l, s, e, leftbrace, enter"), rdescript="C#: Else"),
        #
        "switch":                           R(Text("switch(){\ncase : break;\ndefault: break;")+Key("up,up,left,left"), rdescript="C#: Switch"),
        "K states":                         R(Text("case :")+Key("left"), rdescript="C#: Case"),
        "breaker":                          R(Text("break;"), rdescript="C#: Break"),
        "default":                          R(Text("default: "), rdescript="C#: Default"),
        #
        "do loop":                          R(Text("do {}")+Key("left, enter:2"), rdescript="C#: Do Loop"),
        "while loop":                       R(Text("while ()")+Key("left"), rdescript="C#: While"),
        "for loop":                         R(Text("for (int i=0; i<VALUE; i++)"), rdescript="C#: For i Loop"),
        "for each":                         R(Text("foreach (VALUE in Collection)"), rdescript="C#: For Each Loop"),
        #
        "convert to integer":               R(Text("Convert.ToInt32()")+Key("left"), rdescript="C#: Convert To Integer"),
        "convert to floating point":        R(Text("Convert.ToDouble()")+Key("left"), rdescript="C#: Convert To Floating-Point"),
        "convert to string":                R(Text("Convert.ToString()")+Key("left"), rdescript="C#: Convert To String"),
        #
        "lodge and":                        R(Text("&&"), rdescript="C#: And"),
        "lodge or":                         R(Text("||"), rdescript="C#: Or"),
        "lodge not":                        R(Text("!"), rdescript="C# Not"),
        #
        "print to console":                 R(Text("Console.WriteLine()")+ Key("left"), rdescript="C#: Print"),
        
        #
        "function":                         R(Text("TYPE NAME(){}")+Key("left"), rdescript="C#: Function"),
        "class":                            R(Text("class NAME{}")+Key("left"), rdescript="C#: Class"),
       #
        
        "add comment":                      R(Text( "//" ), rdescript="C#: Add Comment"),
        "long comment":                     R(Text("/**/")+Key("left, left"), rdescript="C#: Long Comment"),
        #
        "value not":                        R(Text("null"), rdescript="C#: Null Value"),
        #
        "return":                           R(Text("return"), rdescript="C#: Return"),
        #
        "value true":                       R(Text("true"), rdescript="C#: True"),
        "value false":                      R(Text("false"), rdescript="C#: False"),
        
        
        # C# specific
        
        "using":                            R(Text("using"), rdescript="C#: Using"),      
        "enum":                             R(Text("enum NAME {}")+Key("left"), rdescript="C#: Enum"),   
        "struct":                           R(Text("struct NAME {}")+Key("left"), rdescript="C#: Struct"),
        "interface":                        R(Text("interface NAME {}")+Key("left"), rdescript="C#: Struct"),
        
        "public":                           R(Text("public "), rdescript="C#: Public"),
        "private":                          R(Text("private "), rdescript="C#: Private"),
        "static":                           R(Text("static "), rdescript="C#: Static"),
        "internal":                         R(Text("internal "), rdescript="C#: Internal"),        
        
        "cast integer":                     R(Text("(int)") + Key("left"), rdescript="C#:  Cast Integer"),
        "cast double":                      R(Text("(double)") + Key("left"), rdescript="C#: Cast Double"),
        
        "constant":                         R(Text("const"), rdescript="C#: Constant"),
        "array":                            R(Mimic("brackets"), rdescript="C#: Array"),
        "list":                             R(Text("List<>")+Key("left"), rdescript="C# List"),
        "var":                              R(Text("var NAME = TYPE;"), rdescript="C# variable"),
        "(lambda|goes to)":                 R(Text("->"), rdescript="C#: lambda"),
        
        
                
        "new new":                          R(Text("new "), rdescript="C#: New"),
        "integer":                          R(Text("int "), rdescript="C#: Integer"),
        "double":                           R(Text("double "), rdescript="C#: Double"),
        "character":                        R(Text("char "), rdescript="C#: Character"),
        "big integer":                      R(Text("Integer"), rdescript="C#: Big Integer"),
        "string":                           R(Text("string "), rdescript="C#: String"),
        
        "ternary":                          R(Text("()?t:f") + (Key("left") * 5), rdescript="C#: Ternary"),
    }

    extras   = []
    defaults = {}


control.nexus().merger.add_global_rule(CSharp())