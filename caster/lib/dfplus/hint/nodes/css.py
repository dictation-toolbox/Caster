'''
Created on May 30, 2015

@author: dave
'''
from caster.lib.dfplus.hint import hintnode

H = hintnode.HintNode
_style = H("-style: ", [H("none"),H("hidden"),H("dotted"),H("dashed"),   
                    H("solid"),H("double"),H("groove"),H("ridge"),
                    H("inset"),H("outset"),      
                    ], ["style"])

def getCSSNode():
    H = hintnode.HintNode
    css_sections = []
    css_sections.append(_get_background())
    css_sections.append(_get_border())
    css_sections.append(_get_box())
    css_sections.append(_get_font())
    css_sections.append(_get_box_model())
    css_sections.append(_get_text())
    css_sections.append(_get_column())
    css_sections.append(_get_speech())
    css_sections+=_get_miscellaneous()
    
    return H("css", css_sections)

def _get_speech():
    _volume = [H("uri"),H("silent"),H("x-soft", [], ["extra soft"]),
            H("soft"),H("medium"),H("loud"),H("x-loud", [], ["extra loud"]),
            H("none"),H("inherit")
            ]
    _pause_rest = [H("none"),H("x-weak", [], ["extra week"]),H("weak"), 
                   H("medium"),H("strong"),H("x-strong", [], ["extra strong"]),
                   H("inherit")
                   ]
    _pitch = [H("x-low", [], ["extra low"]),H("low"),H("medium"),H("high"),
              H("x-high", [], ["extra high"]),H("inherit")
              ]
    return H("", [
            H("cue", [
                      H("-before: ", _volume, ["before"]),
                      H("-after: ", _volume, ["after"])
                      ]),
            H("mark", [
                       H("-before: ", [], ["before"]),
                       H("-after", [], ["after"])
                       ]),
            H("pause", [
                        H("-before: ", _pause_rest, ["before"]),
                        H("-after: ", _pause_rest, ["after"])
                        ]),
            H("rest", [
                        H("-before: ", _pause_rest, ["before"]),
                        H("-after: ", _pause_rest, ["after"])
                        ]),
            H("speak: ", [
                          H("none"),H("normal"),H("spell-out", [], ["spell out"]),
                          H("digits"),H("literal-punctuation", [], ["literal punctuation"]),
                          H("no-punctuation", [], ["no punctuation"]),H("inherit")
                          ], ["speak"]),
            H("voice", [
                        H("-balance: ", [
                              H("left"),H("center"),H("right"),H("leftwards"),
                              H("rightwards"),H("inherit")
                              ], ["balance"]),
                        H("-duration: ", [], ["duration"]), 
                        H("-family: ", [H("inherit")], ["family"]),
                        H("-rate: ", [
                                      H("x-low", [], ["extra low"]),H("low"),H("medium"),
                                      H("fast"),H("x-fast", [], ["extra fast"]),H("inherit"),
                                      ], ["rate"]),
                        H("-pitch: ", _pitch, ["pitch"]),
                        H("-pitch-range: ", _pitch, ["pitch range"]),
                        H("-stress: ", [
                                        H("strong"),H("moderate"),H("none"),
                                        H("reduced"),H("inherit")
                                        ], ["stress"]),
                        H("-volume: ", _volume, ["volume"])
                        ]),
                  ], ["speech"])

def _get_column():
    H = hintnode.HintNode
    global _style
    return H("column", [
                        H("-count: ", [H("auto")], ["count"]),
                        H("-fill: ", [
                                      H("auto"),
                                      H("balance")
                                      ], ["fill"]),
                        H("-gap: ", [H("normal")], ["gap"]),
                        H("-rule", [
                                    H("-color: ", [H("COLOR", [], ["color"])], ["color"]),
                                    _style,  
                                    H("-width: ", [
                                                   H("thin"),
                                                   H("medium"),
                                                   H("thick")
                                                   ], ["width"]),
                                    ], ["rule"]),
                        H("-width: ", [H("auto")], ["width"]),
                        H("-span: ", [
                                      H("1", [], ["one"]),
                                      H("all")
                                      ], ["span"])
                        ])    

