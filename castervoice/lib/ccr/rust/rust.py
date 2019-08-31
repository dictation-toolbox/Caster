from castervoice.lib.imports import *


class RustNon(MappingRule):
    mapping = {
        "macro format string": R(Text("format!()") + Key("left")),
        "macro panic": R(Text("panic!()") + Key("left")),
        "macro assertion": R(Text("assert_eq!()") + Key("left")),
        "ternary": R(Text("if TOKEN == TOKEN { TOKEN } else { TOKEN }")),
        "function [<return>]": R(Text("fn TOKEN(TOKEN)%(return)s{}")),
        "infinite loop": R(Text("loop {}") + Key("left")),
    }
    extras = [
        Choice("return", {"return": " -> TOKEN "}),
    ]
    defaults = {"return": " "}


class Rust(MergeRule):
    non = RustNon

    mapping = {
        SymbolSpecs.IF:
            R(Text("if  {}") + Key("left/5:3")),
        SymbolSpecs.ELSE:
            R(Text("else {}") + Key("left/5:3")),
        #
        SymbolSpecs.SWITCH:
            R(Text("match")),
        SymbolSpecs.CASE:
            R(Text(" => ") + Key("left")),
        SymbolSpecs.BREAK:
            R(Text("break;")),
        SymbolSpecs.DEFAULT:
            R(Text("_")),
        #
        SymbolSpecs.DO_LOOP:
            R(Text("while {TOKEN;TOKEN}{}")),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while TOKEN {}") + Key("left")),
        "for loop [of <a> [in <n>]]":
            R(Text("for %(a)s in 0..%(n)d {}") + Key("left")),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for TOKEN in TOKEN {}") + Key("left")),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("parse::<i32>().unwrap()")),
        SymbolSpecs.TO_FLOAT:
            R(Text("parse::<f64>().unwrap()")),
        SymbolSpecs.TO_STRING:
            R(Text("to_string()")),
        #
        SymbolSpecs.AND:
            R(Text(" && ")),
        SymbolSpecs.OR:
            R(Text(" || ")),
        SymbolSpecs.NOT:
            R(Text("!")),
        #
        SymbolSpecs.SYSOUT:
            R(Text("println!()") + Key("left")),
        #
        SymbolSpecs.IMPORT:
            R(Text("use ")),
        #
        # function moved to ncmap
        SymbolSpecs.CLASS:
            R(Text("struct ")),
        #
        SymbolSpecs.COMMENT:
            R(Text("//")),
        SymbolSpecs.LONG_COMMENT:
            R(Text("///")),
        #
        SymbolSpecs.NULL:
            R(Text("None")),
        #
        SymbolSpecs.RETURN:
            R(Text("return ")),
        #
        SymbolSpecs.TRUE:
            R(Text("true")),
        SymbolSpecs.FALSE:
            R(Text("false")),

        # Rust specific
        "value some":
            R(Text("Some()") + Key("left")),
        "enumerate for loop [of <a> [in <n>]]":
            R(Text("for (%(a)s, TOKEN) in (0..%(n)d).enumerate() {}") + Key("left")),
        "enumerate for each [<a> <b>]":
            R(Text("for (%(a)s, %(b)s) in TOKEN.enumerate() {}") + Key("left")),
        "bind [<mutability>]":
            R(Text("let %(mutability)s")),
        "of type":
            R(Text(": ")),
        "[<signed>] integer [<ibits>]":
            R(Text("%(signed)s%(bits)s ")),
        "float [<fbits>]":
            R(Text("f%(fbits)s ")),
        "boolean":
            R(Text("bool ")),
        "string":
            R(Text("String ")),
        "array [of] size <n>":
            R(Text("[TOKEN; %(n)d]")),
        "macro vector":
            R(Text("vec![]") + Key("left")),
        "refer to [<mutability>]":
            R(Text("&%(mutability)s")),
        "lifetime":
            R(Text("'")),
        "static":
            R(Text("static ")),
        "brace pan":
            R(Key("escape, escape, end, left, enter, enter, up, tab")),
        "name space":
            R(Key("colon, colon")),
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


control.global_rule(Rust())
