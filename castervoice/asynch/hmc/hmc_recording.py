import sys, os
from threading import Timer

import six
if six.PY2:
    from Tkinter import Label, Entry, Checkbutton # pylint: disable=import-error
    import Tkinter as tk # pylint: disable=import-error
else:
    from tkinter import Label, Entry, Checkbutton
    import tkinter as tk

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import settings
    from castervoice.asynch.hmc.homunculus import Homunculus


class HomunculusRecording(Homunculus):
    def get_row(self, cut_off=0):
        result = self.grid_row - cut_off
        self.grid_row += 1
        return result

    def __init__(self, params):
        self.grid_row = 0
        Homunculus.__init__(self, params[0])
        self.title(settings.HOMUNCULUS_VERSION + settings.HMC_TITLE_RECORDING)

        self.geometry("640x480+" + str(int(self.winfo_screenwidth()/2 - 320)) + "+" +
                      str(int(self.winfo_screenheight()/2 - 240)))
        self.instructions = "Macro Recording Options"
        Label(
            self, text=self.instructions, name="pathlabel").grid(
                row=self.get_row(), column=1, sticky=tk.E)

        wf_row = self.get_row()
        Label(
            self, text="Command Words:", name="wordlabel").grid(
                row=wf_row, column=0, sticky=tk.W)
        self.word_box = Entry(self, name="word_box")
        self.word_box.grid(row=wf_row, column=1, sticky=tk.W)

        self.repeatable = tk.IntVar()
        Checkbutton(
            self, text="Make Repeatable", variable=self.repeatable).grid(
                row=self.get_row(), column=0, sticky=tk.W)

        Label(
            self, text="Dictation History", name="optionslabel").grid(
                row=self.get_row(), column=1, sticky=tk.E)
        self.word_state = []
        cb_number = 1

        sentences = params[1].split("[s]")
        sentences.pop()
        for sentence in sentences:
            sentence_words = sentence.split("[w]")
            sentence_words.pop()
            display_sentence = " ".join(sentence_words).decode("unicode_escape")

            cb_row = 0  # self.get_row()
            cb_col = 0
            row_cut_off = 14
            col2_inc = -1
            word_state_var = tk.IntVar()

            if cb_number == 1:
                word_state_var.set(True)

            if cb_number < row_cut_off:
                cb_row = cb_row = self.get_row()
            else:
                cb_row = cb_row = self.get_row(row_cut_off + col2_inc)
                cb_col = 2
                col2_inc += 1

            Checkbutton(
                self, text="(" + str(cb_number) + ")", variable=word_state_var).grid(
                    row=cb_row, column=cb_col + 1, sticky=tk.W)
            self.word_state.append((word_state_var, cb_number))
            cb_number += 1
            Label(
                self, text=display_sentence, name="cb_label" + str(cb_number)).grid(
                    row=cb_row, column=cb_col, sticky=tk.W)

        self.cb_max = cb_number

    def xmlrpc_get_message(self):
        if self.completed:
            response = {"mode": "recording"}
            word = self.word_box.get()
            if len(word) == 0:
                self.xmlrpc_kill()
            response["word"] = word
            response["repeatable"] = self.repeatable.get()

            selected_indices = []
            for ws in self.word_state:
                if ws[0].get() == 1:
                    selected_indices.append(ws[1] - 1)
            response["selected_indices"] = selected_indices

            Timer(1, self.xmlrpc_kill).start()
            self.after(10, self.withdraw)
            return response
        else:
            return None

    def check_boxes(self, details):
        for box_index in details:
            if box_index >= 1 and box_index <= self.cb_max:
                self.word_state[box_index - 1][0].set(self.word_state[box_index
                                                                      - 1][0].get() == 0)

    def check_range_of_boxes(self, details):
        box_index_from = details[0] - 1
        box_index_to = details[1] - 1
        for i in range(0, self.cb_max):
            if i <= self.cb_max:
                self.word_state[i][0].set(i >= box_index_from and i <= box_index_to)

    def xmlrpc_do_action(self, action, details=None):
        '''acceptable keys are numbers and w and p'''
        if action == "check":
            self.check_boxes(details)
        elif action == "focus":
            if details == "word":
                self.word_box.focus_set()
        elif action == "check_range":
            self.check_range_of_boxes(details)
        elif action == "exclude":
            box_index = details
            if box_index >= 1 and box_index <= self.cb_max:
                self.word_state[box_index - 1][0].set(False)
        elif action == "repeatable":
            self.repeatable.set(not self.repeatable.get())
