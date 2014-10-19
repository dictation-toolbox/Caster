import os, sys

from PIL import ImageGrab

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
    img = ImageGrab.grab()
    if not os.path.exists(paths.LEGION_SIGNATURE_PATH):
        os.makedirs(paths.LEGION_SIGNATURE_PATH)
    signature_path = paths.LEGION_SIGNATURE_PATH + utilities.current_time_to_string() + ".png"
    img.save(signature_path)
    sig = Signature(img)
    LAST_SIGNATURE = sig
    
def compare_signatures():
    print ""
    
