'''
Created on May 30, 2015

@author: dave
'''
from caster.lib.dfplus.hint import hintnode
    

def getCSSNode():
    H = hintnode.HintNode
    css_sections = []
    css_sections.append(_get_background())
#     css_sections.append(_get_border())
    css_sections.append(_get_box_shadow())
#     css_sections.append(_get_font())
    
    return H("css", css_sections)

def _get_box_model():
    H = hintnode.HintNode
    return H("", [
                  H("clear: ", [
                                H("left"), 
                                H("right"), 
                                H("both"), 
                                H("none") 
                                ], ["clear"]),
                  H("display: ", [
                                  H("none"),H("in line"),H("block"),
                                  H("inline-block", [], ["in line block"]),
                                  H("run-in", [], ["run in"]),
                                  H("list-item", [], ["list item"]),
                                  H("compact"),H("table"),
                                  H("inline-table", [], ["in line table"]),      
                                  H("table-row-group", [], ["table row group"]),
                                  H("table-footer-group", [], ["table footer group"]), 
                                  H("table-row", [], ["table row"]),
                                  H("table-column-group", [], ["table column group"]),
                                  H("table-column", [], ["table column"]),
                                  H("table-cell", [], ["table cell"]),
                                  H("table-caption", [], ["table caption"]),
                                  H("ruby"),
                                  H("ruby-base", [], ["ruby base"]),
                                  H("ruby-text", [], ["ruby text"]),
                                  H("ruby-base-group", [], ["ruby base group"]),
                                  H("ruby-text-group", [], ["ruby text group"])
                                  ], ["display"]),  
                  
                  
                  
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
                      ], ["font"]),     

def _get_box_shadow():
    H = hintnode.HintNode
    return H("box-shadow: ", [
                              H("inset"), 
                              H("none"), 
                              H("COLOR", [], ["color"])
                              ], ["box shadow"])
    
def _get_border():
    H = hintnode.HintNode
    _width = H("-width: ", [H("thin"), H("medium"), H("thick")], ["width"])
    
    _style = H("-style: ", [H("none"),H("hidden"),H("dotted"),H("dashed"),   
                    H("solid"),H("double"),H("groove"),H("ridge"),
                    H("inset"),H("outset"),      
                    ], ["style"])
    
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
                                     H("close")], ["break"])
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











    
    