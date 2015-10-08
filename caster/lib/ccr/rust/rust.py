from dragonfly import Key, Text, Choice, MappingRule

from caster.lib import navigation
from caster.lib import control
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class RustNon(MappingRule):
    mapping = {
        "macro format string":        R(Text("format!()")+Key("left"), rdescript="Rust: Format String"), 
        "macro panic":                R(Text("panic!()")+Key("left"), rdescript="Rust: Panic"),
        "macro assertion":            R(Text("assert_eq!()")+Key("left"), rdescript="Rust: Assertion"),
        "ternary":                    R(Text("if NAME == VALUE { VALUE } else { VALUE }"), rdescript="Rust: Ternary"),
        "function [<return>]":        R(Text("fn NAME(VALUE)%(return)s{}"),  rdescript="Rust: Function"),
        "infinite loop":              R(Text("loop {}")+Key("left"), rdescript="Rust: Infinite Loop"), 
         
        }
    extras   = [
           Choice("return", {"return": " -> TYPE "}),
        ]
    defaults = {
             "return": " "
        }

class Rust(MergeRule):
    auto = [".rs"]
    non = RustNon
    
    mapping = {
        # CCR PROGRAMMING STANDARD
        "iffae":                        R(Text("if  {}")+Key("left/5:3"), rdescript="Rust: If"),
        "shells":                       R(Text("else {}")+Key("left/5:3"), rdescript="Rust: Else"),
        #
        "switch":                       R(Text("match"), rdescript="Rust: Switch (match)"),
        "case of":                      R(Text(" => ")+Key("left"), rdescript="Rust: Case"),
        "breaker":                      R(Text("break;"), rdescript="Rust: Break"),
        "default":                      R(Text("_"), rdescript="Rust: Default"),
        #
        "do loop":                      R(Text("while {EXPRESSION;VALUE}{}"), rdescript="Rust: Do Loop"),
        "while loop":                   R(Text("while VALUE {}")+Key("left"), rdescript="Rust: While"),
        "for loop [of <a> [in <n>]]":   R(Text("for %(a)s in 0..%(n)d {}")+Key("left"), rdescript="Rust: For i Loop"),
        "for each":                     R(Text("for NAME in VALUE {}")+Key("left"), rdescript="Rust: For Each Loop"), 
        #
        "convert to string":            R(Text("to_string()"), rdescript="Rust: Convert To String"),
        "convert to integer":           R(Text("parse::<i32>().unwrap()"), rdescript="Rust: Convert To Integer"),
        "convert to floating point":    R(Text("parse::<f64>().unwrap()"), rdescript="Rust: Convert To Floating-Point"),
        #
        "lodge and":                    R(Text(" && "), rdescript="Rust: And"),
        "lodge or":                     R(Text(" || "), rdescript="Rust: Or"),
        "lodge not":                    R(Text("!"), rdescript="Rust: Not"),
        #
        "print to console":             R(Text("println!()")+Key("left"), rdescript="Rust: Print"),
        #
        "import":                       R(Text("use "), rdescript="Rust: Import (use)"), 
        # 
        # function moved to ncmap
        "class":                        R(Text("struct "), rdescript="Rust: Class (struct)"), 
        #
        "add comment":                  R(Text("//"), rdescript="Rust: Add Comment"),
        "doc comment":                  R(Text("///"), rdescript="Rust: Doc Comment"),
        #
        "value not":                    R(Text("None"), rdescript="Rust: None"),
        #
        "return":                       R(Text("return "), rdescript="Rust: Early Return"),
        #
        "value true":                   R(Text("true"), rdescript="Rust: True"),
        "value false":                  R(Text("false"), rdescript="Rust: False"),
        
        
        # Rust specific
        "value some":                   R(Text("Some()")+Key("left"), rdescript="Rust: Some"),
        
        "enumerate for loop [of <a> [in <n>]]": R(Text("for (%(a)s, NAME) in (0..%(n)d).enumerate() {}")+Key("left"), rdescript="Rust: Enumerated For i Loop"),
        "enumerate for each [<a> <b>]":         R(Text("for (%(a)s, %(b)s) in VALUE.enumerate() {}")+Key("left"), rdescript="Rust: Enumerated For Each Loop"),
                
        "bind [<mutability>]":          R(Text("let %(mutability)s"), rdescript="Rust: Bind Variable"),
        "of type":                      R(Text(": "), rdescript="Rust: Set Type"), 
        "[<signed>] integer [<ibits>]": R(Text("%(signed)s%(bits)s "), rdescript="Rust: Integer"),
        "float [<fbits>]":              R(Text("f%(fbits)s "), rdescript="Rust: Float"), 
        "boolean":                      R(Text("bool "), rdescript="Rust: Boolean"), 
        "string":                       R(Text("String "), rdescript="Rust: String"),
        "array [of] size <n>":          R(Text("[TYPE; %(n)d]"), rdescript="Rust: Array"), 
        "macro vector":                 R(Text("vec![]")+Key("left"), rdescript="Rust: Vector"),
        
        "refer to [<mutability>]":      R(Text("&%(mutability)s"), rdescript="Rust: Borrow"),
        "lifetime":                     R(Text("'"), rdescript="Rust: Lifetime"), 
        "static":                       R(Text("static "), rdescript="Rust: Static"), 
        
        "brace pan":                    R(Key("escape, escape, end, left, enter, enter, up, tab"), rdescript="Rust: Expand Curly Braces"),
        "namespace":                    R(Key("colon, colon"), rdescript="Rust: Namespace"), 
       
          }

    extras   = [
            Choice("ibits", {"eight": "8", "sixteen": "16", "thirty two": "32", "sixty four": "64"}), 
            Choice("fbits", {"thirty two": "32", "sixty four": "64"}),
            Choice("signed", {"unsigned": "u"}), 
            Choice("mutability", {"mute ah | mute": "mut "}), 
            IntegerRefST("n", 0, 1000), 
            navigation.get_alphabet_choice("a"), 
            navigation.get_alphabet_choice("b"),
           ]
    defaults = {
            "bits": "32", "signed": "i", "mutability": "", "a": "i", "b": "j", "n": 1
           }

control.nexus().merger.add_global_rule(Rust())