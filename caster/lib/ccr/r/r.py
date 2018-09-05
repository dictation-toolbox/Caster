'''
Created on May 23, 2017

@author: shippy
'''

from dragonfly import Key, Text, Dictation, MappingRule

from caster.lib import control
from caster.lib.ccr.standard import SymbolSpecs
from caster.lib.dfplus.merge.mergerule import MergeRule, TokenSet
from caster.lib.dfplus.state.short import R


class RlangNon(MappingRule):
    mapping = {
        "options":
            R(Text("options") + Key("lparen, rparen, left"), rdescript="Rlang: Options"),
    }


class Rlang(MergeRule):
    auto = [".R", ".r"]
    pronunciation = "are"
    non = RlangNon

    mapping = {
        SymbolSpecs.IF:
            R(Text("if ()") + Key("left"), rdescript="Rlang: If"),
        SymbolSpecs.ELSE:
            R(Text("else ") + Key("enter"), rdescript="Rlang: Else"),
        #
        # (no switch in Rlang)
        SymbolSpecs.BREAK:
            R(Text("break"), rdescript="Rlang: Break"),
        #
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for ( in ):") + Key("left:6"), rdescript="Rlang: For Each Loop"),
        SymbolSpecs.FOR_LOOP:
            R(Text("for (i in 1:)") + Key("left"), rdescript="Rlang: For i Loop"),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while ()") + Key("left"), rdescript="Rlang: While"),
        # (no do-while in Rlang)
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("as.numeric()") + Key("left"), rdescript="Rlang: Convert To Integer"),
        SymbolSpecs.TO_FLOAT:
            R(Text("as.double()") + Key("left"),
              rdescript="Rlang: Convert To Floating-Point"),
        SymbolSpecs.TO_STRING:
            R(Text("as.character()") + Key("left"), rdescript="Rlang: Convert To String"),
        #
        SymbolSpecs.AND:
            R(Text(" && "), rdescript="Rlang: And"),
        SymbolSpecs.OR:
            R(Text(" || "), rdescript="Rlang: Or"),
        SymbolSpecs.NOT:
            R(Text("!"), rdescript="Rlang: Not"),
        #
        SymbolSpecs.SYSOUT:
            R(Text("print()") + Key("left"), rdescript="Rlang: Print"),
        #
        SymbolSpecs.IMPORT:
            R(Text("library()") + Key("left"), rdescript="Rlang: Import"),
        #
        SymbolSpecs.FUNCTION:
            R(Text("function()") + Key("left"), rdescript="Rlang: Function"),
        # SymbolSpecs.CLASS:          R(Text("setClass()") + Key("left"), rdescript="Rlang: Class"),
        #
        SymbolSpecs.COMMENT:
            R(Text("#"), rdescript="Rlang: Add Comment"),
        SymbolSpecs.LONG_COMMENT:
            R(Text('""') + Key("left"), rdescript="Rlang: Long Comment"),
        #
        SymbolSpecs.NULL:
            R(Text("NULL"), rdescript="Rlang: Null"),
        #
        SymbolSpecs.RETURN:
            R(Text("return()") + Key("left"), rdescript="Rlang: Return"),
        #
        SymbolSpecs.TRUE:
            R(Text("TRUE"), rdescript="Rlang: True"),
        SymbolSpecs.FALSE:
            R(Text("FALSE"), rdescript="Rlang: False"),

        # Rlang specific
        "assign":
            R(Text(" <- "), rdescript="Rlang: Assignment"),
        "contained in":
            R(Key('space, percent, i, n, percent, space'),
              rdescript="Rlang: In operator"),
        "slurp | magic con":
            R(Key('space, percent, rangle, percent, space'), rdescript="Rlang: Pipe"),
        "NA":
            R(Text("NA"), rdescript="Rlang: Not Available"),
        "shell iffae | LFA":
            R(Text("elseif ()") + Key("left"), rdescript="Rlang: Else If"),
        "length of":
            R(Text("length()") + Key("left"), rdescript="Rlang: Length"),
        "names of":
            R(Text("names()") + Key("left"), rdescript="Rlang: Names"),
        "head of":
            R(Text("head()") + Key("left"), rdescript="Rlang: Head"),
        "paste of":
            R(Text("paste0()") + Key("left"), rdescript="Rlang: Paste"),
        "convert to factor":
            R(Text("as.factor()") + Key("left"), rdescript="Rlang: Convert to factor"),
        "vector of":
            R(Text("c()") + Key("left"), rdescript="Rlang: Vector"),
        "list of":
            R(Text("list()") + Key("left"), rdescript="Rlang: List"),
        "list index of":
            R(Text("[[]]") + Key("left:2"), rdescript="Rlang: List index"),
        "name index of":
            R(Text("$"), rdescript="Rlang: Name index"),
        "index":
            R(Text("[]") + Key("left"), rdescript="Rlang: Index"),
        # "[dot] (our)":              R(Text(".R"), rdescript="Rlang: .py"),
        "see as vee":
            R(Text("csv"), rdescript="Rlang: csv"),
        "gee plot":
            R(Text("ggplot"), rdescript="Rlang: ggplot"),
        "gee aesthetics":
            R(Text("aes()") + Key('left'), rdescript="Rlang: ggplot::aes"),
        "gee theme":
            R(Text("theme()") + Key('left'), rdescript="Rlang: ggplot::aes"),
        "gee title":
            R(Text("ggtitle()") + Key('left'), rdescript="Rlang: ggplot::ggtitle"),
        "gee x label":
            R(Text("xlab()") + Key('left'), rdescript="Rlang: ggplot::ggtitle"),
        "gee y label":
            R(Text("ylab()") + Key('left'), rdescript="Rlang: ggplot::ggtitle"),
        "gee x limit":
            R(Text("xlim()") + Key('left'), rdescript="Rlang: ggplot::ggtitle"),
        "gee y limit":
            R(Text("ylim()") + Key('left'), rdescript="Rlang: ggplot::ggtitle"),
        "graph scatter [plot]":
            R(Text("geom_point()") + Key('left'), rdescript="Rlang: ggplot::scatterplot"),
        "graph line [plot]":
            R(Text("geom_line()") + Key('left'), rdescript="Rlang: ggplot::scatterplot"),
        "graph path [plot]":
            R(Text("geom_path()") + Key('left'), rdescript="Rlang: ggplot::scatterplot"),
        "graph histogram [plot]":
            R(Text("geom_histogram()") + Key('left'),
              rdescript="Rlang: ggplot::scatterplot"),
        "graph density [plot]":
            R(Text("geom_density()") + Key('left'),
              rdescript="Rlang: ggplot::scatterplot"),
        "deeply":
            R(Text("dplyr"), rdescript="Rlang: dplyr"),
        "tidier":
            R(Text("tidyr"), rdescript="Rlang: tidyr"),
        # TODO: implement dplyr and tidyr keywords
    }

    extras = [
        Dictation("text"),
    ]
    defaults = {}

    token_set = TokenSet([
        "if", "else", "repeat", "while", "function", "for", "in", "next", "break", "TRUE",
        "FALSE", "NULL", "Inf", "NaN", "NA"
    ], "#", [])


control.nexus().merger.add_global_rule(Rlang())