def _get_text():
    H = hintnode.HintNode
    _align = [H("start"),H("end"),H("left"),H("right"),H("center"),H("justify")]
    return H("text", [
                       H("-align: ", _align, ["align"]),
                       H("-align-last: ", _align, ["align last"]),
                       H("-decoration: ", [
                                           H("none"),
                                           H("underline"),
                                           H("overline"),
                                           H("line-through", [], ["line through"]),
                                           H("blink")
                                           ], ["decoration"]),
                      H("-emphasis: ", [
                                        H("none"),
                                        H("accent"),
                                        H("dot"),
                                        H("circle"),
                                        H("disc"),
                                        H("before"),
                                        H("after")
                                        ], ["emphasis"]),
                      H("-indent: ", [], ["indent"]),
                      H("-justify: ", [
                                       H("auto"),
                                       H("inter-word", [], ["inter word"]),
                                       H("inter-ideograph", [], ["inter ideograph"]),
                                       H("distribute"),
                                       H("kashida"),
                                       H("tibetan")
                                       ], ["justify"]),
                      H("-outline: ", [H("none")], ["outline"]),
                      H("-shadow: ", [H("none"),
                                      H("COLOR", [], ["color"])
                                      ], ["shadow"]),
                      H("-transform: ", [
                                         H("none"),
                                         H("capitalize"),
                                         H("uppercase"),
                                         H("lowercase")
                                         ], ["transform"]),
                      H("-wrap: ", [
                                    H("normal"),
                                    H("unrestricted"),
                                    H("none"),
                                    H("override")
                                    ], ["wrap"])
                       ])

def _get_miscellaneous():
    H = hintnode.HintNode
    _sides = [
             H("top"),
             H("bottom"),
             H("left"),
             H("right") 
             ]
    return [
            H("direction: ", [
                              H("ltr", [], ["left to right"]),
                              H("rtl", [], ["right to left"]),
                              H("inherit")
                              ], ["direction"]),
            H("hanging-punctuation: ", [
                                      H("none"),
                                      H("start"),
                                      H("end"),
                                      H("end-edge", [], ["end edge"])
                                      ], ["hanging punctuation"]),
            H("letter-spacing: ", [H("normal")], ["letter spacing"]),
            H("unicode-bidi: ", [
                                 H("normal"),
                                 H("embed"),
                                 H("bidi-override", [], ["bid override"])
                                 ], ["unicode bid"]),
            H("white-space: ", [
                                H("normal"),
                                H("pre"),
                                H("nowrap", [], ["no wrap"]),
                                H("pre-wrap", [], ["pre wrap"]),
                                H("pre-line", [], ["pre line"])
                                ], ["white space"]),
            H("white-space-collapse: ", [
                                       H("preserve"),
                                       H("collapse"),
                                       H("preserve-breaks"),
                                       H("discard")
                                       ], ["white space collapse"]),
            H("word", [
                       H("-break: ", [
                                      H("normal"),
                                      H("keep-all", [], ["keep all"]),
                                      H("loose"),
                                      H("break-strict", [], ["break strict"]),
                                      H("break-all", [], ["break all"]),
                                      ], ["break"]),
                       H("-spacing: ", [H("normal")], ["spacing"]),
                       H("-wrap: ", [
                                     H("normal"),
                                     H("break-word", [], ["break word"])
                                     ], ["wrap"])
                       ]),
            H("color: ", [
                          H("inherit"),
                          H("COLOR", [], ["color"])
                          ], ["color"]),
            H("opacity: ", [H("inherit")], ["opacity"]), 
            H("tab-side: ", _sides, ["tab side"]), 
            H("caption-side: ", _sides, ["caption side"]),
            H("empty-cells: ", [
                                H("show"),
                                H("hide")
                                ], ["empty cells"]), 
            H("table-layout", [
                               H("auto"),
                               H("fixed")
                               ], ["table layout"]),
            
            
            
            
            
            
            ]

