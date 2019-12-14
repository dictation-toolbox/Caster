'''
Created on May 23, 2017

@author: shippy
'''
from dragonfly import Key, Dictation, Choice

from castervoice.lib.actions import Text
from castervoice.rules.ccr.standard import SymbolSpecs
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Rlang(MergeRule):
    auto = [".R", ".r"]
    pronunciation = "are"

    mapping = {
        SymbolSpecs.IF:
            R(Text("if ()") + Key("left")),
        SymbolSpecs.ELSE:
            R(Text("else ") + Key("enter")),
        #
        # (no switch in Rlang)
        SymbolSpecs.BREAK:
            R(Text("break")),
        #
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for ( in ):") + Key("left:6")),
        SymbolSpecs.FOR_LOOP:
            R(Text("for (i in 1:)") + Key("left")),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while ()") + Key("left")),
        # (no do-while in Rlang)
        #
        SymbolSpecs.AND:
            R(Text(" & ")),
        SymbolSpecs.OR:
            R(Text(" | ")),
        SymbolSpecs.NOT:
            R(Text("!")),
        #
        SymbolSpecs.SYSOUT:
            R(Text("print()") + Key("left")),
        #
        SymbolSpecs.IMPORT:
            R(Text("library()") + Key("left")),
        #
        SymbolSpecs.FUNCTION:
            R(Text("function()") + Key("left")),
        # SymbolSpecs.CLASS:          R(Text("setClass()") + Key("left")),
        #
        SymbolSpecs.COMMENT:
            R(Text("#")),
        #
        SymbolSpecs.NULL:
            R(Text("NULL")),
        #
        SymbolSpecs.RETURN:
            R(Text("return()") + Key("left")),
        #
        SymbolSpecs.TRUE:
            R(Text("TRUE")),
        SymbolSpecs.FALSE:
            R(Text("FALSE")),

        # Rlang specific
        "assign":
            R(Text(" <- ")),
        "contained in":
            R(Key('space, percent, i, n, percent, space')),
        "slurp | chain":
            R(Key('space, percent, rangle, percent, space')),
        "tell (slurp | chain)":
            R(Key('end, space, percent, rangle, percent, enter')),
        "tell add":
            R(Key('end, space, plus, enter')),
        "NA":
            R(Text("NA")),
        "shell iffae | LFA":
            R(Text("else if ()") + Key("left")),
        "dot (our|are)":
            R(Text(".R")),
        "see as vee":
            R(Text("csv")),


        "tidy verse":
            R(Text("tidyverse")),
        "<function>":
            R(Text("%(function)s()") + Key("left")),
        "graph <ggfun>":
            R(Text("%(ggfun)s()") + Key("left")),
        "pack <pacfun>":
            R(Text("%(pacfun)s()") + Key("left")),
    }

    extras = [
        Dictation("text"),
        Choice(
            "function", {
                "arrange": "arrange",
                "as character": "as.character",
                "as data frame": "as.data.frame",
                "as double": "as.double",
                "as factor": "as.factor",
                "as numeric": "as.numeric",
                "bind rows": "bind_rows",
                "case when": "case_when",
                "count": "count",
                "drop NA": "drop_na",
                "filter": "filter",
                "full join": "full_join",
                "gather": "gather",
                "group by": "group_by",
                "head": "head",
                "inner join": "inner_join",
                "install packages":"install.packages",
                "is NA":"is.na",
                "left join": "left_join",
                "length": "length",
                "library": "library",
                "list": "list",
                "(LM | linear model)": "lm",
                "mean": "mean",
                "mutate": "mutate",
                "names": "names",
                "paste": "paste0",
                "read CSV": "read_csv",
                "rename": "rename",
                "select": "select",
                "string contains": "str_contains",
                "string detect": "str_detect",
                "string replace": "str_replace",
                "string replace all": "str_replace_all",
                "starts with": "starts_with",
                "sum": "sum",
                "summarise": "summarise",
                "tail":"tail",
                "trim white space": "trimws",
                "ungroup": "ungroup",
                "vector": "c",
            }),
        Choice(
            "ggfun", {
                "aesthetics": "aes",
                "column [plot]": "geom_col",
                "density [plot]": "geom_density",
                "ex label":"xlab",
                "ex limit": "xlim",
                "facet grid": "facet_grid",
                "histogram [plot]": "geom_histogram",
                "labels": "labs",
                "line [plot]": "geom_line",
                "path [plot]": "geom_path",
                "plot": "ggplot",
                "point [plot]": "geom_point",
                "save": "ggsave",
                "smooth [plot]": "geom_smooth",
                "theme minimal": "theme_minimal",
                "why label":"ylab",
                "why limit": "ylim",
            }),
        Choice(
            "pacfun", {
                "install":"p_install",
                "install hub":"p_install_gh",
                "install version":"p_install_version",
                "install temp":"p_temp",
                "load":"p_load",
                "unload":"p_unload",
                "update":"p_update",
            }),
    ]
    defaults = {}


def get_rule():
    return Rlang, RuleDetails(ccrtype=CCRType.GLOBAL)
