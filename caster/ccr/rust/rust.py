from dragonfly import Choice, MappingRule

from caster.lib import control, alphanumeric
from caster.lib.actions import Key, Text
from caster.ccr.standard import SymbolSpecs
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class RustNon(MappingRule):
    mapping = {
        "macro format string":
            R(Text("format!()") + Key("left"), rdescript="Rust: Format String"),
        "macro panic":
            R(Text("panic!()") + Key("left"), rdescript="Rust: Panic"),
        "macro assertion":
            R(Text("assert_eq!()") + Key("left"), rdescript="Rust: Assertion"),
        "ternary":
            R(Text("if TOKEN == TOKEN { TOKEN } else { TOKEN }"),
              rdescript="Rust: Ternary"),
        "function [<return>]":
            R(Text("fn TOKEN(TOKEN)%(return)s{}"), rdescript="Rust: Function"),
        "infinite loop":
            R(Text("loop {}") + Key("left"), rdescript="Rust: Infinite Loop"),
    }
    extras = [
        Choice("return", {"return": " -> TOKEN "}),
    ]
    defaults = {"return": " "}


class Rust(MergeRule):
    non = RustNon

    mapping = {
        SymbolSpecs.IF:
            R(Text("if  {}") + Key("left/5:3"), rdescript="Rust: If"),
        SymbolSpecs.ELSE:
            R(Text("else {}") + Key("left/5:3"), rdescript="Rust: Else"),
        #
        SymbolSpecs.SWITCH:
            R(Text("match"), rdescript="Rust: Switch (match)"),
        SymbolSpecs.CASE:
            R(Text(" => ") + Key("left"), rdescript="Rust: Case"),
        SymbolSpecs.BREAK:
            R(Text("break;"), rdescript="Rust: Break"),
        SymbolSpecs.DEFAULT:
            R(Text("_"), rdescript="Rust: Default"),
        #
        SymbolSpecs.DO_LOOP:
            R(Text("while {TOKEN;TOKEN}{}"), rdescript="Rust: Do Loop"),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while TOKEN {}") + Key("left"), rdescript="Rust: While"),
        "for loop [of <a> [in <n>]]":
            R(Text("for %(a)s in 0..%(n)d {}") + Key("left"),
              rdescript="Rust: For i Loop"),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for TOKEN in TOKEN {}") + Key("left"),
              rdescript="Rust: For Each Loop"),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("parse::<i32>().unwrap()"), rdescript="Rust: Convert To Integer"),
        SymbolSpecs.TO_FLOAT:
            R(Text("parse::<f64>().unwrap()"),
              rdescript="Rust: Convert To Floating-Point"),
        SymbolSpecs.TO_STRING:
            R(Text("to_string()"), rdescript="Rust: Convert To String"),
        #
        SymbolSpecs.AND:
            R(Text(" && "), rdescript="Rust: And"),
        SymbolSpecs.OR:
            R(Text(" || "), rdescript="Rust: Or"),
        SymbolSpecs.NOT:
            R(Text("!"), rdescript="Rust: Not"),
        #
        SymbolSpecs.SYSOUT:
            R(Text("println!()") + Key("left"), rdescript="Rust: Print"),
        #
        SymbolSpecs.IMPORT:
            R(Text("use "), rdescript="Rust: Import (use)"),
        #
        # function moved to ncmap
        SymbolSpecs.CLASS:
            R(Text("struct "), rdescript="Rust: Class (struct)"),
        #
        SymbolSpecs.COMMENT:
            R(Text("//"), rdescript="Rust: Add Comment"),
        SymbolSpecs.LONG_COMMENT:
            R(Text("///"), rdescript="Rust: Doc Comment"),
        #
        SymbolSpecs.NULL:
            R(Text("None"), rdescript="Rust: None"),
        #
        SymbolSpecs.RETURN:
            R(Text("return "), rdescript="Rust: Early Return"),
        #
        SymbolSpecs.TRUE:
            R(Text("true"), rdescript="Rust: True"),
        SymbolSpecs.FALSE:
            R(Text("false"), rdescript="Rust: False"),

        # Rust specific
        "value some":
            R(Text("Some()") + Key("left"), rdescript="Rust: Some"),
        "enumerate for loop [of <a> [in <n>]]":
            R(Text("for (%(a)s, TOKEN) in (0..%(n)d).enumerate() {}") + Key("left"),
              rdescript="Rust: Enumerated For i Loop"),
        "enumerate for each [<a> <b>]":
            R(Text("for (%(a)s, %(b)s) in TOKEN.enumerate() {}") + Key("left"),
              rdescript="Rust: Enumerated For Each Loop"),
        "bind [<mutability>]":
            R(Text("let %(mutability)s"), rdescript="Rust: Bind Variable"),
        "of type":
            R(Text(": "), rdescript="Rust: Set Type"),
        "[<signed>] integer [<ibits>]":
            R(Text("%(signed)s%(bits)s "), rdescript="Rust: Integer"),
        "float [<fbits>]":
            R(Text("f%(fbits)s "), rdescript="Rust: Float"),
        "boolean":
            R(Text("bool "), rdescript="Rust: Boolean"),
        "string":
            R(Text("String "), rdescript="Rust: String"),
        "array [of] size <n>":
            R(Text("[TOKEN; %(n)d]"), rdescript="Rust: Array"),
        "macro vector":
            R(Text("vec![]") + Key("left"), rdescript="Rust: Vector"),
        "refer to [<mutability>]":
            R(Text("&%(mutability)s"), rdescript="Rust: Borrow"),
        "lifetime":
            R(Text("'"), rdescript="Rust: Lifetime"),
        "static":
            R(Text("static "), rdescript="Rust: Static"),
        "brace pan":
            R(Key("escape, escape, end, left, enter, enter, up, tab"),
              rdescript="Rust: Expand Curly Braces"),
        "namespace":
            R(Key("colon, colon"), rdescript="Rust: Namespace"),
    }

    extras = [
        Choice("ibits", {
            "eight": "8",
            "sixteen": "16",
            "thirty two": "32",
            "sixty four": "64"
        }),
        Choice("fbits", {
            "thirty two": "32",
            "sixty four": "64"
        }),
        Choice("signed", {"unsigned": "u"}),
        Choice("mutability", {"mute ah | mute": "mut "}),
        IntegerRefST("n", 0, 1000),
        alphanumeric.get_alphabet_choice("a"),
        alphanumeric.get_alphabet_choice("b"),
    ]
    defaults = {"bits": "32", "signed": "i", "mutability": "", "a": "i", "b": "j", "n": 1}


control.nexus().merger.add_global_rule(Rust())