def _get_box_model():# display can be optimized by doing more nesting, this whole section is to be moved somewhere else 
    H = hintnode.HintNode
    _height = H("height: ", [H("auto")], ["height"])
    _width = H("width: ", [H("auto")], ["width"])
    _sides = [H("-top: ", [H("auto")], ["top"]),
              H("-bottom: ", [H("auto")], ["bottom"]),
              H("-left: ", [H("auto")], ["left"]),
              H("-right: ", [H("auto")], ["right"])
              ]
    _overflow = [H("visible"),H("hidden"),H("scroll"),
                 H("auto"),H("no-display", [], ["no display"]),
                 H("no-content", [], ["no content"]),
                 ]
    return H("", [
                  H("clear: ", [
                                H("left"), 
                                H("right"), 
                                H("both"), 
                                H("none") 
                                ], ["clear"]),
                  H("display: ", [
                                  H("none"),H("block"),H("compact"),H("table"),
                                  H("inline", [
                                               H("-block", [], ["block"]),
                                               H("-table", [], ["table"])
                                               ]),
                                  H("run-in", [], ["run in"]),
                                  H("list-item", [], ["list item"]),
                                  H("table", [
                                              H("-row", [H("-group", [], ["group"])], ["row"]),
                                              H("-footer", [H("-group", [], ["group"])], ["footer"]),
                                              H("-column", [H("-group", [], ["group"])], ["column"]),
                                              H("-cell", [], ["cell"]),
                                              H("-caption", [], ["caption"])
                                              ]),                                  
                                  H("ruby", [
                                             H("-base", [H("-group", [], ["group"])], ["base"]),
                                             H("-text", [H("-group", [], ["group"])], ["text"])
                                             ])
                                  ], ["display"]),  
                  H("float: ", [
                                H("left"),
                                H("right"),
                                H("none")
                                ], ["float"]),
                  _height, _width,  
                  H("max-", [_height, _width], ["max"]),
                  H("min-", [_height, _width], ["min"]),
                  H("margin", _sides),
                  H("padding", _sides),
                  H("marquee", [
                                H("-direction: ", [
                                                   H("forward"),
                                                   H("reverse")
                                                   ], ["direction"]),
                                H("-loop: ", [
                                              H("infinite")
                                              ], ["loop"]), 
                                H("-play-count: ", [H("infinite")], ["play count"]),
                                H("-speed: ", [
                                               H("slow"),H("normal"),H("fast")
                                               ], ["speed"]),
                                H("-style: ", [H("scroll"),H("slide"),H("alternate")], ["style"])
                                ]),
                  H("overflow: ", _overflow, ["overflow"]),
                  H("overflow-x: ", _overflow, ["overflow X"]),
                  H("overflow-y: ", _overflow, ["overflow Y"]),
                  H("overflow-style: ", [
                                         H("auto"),
                                         H("marquee-line", [], ["marquee line"]),
                                         H("marquee-block", [], ["marquee block"])
                                         ], ["overflow style"]),
                  H("rotation: ", [H("ANGLE", [], ["angle"])], ["rotation"]),
                  H("rotation-point: ", [], ["rotation point"]),
                  H("visibility: ", [
                                     H("visible"),
                                     H("hidden"),
                                     H("collapse")
                                     ], ["visibility"])
                  ], ["box model"])

def _get_font():
    H = hintnode.HintNode
    return H("font", [
                      H("-family: ", [H("inherit")], ["family"]),
                      H("-size: ", [
                                    H("xx-small", [], ["extra extra small"]), 
                                    H("x-small", [], ["extra small"]), 
                                    H("small"), 
                                    H("medium"), 
                                    H("large"), 
                                    H("x-large", [], ["extra-large"]), 
                                    H("xx-large", [], ["extra extra-large"]), 
                                    H("smaller"), 
                                    H("larger"), 
                                    H("inherit") 
                                    ], ["size"]), 
                      H("-size-adjust: ", [
                                           H("none"), 
                                           H("inherit")
                                           ], ["size adjust"]), 
                      H("-stretch: ", [
                                       H("normal"), 
                                       H("wider"),
                                       H("narrower"),
                                       H("ultra-condensed", [], ["ultra condensed"]),
                                       H("extra-condensed", [], ["extra condensed"]),
                                       H("condensed"),
                                       H("semi-condensed", [], ["semi condensed"]),
                                       H("semi-expanded", [], ["semi expanded"]),
                                       H("expanded"),
                                       H("extra-expanded", [], ["extra expanded"]),
                                       H("ultra-expanded", [], ["ultra-expanded"]),
                                       H("inherit")
                                       ], ["stretch"]), 
                      H("-style: ", [
                                      H("normal"),
                                      H("italic"),  
                                      H("oblique"), 
                                      H("inherit") 
                                      ], ["style"]),
                      H("-variant: ", [
                                       H("normal"), 
                                       H("small-caps", [], ["small caps"]), 
                                       H("inherit")
                                       ], ["variant"]),
                      H("-weight: ", [
                                      H("normal"),
                                      H("bold"),  
                                      H("bolder"),
                                      H("lighter"),  
                                      H("inherit"),
                                      H("100", [], ["one hundred"]),
                                      H("900", [], ["nine hundred"])
                                      ], ["weight"])
                      ], ["font"])     

