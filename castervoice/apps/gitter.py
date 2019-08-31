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
            R(Store() + Text("****") + Key("left:2") +
              Retrieve(action_if_text="right:2")),
        "emphasize":
            R(Store() + Text("**") + Key("left") + Retrieve(action_if_text="right")),
        "strike through":
            R(Store() + Text("~~~~") + Key("left:2") +
              Retrieve(action_if_text="right:2")),
        "latex":
            R(Store() + Text("$$$$") + Key("left:2") +
              Retrieve(action_if_text="right:2")),
        "<header_size> header":
            R(Store() + Text("%(header_size)s ") + Retrieve(action_if_text="s-enter")),
        "insert item":
            R(Store() + Text("*") + Key("space") + Retrieve(action_if_text="s-enter")),
        "block quote":
            R(Store() + Text(">") + Key("space") + Retrieve(action_if_text="s-enter")),
        "mention":
            R(Store() + Text("@") + Retrieve(action_if_text="right, space")),
        "insert link":
            R(Store() + Text("[]()") + Key("left:3") +
              Retrieve(action_if_text="right:2")),
        "insert image":
            R(Store() + Text("![]()") + Key("left:3") +
              Retrieve(action_if_text="right:2")),
        "insert code":
            R(Store() + Text("``") + Key("left") + Retrieve(action_if_text="right")),
        "formatted code":
            R(Store() + Text("``````") + Pause("0.5") + Key("left:3,s-enter:2,up") +
              Retrieve()),
    }
    extras = [
        Choice("header_size", {
            "small": "###",
            "medium": "##",
            "large": "#",
        }),
    ]
    Defaults = {}


context = AppContext(executable="gitter")
control.non_ccr_app_rule(GitterRule(), context=context)
