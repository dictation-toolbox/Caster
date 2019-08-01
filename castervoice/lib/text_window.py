import ScrolledText
from Tkinter import BOTH, END, LEFT
import threading
import queue
from SimpleXMLRPCServer import SimpleXMLRPCServer

class ServerThread(threading.Thread):
    def __init__(self, queue, window):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.queue = queue
        self.window = window
        self.local_server = SimpleXMLRPCServer(("localhost", 10011), allow_none=True)
        self.local_server.register_function(self.message)
        self.local_server.register_function(self.shutdown)

    def run(self):
         self.local_server.serve_forever()

    def shutdown(self):
        self.window.exit()
        # self.local_server.shutdown()

    def message(self, msg):
        self.queue.put(str(msg))

class TextWindow(object):

    DELAY = 50

    def update_clock(self):
        text = []             
        while not self.queue.empty():
            text.append(self.queue.get())
        if text:
            self.stext.configure(state='normal')
            self.stext.delete('1.0', END)
            self.display('\n'.join(text))
        self.stext.after(self.DELAY, self.update_clock)

    def display(self, msg):
        self.stext.insert(END, msg)
        self.stext.configure(state='disabled')
        self.stext.see("end")

    def __init__(self):
        self.queue = queue.Queue()
        server_thread = ServerThread(self.queue, self)
        server_thread.start()
        self.stext = ScrolledText.ScrolledText(bg='white', height=20, state="disabled")
        self.stext.pack(fill=BOTH, side=LEFT, expand=True)
        self.stext.focus_set()
        self.stext.after(self.DELAY, self.update_clock)
        toplevel = self.stext._root()
        toplevel.attributes('-topmost', 'true')
        #toplevel.overrideredirect(True)
        toplevel.attributes('-toolwindow', 'true')
        self.stext.mainloop()

    def exit(self):
        self.stext.quit()

def run():
    TextWindow()

if __name__ == "__main__":
    run()
