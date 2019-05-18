'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice

from castervoice.lib import control
from castervoice.lib.actions import Key, Text
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.ccr.standard import SymbolSpecs


# Return \first{second}, if second is empty then end inside the brackets for user input
def back_curl(first, second):
    if str(second) != "":
        return (Text("\\") + Text(str(first)) + Key("lbrace, rbrace, left") + Text(
            str(second)) + Key("right"))
    if str(second) == "":
        return (Text("\\") + Text(str(first)) + Key("lbrace, rbrace, left"))


def symbol_letters(big, symbol):
    if big:
        symbol = symbol.title()
    Text(str(symbol)).execute()


class LaTeX(MergeRule):
    pronunciation = "latex"

    mapping = {
        SymbolSpecs.COMMENT:
            R(Text("%"), rdescript="LaTeX: Add Comment"),
        "begin <element>":
            R(back_curl("begin", "%(element)s") + Key("enter:2") + back_curl(
                "end", "%(element)s") + Key("up"),
              rdescript="LaTeX: Define beginning and end of an element"),
        #
        "[use] package [<packages>]":
            R(back_curl("usepackage", "%(packages)s"), rdescript="LaTeX: Import packages"),
        "[use] package bib latex":
            R(back_curl("usepackage[style=authoryear]", "biblatex"),
              rdescript="LaTeX: Import biblatex package"),
        #
        "symbol [<big>] <symbol>":
            R(Text("\\") + Function(symbol_letters, extra={"big", "symbol"}) + Text(" "),
              rdescript="LaTeX: Insert symbols"),
        #
        "insert <command>":
            R(back_curl("%(command)s", ""),
            rdescript="LaTeX: Insert command requiring an argument"),
        "insert <commandnoarg>":
            R(Text("\\%(commandnoarg)s "),
            rdescript="LaTeX: Insert command not requiring an argument"),
        "insert quote":
            R(Text("``\'\'") + Key("left:2"), rdescript="LaTeX: Insert a quote"),
        #
        "superscript":
            R(Text("^") + Key("lbrace, rbrace, left"), rdescript="LaTeX: Superscript"),
        "subscript":
            R(Text("_") + Key("lbrace, rbrace, left"), rdescript="LaTeX: Subscript"),
        "math fraction":
            R(Text("\\") + Text("frac") +
                Key("lbrace, rbrace, lbrace, rbrace, space, left:4"),
                rdescript="LaTeX: Fraction"),
    }

    extras = [
        Choice("packages", {
            "math tools": "mathtools",
            "graphic ex": "graphicx",
            "wrap figure": "wrapfig",
        }),
        Choice(
            "element", {
                "center": "center",
                "columns": "columns",
                "description": "description",
                "document": "document",
                "(enumerate | numbered list)": "enumerate",
                "equation": "equation",
                "figure": "figure",
                "flush left": "flushleft",
                "flush right": "flushright",
                "frame": "frame",
                "list": "list",
                "mini page": "minipage",
                "quotation": "quotation",
                "quote": "quote",
                "table": "table",
                "title page": "titlepage",
                "verbatim": "verbatim",
                "verse": "verse",
                "wrap figure": "wrapfigure",
            }),
        Choice(
            "command", {
                "author": "author",
                "[add] bib resource": "addbibresource",
                "caption": "caption",
                "chapter": "chapter",
                "column": "column",
                "document class": "documentclass",
                "graphics path": "graphicspath",
                "[include] graphics": "includegraphics[width=1\\textwidth]",
                "label": "label",
                "new command": "newcommand",
                "paragraph": "paragraph",
                "paren cite": "parencite",
                "part": "part",
                "reference": "ref",
                "sub paragraph": "subparagraph",
                "(section | heading)": "section",
                "sub (section | heading)": "subsection",
                "sub sub (section | heading)": "subsubsection",
                "text cite": "textcite",
                "[text] bold": "textbf",
                "[text] italics": "textit",
                "[text] slanted": "textsl",
                "title": "title",
                "use theme": "usetheme",
            }),
        Choice(
            "commandnoarg", {
                "line break": "linebreak",
                "[list] item": "item",
                "make title": "maketitle",
                "new page": "newpage",
                "page break": "pagebreak",
                "print bibliography": "printbibliography",
                "table of contents": "tableofcontents",
                "text width": "textwidth",
            }),
        Choice(
            "symbol",
            {
                "alpha": "alpha",
                "beater": "beta",
                "gamma": "gamma",
                "delta": "delta",
                "epsilon": "epsilon",
                "var epsilon": "varepsilon",
                "zita": "zeta",
                "eater": "eta",
                "theta": "theta",
                "iota": "iota",
                "kappa": "kappa",
                "lambda": "lambda",
                "mu": "mu",
                "new": "nu",
                "zee": "xi",
                "pie": "pi",
                "row": "rho",
                "sigma": "sigma",
                "tau": "tau",
                "upsilon": "upsilon",
                "phi": "phi",
                "chi": "chi",
                "sigh": "psi",
                "omega": "omega",
                #
                "times": "times",
                "divide": "div",
                "intersection": "cap",
                "union": "cup",
                "stop": "cdot",
                "approximate": "approx",
                "proportional": "propto",
                "not equal": "neq",
                "member": "in",
                "for all": "forall",
                "partial": "partial",
                "infinity": "infty",
                "dots": "dots",
                #
                "left arrow": "leftarrow",
                "right arrow": "rightarrow",
                "up arrow": "uparrow",
                "down arrow": "downarrow",
                #
                "left": "left(",
                "right": "right)",
            }),
        Choice("big", {
            "big": True,
        }),
    ]
    defaults = {
        "big": False,
        "packages": "",
    }


control.nexus().merger.add_global_rule(LaTeX())
