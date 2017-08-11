from dragonfly import Key, Text, Dictation, Function, Choice

from caster.lib import control, textformat
from caster.lib.ccr.standard import SymbolSpecs
from caster.lib.dfplus.additions import SelectiveAction
from caster.lib.dfplus.merge.mergerule import MergeRule, TokenSet
from caster.lib.dfplus.state.short import R

class React(MergeRule):
    auto = [".jsx"]
    pronunciation = "react"
        
    mapping = {
        # React stuff
        "react":                        R(Text("react"), rdescript="react"),
        "react router dom":             R(Text("react-router-dom"), rdescript="react-router"),
        "my props":                     R(Text("this.props"), rdescript="React props"),
        "my state":                     R(Text("this.state"), rdescript="React state"),
        "set state":                    R(Text("this.setState") + Key("lparen, lbrace"), rdescript="React setState"),
        "set state funk":               R(Text("this.setState") + Key("lparen"), rdescript="React functional setState"),
        "<lifecycle>":                  R(Text("%(lifecycle)s") + Key("lparen, rparen, space, lbrace, enter"),
                                            rdescript="React component lifecycle methods"),
        "react constructor":            R(Text("constructor(props) ") + Key("lbrace, enter") + Text("super(props)")
                                            + Key("enter"), rdescript="React constructor"),
        "react (main | maine) import":  R(Text("import React, { Component } from 'react';") + Key("enter"),
                                            rdescript="main React imports"),
        "react dom import":             R(Text("import ReactDOM from 'react-dom';") + Key("enter"),
                                            rdescript="React imports"),
        "class name":                   R(Text("className"), rdescript="React: className"),
        "browser router":               R(Text("BrowserRouter"), rdescript="react-router: BrowserRouter"),
        "react component <textnv>":     R(Text("class ") + Function(textformat.js_format)
                                           + Text(" extends Component ") + Key("lbrace, enter"),
                                            rdescript="React component"),
        "proper":                       R(Key("equals, lbrace"), rdescript="react:prop"),
        "proper <textnv>":              R(Function(textformat.camel_format) + Key("equal, lbrace"),
                                            rdescript="react: prop w/ name"),
        "comp tag <textnv>":            R(Key("langle") + Function(textformat.upper_camel) + Text(" /") + Key("left:2"),
                                            rdescript="react: self-closing component tag"),
        "comp tag <textnv> matched":    R(Key("langle") + Function(textformat.upper_camel) + Key("rangle, langle")
                                            + Text("/") + Function(textformat.upper_camel) + Key("c-left:3"),
                                            rdescript="react: matched component tag"),
          }

    extras = [
        Dictation("textnv"),
        Choice("is_method", {
            "met": 3,
            "ob": 2
            }),
        Choice("lifecycle", {
            "react render": "render",
            "component will mount": "componentWillMount",
            "component did mount": "componentDidMount",
            "component will receive props": "componentWillReceiveProps",
            "should component update": "shouldComponentUpdate",
            "component will update": "componentWillUpdate",
            "component did update": "componentDidUpdate",
            "component will unmount": "componentWillUnmount"
            }),will
        ]

    defaults = {
        "is_method": 2,
    }

     
    token_set = TokenSet(["abstract", "continue", "for", "new", "switch", "assert",
                 "default", "goto", "package", "synchronized", "boolean",
                 "do", "if", "private", "this", "break", "double",
                 "implements", "protected", "throw", "byte", "else",
                 "import", "public", "throws", "case", "enum",
                 "instanceof", "return", "transient", "catch", "extends",
                 "int", "short", "try", "char", "final", "interface",
                 "static", "void", "class", "finally", "long", "strictfp",
                 "volatile", "const", "float", "native", "super", "while"], 
                         "//", 
                         ["/*", "*/"])
    
control.nexus().merger.add_global_rule(React())
