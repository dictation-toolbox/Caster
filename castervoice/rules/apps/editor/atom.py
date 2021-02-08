"""
__author__ = 'LexiconCode'
Command-module for Atom
Official Site "https://atom.io/"
"""

# How long to wait for the Atom palette to load before hitting the enter key
from dragonfly import Pause, Function, Repeat, Dictation, Choice, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Text, Key

from castervoice.lib import settings, navigation
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

atom_palette_wait = 30
if settings.settings(["miscellaneous", "atom_palette_wait"]):
    atom_palette_wait = int(settings.SETTINGS["miscellaneous"]["atom_palette_wait"])


def ACP(command):
    """Utilize the Palette UI to execute commands."""
    return R(Key("cs-p") + Pause(str(atom_palette_wait)) + Text(command) + Key("enter"))

class AtomRule(MappingRule):
    """
    Commands for the Atom editor.

    `R(Key("command keys"))`
        Registers a key and label combination for use in a voice commands.
    `ACP("command name")`
        Registers an Atom Palette Command and label combination for use in voice commands.

    Spoken commands that are commented out do not have assigned default shortcut keys or
    are incompatible. The '#extra' subsection of commands are commands that fit within
    the category but are not displayed by the menu or UI Legend: '#' for not assigned,
    '##' for shortcut or functional duplicate.
    """

    mapping = {
        # Menu UI------------------------------------------------------------------------
        #File Menu
        "[open] new window":
            R(Key("cs-n")),
        "new file":
            R(Key("c-n")),
        "open file":
            R(Key("c-o")),
        "open folder":
            R(Key("cs-o")),
        "add project folder":
            R(Key("ac-o")),
        "open settings":
            R(Key("c-comma")),
        "reopen closed item":
            ACP("Reopen Closed Item"),
        "open [your] config":
            ACP("Open Your Config"),
        "open [your] int script":
            ACP("Open Your Int Script"),
        "open [your] key map":
            ACP("Open Your Key Map"),
        "open [your] snippet":
            ACP("Open Your Snippet"),
        "open [your] style sheet":
            ACP("Open your Stylesheet"),
        "save as":
            R(Key("cs-s")),
        "save all":
            ACP("Save All"),
        "close pane":
            R(Key("c-k, c-w")),
        "close pane others":
            R(Key("c-k, ca-w")),
        "close window":
            R(Key("cs-w")),
        #Extra
        #Edit Menu
        "copy path":
            R(Key("cs-c")),
        "select all":
            R(Key("c-a")),
        "[toggle] (comments | comment line)":
            R(Key("c-slash")),
        "reflow section":
            R(Key("ac-q")),
        "select encoding":
            R(Key("cs-u")),
        "[go to] line <ln1>":
            R(
                Key("c-g") + Pause(str(atom_palette_wait)) + Text("%(ln1)s") +
                Key("enter")),
        "<action> [line] <ln1> [by <ln2>]":
            R(Function(navigation.action_lines)),
        "select grammar":
            R(Key("cs-l")),
        #Lines Submenu
        "toggle out dent":
            R(Key("c-rightbrace")),
        "auto indent windows":
            ACP("Window Auto Indent"),
        "[move] line up [<n>]":
            R(Key("c-up")*Repeat(extra="n")),
        "[move] line down [<n>]":
            R(Key("c-down")*Repeat(extra="n")),
        "delete line [<n>]":
            R(Key("cs-k")*Repeat(extra="n")),
        "join line":
            R(Key("c-j")),
        #Text Submenu
        "uppercase":
            ACP("Editor Upper Case"),
        "lowercase":
            ACP("Editor Lower Case"),
        "delete sub [word] [<n>]":
            R(Key("a-backspace")*Repeat(extra="n")),
        "delete [to] previous [word] [<n>]":
            ACP("Delete to Previous Word boundary")*Repeat(extra="n"),
        "delete [to] next [word] [<n>]":
            ACP("Delete to Next Word Boundary")*Repeat(extra="n"),
        "transpose":
            ACP("Transpose"),
        #Folding Submenu
        "fold":
            R(Key("ac-lbrace")),
        "unfold":
            R(Key("ac-rightbrace")),
        "unfold all":
            R(Key("c-k, c-0, acs-rightbrace")),
        "fold [level] <n2>":
            R(Key("c-k, c-%(n2)s")),
        #Bookmarks Submenu
        "view (all | [all] bookmarks)":
            R(Key("c-f2")),
        "bookmark | book":
            R(Key("ca-f2")),
        "next (bookmark | book)":
            R(Key("f2")),
        "previous (bookmark | book)":
            R(Key("s-f2")),
        #View Menu
        "reload file":
            R(Key("ac-r")),
        "full screen":
            R(Key("f11")),
        "toggle menu bar":
            ACP("Toggle Menu Bar"),
        "increase font [size] [<n>]":
            R(Key("cs-equals")*Repeat(extra="n")),
        "decrease font [size] [<n>]":
            R(Key("cs-minus")*Repeat(extra="n")),
        "reset font [size]":
            R(Key("c-0")),
        "toggle soft wrap":
            ACP("Toggle Soft Wrap"),
        "[toggle] tree view":
            R(Key("c-backslash")),
        #Panes Submenu
        "split [pane] above":
            R(Key("c-k, up")),
        "split [pane] below":
            R(Key("c-k, down")),
        "split [pane] left":
            R(Key("c-k, left")),
        "split [pane] right":
            R(Key("c-k, right")),
        "[focus [on]] next pane":
            R(Key("c-k, c-n")),
        "[focus [on]] previous pane":
            R(Key("c-k, c-p")),
        "(focus [on] [pane] | pane) above":
            R(Key("c-k, c-up")),
        "(focus [on] [pane] | pane) below":
            R(Key("c-k, c-down")),
        "(focus [on] [pane] | pane) left":
            R(Key("c-k, c-left")),
        "(focus [on] [pane] | pane) right":
            R(Key("c-k, c-right")),
        #extras
        "[go to] pane [item] <n2>":
            R(Key("a-%(n2)s")),
        "[go to] <nrw> (tab | pane [item])":
            R(Key("a-%(nrw)s")),
        #Developer Submenu
        #"open in development mode":    R(Key("", "Open in Development Mode")),
        "run atom [specs]":
            R(Key("ac-s")),
        "run package [specs]":
            R(Key("ac-p")),
        "[toggle] developer tools":
            R(Key("ac-i")),
        #Selection Menu
        "[add] select above [<n>]":
            R(Key("ac-up")*Repeat(extra="n")),
        "[add] select below [<n>]":
            R(Key("ac-down")*Repeat(extra="n")),
        "split into lines":
            ACP("Split Into Lines"),
        "select line":
            R(Key("c-l")),
        "[select] [to] (begin | beginning) [of] line":
            ACP("Editor: Select to Beginning of Line"),
        "[select] inside brackets":
            R(Key("ac-comma")),
        #Find Menu
        "find (selection | selected)":
            R(Key("c-e")),
        "find [and] select all":
            R(Key("a-f3")),
        "[find] select next [<n>]":
            R(Key("c-d")*Repeat(extra="n")),
        "[find] select skip [this] [<n>]":
            R(Key("c-k, c-d")*Repeat(extra="n")),
        "[find] select skip next [<n>]":
            R(Key("c-d")) + R(Key("c-k, c-d")*Repeat(extra="n")),
        "find replace next":
            ACP("Find and Replace: Replace Next"),
        "find replace all":
            ACP("Find and Replace: Replace All"),
        "find buffer":
            R(Key("c-b")),
        "(find | go to) file":
            R(Key("c-p")),
        "find modified file":
            R(Key("cs-b")),
        #Packages Menu
        #Bracket Matcher Submenu
        "bracket [go to] match":
            R(Key("c-m")),
        "bracket remove [from] selection":
            R(Key("c-lbrace")),
        "close [current] tag":
            ACP("Bracket Matcher: Close Tag"),
        "bracket remove matching":
            R(Key("ac-backspace")),
        #Command Palette Submenu
        "[toggle] [command] palette":
            R(Key("cs-p")),
        #Dev Live Reload Submenu
        "reload [all] styles":
            R(Key("acs-r")),
        #Git Diff Submenu
        "move to next diff [different]":
            ACP("Move to Next Diff"),
        "move to previous diff [different]":
            ACP("Move to Previous Diff"),
        "[toggle] diff List":
            ACP("Toggle Diff List"),
        #Keybinding Resolver Submenu
        "toggle key [binding] resolver":
            ACP("Key Binding Resolver: Toggle"),
        #Markdown Preview Submenu
        "markdown preview":
            R(Key("cs-m")),
        #Extras
        "markdown copy html":
            ACP("Markdown Preview: Copy HTML"),
        "markdown toggle break on new line":
            ACP("Markdown Preview: Toggle Break On Single Newline"),
        #Package Generator Submenu
        "(make|generate) package":
            ACP("Package Generator: Generate Package"),
        "(make|generate) syntax theme":
            ACP("Package Generator: Generate Syntax Theme"),
        #Settings View Submenu
        ##"open setting":                             R(Key("c-comma")),
        "show key bindings":
            ACP("Settings View: Show Key Bindings"),
        "installed themes":
            ACP("Settings View: Installed Themes"),
        "uninstalled themes":
            ACP("Settings View: Uninstall Themes"),
        "installed packages":
            ACP("Settings View: Installed Packages"),
        "uninstalled packages":
            ACP("Settings View: Uninstalled Packages"),
        "search (packages|themes)":
            ACP("Settings View: Install Packages and Themes"),
        "update packages":
            ACP("Settings View: Check for Package Update"),
        #Snippets Submenu
        "expand snippets":
            ACP("Snippets: Expand"),
        "next snippet":
            R(Key("tab")),
        "previous snippet":
            R(Key("a-tab")),
        "available snippet":
            R(Key("as-tab")),
        #Styleguide Submenu
        "show style [guide]":
            R(Key("cs-g")),
        #Symbol
        "find symbol":
            R(Key("c-r")),
        "project symbol":
            R(Key("cs-r")),
        #Timecop Submenu
        "time cop":
            ACP("Timecop: View"),
        #Tree View Submenu
        "tree focus":
            R(Key("c-0")),
        "tree [View] [toggle] view":
            R(Key("c-backslash")),
        "tree [View] [reveal] active file":
            R(Key("cs-backslash")),
        "tree [View] [toggle] side":
            ACP("Tree View: show"),
        #Extras
        "tree show":
            ACP("Tree View: Show"),
        "tree rename":
            ACP("Tree View: Rename"),
        "tree remove":
            ACP("Tree View: Remove"),
        "tree add file":
            ACP("Tree View: Add File"),
        "tree duplicate":
            ACP("Tree View: Duplicate"),
        "tree add folder":
            ACP("Tree View: Add Folder"),
        #Whitespaces Submenu
        "remove trailing [white] spaces":
            ACP("Whitespace: Remove Trailing Whitespace"),
        "convert tabs [to] spaces":
            ACP("Whitespace: Convert Tabs to Spaces"),
        "convert spaces [to] tabs":
            ACP("Whitespace: Convert Spaces to Tabs"),
        #Open on GitHub
        "github [open] blame":
            ACP("Open on GitHub: Blame"),
        "github [open] [branch] compare":
            ACP("Open on GitHub: Branch Compare"),
        "github [open] [copy] URL":
            ACP("Open on GitHub: Copy URL"),
        "github [open] file":
            ACP("Open on GitHub: File"),
        "github [open] history":
            ACP("Open on GitHub: History"),
        "github [open] issues":
            ACP("Open on GitHub: Issues"),
        "github [open] repository":
            ACP("Open on GitHub: Repository"),
        #Open on GitHub
        "github close different":
            ACP("GitHub: Close All Diff Views"),
        "github empty different":
            ACP("GitHub: Close Empty Diff Views"),
        "github [show waterfall] diagnostics":
            ACP("GitHub:Okay Show Waterfall Diagnostics"),
        "github [open] (issues | pull request)":
            ACP("GitHub: Open Issue or Pull Request"),
        "github view staged changes [for current file]":
            ACP("GitHub: View Staged Changes for Current File"),
        "github view unstaged changes [for current file]":
            ACP("GitHub: View Unstaged Changes for Current File"),
        #Open on GitHub
        "github pull":
            R(Key("a-g, s-f")),
        "github push":
            R(Key("a-g, p")),
        "github clone":
            R(Key("a-g, equal")),
        "github fetch":
            R(Key("a-g, f")),
        "github logout":
            ACP("GitHub: Logout"),
        "github force push":
            R(Key("a-g, s-p")),
        "github tab [toggle]":
            R(Key("c-8")),
        "github focus [tab]":
            R(Key("c-9")),
        # Atom Development
        "dev (restart | reload) [atom]":
            ACP("Window: Reload"),

        # ----Atom Optional Third-Party Packages and Dependencies-----------------------------------------------------------------------------
        #Install through command prompt, Atom install manager or a .bat file at http://tinyurl.com/Atom-Dependencies
        # pip install --upgrade autopep8T
        # apm install project-sidebar
        # apm install project-manager
        # apm install git-plus
        # apm install script
        # apm install atom-beautify
        # apm install goto-last-edit
        # apm install tab-numbers
        # apm install menu-manager
        # apm install string-looper
        # apm install toggle-quotes
        # apm install delete-Plus
        # apm install expand-selection-to-quotes
        # apm install highlight-selected
        # apm install sublime-style-column-selection

        #Atom Third-Party Package Commands-------------------------------------------------------------------------------------------------
        #Atom Beautify
        "beautify editor":
            ACP("Atom Beautify: Beautify Editor"),
        "beautify migrate settings":
            ACP("Atom Beautify: Migrate Settings"),
        "beautify debug editor":
            ACP("Atom Beautify: Help Debug Editor"),
        #Toggle Quotes
        "toggle quotes":
            R(Key("cs-apostrophe")),
        #Script
        "script run":
            ACP("Script: Run"),
        "script [run] options":
            ACP("Script: Run Options"),
        "script [run] profile":
            ACP("Script: Run With Profile"),
        "script run [by] line":
            ACP("Script: Run By Line Number"),
        "script kill [process]":
            ACP("Script: Kill Process"),
        "script close view":
            ACP("Script: Close View"),
        "script copy [run] [results]":
            ACP("Script: Copy Run Results"),
        #"script close window and stop script":     ACP("Script: Close Window and Stop Script"),
        #Delete Plus
        "delete words":
            ACP("Delete Plus: Delete"),
        #Last Edit
        "back edit":
            R(Key("c-i")),
        "next edit":
            R(Key("ca-i")),
        #Looper
        #"cursor loud|capitalize [<n3>]":           R(Key("a-down") * Repeat(extra="n")), # Not fully implemented
        #"cursor camel [<n4>]":                     R(Key("a-down") * Repeat(extra="n")), # Not fully implemented
        #"cursor lowercase [<n5>]":                 R(Key("a-down") * Repeat(extra="n")), # Not fully implemented
        "looping down cursor":
            R(Key("a-down")),
        "looping up cursor":
            R(Key("a-up")),
        "looping up":
            R(Key("wa-up")),
        #Git Plus
        "git (custom|run)":
            ACP("Git Plus: Run"),
        "git log":
            ACP("Git Plus: Log"),
        "git log current [file]":
            ACP("Git Plus: Log Current File"),
        "git status":
            ACP("Git Plus: Status"),
        "git show":
            ACP("Git Plus: Show"),
        "git tags":
            ACP("Git Plus: Tags"),
        "git open changed files":
            ACP("Git Plus: Git Open Changed Files"),
        "git checkout [branch|tag]":
            ACP("Git Plus: Checkout"),
        "git menu":
            ACP("Git Plus: Menu"),
        "git pull":
            ACP("Git Plus: Pull"),
        "git pull [using] rebase":
            ACP("Git Plus: Pull Using Rebase"),
        "git push":
            ACP("Git Plus: Push"),
        "git commit":
            ACP("Git Plus: Commit"),
        "git commit amend":
            ACP("Git Plus: Commit Amend"),
        "git merge":
            ACP("Git Plus: Merge"),
        "git merge remote":
            ACP("Git Plus: Merge Remote"),
        "git diff":
            ACP("Git Plus: Diff"),
        "git diff all":
            ACP("Git Plus: Diff All"),
        "git add":
            ACP("Git Plus: Add"),
        "git add all":
            ACP("Git plus: Add All"),
        "git add [and] commit":
            ACP("Git Plus: Add And Commit"),
        "git add all [and] commit":
            ACP("Git Plus: Add All and Commit"),
        "git add all commit [and] push":
            ACP("Git Plus: Add All Commit And Push"),
        "git new branch":
            ACP("Git Plus: New Branch"),
        "git (rm|remove)":
            ACP("Git Plus: Remove"),
        #Project Manager
        "project manager [list]":
            ACP("Project Manager:List"),
        "project manager save":
            ACP("Project Manager:Save Project"),
        "project manager edit":
            ACP("Project Manager:Edit Project"),
        #Menu Sidebar
        "[project manager] sidebar":
            ACP("Project Sidebar: Toggle"),
        #Expand Selection to Quotes
        "(expand|fill) quotes":
            R(Key("c-apostrophe")),
        #Auto Complete
        "auto [complete]":
            R(Key("c-space")),
        #Highlight Selected---- #Placeholder
        #Sublime Style Column Selection---- #Placeholder

        #Atom | Dragonfly Development--------------------------------------------------------------------------------------------------------------------------------------------------------
        # Template to create more commands. Documentation: https://dragonfly.readthedocs.org/en/latest/actions.html and http://castervoice.readthedocs.io/en/latest/castervoice/doc/Intro/
        # Used for basic key shortcuts
        #"text for voice command":               R(Key("modifier-key", "program name: command name/description")),
        #"":                                     R(Key("")),
        # Used for command that utilizes the "command palette" shortcut in the absence of assigned keyboard shortcut.
        #"text for voice command":               ACP("text as described in command palette", "command name/description"),
        #"":                                     ACP(""),
        #Atom Shortcut Snippets
        "dev keys [input] [<n>]":
            R(Text('#"": R(Key("-"),') + Key("enter"))*Repeat(extra="n"),
        "dev [command] palette [<n>]":
            R(Text('#"": ACP(""),') + Key("enter"))*Repeat(extra="n"),
        #Repeatable Snippets
        "dev numb keys [input] [<n>]":
            R(Text('#" [<n>]": R(Key("-") * Repeat(extra="n"),') + Key("enter"))*
            Repeat(extra="n"),
        "dev numb [command] palette [<n>]":
            R(Text('#" [<n>]": ACP("") * Repeat(extra="n"),') + Key("enter"))*
            Repeat(extra="n"),
        #Basic Dragonfly Snippets
        "dev key [<n>]":
            R(Text('"": Key(""),'))*Repeat(extra="n"),
        "dev text [<n>]":
            R(Text('"": Text(""),'))*Repeat(extra="n"),
        "send command [<n>]":
            R(Text('"": R(Function(SendJsonCommands, a_command=""), rdescript=""),'))*
            Repeat(extra="n"),
    }

    extras = [
        Dictation("text"),
        Dictation("mim"),
        ShortIntegerRef("n", 1, 50),
        ShortIntegerRef("ln1", 1, 50000),
        ShortIntegerRef("ln2", 1, 50000),
        ShortIntegerRef("n2", 1, 10),
        Choice("action", navigation.actions),
        Choice(
            "nrw", {
                "first": 1,
                "second": 2,
                "third": 3,
                "fourth": 4,
                "fifth": 5,
                "sixth": 6,
                "seventh": 7,
                "eighth": 8,
                "(ninth | last)": 9,
            }),
    ]
    defaults = {
        "n": 1,
        "ln2": "",
        "mim": "",
    }


def get_rule():
    return AtomRule, RuleDetails(name="atom", executable="atom", title="Atom")
