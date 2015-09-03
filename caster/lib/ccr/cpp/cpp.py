'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import Key, Mimic, Text

from caster.lib.dfplus.mergerule import MergeRule, TokenSet
from caster.lib.dfplus.state.short import R


class CPP(MergeRule):
    auto = [(".h", "c++"), (".cpp", "c++")]
    pronunciation = "C plus plus"
    TOKEN_SET = TokenSet(["alignas", "alignof", "and", "and_eq", "asm", "auto", 
                "bitand", "bitor", "bool", "break", "case", "catch", 
                "char", "char16_t", "char32_t", "class", "compl", 
                "concept", "const", "constexpr", "const_cast", "continue", 
                "decltype", "default", "delete", "do", "double", 
                "dynamic_cast", "else", "enum", "explicit", "export", 
                "extern", "false", "float", "for", "friend", "goto", "if", 
                "inline", "int", "long", "mutable", "namespace", "new", 
                "noexcept", "not", "not_eq", "nullptr", "operator", "or", 
                "or_eq", "private", "protected", "public", "register", 
                "reinterpret_cast", "requires", "return", "short", "signed", 
                "sizeof", "static", "static_assert", "static_cast", "struct", 
                "switch", "template", "this", "thread_local", "throw", "true", 
                "try", "typedef", "typeid", "typename", "union", "unsigned", 
                "using", "virtual", "void", "volatile", "wchar_t", "while", 
                "xor", "xor_eq"   ], 
                         "//", 
                         ["/*", "*/"])
    
    mapping = {
        # CCR PROGRAMMING STANDARD
        "iffae":                            R(Key("i, f, lparen, rparen, leftbrace, enter,up,left"), rdescript="C++: If"),
        "shells":                           R(Key("e, l, s, e, leftbrace, enter"), rdescript="C++: Else"),
        #
        "switch":                           R(Text("switch(){\ncase : break;\ndefault: break;")+Key("up,up,left,left"), rdescript="C++: Switch"),
        "case of":                          R(Text("case :")+Key("left"), rdescript="C++: Case"),
        "breaker":                          R(Text("break;"), rdescript="C++: Break"),
        "default":                          R(Text("default: "), rdescript="C++: Default"),
        #
        "do loop":                          R(Text("do {}")+Key("left, enter:2"), rdescript="C++: Do Loop"),
        "while loop":                       R(Text("while ()")+Key("left"), rdescript="C++: While"),
        "for loop":                         R(Text("for (int i=0; i<VALUE; i++)"), rdescript="C++: For i Loop"),
        "for each":                         R(Text("for_each (VALUE, VALUE, FUNCTION);"), rdescript="C++: For Each Loop"),
        #
        "convert to integer":               R(Text("(int)"), rdescript="C++: Convert To Integer"),
        "convert to floating point":        R(Text("(double)"), rdescript="C++: Convert To Floating-Point"),
        "convert to string":                R(Text("std::to_string()")+Key("left"), rdescript="C++: Convert To String"),
        #
        "lodge and":                        R(Text("&&"), rdescript="C++: And"),
        "lodge or":                         R(Text("||"), rdescript="C++: Or"),
        "lodge not":                        R(Text("!"), rdescript="Not"),
        #
        "print to console":                 R(Text("cout <<"), rdescript="C++: Print"),
        #
        "import":                           R(Text("#include"), rdescript="C++: Import"),
        #
        "function":                         R(Text("TYPE NAME(){}")+Key("left"), rdescript="C++: Function"),
        "class":                            R(Text("class NAME{}")+Key("left"), rdescript="C++: Class"),
        #
        "add comment":                      R(Text( "//" ), rdescript="C++: Add Comment"),
        "long comment":                     R(Text("/**/")+Key("left, left"), rdescript="C++: Long Comment"),
        #
        "value not":                        R(Text("null"), rdescript="C++: Null Value"),
        #
        "return":                           R(Text("return"), rdescript="C++: Return"),
        #
        "value true":                       R(Text("true"), rdescript="C++: True"),
        "value false":                      R(Text("false"), rdescript="C++: False"),
        
        
        # C++ specific
        
        "public":                           R(Text("public "), rdescript="C++: Public"),
        "private":                          R(Text("private "), rdescript="C++: Private"),
        "static":                           R(Text("static "), rdescript="C++: Static"),
        "final":                            R(Text("final "), rdescript="C++: Final"),
        
        "static cast integer":              R(Text("static_cast<int>()") + Key("left"), rdescript="C++: Static Cast Integer"),
        "static cast double":               R(Text("static_cast<double>()") + Key("left"), rdescript="C++: Static Cast Double"),
        
        "([global] scope | name)":          R(Text("::"), rdescript="C++: ::"),
        "Vic":                              R(Text("vector"), rdescript="C++: Vector"),
        "pushback":                         R(Text("push_back"), rdescript="C++: Pushback"),
        
        "standard":                         R(Text("std"), rdescript="C++: Standard"),
        "constant":                         R(Text("const"), rdescript="C++: Constant"),
        "array":                            R(Mimic("brackets"), rdescript="C++: Array"),
        
        #http://www.learncpp.com/cpp-tutorial/67-introduction-to-pointers/
        "(reference to | address of)":      R(Text("&"), rdescript="C++: Reference"),
        "(pointer | D reference)":          R(Text("*"), rdescript="C++: Dereference"),
        "member":                           R(Text("->"), rdescript="C++: Member"),
        
                
        "new new":                          R(Text("new "), rdescript="C++: New"),
        "integer":                          R(Text("int "), rdescript="C++: Integer"),
        "double":                           R(Text("double "), rdescript="C++: Double"),
        "character":                        R(Text("char "), rdescript="C++: Character"),
        "big integer":                      R(Text("Integer"), rdescript="C++: Big Integer"),
        "string":                           R(Text("string "), rdescript="C++: String"),
        
        "ternary":                          R(Text("()?;") + (Key("left") * 3), rdescript="C++: Ternary"),
    }

    extras   = []
    defaults = {}