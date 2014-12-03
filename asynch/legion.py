from ctypes import *
import re
import threading

from PIL import ImageGrab

from lib import paths

class LegionScanner:
    def __init__(self):
        # setup dll
        self.tirg_dll = None
        self.setup_dll()
        
        self.lock = threading.Lock()
        self.last_signature = None
        self.screen_has_changed = False

    def setup_dll(self):
        self.tirg_dll = cdll.LoadLibrary(paths.DLL_PATH + "tirg-dll.dll")
        self.tirg_dll.getTextBBoxesFromFile.argtypes = [c_char_p, c_int, c_int]
        self.tirg_dll.getTextBBoxesFromFile.restype = c_char_p
        self.tirg_dll.getTextBBoxesFromBytes.argtypes = [c_char_p, c_int, c_int]
        self.tirg_dll.getTextBBoxesFromBytes.restype = c_char_p
        
    def tirg_scan(self, img):
        bbstring = self.tirg_dll.getTextBBoxesFromBytes(img.tobytes(), img.size[0], img.size[1])
        # clean the results in case any garbage letters come through
        result = re.sub("[^0-9,]", "", bbstring)
        return result
        
    def scan(self):
        img = ImageGrab.grab()
        result=self.tirg_scan(img)
        if result != self.last_signature:
            with self.lock:
                self.last_signature = result
                self.screen_has_changed = True
        # do rectangle scans here
        
    def get_update(self):
        with self.lock:
            if self.screen_has_changed:
                self.screen_has_changed=False
                return (self.last_signature, None)#None should be replaced with rectangle scan results
            else:
                return None
