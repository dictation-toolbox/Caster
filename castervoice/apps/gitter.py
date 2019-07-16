"""
__author__ = 'LexiconCode'
Command-module for Gitter
Official Site "https://gitter.im/"
"""
from castervoice.lib.imports import *


class GitterRule(MergeRule):
    pronunciation = "Gitter"

    mapping = {
        "bold":
            R(Store() + Text("**") + Retrieve() + Text("**")),
        "emphasize":
            R(Store() + Text("*") + Retrieve() + Text("*")),
        # "header":  R(Text( "" )), # H1 ## H2 ### H3
        "insert item":
            R(Text("* ")),
        "block quote":
            R(Text("> ")),
        "mention":
            R(Store() + Text("@") + Retrieve()),
        "insert link":
            R(Store() + Text("[") + Retrieve() + Text("]()") + Key("left:2")),
        "insert image":
            R(Store() + Text("![") + Retrieve() + Text("]()") + Key("left:2")),
        "insert code":
            R(Store() + Text("`") + Retrieve() + Text("`")),
        "formatted code":
            R(Text("```") + Key("s-enter")),
    }
    extras = [
        Dictation("text"),
    ]
    Defaults = {}


context = AppContext(executable="gitter")
control.non_ccr_app_rule(GitterRule(), context=context)
