
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
    from caster.lib import settings

class StatusWindow(TkTransparent):
    def __init__(self):
        
        TkTransparent.__init__(self, "caster_status_window", None, False)
        self.dimensions=Dimensions(300, 200, self.winfo_screenwidth()-300, self.winfo_screenheight()-200)
        self.wm_geometry(self.get_dimensions_string())
#         self._canvas.destroy()
        self.v = StringVar()
        self.v.set("Caster Status Window")
        self.label = tk.Label(self, textvariable=self.v)
        
        self.grip = tk.Label(self, bitmap="gray25", height=100, width=40, background="green")
        self.grip.pack(side="left", fill="y")
        self.label.pack(side="right", fill="both", expand=True)

        self.grip.bind("<ButtonPress-1>", self.StartMove)
        self.grip.bind("<ButtonRelease-1>", self.StopMove)
        self.grip.bind("<B1-Motion>", self.OnMotion)
        
        self.mainloop()

    def setup_XMLRPC_server(self):
        self.server_quit = 0
        self.server = SimpleXMLRPCServer(("127.0.0.1", settings.STATUS_LISTENING_PORT), allow_none=True)
        self.server.register_function(self.xmlrpc_kill, "kill")
        self.server.register_function(self.xmlrpc_text, "text")
     
    def xmlrpc_text(self, text):
        self.after(10, lambda: self.v.set(text))
    
    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))


if __name__ == '__main__':
    app = StatusWindow()