def _get_box():
    H = hintnode.HintNode
    return H("box", [
                     H("-shadow: ", [
                              H("inset"), 
                              H("none"), 
                              H("COLOR", [], ["color"])
                              ], ["shadow"]), 
                     H("-align: ", [
                                    H("start"),
                                    H("end"),
                                    H("center")
                                    ], ["align"]),
                     H("-direction: ", [
                                        H("marmol"),
                                        H("reverse")
                                        ], ["direction"]),
                     H("-flex: ", [], ["flex"]),
                     H("-flex-group: ", [], ["flex group"]),
                     H("-lines: ", [
                                    H("single"),
                                    H("multiple")
                                    ], ["lines"]),
                     H("-orient: ", [
                                     H("horizontal"),
                                     H("vertical"),
                                     H("inline-axis", [], ["in line axis"]),
                                     H("block-axis", [], ["block axis"]) 
                                     ], ["orient"]),
                     H("-pack: ", [
                                   H("start"),
                                   H("end"),
                                   H("center"),
                                   H("justify")
                                   ], ["pack"]),
                     H("-sizing: ", [
                                     H("content-box", [], ["content box"]),
                                     H("padding-box", [], ["padding box"]),
                                     H("border-box", [], ["border box"]),
                                     H("margin-box", [], ["margin box"])
                                     ], ["sizing"]),
                     ])
    
def _get_border():
    H = hintnode.HintNode
    _width = H("-width: ", [H("thin"), H("medium"), H("thick")], ["width"])
    global _style
    _color = H("-color: ", [H("COLOR", [], ["color"])], ["color"])
    _radius = H("-radius: ", [], ["radius"])
    return H("border", [ _width, _style, _color, 
                        H("-top", [_width, _style, _color, 
                                   H("-left", [_radius], ["left"]), 
                                   H("-right", [_radius], ["right"])
                                   ], ["top"]), 
                        H("-bottom", [_width, _style, _color, 
                                   H("-left", [_radius], ["left"]), 
                                   H("-right", [_radius], ["right"])
                                      ], ["bottom"]),
                        H("-left", [_width, _style, _color], ["left"]),
                        H("-right", [_width, _style, _color], ["right"]),
                        H("-break", [_width, _style, _color, 
                                     H("close")], ["break"]), 
                        H("-collapse: ", [
                                          H("collapse"),
                                          H("separate")
                                          ], ["collapse"]),
                        H("-spacing: ", [], ["spacing"])
                        ])
    
def _get_background():
    H = hintnode.HintNode
    halign = [H("left"), H("center"), H("right")]
    background_position = halign+[
        H("xpos", [], ["X position"]), 
        H("ypos", [], ["Y position"]), 
        H("initial"), H("inherit")]
    background_box = [
            H("border-box", [], ["border box"]), 
            H("padding-box", [], ["padding box"]),
            H("border-box", [], ["border box"]),
                     ]
    return H("background", [
#     return H("background %(t)s%(tt)d", [
        H("-image: ", [
            H("url", [], ["Earl", "URL"]),        
            H("none"),                    
                    ], ["image"]),                                         
        H("-position: ", [
            H("top ", halign),          
            H("center ", halign),
            H("bottom ", halign),
                       ]+background_position, ["position"]),
        H("-size: ", [H("auto"), H("cover"), H("contain")], ["size"]),
        H("-repeat: ", [
            H("repeat"), 
            H("repeat-x", [], ["repeat X"]),
            H("repeat-y", [], ["repeat Y"]),
            H("no-repeat", [], ["no repeat"]),
                     ], ["repeat"]),
        H("-attachment: ", [
            H("scroll"),
            H("fixed")            
                         ], ["attachment"]),
        H("-origin: ", background_box, ["origin"]),
        H("-clip: ", background_box + [ H("no-clip", [], ["no clip"])], ["clip"]),
        H("-color: ", [
            H("COLOR", [], ["color"]), 
            H("transparent"), 
                    ], ["color"]),
        H("-break: ", [
            H("bounding-box", [], ["bounding box"]), 
            H("each-box", [], ["each box"]),
            H("continuous"),  
                    ], ["break"]),
                                ], ["background"])











    
    