
from Tkinter import StringVar
import sys

import Tkinter as tk


try: # Style C -- may be imported into Caster, or externally
    BASE_PATH = "C:/NatLink/NatLink/MacroSystem/"
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    import SimpleXMLRPCServer
    from SimpleXMLRPCServer import *
    from caster.asynch.mouse.grids import TkTransparent, Dimensions
    from caster.lib import settings, utilities
    from caster.lib.dfplus.communication import Communicator

TITLE="caster_status_window"

class StatusWindow(TkTransparent):
    def __init__(self):
        global TITLE
        TkTransparent.__init__(self, TITLE, None, False)
        self.dimensions=Dimensions(300, 200, self.winfo_screenwidth()-300, self.winfo_screenheight()-200)
        self.wm_geometry(self.get_dimensions_string())
#         self._canvas.destroy()
        self.v = StringVar()
        self.v.set("Caster Status Window")
        self.label = tk.Label(self, textvariable=self.v)
        
        self.grip = tk.Label(self, bitmap="gray25", height=100, width=40, background="green")
        self.grip.pack(side="left", fill="y")
        self.label.pack(side="right", fill="both", expand=True)

        self.grip.bind("<ButtonPress-1>", self.start_move)
        self.grip.bind("<ButtonRelease-1>", self.stop_move)
        self.grip.bind("<B1-Motion>", self.on_motion)
        
        self.visible_messages=[]
        
        self.mainloop()

    def setup_XMLRPC_server(self):
        self.server_quit = 0
        comm = Communicator()
        self.server = SimpleXMLRPCServer(("127.0.0.1", comm.com_registry["status"]), allow_none=True)
        self.server.register_function(self.xmlrpc_kill, "kill")
        self.server.register_function(self.xmlrpc_hint, "hint")
        self.server.register_function(self.xmlrpc_text, "text")
     
    def xmlrpc_text(self, text):
        self.after(10, lambda: self.add_text(text))
    
    def add_text(self, text):
        number_of_lines = 5
        with_lines = ""
        
        while len(self.visible_messages) + 1 > number_of_lines:
            self.visible_messages.remove(self.visible_messages[0])
        self.visible_messages.append(text)
        indices=range(0, len(self.visible_messages))
        indices.reverse()
        for i in indices:
            with_lines += self.visible_messages[i]
            if i!=indices[len(indices)-1]:
                with_lines+="\n"
        self.v.set(with_lines)
    
    def xmlrpc_hint(self, text):
        self.after(10, lambda: self.v.set(text))
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))

if __name__ == '__main__':
    app = StatusWindow()
