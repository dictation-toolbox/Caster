from castervoice.lib.actions import Text
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.selfmod.tree_rule.tree_node import TreeNode
from castervoice.lib.merge.selfmod.tree_rule.tree_rule import TreeRule
from castervoice.lib.merge.state.actions2 import NullAction

H = TreeNode
_style = H("style", Text("-style: "), [
    H("none", Text("none")),
    H("hidden", Text("hidden")),
    H("dotted", Text("dotted")),
    H("dashed", Text("dashed")),
    H("solid", Text("solid")),
    H("double", Text("double")),
    H("groove", Text("groove")),
    H("ridge", Text("ridge")),
    H("inset", Text("inset")),
    H("outset", Text("outset")),
])


def get_css_node():
    H = TreeNode
    css_sections = []
    css_sections.append(_get_background())
    css_sections.append(_get_border())
    css_sections.append(_get_box())
    css_sections.append(_get_font())
    css_sections.append(_get_box_model())
    css_sections.append(_get_text())
    css_sections.append(_get_column())
    css_sections.append(_get_speech())
    css_sections += _get_miscellaneous()

    return H("css", NullAction(), css_sections)


def _get_speech():
    _volume = [
        H("uri", Text("uri")),
        H("silent", Text("silent")),
        H("extra soft", Text("x-soft")),
        H("soft", Text("soft")),
        H("medium", Text("medium")),
        H("loud", Text("loud")),
        H("extra loud", Text("x-loud")),
        H("none", Text("none")),
        H("inherit", Text("inherit"))
    ]
    _pause_rest = [
        H("none", Text("none")),
        H("extra weak", Text("x-weak")),
        H("weak", Text("weak")),
        H("medium", Text("medium")),
        H("strong", Text("strong")),
        H("extra strong", Text("x-strong")),
        H("inherit", Text("inherit"))
    ]
    _pitch = [
        H("extra low", Text("x-low")),
        H("low", Text("low")),
        H("medium", Text("medium")),
        H("high", Text("high")),
        H("extra high", Text("x-high")),
        H("inherit", Text("inherit"))
    ]
    return H("speech", NullAction(), [
        H("cue", Text("cue"), [
            H("before", Text("-before: "), _volume),
            H("after", Text("-after: "), _volume)
        ]),
        H("mark", Text("mark"),
          [H("before", Text("-before: ")),
           H("after", Text("-after"))]),
        H("pause", Text("pause"), [
            H("before", Text("-before: "), _pause_rest),
            H("after", Text("-after: "), _pause_rest)
        ]),
        H("rest", Text("rest"), [
            H("before", Text("-before: "), _pause_rest),
            H("after", Text("-after: "), _pause_rest)
        ]),
        H("speak", Text("speak: "), [
            H("none", Text("none")),
            H("normal", Text("normal")),
            H("spell out", Text("spell-out")),
            H("digits", Text("digits")),
            H("literal punctuation", Text("literal-punctuation")),
            H("no punctuation", Text("no-punctuation")),
            H("inherit", Text("inherit"))
        ]),
        H("voice", Text("voice"), [
            H("balance", Text("-balance: "), [
                H("left", Text("left")),
                H("center", Text("center")),
                H("right", Text("right")),
                H("leftwards", Text("leftwards")),
                H("rightwards", Text("rightwards")),
                H("inherit", Text("inherit"))
            ]),
            H("duration", Text("-duration: ")),
            H("family", Text("-family: "), [H("inherit", Text("inherit"))]),
            H("rate", Text("-rate: "), [
                H("extra low", Text("x-low")),
                H("low", Text("low")),
                H("medium", Text("medium")),
                H("fast", Text("fast")),
                H("next for fast", Text("x-fast")),
                H("inherit", Text("inherit")),
            ]),
            H("pitch", Text("-pitch: "), _pitch),
            H("pitch range", Text("-pitch-range: "), _pitch),
            H("stress", Text("-stress: "), [
                H("strong", Text("strong")),
                H("moderate", Text("moderate")),
                H("none", Text("none")),
                H("reduced", Text("reduced")),
                H("inherit", Text("inherit"))
            ]),
            H("volume", Text("-volume: "), _volume)
        ]),
    ])


