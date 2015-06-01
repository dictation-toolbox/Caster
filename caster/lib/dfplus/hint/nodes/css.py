'''
Created on May 30, 2015

@author: dave
'''
from caster.lib.dfplus.hint import hintnode

class MN(hintnode.HintNode):# Measurement Node
    def __init__(self, text, extras=[]):
        children = [
             hintnode.HintNode("px", [], ["pixels"]),# %(n)d 
             hintnode.HintNode("em", [], ["EM"]),
             hintnode.HintNode("%", [], ["percent"]),
             ] + extras
        hintnode.HintNode.__init__(self, text, children)
    

def getCSSNode():
    H = hintnode.HintNode
    
    background = _get_background()
    
    return H("css", [background])
    
    
def _get_background():
    H = hintnode.HintNode
    halign = [MN("left"), MN("center"), MN("right")]
    background_position = halign+[
        MN("xpos"), MN("ypos"), H("initial"), H("inherit")]
    background_box = [
            H("border-box", [], ["border box"]), 
            H("padding-box", [], ["padding box"]),
            H("border-box", [], ["border box"]),
                     ]
    return H("background %(t)s %(tt)d", [
        H("image", [
            H("url", [], ["Earl", "URL"]),        
            H("none"),                    
                    ]),                                         
        H("position", [
            H("top", background_position),          
            H("center", background_position),
            H("bottom", background_position),
                       ]),
        MN("size", [H("auto"), H("cover"), H("contain")]),
        H("repeat", [
            H("repeat"), 
            H("repeat-x", [], ["repeat X"]),
            H("repeat-y", [], ["repeat Y"]),
            H("no-repeat", [], ["no repeat"]),
                     ]),
        H("attachment", [
            H("scroll"),
            H("fixed")            
                         ]),
        H("origin", background_box),
        MN("clip", background_box + [ H("no-clip", [], ["no clip"])]),
        H("color", [
            H("COLOR", [], ["color"]), 
            H("transparent"), 
                    ]),
        H("break", [
            H("bounding-box", [], ["bounding box"]), 
            H("each-box", [], ["each box"]),
            H("continuous"),  
                    ]),
                                ], ["background [<t>] [<tt>] [toilet] Smith"])











    
    