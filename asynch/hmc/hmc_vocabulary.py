from Tkinter import Frame, Label, Entry, Checkbutton
import sys
BASE_PATH = r"C:\NatLink\NatLink\MacroSystem"
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)
import Tkinter as tk
from asynch.hmc.homunculus import Homunculus
from lib import settings











class Homunculus_Vocabulary(Homunculus):
    '''
    classdocs
    '''
    def get_row(self, cut_off=0):
        result = self.grid_row - cut_off
        self.grid_row += 1
        return result

    def __init__(self, params):
        self.grid_row = 0
        Homunculus.__init__(self, "vocabulary")
        self.title(settings.HOMUNCULUS_VERSION + " :: Vocabulary Manager")
            
        self.mode = params[0]
        
        if self.mode == "set":
            self.geometry("640x480+" + str(int(self.winfo_screenwidth() / 2 - 320)) + "+" + str(int(self.winfo_screenheight() / 2 - 240)))
            self.instructions = "Add/Modify Word"
            Label(self, text=self.instructions, name="pathlabel").grid(row=self.get_row(), column=1, sticky=tk.E)
                      
            wf_row = self.get_row()
            Label(self, text="(W)ord:", name="wordlabel").grid(row=wf_row, column=0, sticky=tk.W)
            self.word_box = Entry(self, name="word_box")
            self.word_box.grid(row=wf_row, column=1, sticky=tk.W)
            
            p_row = self.get_row()
            Label(self, text="(P)ronunciation:", name="pronunciationlabel").grid(row=p_row, column=0, sticky=tk.W)
            self.pronunciation_box = Entry(self, name="pronunciation_box")
            self.pronunciation_box.grid(row=p_row, column=1, sticky=tk.W)
            
            
            
            Label(self, text="Options", name="optionslabel").grid(row=self.get_row(), column=1, sticky=tk.E)
            self.word_state = []
            cb_number = 1
            for state in [("Word added by user", 0x00000001),
                          ("Can't be deleted", 0x00000008),
                          ("Usually cap next (like period)", 0x00000010),
                          ("Always cap next (like Cap Next)", 0x00000020),
                          ("Uppercase next (All Caps Next)", 0x00000040),
                          ("Lowercase next (No Caps Next)", 0x00000080),
                          ("No space following (left paren)", 0x00000100),
                          ("Two spaces following (period)", 0x00000200),
                          ("No spaces between words (numbers)", 0x00000400),
                          ("Capitalization mode on (Caps On)", 0x00000800),
                          ("Uppercase mode on (All Caps On)", 0x00001000),
                          ("Lowercase mode on (No Caps On)", 0x00002000),
                          ("Space betw words off (No Space On)", 0x00004000),
                          ("Restore normal spacing (No Space Off)", 0x00008000),
                          ("Suppress period (...)", 0x00020000),
                          ("No formatting (like Cap)", 0x00040000),
                          ("No reset spacing (like Cap)", 0x00080000),
                          ("No reset caps (close quote)", 0x00100000),
                          ("No space preceeding (comma)", 0x00200000),
                          ("Restore normal caps (Caps Off)", 0x00400000),
                          ("Follow with new line (New-Line)", 0x00800000),
                          ("Follow with new-p (New-Paragraph)", 0x01000000),
                          ("Don't cap in title (like and)", 0x02000000),
                          ("Follow with extra space (space)", 0x08000000),
                          ("Word added by vocab builder.", 0x40000000)
                          
                          ]:
                cb_row = 0  # self.get_row()
                cb_col = 0
                row_cut_off = 14
                col2_inc = -1
                word_state_var = tk.IntVar()
                
                if cb_number == 1:
                    word_state_var.set(True)
                    
                if cb_number < row_cut_off:
                    cb_row = cb_row = self.get_row()
                else :
                    cb_row = cb_row = self.get_row(row_cut_off + col2_inc)
                    cb_col = 2
                    col2_inc += 1
                
                Checkbutton(self, text="(" + str(cb_number) + ")", variable=word_state_var).grid(row=cb_row, column=cb_col + 1, sticky=tk.W)
                cb_number += 1
                Label(self, text=state[0], name="cb_label" + str(cb_number)).grid(row=cb_row, column=cb_col, sticky=tk.W)
                self.word_state.append((word_state_var, state[1]))
        elif self.mode == "del":
            self.geometry("300x100+" + str(int(self.winfo_screenwidth() / 2 - 150)) + "+" + str(int(self.winfo_screenheight() / 2 - 50)))
            
            self.instructions = "Delete Word"
            Label(self, text=self.instructions, name="pathlabel").grid(row=self.get_row(), column=1, sticky=tk.E)
                      
            wf_row = self.get_row()
            Label(self, text="(W)ord:", name="wordlabel").grid(row=wf_row, column=0, sticky=tk.W)
            self.word_box = Entry(self, name="word_box")
            self.word_box.grid(row=wf_row, column=1, sticky=tk.W)
                # var.get()# will return a zero or one
#             cb_frame.grid(row=3, column=0)
        
        
        
    
    def complete(self, e):
        ''''''   

c = Homunculus_Vocabulary(["del"])
