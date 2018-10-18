'''
Created on May 23, 2017

@author: shippy
'''

from dragonfly import Key, Text, Dictation, MappingRule

from caster.lib import control
from caster.lib.ccr.standard import SymbolSpecs
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R



class Rlang(MergeRule):
    auto = [".R", ".r"]
    pronunciation = "are"

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
        "library":
            R(Text("library()") + Key("left"), rdescript="Rlang: Import"),
        "assign":
            R(Text(" <- "), rdescript="Rlang: Assignment"),
        "contained in":
            R(Key('space, percent, i, n, percent, space'),
              rdescript="Rlang: In operator"),
        "slurp | chain":
            R(Key('space, percent, rangle, percent, space'), rdescript="Rlang: Pipe"),
        "tell (slurp | chain)":
            R(Key('end, space, percent, rangle, percent, enter'), rdescript="Rlang: Pipe at end"),
        "tell add":
            R(Key('end, space, plus, enter'), rdescript="Rlang: plus at end"),
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
        "trim white space":
            R(Text("trimws()") + Key("left"), rdescript="Rlang: trim whitespace"),
        #
        "as factor":
            R(Text("as.factor()") + Key("left"), rdescript="Rlang: Convert to factor"),
        "as numeric":
            R(Text("as.numeric()") + Key("left"), rdescript="Rlang: Convert To Integer"),
        "as double":
            R(Text("as.double()") + Key("left"), rdescript="Rlang: Convert To Floating-Point"),
        "as character":
            R(Text("as.character()") + Key("left"), rdescript="Rlang: Convert To character"),
        "as data frame":
            R(Text("as.data.frame()") + Key("left"), rdescript="Rlang: Convert To Data Frame"),
        #
        "vector of":
            R(Text("c()") + Key("left"), rdescript="Rlang: Vector"),
        "list of":
            R(Text("list()") + Key("left"), rdescript="Rlang: List"),
        "dot (our|are)":
            R(Text(".R"), rdescript="Rlang: .py"),
        "see as vee":
            R(Text("csv"), rdescript="Rlang: csv"),
        # ggplot keywords
        "gee plot":
            R(Text("ggplot()") + Key('left'), rdescript="Rlang: ggplot"),
        "gee aesthetics":
            R(Text("aes()") + Key('left'), rdescript="Rlang: ggplot::aes"),
        "gee theme":
            R(Text("theme()") + Key('left'), rdescript="Rlang: ggplot::aes"),
        "gee title":
            R(Text("ggtitle()") + Key('left'), rdescript="Rlang: ggplot::ggtitle"),
        "gee ex label":
            R(Text("xlab()") + Key('left'), rdescript="Rlang: ggplot::ggtitle"),
        "gee why label":
            R(Text("ylab()") + Key('left'), rdescript="Rlang: ggplot::ggtitle"),
        "gee labels":
            R(Text("labs()") + Key('left'), rdescript="Rlang: ggplot::labels"),
        "gee ex limit":
            R(Text("xlim()") + Key('left'), rdescript="Rlang: ggplot::ggtitle"),
        "gee why limit":
            R(Text("ylim()") + Key('left'), rdescript="Rlang: ggplot::ggtitle"),
        "graph (scatter | point) [plot]":
            R(Text("geom_point()") + Key('left'), rdescript="Rlang: ggplot::scatterplot"),
        "graph line [plot]":
            R(Text("geom_line()") + Key('left'), rdescript="Rlang: ggplot::scatterplot"),
        "graph path [plot]":
            R(Text("geom_path()") + Key('left'), rdescript="Rlang: ggplot::scatterplot"),
        "graph smooth [plot]":
            R(Text("geom_smooth()") + Key('left'), rdescript="Rlang: ggplot::scatterplot"),
        "graph column [plot]":
            R(Text("geom_col()") + Key('left'), rdescript="Rlang: ggplot::scatterplot"),
        "graph histogram [plot]":
            R(Text("geom_histogram()") + Key('left'),
              rdescript="Rlang: ggplot::scatterplot"),
        "graph density [plot]":
            R(Text("geom_density()") + Key('left'),
              rdescript="Rlang: ggplot::scatterplot"),

        # dplyr and tidyr keywords: https://www.rstudio.com/wp-content/uploads/2015/02/data-wrangling-cheatsheet.pdf
        "deeply":
            R(Text("dplyr"), rdescript="Rlang: dplyr"),
        "tidier":
            R(Text("tidyr"), rdescript="Rlang: tidyr"),
        "tidy verse":
            R(Text("tidyverse"), rdescript="Rlang: tidyverse"),
        "arrange":
            R(Text("arrange()") + Key('left'), rdescript="Rlang: dplyr::arrange"),
        "rename":
            R(Text("rename()") + Key('left'), rdescript="Rlang: dplyr::rename"),
        "filter":
            R(Text("filter()") + Key('left'), rdescript="Rlang: dplyr::filter"),
        "select":
            R(Text("select()") + Key('left'), rdescript="Rlang: dplyr::select"),
        "summarise":
            R(Text("summarise()") + Key('left'), rdescript="Rlang: dplyr::summarise"),
        "count":
            R(Text("count()") + Key('left'), rdescript="Rlang: dplyr::count"),
        "mutate":
            R(Text("mutate()") + Key('left'), rdescript="Rlang: dplyr::mutate"),
        "group by":
            R(Text("group_by()") + Key('left'), rdescript="Rlang: dplyr::group_by"),
        "ungroup":
            R(Text("ungroup()"), rdescript="Rlang: dplyr::ungroup"),
        "bind rows":
            R(Text("bind_rows()") + Key('left'), rdescript="Rlang: dplyr::bind_rows"),
        "left join":
            R(Text("left_join()") + Key('left'), rdescript="Rlang: dplyr::left_join"),
        "inner join":
            R(Text("inner_join()") + Key('left'), rdescript="Rlang: dplyr::inner_join"),
        "full join":
            R(Text("full_join()") + Key('left'), rdescript="Rlang: dplyr::full_join"),
        "case when":
            R(Text("case_when()") + Key('left'), rdescript="Rlang: dplyr::case_when"),
        "gather":
            R(Text("gather()") + Key('left'), rdescript="Rlang: tidyr::gather"),
    }

    extras = [
        Dictation("text"),
    ]
    defaults = {}


control.nexus().merger.add_global_rule(Rlang())
