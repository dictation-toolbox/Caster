from castervoice.lib.imports import *


class Markdown(MergeRule):
    pronunciation = "mark down"

    mapping = {
        "heading [<num>] [<dict>]":
            R(Store() + Function(lambda num, dict: Text(
                ("#"*num) + " " + str(dict).capitalize()).execute()) + Retrieve() +
              Key("enter")),
        "table row <n>":
            R(Function(lambda n: Text("|"*(n - 1)).execute()) + Key("home")),
        "table (break | split) <n>":
            R(Function(lambda n: Text("---|"*(n - 1) + "---").execute()) + Key("enter")),
        "insert <element>":
            R(Store() + Key("%(element)s") + Retrieve(action_if_text="c-right")),
        "insert header":
            R(Text("---\nauthor: \ntitle: \n---\n")),
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 12),
        IntegerRefST("num", 1, 7),
        Choice(
            "element", {
                "list": "asterisk, space",
                "numbered list": "one, dot, space",
                "[block] quote": "rangle, space",
                "link": "lbracket, rbracket, lparen, rparen, left:3",
                "image": "exclamation, lbracket, rbracket, lparen, rparen, left:3",
                "reference": "lbracket, rbracket, left, at",
                "equation": "dollar, dollar, enter:2, dollar, dollar, up",
                "math": "dollar, dollar, left",
                "(italics | italic text)": "underscore:2, left",
                "bold [text]": "asterisk:4, left:2",
                "strike through [text]": "tilde:4, left:2",
                "horizontal rule": "asterisk, asterisk, asterisk, enter",
                "R code": "backtick:3, lbrace, r, rbrace, enter:2, backtick:3, up",
                "in line code": "backtick:2, left",
                "code [block]": "backtick:6, left:3, enter:2, up",
            }),
    ]
    defaults = {
        "num": 1,
        "dict": "",
    }


control.global_rule(Markdown())
