'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import Key, Mimic, Text

from caster.lib import control
from caster.lib.ccr.standard import SymbolSpecs
from caster.lib.dfplus.merge.mergerule import MergeRule, TokenSet
from caster.lib.dfplus.state.short import R


class CPP(MergeRule):
    auto = [".h",".cpp"]
    pronunciation = "C plus plus"
        
    mapping = {
        SymbolSpecs.IF:                     R(Key("i, f, lparen, rparen, leftbrace, enter,up,left"), rdescript="C++: If"),
        SymbolSpecs.ELSE:                   R(Key("e, l, s, e, leftbrace, enter"), rdescript="C++: Else"),
        #
        SymbolSpecs.SWITCH:                 R(Text("switch(){\ncase : break;\ndefault: break;")+Key("up,up,left,left"), rdescript="C++: Switch"),
        SymbolSpecs.CASE:                   R(Text("case :")+Key("left"), rdescript="C++: Case"),
        SymbolSpecs.BREAK:                  R(Text("break;"), rdescript="C++: Break"),
        SymbolSpecs.DEFAULT:                R(Text("default: "), rdescript="C++: Default"),
        #
        SymbolSpecs.DO_LOOP:                R(Text("do {}")+Key("left, enter:2"), rdescript="C++: Do Loop"),
        SymbolSpecs.WHILE_LOOP:             R(Text("while ()")+Key("left"), rdescript="C++: While"),
        SymbolSpecs.FOR_LOOP:               R(Text("for (int i=0; i<TOKEN; i++)"), rdescript="C++: For i Loop"),
        SymbolSpecs.FOR_EACH_LOOP:          R(Text("for_each (TOKEN, TOKEN, TOKEN);"), rdescript="C++: For Each Loop"),
        #
        SymbolSpecs.TO_INTEGER:             R(Text("(int)"), rdescript="C++: Convert To Integer"),
        SymbolSpecs.TO_FLOAT:               R(Text("(double)"), rdescript="C++: Convert To Floating-Point"),
        SymbolSpecs.TO_STRING:              R(Text("std::to_string()")+Key("left"), rdescript="C++: Convert To String"),
        #
        SymbolSpecs.AND:                    R(Text("&&"), rdescript="C++: And"),
        SymbolSpecs.OR:                     R(Text("||"), rdescript="C++: Or"),
        SymbolSpecs.NOT:                    R(Text("!"), rdescript="Not"),
        #
        SymbolSpecs.SYSOUT:                 R(Text("cout <<"), rdescript="C++: Print"),
        #
        SymbolSpecs.IMPORT:                 R(Text("#include"), rdescript="C++: Import"),
        #
        SymbolSpecs.FUNCTION:               R(Text("TOKEN TOKEN(){}")+Key("left"), rdescript="C++: Function"),
        SymbolSpecs.CLASS:                  R(Text("class TOKEN{}")+Key("left"), rdescript="C++: Class"),
        #
        SymbolSpecs.COMMENT:                R(Text( "//" ), rdescript="C++: Add Comment"),
        SymbolSpecs.LONG_COMMENT:           R(Text("/**/")+Key("left, left"), rdescript="C++: Long Comment"),
        #
        SymbolSpecs.NULL:                   R(Text("null"), rdescript="C++: Null Value"),
        #
        SymbolSpecs.RETURN:                 R(Text("return"), rdescript="C++: Return"),
        #
        SymbolSpecs.TRUE:                   R(Text("true"), rdescript="C++: True"),
        SymbolSpecs.FALSE:                  R(Text("false"), rdescript="C++: False"),
        
        
        # C++ specific
        "static cast integer":              R(Text("static_cast<int>()") + Key("left"), rdescript="C++: Static Cast Integer"),
        "static cast double":               R(Text("static_cast<double>()") + Key("left"), rdescript="C++: Static Cast Double"),
        
        "(scope | lee)":                    R(Text("::"), rdescript="C++: ::"),
        "stead":                            R(Text("std"), rdescript="standard namespace"),
        "steadily":                         R(Text("std::"), rdescript="standard namespace"),

        "Vic":                              R(Text("vector"), rdescript="C++: Vector"),
        "pushback":                         R(Text("push_back"), rdescript="C++: Pushback"),
        
        "standard":                         R(Text("std"), rdescript="C++: Standard"),
        "constant":                         R(Text("const"), rdescript="C++: Constant"),
        "array":                            R(Mimic("brackets"), rdescript="C++: Array"),
        
        "(reference to | address of)":      R(Text("&"), rdescript="C++: Reference"),
        "(pointer | point)":                R(Text("*"), rdescript="C++: Pointer"),
        "(D reference | D ref)":            R(Text("->"), rdescript="C++: Arrow dereference"),
                
        "new new":                          R(Text("new "), rdescript="C++: New"),
        "integer":                          R(Text("int "), rdescript="C++: Integer"),
        "double":                           R(Text("double "), rdescript="C++: Double"),
        "character":                        R(Text("char "), rdescript="C++: Character"),
        "big int":                          R(Text("Integer"), rdescript="C++: Big Integer"),
        "string":                           R(Text("string"), rdescript="C++: String"),

        "stir":                             R(Text("str()"), rdescript="C++: str()"),
        
        "ternary":                          R(Text("()?;") + (Key("left") * 3), rdescript="C++: Ternary"),
        
        "put to":                           R(Text(" << "), rdescript="put to operator"),
        "get from":                         R(Text(" >> "), rdescript="get from operator"),
    }

    extras   = []
    defaults = {}
    
    token_set = TokenSet(["alignas", "alignof", "and", "and_eq", "asm", "auto", 
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

control.nexus().merger.add_global_rule(CPP())