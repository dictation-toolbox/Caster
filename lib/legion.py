import os, sys

from PIL import ImageGrab
from ctypes import *
from lib import paths, utilities

LAST_SIGNATURE = None

class Signature:
    def __init__(self, img):
        try:
            xsize, ysize = img.size
            tsize = float(xsize + ysize)
            nPointsX = int(xsize / tsize * 100)
            nPointsY = int(ysize / tsize * 100)
            xinterval = nPointsX / float(xsize)
            yinterval = nPointsY / float(ysize)
            xhalf = xinterval / 2
            yhalf = yinterval / 2
            self.data = []
            for i in range(0, nPointsX):
                x = int(i * xinterval + xhalf)
                self.data.append([])
                for j in range(0, nPointsY):
                    y = int(j * yinterval + yhalf)
                    self.data[i].append(img.getpixel((x, y)))
                    
            print "grid should be " + str(nPointsX) + " by " + str(nPointsY) + " :: it is " + str(len(self.data)) + " by " + str(len(self.data[0]))
        except Exception:
            utilities.report(utilities.list_to_string(sys.exc_info()))
    
    def compare(self, img):
        print ""

def get_screen_signature():
    global LAST_SIGNATURE
    signature_path = paths.LEGION_SIGNATURE_PATH + utilities.current_time_to_string()
    if not os.path.exists(paths.LEGION_SIGNATURE_PATH):
        os.makedirs(paths.LEGION_SIGNATURE_PATH)
    
    sw = 101
    sh = 101
    img = ImageGrab.grab(bbox=(sw, sh, sw + 300, sh + 225))
    sig = Signature(img)
    LAST_SIGNATURE = sig
    
    # write raw bytes to file
    with open(signature_path, 'wb') as f:
        f.write(img.tobytes())
    
    # setup dll
    tirg_dll = cdll.LoadLibrary(paths.DLL_PATH + "tirg-dll.dll")
    tirg_dll.getTextBBoxes.argtypes = [c_char_p, c_int, c_int]
    tirg_dll.getTextBBoxes.restype = c_char_p  
    tirg_dll.getTextBBoxesFromBytes.argtypes = [c_char_p, c_int, c_int]
    tirg_dll.getTextBBoxesFromBytes.restype = c_char_p  
    
    try:
        result2 = tirg_dll.getTextBBoxes(signature_path, img.size[0], img.size[1])
        print "was path returned: " + str(result2)
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))
    
def compare_signatures():
    print ""
    