def _get_column():
    H = TreeNode
    global _style
    return H("column", Text("column"), [
        H("count", Text("-count: "), [H("auto", Text("auto"))]),
        H("fill", Text("-fill: "),
          [H("auto", Text("auto")),
           H("balance", Text("balance"))]),
        H("gap", Text("-gap: "), [H("normal", Text("normal"))]),
        H("rule", Text("-rule"), [
            H("color", Text("-color: "), [H("color", Text("COLOR"))]),
            _style,
            H("width", Text("-width: "), [
                H("thin", Text("thin")),
                H("medium", Text("medium")),
                H("thick", Text("thick"))
            ]),
        ]),
        H("width", Text("-width: "), [H("auto", Text("auto"))]),
        H("span", Text("-span: "),
          [H("one", Text("1")), H("all", Text("all"))])
    ])


def _get_text():
    H = TreeNode
    _align = [
        H("start", Text("start")),
        H("end", Text("end")),
        H("left", Text("left")),
        H("right", Text("right")),
        H("center", Text("center")),
        H("justify", Text("justify"))
    ]
    return H("text", Text("text"), [
        H("align", Text("-align: "), _align),
        H("align last", Text("-align-last: "), _align),
        H("decoration", Text("-decoration: "), [
            H("none", Text("none")),
            H("underline", Text("underline")),
            H("overline", Text("overline")),
            H("line through", Text("line-through")),
            H("blink", Text("blink"))
        ]),
        H("emphasis", Text("-emphasis: "), [
            H("none", Text("none")),
            H("accent", Text("accent")),
            H("dot", Text("dot")),
            H("circle", Text("circle")),
            H("disc", Text("disc")),
            H("before", Text("before")),
            H("after", Text("after"))
        ]),
        H("indent", Text("-indent: ")),
        H("justify", Text("-justify: "), [
            H("auto", Text("auto")),
            H("inter word", Text("inter-word")),
            H("inter ideograph", Text("inter-ideograph")),
            H("distribute", Text("distribute")),
            H("kashida", Text("kashida")),
            H("tibetan", Text("tibetan"))
        ]),
        H("outline", Text("-outline: "), [H("none", Text("none"))]),
        H("shadow", Text("-shadow: "),
          [H("none", Text("none")), H("color", Text("COLOR"))]),
        H("transform", Text("-transform: "), [
            H("none", Text("none")),
            H("capitalize", Text("capitalize")),
            H("uppercase", Text("uppercase")),
            H("lowercase", Text("lowercase"))
        ]),
        H("wrap", Text("-wrap: "), [
            H("normal", Text("normal")),
            H("unrestricted", Text("unrestricted")),
            H("none", Text("none")),
            H("override", Text("override"))
        ])
    ])


