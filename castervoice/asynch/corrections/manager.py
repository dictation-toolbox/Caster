"""
Manager for the corrections window. This module runs in the 
Caster process. Its primary purpose is to initialize, manage, and communicate
with the process that is actively displaying the window.

The new process is initialized using multiprocessing.
It is initialized as caster starts so there is no startup cost
at the time the user asks to display the window.
The window can be reused so the process never has to stop.
"""
import threading
from castervoice.lib import control
from castervoice.lib.context import paste_string_without_altering_clipboard
from castervoice.lib import settings
from dragonfly import Pause, Window
from multiprocessing import get_context, Process, Pipe
from .process import window_manager

GRAMMAR_ENABLED = False

def choice_grammar_enabled():
    return GRAMMAR_ENABLED

def set_enabled(enabled: bool):
    global GRAMMAR_ENABLED
    GRAMMAR_ENABLED = True

# If the user hasn't made a selection in 15 seconds,
# instruct the subprocess to hide the remedy window.
WAIT_FOR_CHOICE_TIMEOUT = 15

# Instruct the multi- processing library to use pythonw
# for spawning tasks. Otherwise it tries to boot new copy of DNS.
#
# TODO: This shouldn't run at the script level

# Caster probably has some initialization hooks to use instead
# The setting needs only be set once, even if we use this
# structure for other async commands (eg the mouse grids)
pythonw = settings.settings(["paths", "PYTHONW"])
get_context("spawn").set_executable(pythonw)

# Start a new process initialized from the window_manager function
# in the process module. All communication happens over a subprocess pipe.
(PIPE, SUB_PIPE) = Pipe()
WINDOW_PROCESS = Process(target=window_manager, args=(SUB_PIPE,))
WINDOW_PROCESS.start()


def send_choice(choice):
    """
    Instruct the corrections window process that a user choice has been selected.
    """
    PIPE.send(("SELECT CHOICE", choice))


def cancel():
    """
    Instruct the corrections window process that the user has said "cancel"
    So it can hide the window.
    """
    PIPE.send(("CANCEL", ""))


def query_user_for_choice(selected_text):
    """
    Start a thread to show the corrections window and wait for the user to
    select a choice.
    """
    threading.Thread(target=wait_for_choice, args=(selected_text,)).start()



def wait_for_choice(selected_text):
    """
    Function running in a thread to tell the subprocess module to
    show the window with the appropriate choices.
    Then wait for the window to inform us which choice the user selected,
    and replace the current selection with whatever they chose.
    Thread ends if the user doesn't make a choice within a set number of seconds.
    """
    set_enabled(True)

    while PIPE.poll():
        # It is possible there are cancel messages in the pipe
        # from the previous run. Remove them to get into a known state
        # before showing the window again.
        (message_type, message) = PIPE.recv()
        if message_type != "CANCEL":
            print("unexpected value in pipe")
    PIPE.send(("SHOW WINDOW", selected_text))

    if PIPE.poll(WAIT_FOR_CHOICE_TIMEOUT):
        (message_type, message) = PIPE.recv()
        print(f"Got a message {message_type}, {message}")
        if message_type == "CHOICE":
            paste_string_without_altering_clipboard(message)
        elif message_type == "CANCEL":
            print("Corrections dialogue closed by user")
    else:
        print("Timed out waiting for choice")
        PIPE.send(("CANCEL", ""))
    set_enabled(False)
