'''
Created on May 30, 2015

@author: dave
'''
from caster.lib.dfplus.hint import hintnode

class MN(hintnode.HintNode):# Measurement Node
    def __init__(self, text, extras=[], spec=None):
        children = [
             hintnode.HintNode("px", [], ["pixels"]),# %(n)d 
             hintnode.HintNode("em", [], ["EM"]),
             hintnode.HintNode("%", [], ["percent"]),
             ] + extras
        hintnode.HintNode.__init__(self, text, children, spec)
    

def getCSSNode():
    H = hintnode.HintNode
    
    background = _get_background()
    
    return H("css", [background])
    
    
def _get_background():
    H = hintnode.HintNode
    halign = [MN("left"), MN("center"), MN("right")]
    background_position = halign+[
        MN("xpos", [], ["X position"]), MN("ypos", [], ["Y position"]), H("initial"), H("inherit")]
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
            H("top ", background_position),          
            H("center ", background_position),
            H("bottom ", background_position),
                       ], ["position"]),
        MN("-size: ", [H("auto"), H("cover"), H("contain")], ["size"]),
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
        MN("-clip: ", background_box + [ H("no-clip", [], ["no clip"])], ["clip"]),
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











    
    