def _get_miscellaneous():
    H = TreeNode
    _sides = [
        H("top", Text("top")),
        H("bottom", Text("bottom")),
        H("left", Text("left")),
        H("right", Text("right"))
    ]
    return [
        H("direction", Text("direction: "), [
            H("left to right", Text("ltr")),
            H("right to left", Text("rtl")),
            H("inherit", Text("inherit"))
        ]),
        H("hanging punctuation", Text("hanging-punctuation: "), [
            H("none", Text("none")),
            H("start", Text("start")),
            H("end", Text("end")),
            H("end edge", Text("end-edge"))
        ]),
        H("letterspacing", Text("letter-spacing: "), [H("normal", Text("normal"))]),
        H("unicode bidi", Text("unicode-bidi: "), [
            H("normal", Text("normal")),
            H("embed", Text("embed")),
            H("bidi override", Text("bidi-override"))
        ]),
        H("whitespace", Text("white-space: "), [
            H("normal", Text("normal")),
            H("pre", Text("pre")),
            H("no wrap", Text("nowrap")),
            H("pre wrap", Text("pre-wrap")),
            H("pre line", Text("pre-line"))
        ]),
        H("white space collapse", Text("white-space-collapse: "), [
            H("preserve", Text("preserve")),
            H("collapse", Text("collapse")),
            H("preserve breaks", Text("preserve-breaks")),
            H("discard", Text("discard"))
        ]),
        H("word", Text("word"), [
            H("break", Text("-break: "), [
                H("normal", Text("normal")),
                H("keep all", Text("keep-all")),
                H("loose", Text("loose")),
                H("break strict", Text("break-strict")),
                H("break all", Text("break-all")),
            ]),
            H("spacing", Text("-spacing: "), [H("normal", Text("normal"))]),
            H("wrap", Text("-wrap: "),
              [H("normal", Text("normal")),
               H("break word", Text("break-word"))])
        ]),
        H("color", Text("color: "),
          [H("inherit", Text("inherit")),
           H("color", Text("COLOR"))]),
        H("opacity", Text("opacity: "), [H("inherit", Text("inherit"))]),
        H("tab side", Text("tab-side: "), _sides),
        H("caption side", Text("caption-side: "), _sides),
        H("empty cells", Text("empty-cells: "),
          [H("show", Text("show")), H("hide", Text("hide"))]),
        H("table layout", Text("table-layout"),
          [H("auto", Text("auto")), H("fixed", Text("fixed"))])
    ]


def _get_box_model(
):  # display can be optimized by doing more nesting, this whole section is to be moved somewhere else
    H = TreeNode
    _auto = [H("auto", Text("auto"))]
    _height = H("height", Text("height: "), _auto)
    _width = H("width", Text("width: "), _auto)
    _sides = [
        H("top", Text("-top: "), _auto),
        H("bottom", Text("-bottom: "), _auto),
        H("left", Text("-left: "), _auto),
        H("right", Text("-right: "), _auto)
    ]
    _overflow = [
        H("visible", Text("visible")),
        H("hidden", Text("hidden")),
        H("scroll", Text("scroll")),
        H("auto", Text("auto")),
        H("no display", Text("no-display")),
        H("no content", Text("no-content")),
    ]
    return H("box model", NullAction(), [
        H("clear", Text("clear: "), [
            H("left", Text("left")),
            H("right", Text("right")),
            H("both", Text("both")),
            H("none", Text("none"))
        ]),
        H("display", Text("display: "), [
            H("none", Text("none")),
            H("block", Text("block")),
            H("compact", Text("compact")),
            H("table", Text("table")),
            H("inline", Text("inline"),
              [H("block", Text("-block")),
               H("table", Text("-table"))]),
            H("run in", Text("run-in")),
            H("list item", Text("list-item")),
            H("table", Text("table"), [
                H("row", Text("-row"), [H("group", Text("-group"))]),
                H("footer", Text("-footer"), [H("group", Text("-group"))]),
                H("column", Text("-column"), [H("group", Text("-group"))]),
                H("cell", Text("-cell")),
                H("caption", Text("-caption"))
            ]),
            H("ruby", Text("ruby"), [
                H("base", Text("-base"), [H("group", Text("-group"))]),
                H("text", Text("-text"), [H("group", Text("-group"))])
            ])
        ]),
        H("float", Text("float: "),
          [H("left", Text("left")),
           H("right", Text("right")),
           H("none", Text("none"))]), _height, _width,
        H("max", Text("max-"), [_height, _width]),
        H("min", Text("min-"), [_height, _width]),
        H("margin", Text("margin"), _sides),
        H("padding", Text("padding"), _sides),
        H("marquee", Text("marquee"), [
            H("direction", Text("-direction: "),
              [H("forward", Text("forward")),
               H("reverse", Text("reverse"))]),
            H("loop", Text("-loop: "), [H("infinite", Text("infinite"))]),
            H("play count", Text("-play-count: "), [H("infinite", Text("infinite"))]),
            H("speed", Text("-speed: "), [
                H("slow", Text("slow")),
                H("normal", Text("normal")),
                H("fast", Text("fast"))
            ]),
            H("style", Text("-style: "), [
                H("scroll", Text("scroll")),
                H("slide", Text("slide")),
                H("alternate", Text("alternate"))
            ])
        ]),
        H("overflow", Text("overflow: "), _overflow),
        H("overflow X", Text("overflow-x: "), _overflow),
        H("overflow Y", Text("overflow-y: "), _overflow),
        H("overflow style", Text("overflow-style: "), [
            H("auto", Text("auto")),
            H("marquee line", Text("marquee-line")),
            H("marquee block", Text("marquee-block"))
        ]),
        H("rotation", Text("rotation: "), [H("angle", Text("ANGLE"))]),
        H("rotation point", Text("rotation-point: ")),
        H("visibility", Text("visibility: "), [
            H("visible", Text("visible")),
            H("hidden", Text("hidden")),
            H("collapse", Text("collapse"))
        ])
    ])


