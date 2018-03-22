from dragonfly import (AppContext, Dictation, Function, Grammar, Key, Repeat,
                       Text)

from caster.lib import control, settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R
from caster.lib.utilities import command_or_key_nexus as send


def findNthToken(text, n, direction):
    Key("c-f").execute()
    Text("%(text)s").execute({"text": text})
    if direction == "reverse":
        print("yeah? %(n)d")
        Key("s-enter:%(n)d").execute()
    else:
        Key("enter:%(n)d").execute()
        print("no? %(n)d")
    Key('escape').execute()


class VisualStudioCodeRule(MergeRule):
    pronunciation = "visual studio code"

    mapping = {
        # File management
        "select all":
            R(Function(send, key="c-a", cmd="editor.action.selectAll"),
              rdescript="Select All"),
        "[open] command palette":
            R(Function(send, key="c-p", cmd="workbench.action.showCommands"),
              rdescript="Visual Studio Code: Command Palette"),
        "(open [file] | go to [tab]) [<text>]":
            R(Function(send, key="c-p", cmd="workbench.action.quickOpen") +
              Text("%(text)s"),
              rdescript="Visual Studio Code: Go To File"),
        "close tab":
            R(Function(send, key="c-w", cmd="workbench.action.closeWindow"),
              rdescript="Visual Studio Code: Close Tab"),
        "save file":
            R(Function(send, key="c-s", cmd="workbench.action.files.save"),
              rdescript="Visual Studio Code: Save File"),
        "save and close":
            R(Function(
                send,
                key="c-s/10, c-w",
                cmd="workbench.action.files.save, workbench.action.closeActiveEditor"),
              rdescript="Visual Studio Code: Save And Close File"),

        # Search
        "(search | find in) [all] (files | codebase)":
            R(Function(send, key="cs-f", cmd="workbench.action.findInFiles"),
              rdescript="Visual Studio Code: Find in Codebase"),
        "(search | find) [file]":
            R(Function(send, key="c-f", cmd="actions.find"),
              rdescript="Visual Studio Code: Find in File"),
        "(find | jump [to]) next select":
            R(Function(send, key="f7", cmd="editor.action.wordHighlight.next"),
              rdescript="Visual Studio Code: Go to Next Symbol Highlighted"),
        "(find | jump [to]) previous select":
            R(Function(send, key="s-f7", cmd="editor.action.wordHighlight.prev"),
              rdescript="Visual Studio Code: Go to Previous Symbol Highlighted"),
        "build workspace symbols":
            R(Function(send, key="", cmd="python.buildWorkspaceSymbols"),
              rdescript="Visual Studio Code: Build Workspace Symbols"),
        "(find | jump [to]) next <text>":
            R(Function(findNthToken, n=1, direction="forward"),
              rdescript="Visual Studio Code: Find Next"),
        "(find | jump [to]) previous <text>":
            R(Function(findNthToken, n=1, direction="reverse"),
              rdescript="Visual Studio Code: Find Previous"),

        # Tab Management
        "nexta [<n>]":
            R(Function(send, key="c-pgdown", cmd="workbench.action.nextEditor"),
              rdescript="Visual Studio Code: Next Tab") * Repeat(
                  extra="n"
              ),  # These would be next and previous tab but i have a conflict with chrome
        "prexta [<n>]":
            R(Function(send, key="c-pgup", cmd="workbench.action.previousEditor"),
              rdescript="Visual Studio Code: Previous Tab") * Repeat(extra="n"),
        "close tab":
            R(Function(send, key="c-f4", cmd="workbench.action.closeActiveEditor"),
              rdescript="Visual Studio Code: Close Tab"),
        "exit preview":
            R(Function(send, key="space, c-z", cmd=""),
              rdescript="Visual Studio Code: Exit Preview"),

        # Moving Around a File
        "(go to | jump | jump to) line <n>":
            R(Function(send, key="c-g", cmd="workbench.action.gotoLine") + Text("%(n)d") +
              Key("enter"),
              rdescript="Visual Studio Code: Go to Line"),
        "go to definition":
            R(Function(send, key="f12", cmd="editor.action.goToDeclaration"),
              rdescript="Visual Studio Code: Go to Definition"),
        "go to type definition":
            R(Function(send, key="", cmd="editor.action.goToTypeDefinition"),
              rdescript="Visual Studio Code: Go to Type Definition"),
        "go to required definition":
            R(Function(send, key="c-f12:2, c-right:5, left/50, f12", cmd=""),
              rdescript="Visual Studio Code: Go to Required Definition"),
        "go to (top | first line)":
            R(Function(send, key="c-home", cmd="workbench.action.terminal.scrollToTop"),
              rdescript="Visual Studio Code: Go to Top"),
        "go to (bottom | last line)":
            R(Function(send, key="c-end", cmd="cursorBottom"),
              rdescript="Visual Studio Code: Go to Bottom"),
        "ee-ol":
            R(Function(send, key="end", cmd="cursorEnd"),
              rdescript="Visual Studio Code: End Of Line"),
        "beol":
            R(Function(send, key="home", cmd="cursorHome"),
              rdescript="Visual Studio Code: Beginning of Line"),
        "go back [<n>]":
            R(Function(send, key="a-left", cmd="workbench.action.navigateBack"),
              rdescript="Visual Studio Code: Go Back") * Repeat(extra="n"),
        "go forward [<n>]":
            R(Function(send, key="a-right", cmd="workbench.action.navigateForward"),
              rdescript="Visual Studio Code: Go Forward") * Repeat(extra="n"),

        # Formatting
        "indent [<n>]":
            R(Function(send, key="tab", cmd="editor.action.indentLines"),
              rdescript="Visual Studio Code: Indent") * Repeat(extra="n"),
        "unindent [<n>]":
            R(Function(send, key="s-tab", cmd="outdent"),
              rdescript="Visual Studio Code: Unindent") * Repeat(extra="n"),
        "comment":
            R(Function(send, key="c-slash", cmd="editor.action.commentLine"),
              rdescript="Visual Studio Code: Line Comment"),
        "block comment":
            R(Function(send, key="sa-a", cmd="editor.action.blockComment"),
              rdescript="Visual Studio Code: Block Comment"),

        # Window Management
        "[toggle] full screen":
            R(Function(send, key="f11", cmd="workbench.action.toggleFullScreen"),
              rdescript="Visual Studio Code: Fullscreen"),
        "[toggle] zen mode":
            R(Function(send, key="c-k/3, z", cmd="workbench.action.toggleZenMode"),
              rdescript="Visual Studio Code: Zen Mode"),

        # Debugging
        "[toggle] breakpoint":
            R(Function(send, key="f9", cmd="editor.debug.action.toggleBreakpoint"),
              rdescript="Visual Studio Code: Breakpoint"),
        "step over [<n>]":
            R(Function(send, key="f10/50", cmd="workbench.action.debug.stepOver") *
              Repeat(extra="n"),
              rdescript="Visual Studio Code: Step Over"),
        "step into":
            R(Function(send, key="f11", cmd="workbench.action.debug.stepInto"),
              rdescript="Visual Studio Code: Step Into"),
        "step out [of]":
            R(Function(send, key="s-f11", cmd="workbench.action.debug.stepOut"),
              rdescript="Visual Studio Code: Step Out"),
        "resume":
            R(Function(send, key="f5", cmd="workbench.action.debug.start"),
              rdescript="Visual Studio Code: Resume"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": "", "text": ""}


#---------------------------------------------------------------------------
context = AppContext(executable="code")
grammar = Grammar("Visual Studio Code", context=context)
if settings.SETTINGS["apps"]["visualstudiocode"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(VisualStudioCodeRule())
    else:
        rule = VisualStudioCodeRule(name="visualstudiocode")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
