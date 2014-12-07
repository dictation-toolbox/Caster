from ctypes import *
import getopt
import re
import sys
import threading

from PIL import ImageGrab


try:
    from asynch.bottleserver import BottleServer
    from lib import paths
    from lib.display import TkTransparent
except ImportError:
    BASE_PATH = r"C:\NatLink\NatLink\MacroSystem"
    sys.path.append(BASE_PATH)
    from asynch.bottleserver import BottleServer
    from lib import paths
    from lib.display import TkTransparent

LEGION_LISTENING_PORT = 1340

class Rectangle:
    top = None
    bottom = None
    left = None
    right = None

class LServer(BottleServer):
    def __init__(self, tk, draw_fn):
        global LEGION_LISTENING_PORT
        
        # TiRG 
        self.has_tirg_update = False
        self.tirg_rectangles = None
        self.most_recent_tirg_scan = None
        
        self.draw_fn = draw_fn
        self.tk = tk
        
        BottleServer.__init__(self, LEGION_LISTENING_PORT)
    
    def receive_initial_data(self, tirg=None, rex=None):
        data = {}
        if tirg != None:
            data["data_tirg"] = tirg
            self.has_tirg_update = True
        if rex != None:
            data["data_rex"] = rex
        if tirg != None or rex != None:
            data["redraw"] = True
        with self.lock:
            self.incoming.append(data)
        self.process_requests()
        # self.tk.after() doesn't work here because self.mainloop() hasn't been called yet
        if tirg != None or rex != None:
            self.draw_fn()
    
    def receive_request(self):
        BottleServer.receive_request(self)
        self.process_requests()
    
    def process_requests(self):
        '''takes most recent scan result and makes it ready to be read by grid app, then discards everything'''
        do_redraw = False
        
        with self.lock:
            self.has_tirg_update = False
            tirg_string = None
            ts_len = len(self.incoming)
            if ts_len > 0:
                # loop through all requests
                for k in range(0, ts_len):
                    if "data_tirg" in self.incoming[k]:
                        tirg_string = self.incoming[k]["data_tirg"]
                        self.has_tirg_update = True
                    if "redraw" in self.incoming[k]:
                        do_redraw = True
            if self.has_tirg_update:
                if tirg_string.endswith(",") :
                    tirg_string = tirg_string[:-1]
                tirg_list = tirg_string.split(",")
                self.tirg_rectangles = []
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
                        
            self.incoming = []
        
        if do_redraw:
            self.tk.after(10, self.draw_fn)

class LegionGrid(TkTransparent):
    def __init__(self, grid_size=None, tirg=None, auto_quit=False):
        '''square_size is an integer'''
        TkTransparent.__init__(self, "legiongrid", grid_size)
        self.attributes("-alpha", 0.7)
        self.server = LServer(self, self.draw)
        '''mode information:
        t = tirg mode
        e = rex mode
        x = exit
        '''
        self.mode = ""  # null-mode
        self.digits = ""
        self.allowed_characters = r"[tex0-9]"
        self.auto_quit = auto_quit
        
        self.tirg_positions = {}
        self.server.receive_initial_data(tirg=tirg, rex=None)
        
        self.mainloop()
        
    
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
        self.mode=""
        self.digits=""
    
    def draw(self):
        if self.server.has_tirg_update:
            ''' or self.server.has_rect_update'''
            self.pre_redraw()
            self.draw_tirg_squares()
        self.unhide()
        
    def draw_tirg_squares(self):
        ''''''
        font = "Arial 12 bold"
        fill_inner = "Red"
        fill_outer = "Black"
        rect_num = 0
        with self.server.lock:
            for rect in self.server.tirg_rectangles:
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
                
                self.tirg_positions[label] = (center_x, center_y)
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
