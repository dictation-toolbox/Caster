"""
__author__ = 'LexiconCode'
Command-module for Gitter
Official Site "https://gitter.im/"
"""
from castervoice.lib.imports import *

class GitterRule(MergeRule):
    pronunciation = "Gitter"

    mapping = {
        "bold": R(Text("****") + Key("left:2")),
        "emphasize": R(Text("**") + Key("left")),
        # "header":           R(Text( "" )), # H1 ## H2 ### H3
        "insert item": R(Text("* ")),
        "block quote": R(Text("> ")),
        "mention": R(Text("@")),
        "insert link": R(Text("[]()") + Key("left:3")),
        "insert image": R(Text("![]()") + Key("left:3")),
        "insert code": R(Text("``") + Key("left")),
        "formatted code": R(Text("```") + Key("s-enter")),
    }
    extras = [
        Dictation("text"),
    ]
    Defaults = {}


context = AppContext(executable="gitter")
control.non_ccr_app_rule(GitterRule(), context=context)