import SimpleXMLRPCServer
from SimpleXMLRPCServer import *
from ctypes import *
import getopt
import re
import sys
from threading import Timer
import threading

from PIL import ImageGrab




try:
    # this section only necessary if called externally to Dragon
    BASE_PATH = sys.argv[0].split("MacroSystem")[0] + "MacroSystem"
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
except Exception:
    pass

from lib import  settings
from lib.display import TkTransparent



class Rectangle:
    top = None
    bottom = None
    left = None
    right = None

def communicate():
    return xmlrpclib.ServerProxy("http://127.0.0.1:" + str(settings.LEGION_LISTENING_PORT))

class LegionGrid(TkTransparent):
    def __init__(self, grid_size=None, tirg=None, auto_quit=False):
        '''square_size is an integer'''
        self.setup_XMLRPC_server()
        TkTransparent.__init__(self, "legiongrid", grid_size)
        self.attributes("-alpha", 0.7)
        '''mode information:
        t = tirg mode
        r = retrieval
        e = rex mode
        x = exit
        '''
        self.mode = ""  # null-mode
        self.digits = ""
        self.allowed_characters = r"[trex0-9]"
        self.auto_quit = auto_quit
        
        self.tirg_positions = {}
        if tirg != None:
            self.process_rectangles(tirg)
#             self.process_rectangles("1,1,50,50")
            self.draw_tirg_squares()
        
        def start_server():
            while not self.server_quit:
                self.server.handle_request()  
        Timer(1, start_server).start()
        self.mainloop()
    
    def setup_XMLRPC_server(self): 
        self.server_quit = 0
        self.server = SimpleXMLRPCServer(("127.0.0.1", settings.LEGION_LISTENING_PORT), allow_none=True)
        self.server.register_function(self.xmlrpc_retrieve_data_for_highlight, "retrieve_data_for_highlight")
    
    def on_exit(self):
        self.server_quit = 1
        TkTransparent.on_exit(self)
    
    def process_rectangles(self, tirg_string):   
        self.tirg_rectangles = []
        if tirg_string.endswith(",") :
            tirg_string = tirg_string[:-1]
        tirg_list = tirg_string.split(",")
        curr_rect = None
        for i in range(0, len(tirg_list)):
            ii = i % 4
            if ii == 0:
                curr_rect = Rectangle()
                curr_rect.left = int(tirg_list[i])
            elif ii == 1:
                curr_rect.top = int(tirg_list[i])
            elif ii == 2:
                curr_rect.right = int(tirg_list[i])
            elif ii == 3:
                curr_rect.bottom = int(tirg_list[i])
                self.tirg_rectangles.append(curr_rect) 
    
    def key(self, e):
        if re.search(self.allowed_characters, e.char):
            if e.char == 'x':
                if self.mode == "x":
                    self.on_exit()
                self.mode = "x"
            elif e.char == 't':
                self.mode = "t"
            elif e.char == 'e':
                self.mode = "e"
            elif e.char == 'r':
                self.mode = "r"
            else:
                self.digits += e.char
                if len(self.digits) == 2:
                    self.process()
    
    def process(self):
        if self.mode == "t":
            p_index = str(int(self.digits))
            self.move_mouse(int(self.tirg_positions[p_index][0]), int(self.tirg_positions[p_index][1]))
        elif self.mode == "e":
            ''''''
        self.mode = ""
        self.digits = ""
    
    def draw(self):
        ''' or self.server.has_rect_update'''
        self.pre_redraw()
        self.draw_tirg_squares()
        self.unhide()
    
    def xmlrpc_retrieve_data_for_highlight(self, strindex):
        if strindex in self.tirg_positions:
            position_data = self.tirg_positions[strindex]
            Timer(0.01, self.on_exit).start()
            return {"l": position_data[2], "r": position_data[3], "y": position_data[1]}
        else:
            return {"err": strindex + " not in map"}
    
    def draw_tirg_squares(self):
        ''''''
        font = "Arial 12 bold"
        fill_inner = "Red"
        fill_outer = "Black"
        rect_num = 0
        for rect in self.tirg_rectangles:
            center_x = int((rect.left + rect.right) / 2)
            center_y = int((rect.top + rect.bottom) / 2)
            label = str(rect_num)
            # lines
            self._canvas.create_line(rect.left, rect.top, rect.right, rect.top, fill=fill_inner)
            self._canvas.create_line(rect.left, rect.bottom, rect.right, rect.bottom, fill=fill_inner)
            self._canvas.create_line(rect.left, rect.top, rect.left, rect.bottom, fill=fill_inner)
            self._canvas.create_line(rect.right, rect.top, rect.right, rect.bottom, fill=fill_inner)
            
            # text
            self._canvas.create_text(center_x + 1, center_y + 1, text=label, font=font, fill=fill_outer)
            self._canvas.create_text(center_x - 1, center_y + 1, text=label, font=font, fill=fill_outer)
            self._canvas.create_text(center_x + 1, center_y - 1, text=label, font=font, fill=fill_outer)
            self._canvas.create_text(center_x - 1, center_y - 1, text=label, font=font, fill=fill_outer)
            self._canvas.create_text(center_x, center_y, text=label, font=font, fill=fill_inner)
            
            # rect.left, rect.right are now being saved below for the highlight function
            self.tirg_positions[label] = (center_x, center_y, rect.left, rect.right)
            rect_num += 1










class LegionScanner:
    def __init__(self):
        # setup dll
        self.tirg_dll = None
        self.setup_dll()
        
        self.lock = threading.Lock()
        self.last_signature = None
        self.screen_has_changed = False

    def setup_dll(self):
        self.tirg_dll = cdll.LoadLibrary(settings.SETTINGS["paths"]["DLL_PATH"] + "tirg-dll.dll")
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
        result = self.tirg_scan(img)
        if result != self.last_signature:
            with self.lock:
                self.last_signature = result
                self.screen_has_changed = True
        # do rectangle scans here
        
    def get_update(self):
        with self.lock:
            if self.screen_has_changed:
                self.screen_has_changed = False
                return (self.last_signature, None)  # None should be replaced with rectangle scan results
            else:
                return None


def main(argv):
    help_message = 'legion.py -t <tirg> -d <dimensions> -a <autoquit>'
    tirg = None
    dimensions = None
    auto_quit = False
    try:
        opts, args = getopt.getopt(argv, "ht:a:d:", ["tirg=", "dimensions=", "autoquit="])
    except getopt.GetoptError:
        print help_message
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print help_message
            sys.exit()
        elif opt in ("-t", "--tirg"):
            tirg = arg
        elif opt in ("-d", "--dimensions"):
            dimensions = arg
        elif opt in ("-a", "--autoquit"):
            auto_quit = arg in ("1", "t")    
            
    lg = LegionGrid(grid_size=dimensions, tirg=tirg, auto_quit=auto_quit)

if __name__ == "__main__":
    main(sys.argv[1:])
