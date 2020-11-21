import os
import sys
from dragonfly import FuncContext
from castervoice.lib.context import AppContext

def is_windows():
    return sys.platform == "win32"

def is_macos():
    return sys.platform == "darwin"

def is_linux():
    return sys.platform.startswith("linux")

def is_x11():
    return os.environ.get("XDG_SESSION_TYPE") == "x11"

WINDOWS_CONTEXT = FuncContext(is_windows)
MACOS_CONTEXT = FuncContext(is_macos)
LINUX_CONTEXT = FuncContext(is_linux)
X11_CONTEXT = FuncContext(is_x11)

TERMINAL_CONTEXT = AppContext(executable=[
    "\\sh.exe",
    "\\bash.exe",
    "\\cmd.exe",
    "\\mintty.exe",
    "\\powershell.exe",
    "gnome-terminal"
    ])

JETBRAINS_CONTEXT = AppContext(executable="idea", title="IntelliJ") \
          | AppContext(executable="idea64", title="IntelliJ") \
          | AppContext(executable="studio64") \
          | AppContext(executable="pycharm")

DIALOGUE_CONTEXT = AppContext(title=[
        "open",
        "save",
        "select",
    ])
