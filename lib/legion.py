from ctypes import *
import os, sys

from PIL import ImageGrab

from lib import paths, utilities


LAST_SIGNATURE = None
TIRG_DLL = None

def setup_dll():
    TIRG_DLL = cdll.LoadLibrary(paths.DLL_PATH + "tirg-dll.dll")
    TIRG_DLL.getTextBBoxesFromFile.argtypes = [c_char_p, c_int, c_int]
    TIRG_DLL.getTextBBoxesFromFile.restype = c_char_p
    TIRG_DLL.getTextBBoxesFromBytes.argtypes = [c_char_p, c_int, c_int]
    TIRG_DLL.getTextBBoxesFromBytes.restype = c_char_p

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
    global TIRG_DLL

    # use Pillow to get screenshot
    img = ImageGrab.grab()
    sig = Signature(img)
    LAST_SIGNATURE = sig
    
    if not TIRG_DLL:
        setup_dll()    

    # get bounding boxes
    bbstring = TIRG_DLL.getTextBBoxesFromBytes(img.tobytes(), img.size[0], img.size[1])
    print "resulting string: \n" + bbstring
    
def compare_signatures():
    print "1,8,108,15,1,38,58,45,1,53,58,60,3,83,120,90"
    
