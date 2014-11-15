import os
import signal

import Tkinter as tk


# rewrite dp grid using this
class TkTransparent(tk.Tk):

    def __init__(self, name, dimensions):
        tk.Tk.__init__(self, baseName="")
        self.dimensions = dimensions
        self.overrideredirect(True)  
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.wait_visibility(self)
        self.attributes("-alpha", 0.5)
        self.wm_title(name)
        self.wm_geometry("%dx%d+%d+%d" % (self.dimensions.width, self.dimensions.height, self.dimensions.x, self.dimensions.y))
        self._canvas = tk.Canvas(master=self, width=dimensions.width, height=dimensions.height, bg='white', bd=-2)  # Border quirk, default border is 2.
        self._canvas.pack()
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.mainloop()
    
    def hide(self):
        """"""
        self.withdraw()
        
    def on_exit(self):
        self.destroy()
        os.kill(os.getpid(), signal.SIGTERM)