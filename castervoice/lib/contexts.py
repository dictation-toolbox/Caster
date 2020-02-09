from castervoice.lib.context import AppContext

TERMINAL_CONTEXT = AppContext(executable=[
    "\\sh.exe",
    "\\bash.exe",
    "\\cmd.exe",
    "\\mintty.exe",
    "\\powershell.exe"
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