def _get_font():
    H = TreeNode
    return H("font", Text("font"), [
        H("family", Text("-family: "), [H("inherit", Text("inherit"))]),
        H("size", Text("-size: "), [
            H("extra extra small", Text("xx-small")),
            H("extra small", Text("x-small")),
            H("small", Text("small")),
            H("medium", Text("medium")),
            H("large", Text("large")),
            H("extra large", Text("x-large")),
            H("extra extra large", Text("xx-large")),
            H("smaller", Text("smaller")),
            H("larger", Text("larger")),
            H("inherit", Text("inherit"))
        ]),
        H("size adjust", Text("-size-adjust: "),
          [H("none", Text("none")),
           H("inherit", Text("inherit"))]),
        H("stretch", Text("-stretch: "), [
            H("normal", Text("normal")),
            H("wider", Text("wider")),
            H("narrower", Text("narrower")),
            H("ultra condensed", Text("ultra-condensed")),
            H("extra condensed", Text("extra-condensed")),
            H("condensed", Text("condensed")),
            H("semi condensed", Text("semi-condensed")),
            H("semi expanded", Text("semi-expanded")),
            H("expanded", Text("expanded")),
            H("extra expanded", Text("extra-expanded")),
            H("ultra expanded", Text("ultra-expanded")),
            H("inherit", Text("inherit"))
        ]),
        H("style", Text("-style: "), [
            H("normal", Text("normal")),
            H("italic", Text("italic")),
            H("oblique", Text("oblique")),
            H("inherit", Text("inherit"))
        ]),
        H("variant", Text("-variant: "), [
            H("normal", Text("normal")),
            H("small caps", Text("small-caps")),
            H("inherit", Text("inherit"))
        ]),
        H("weight", Text("-weight: "), [
            H("normal", Text("normal")),
            H("bold", Text("bold")),
            H("bolder", Text("bolder")),
            H("lighter", Text("lighter")),
            H("inherit", Text("inherit")),
            H("one hundred", Text("100")),
            H("nine hundred", Text("900"))
        ])
    ])


def _get_box():
    H = TreeNode
    return H("box", Text("box"), [
        H("shadow", Text("-shadow: "),
          [H("inset", Text("inset")),
           H("none", Text("none")),
           H("color", Text("COLOR"))]),
        H("align", Text("-align: "),
          [H("start", Text("start")),
           H("end", Text("end")),
           H("center", Text("center"))]),
        H("direction", Text("-direction: "),
          [H("normal", Text("normal")),
           H("reverse", Text("reverse"))]),
        H("flex", Text("-flex: ")),
        H("flex group", Text("-flex-group: ")),
        H("lines", Text("-lines: "),
          [H("single", Text("single")),
           H("multiple", Text("multiple"))]),
        H("orient", Text("-orient: "), [
            H("horizontal", Text("horizontal")),
            H("vertical", Text("vertical")),
            H("inline axis", Text("inline-axis")),
            H("block axis", Text("block-axis"))
        ]),
        H("pack", Text("-pack: "), [
            H("start", Text("start")),
            H("end", Text("end")),
            H("center", Text("center")),
            H("justify", Text("justify"))
        ]),
        H("sizing", Text("-sizing: "), [
            H("content box", Text("content-box")),
            H("padding box", Text("padding-box")),
            H("border box", Text("border-box")),
            H("margin box", Text("margin-box"))
        ])
    ])


