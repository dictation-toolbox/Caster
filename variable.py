#http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
import Tkinter as tk

class App:
    
    
    def move_to_top(self,name):
        self.all_names.remove(name)
        self.all_names=[name]+self.all_names
    
    def __init__(self):
        self.all_names=[]
        
        root = tk.Tk()
        root.bind_all("1", self.woot)
        label1 = tk.Label(text="Label 1", name="label1")
        label2 = tk.Label(text="Label 2", name="label2")
        entry1 = tk.Entry(name="entry1")
        entry2 = tk.Entry(name="entry2")
        label1.pack()
        label2.pack()
        entry1.pack()
        entry2.pack()
        root.mainloop()

    def woot(self, event):
        print "woot!", event.widget

app=App()