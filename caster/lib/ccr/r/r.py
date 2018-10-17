'''
Created on May 23, 2017

@author: shippy
'''

from dragonfly import Key, Text, Dictation, MappingRule, Choice

from caster.lib import control
from caster.lib.ccr.standard import SymbolSpecs
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

def rfunction(function):
    return (Text(function + "()") + Key("left"))

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
        "dot (our|are)":
            R(Text(".R"), rdescript="Rlang: .py"),
        "see as vee":
            R(Text("csv"), rdescript="Rlang: csv"),

        # dplyr and tidyr keywords: https://www.rstudio.com/wp-content/uploads/2015/02/data-wrangling-cheatsheet.pdf

        "tidy verse":
            R(Text("tidyverse"), rdescript="Rlang: tidyverse"),

        "fun <function>":
            R(rfunction("%(function)s"), rdescript="Rlang: insert a function"),

        "graph <ggfun>":
            R(rfunction("%(ggfun)s"), rdescript="Rlang: insert a ggplot function"),
    }

    extras = [
        Dictation("text"),
        Choice("function", {
            "arrange": "arrange",
            "as character": "as.character",
            "as data frame": "as.data.frame",
            "as double": "as.double",
            "as factor": "as.factor",
            "as numeric": "as.numeric",
            "bind rows": "bind_rows",
            "case when": "case_when",
            "count": "count",
            "drop NA":"drop_na",
            "filter": "filter",
            "full join": "full_join",
            "gather": "gather",
            "group by": "group_by",
            "head": "head",
            "inner join": "inner_join",
            "left join": "left_join",
            "length": "length",
            "library": "library",
            "list": "list",
            "(LM | linear model)": "lm",
            "mean":"mean",
            "mutate": "mutate",
            "names": "names",
            "paste": "paste0",
            "read CSV":"read_csv",
            "rename": "rename",
            "select": "select",
            "string contains":"str_contains",
            "string detect":"str_detect",
            "string replace":"string_replace",
            "string replace all":"string_replace_all",
            "starts with":"starts_with",
            "sum":"sum",
            "summarise": "summarise",
            "trim white space": "trimws",
            "ungroup": "ungroup",
            "vector": "c",
        }),
        Choice("ggfun", {
            "aesthetics": "aes",
            "column [plot]": "geom_col",
            "density [plot]": "geom_density",
            "ex limit":"xlim",
            "facet grid": "facet_grid",
            "histogram [plot]": "geom_histogram",
            "labels": "labs",
            "line [plot]": "geom_line",
            "path [plot]": "geom_path",
            "plot": "ggplot",
            "point [plot]": "geom_point",
            "save":"ggsave",
            "smooth [plot]": "geom_smooth",
            "theme minimal": "theme_minimal",
            "why limit":"ylim",
        }),

    ]
    defaults = {}


control.nexus().merger.add_global_rule(Rlang())
