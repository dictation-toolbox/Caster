from collections import namedtuple
from ctypes import *
import re

from PIL import ImageGrab

from lib import paths, utilities
from lib.display import TkTransparent


# things to fix: _general, 
class LegionScanner:
    def __init__(self):
        # setup dll
        self.tirg_dll =None
        self.setup_dll()
        self.last_signature=None

    def setup_dll(self):
        self.tirg_dll = cdll.LoadLibrary(paths.DLL_PATH + "tirg-dll.dll")
        self.tirg_dll.getTextBBoxesFromFile.argtypes = [c_char_p, c_int, c_int]
        self.tirg_dll.getTextBBoxesFromFile.restype = c_char_p
        self.tirg_dll.getTextBBoxesFromBytes.argtypes = [c_char_p, c_int, c_int]
        self.tirg_dll.getTextBBoxesFromBytes.restype = c_char_p
        
    def tirg_scan(self, img):
        bbstring=self.tirg_dll.getTextBBoxesFromBytes(img.tobytes(), img.size[0], img.size[1])
        self.last_signature=re.sub("[^0-9,]", "", bbstring)
        
    def do_scans(self):
        img = ImageGrab.grab()
        self.tirg_scan(img)

class LegionDisplay(TkTransparent):
    def __init__(self, name):
        TkTransparent.__init__(self, name, namedtuple("test", "width height x y")(width=400,height=300, x=0, y=0))
    
if __name__ == "__main__":
    ld=LegionDisplay("Legion Display")
    
