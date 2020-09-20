import os
import sys
from dragonfly import FuncContext
from castervoice.lib.context import AppContext

WINDOWS_CONTEXT = FuncContext(lambda: sys.platform == "win32")
MACOS_CONTEXT = FuncContext(lambda: sys.platform == "darwin")
LINUX_CONTEXT = FuncContext(lambda: sys.platform.startswith("linux"))
X11_CONTEXT = FuncContext(lambda: os.environ.get("XDG_SESSION_TYPE") == "x11")

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
        "Open Project",
        "Choose Directory"
    ])