def _get_border():
    H = TreeNode
    _width = H(
        "width", Text("-width: "),
        [H("thin", Text("thin")),
         H("medium", Text("medium")),
         H("thick", Text("thick"))])
    global _style
    _color = H("color", Text("-color: "), [H("color", Text("COLOR"))])
    _radius = H("radius", Text("-radius: "))
    return H("border", Text("border"), [
        _width, _style, _color,
        H("top", Text("-top"), [
            _width, _style, _color,
            H("left", Text("-left"), [_radius]),
            H("right", Text("-right"), [_radius])
        ]),
        H("bottom", Text("-bottom"), [
            _width, _style, _color,
            H("left", Text("-left"), [_radius]),
            H("right", Text("-right"), [_radius])
        ]),
        H("left", Text("-left"), [_width, _style, _color]),
        H("right", Text("-right"), [_width, _style, _color]),
        H("break", Text("-break"),
          [_width, _style, _color, H("close", Text("close"))]),
        H("collapse", Text("-collapse: "),
          [H("collapse", Text("collapse")),
           H("separate", Text("separate"))]),
        H("spacing", Text("-spacing: "))
    ])


def _get_background():
    H = TreeNode
    halign = [
        H("left", Text("left")),
        H("center", Text("center")),
        H("right", Text("right"))
    ]
    background_position = halign + [
        H("X position", Text("xpos")),
        H("Y position", Text("ypos")),
        H("initial", Text("initial")),
        H("inherit", Text("inherit"))
    ]
    background_box = [
        H("border box", Text("border-box")),
        H("padding box", Text("padding-box")),
        H("border box", Text("border-box")),
    ]
    return H("background", Text("background"), [
        H("image", Text("-image: "), [
            H("(Earl | URL)", Text("url")),
            H("none", Text("none")),
        ]),
        H("position", Text("-position: "), [
            H("top", Text("top "), halign),
            H("center", Text("center "), halign),
            H("bottom", Text("bottom "), halign),
        ] + background_position),
        H("size", Text("-size: "), [
            H("auto", Text("auto")),
            H("cover", Text("cover")),
            H("contain", Text("contain"))
        ]),
        H("repeat", Text("-repeat: "), [
            H("repeat", Text("repeat")),
            H("repeat X", Text("repeat-x")),
            H("repeat Y", Text("repeat-y")),
            H("no repeat", Text("no-repeat")),
        ]),
        H("attachment", Text("-attachment: "),
          [H("scroll", Text("scroll")),
           H("fixed", Text("fixed"))]),
        H("origin", Text("-origin: "), background_box),
        H("clip", Text("-clip: "), background_box + [H("no clip", Text("no-clip"))]),
        H("color", Text("-color: "), [
            H("color", Text("COLOR")),
            H("transparent", Text("transparent")),
        ]),
        H("break", Text("-break: "), [
            H("bounding box", Text("bounding-box")),
            H("each box", Text("each-box")),
            H("continuous", Text("continuous")),
        ])
    ])


class CSSTreeRule(TreeRule):

    pronunciation = "CSS"

    def __init__(self):
        super(CSSTreeRule, self).__init__("CSS", get_css_node())


def get_rule():
    return [CSSTreeRule, RuleDetails(ccrtype=CCRType.SELFMOD)]

