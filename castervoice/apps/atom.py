"""
__author__ = 'LexiconCode'
Command-module for Atom
Official Site "https://atom.io/"
"""

from caster.lib import control, settings
from caster.lib.actions import Key, Text
from caster.lib.context import AppContext
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R
from dragonfly import Choice, Dictation, Grammar, Pause, Repeat

# How long to wait for the Atom palette to load before hitting the enter key
atom_palette_wait = 30
if settings.SETTINGS["miscellaneous"]["atom_palette_wait"]:
    atom_palette_wait = int(settings.SETTINGS["miscellaneous"]["atom_palette_wait"])


def ACP(command, label=None):
    """Utilize the Palette UI to execute commands."""
    if not label:
        label = "Atom: Unlabeled Palette Command: " + command
    return R(
        Key("cs-p") + Pause(str(atom_palette_wait)) + Text(command) + Key("enter"),
        rdescript=label)


def ACK(command, label=None):
    """Generate a keyboard shortcut."""
    if not label:
        label = "Atom: Unlabeled Keyboard Shortcut: " + command
    return R(Key(command), rdescript=label)


class AtomRule(MergeRule):
    """
    Commands for the Atom editor.

    `ACK("command keys", "label text")`
        Registers a key and label combination for use in a voice commands.
    `ACP("command name", "label text")`
        Registers an Atom Palette Command and label combination for use in voice commands.

    Spoken commands that are commented out do not have assigned default shortcut keys or
    are incompatible. The '#extra' subsection of commands are commands that fit within
    the category but are not displayed by the menu or UI Legend: '#' for not assigned,
    '##' for shortcut or functional duplicate.
    """

    pronunciation = "atom"

    mapping = {
        # Menu UI------------------------------------------------------------------------
        #File Menu
        "[open] new window":
            ACK("cs-n", "Atom: New Window"),
        "new file":
            ACK("c-n", "Atom: New File"),
        "open file":
            ACK("c-o", "Atom: Open File"),
        "open folder":
            ACK("cs-o", "Atom: Open Folder"),
        "add project folder":
            ACK("ac-o", "Atom: Add Project Folder"),
        "open settings":
            ACK("c-comma", "Atom: Open Settings"),
        "reopen closed item":
            ACP("Reopen Closed Item", "Atom: Reopen Last File or Tab"),
        "open [your] config":
            ACP("Open Your Config", "Atom: Open Your Config"),
        "open [your] int script":
            ACP("Open Your Int Script", "Atom: Open Your Int Script"),
        "open [your] key map":
            ACP("Open Your Key Map", "Atom: Open Your Key Map"),
        "open [your] snippet":
            ACP("Open Your Snippet", "Atom: Open Your Snippet"),
        "open [your] stylesheet":
            ACP("Open your Stylesheet", "Atom: Open Your Stylesheet"),
        "save as":
            ACK("cs-s", "Atom: Save As"),
        "save all":
            ACP("Save All", "Atom: Save All"),
        "close pane":
            ACK("c-k, c-w", "Atom: Close Pane"),
        "close pane others":
            ACK("c-k, ca-w", "Atom: Close Pane"),
        "close window":
            ACK("cs-w", "Atom: Close Window"),
        #Extra
        #Edit Menu
        "copy path":
            ACK("cs-c", "Atom: Copy Path"),
        "select all":
            ACK("c-a", "Atom: Select All"),
        "[toggle] (comments | comment line)":
            ACK("c-slash", "Atom: Toggle Comments"),
        "reflow section":
            ACK("ac-q", "Atom: Reflow Section"),
        "select encoding":
            ACK("cs-u", "Atom: Select Encoding"),
        "[go to] line <line_number>":
            R(Key("c-g") + Pause(str(atom_palette_wait)) + Text("%(line_number)s") +
              Key("enter"),
              rdescript="Atom: Go to Line #"),
        "select grammar":
            ACK("cs-l", "Atom: Select Grammar"),
        #Lines Submenu
        "toggle outdent":
            ACK("c-rightbrace", "Atom: Toggle Auto Outdent"),
        "auto indent windows":
            ACP("Window Auto Indent", "Atom: Auto Indent"),
        "[move] line up [<n>]":
            ACK("c-up", "Atom: Move Line Up #")*Repeat(extra="n"),
        "[move] line down [<n>]":
            ACK("c-down", "Atom: Move Line Down #")*Repeat(extra="n"),
        "delete line [<n>]":
            ACK("cs-k", "Atom: Delete Line or # Lines Below")*Repeat(extra="n"),
        "join line":
            ACK("c-j", "Atom: Join Line"),
        #Text Submenu
        "uppercase":
            ACP("Editor Upper Case", "Atom: Convert Uppercase"),
        "lowercase":
            ACP("Editor Lower Case", "Atom: Convert lowercase"),
        "delete sub [word] [<n>]":
            ACK("a-backspace", "Atom: Delete to End of Subword")*Repeat(extra="n"),
        "delete [to] previous [word] [<n>]":
            ACP("Delete to Previous Word boundary",
                "Atom: Delete to previous word boundary")*Repeat(extra="n"),
        "delete [to] next [word] [<n>]":
            ACP("Delete to Next Word Boundary", "Atom: Delete to next word boundary")*
            Repeat(extra="n"),
        "transpose":
            ACP("Transpose", "Atom: Transpose"),
        #Folding Submenu
        "fold":
            ACK("ac-lbrace", "Atom: Fold"),
        "unfold":
            ACK("ac-rightbrace", "Atom: Unfold"),
        "unfold all":
            ACK("c-k, c-0, acs-rightbrace", "Atom: Unfold All"),
        "fold [level] <n2>":
            ACK("c-k, c-%(n2)s", "Atom: Fold Level 1-9"),
        #Bookmarks Submenu
        "view (all | [all] bookmarks)":
            ACK("c-f2", "Atom: View All Bookmarks"),
        "bookmark | book":
            ACK("ca-f2", "Atom: Toggle Bookmark"),
        "next (bookmark | book)":
            ACK("f2", "Atom: Jump to Next Bookmark"),
        "previous (bookmark | book)":
            ACK("s-f2", "Atom: Jump to Previous Bookwork"),
        #View Menu
        "reload file":
            ACK("ac-r", "Atom: Reload File"),
        "fullscreen":
            ACK("f11", "Atom: Toggle Fullscreen"),
        "toggle menubar":
            ACP("Toggle Menu Bar", "Atom: Toggle Menubar"),
        "increase font [size] [<n>]":
            ACK("cs-equals", "Atom: Increase Font Size")*Repeat(extra="n"),
        "decrease font [size] [<n>]":
            ACK("cs-minus", "Atom: Decrease Font size")*Repeat(extra="n"),
        "reset font [size]":
            ACK("c-0", "Atom: Reset Font Size"),
        "toggle soft wrap":
            ACP("Toggle Soft Wrap", "Atom: Toggle Soft Wrap"),
        "[toggle] treeview":
            ACK("c-backslash", "Atom: Toggle Treeview"),
        #Panes Submenu
        "split [pane] above":
            ACK("c-k, up", "Atom: Split Up"),
        "split [pane] below":
            ACK("c-k, down", "Atom: Split Down"),
        "split [pane] left":
            ACK("c-k, left", "Atom: Split Left"),
        "split [pane] right":
            ACK("c-k, right", "Atom: Split Right"),
        "[focus [on]] next pane":
            ACK("c-k, c-n", "Atom: Focus Next Pane"),
        "[focus [on]] previous pane":
            ACK("c-k, c-p", "Atom: Focus Previous Pane"),
        "(focus [on] [pane] | pane) above":
            ACK("c-k, c-up", "Atom: Focused Pane Above"),
        "(focus [on] [pane] | pane) below":
            ACK("c-k, c-down", "Atom: Focus Pane Below"),
        "(focus [on] [pane] | pane) left":
            ACK("c-k, c-left", "Atom: Focus On left"),
        "(focus [on] [pane] | pane) right":
            ACK("c-k, c-right", "Atom: Focus Pane on Right"),
        #extras
        "[go to] pane [item] <n2>":
            ACK("a-%(n2)s", "Atom: Go to Pane 1-9"),
        "[go to] <nrw> (tab | pane [item])":
            ACK("a-%(nrw)s", "Atom: Go to Pane 1-9"),
        #Developer Submenu
        #"open in development mode":    ACK("", "Open in Development Mode"),
        "run atom [specs]":
            ACK("ac-s", "Atom: Run Atoms Specs"),
        "run package [specs]":
            ACK("ac-p", "Atom: Run Package Specs"),
        "[toggle] developer tools":
            ACK("ac-i", "Atom: Toggle Developer Tools"),
        #Selection Menu
        "[add] select above [<n>]":
            ACK("ac-up", "Atom: Add Selection Above #")*Repeat(extra="n"),
        "[add] select below [<n>]":
            ACK("ac-down", "Atom: Add Selection Below #")*Repeat(extra="n"),
        "split into lines":
            ACP("Split Into Lines", "Atom: Split Into lines"),
        "select line":
            ACK("c-l", "Atom: Select Line"),
        "[select] [to] (begin | beginning) [of] line":
            ACP("Editor: Select to Beginning of Line",
                "Atom: Select to Beginning of line"),
        "[select] inside brackets":
            ACK("ac-comma", "Atom: Select Inside Brackets"),
        #Find Menu
        "find (selection | selected)":
            ACK("c-e", "Atom: Replacing in Buffer"),
        "find [and] select all":
            ACK("a-f3", "Atom: Select All"),
        "[find] select next [<n>]":
            ACK("c-d", "Atom: Select Next")*Repeat(extra="n"),
        "[find] select skip [this] [<n>]":
            ACK("c-k, c-d", "Atom: Select Skip")*Repeat(extra="n"),
        "[find] select skip next [<n>]":
            ACK("c-d", "Atom: Select Skip") +
            ACK("c-k, c-d", "Atom: Select Skip")*Repeat(extra="n"),
        "find replace next":
            ACP("Find and Replace: Replace Next", "Atom: Replace Next"),
        "find replace all":
            ACP("Find and Replace: Replace All", "Atom: Replace All"),
        "find buffer":
            ACK("c-b", "Atom: Find Buffer"),
        "(find | go to) file":
            ACK("c-p", "Atom: Find File"),
        "find modified file":
            ACK("cs-b", "Atom: Find Modified File"),
        #Packages Menu
        #Bracket Matcher Submenu
        "bracket [go to] match":
            ACK("c-m", "Atom: Go To Matching Bracket"),
        "bracket remove [from] selection":
            ACK("c-lbrace", "Atom: Remove Bracket from Selection"),
        "close [current] tag":
            ACP("Bracket Matcher: Close Tag", "Atom: Close current tag"),
        "bracket remove matching":
            ACK("ac-backspace", "Atom: Remove matching brackets"),
        #Command Palette Submenu
        "[toggle] [command] palette":
            ACK("cs-p", "Atom: Toggle Command Palette"),
        #Dev Live Reload Submenu
        "reload [all] styles":
            ACK("acs-r", "Atom: Reload All Styles"),
        #Git Diff Submenu
        "move to next diff [different]":
            ACP("Move to Next Diff", "Atom: Move to Next Diff"),
        "move to previous diff [different]":
            ACP("Move to Previous Diff", "Atom: Move to Previous Different"),
        "[toggle] diff List":
            ACP("Toggle Diff List", "Atom: Toggle Diff List"),
        #Keybinding Resolver Submenu
        "toggle key [binding] resolver":
            ACP("Key Binding Resolver: Toggle", "Atom: Toggle Keybinding Resolver"),
        #Markdown Preview Submenu
        "markdown preview":
            ACK("cs-m", "Atom: Markdown Toggle Preview"),
        #Extras
        "markdown copy html":
            ACP("Markdown Preview: Copy HTML", "Atom: Markdown Preview: Copy HTML"),
        "markdown toggle break on newline":
            ACP("Markdown Preview: Toggle Break On Single Newline",
                "Atom: Markdown Preview: Toggle Break On Single Newline"),
        #Package Generator Submenu
        "(make|generate) package":
            ACP("Package Generator: Generate Package", "Atom: Generate Atom Package"),
        "(make|generate) syntax theme":
            ACP("Package Generator: Generate Syntax Theme",
                "Atom: Generate Atom Syntax Theme"),
        #Settings View Submenu
        ##"open setting":                             ACK("c-comma", "Atom: Open Setting"),
        "show key bindings":
            ACP("Settings View: Show Key Bindings", "Atom: Show Keybindings"),
        "installed themes":
            ACP("Settings View: Installed Themes", "Atom: Install Themes"),
        "uninstalled themes":
            ACP("Settings View: Uninstall Themes", "Atom: Uninstall Themes"),
        "installed packages":
            ACP("Settings View: Installed Packages", "Atom: Install Packages"),
        "uninstalled packages":
            ACP("Settings View: Uninstalled Packages", "Atom: Uninstall packages/themes"),
        "search (packages|themes)":
            ACP("Settings View: Install Packages and Themes",
                "Atom: Install Packages/Themes"),
        "update packages":
            ACP("Settings View: Check for Package Update", "Atom: Check for Packages"),
        #Snippets Submenu
        "expand snippets":
            ACP("Snippets: Expand", "Atom: Expand Snippets"),
        "next snippet":
            ACK("tab", "Atom: Next Stop|Snippet"),
        "previous snippet":
            ACK("a-tab", "Atom: Previous Stop|Snippet"),
        "available snippet":
            ACK("as-tab", "Atom: Available Snippets"),
        #Styleguide Submenu
        "show style [guide]":
            ACK("cs-g", "Atom: Show Styleguide"),
        #Symbol
        "find symbol":
            ACK("c-r", "Atom: Find Symbol"),
        "project symbol":
            ACK("cs-r", "Atom: Project Symbol"),
        #Timecop Submenu
        "timecop":
            ACP("Timecop: View", "Atom: Show Timecop"),
        #Tree View Submenu
        "tree focus":
            ACK("c-0", "Atom: Toggle Focus on TreeView"),
        "tree [View] [toggle] view":
            ACK("c-backslash", "Atom: Toggle"),
        "tree [View] [reveal] active file":
            ACK("cs-backslash", "Atom: Reveal Active File"),
        "tree [View] [toggle] side":
            ACP("Tree View: show", "Atom: Toggle Tree Side"),
        #Extras
        "tree show":
            ACP("Tree View: Show", "Atom: Tree View: Show"),
        "tree rename":
            ACP("Tree View: Rename", "Atom: Tree View: Rename"),
        "tree remove":
            ACP("Tree View: Remove", "Atom: Tree View: Remove"),
        "tree add file":
            ACP("Tree View: Add File", "Atom: Tree View: Add File"),
        "tree duplicate":
            ACP("Tree View: Duplicate", "Atom: Tree View: Duplicate"),
        "tree add folder":
            ACP("Tree View: Add Folder", "Atom: Tree View: Add Folder"),
        #Whitespaces Submenu
        "remove trailing [white] spaces":
            ACP("Whitespace: Remove Trailing Whitespace",
                "Atom: Remove Trailing White Spaces"),
        "convert tabs [to] spaces":
            ACP("Whitespace: Convert Tabs to Spaces", "Atom: Convert Tabs to Spaces"),
        "convert spaces [to] tabs":
            ACP("Whitespace: Convert Spaces to Tabs", "Atom: Convert Spaces to Tabs"),
        #Open on GitHub
        "github [open] blame":
            ACP("Open on GitHub: Blame", "Atom: Open On Github @ Blame"),
        "github [open] [branch] compare":
            ACP("Open on GitHub: Branch Compare",
                "Atom: Open On Github @ Branch Compare"),
        "github [open] [copy] URL":
            ACP("Open on GitHub: Copy URL", "Atom: Open On Github @ Copy URL"),
        "github [open] file":
            ACP("Open on GitHub: File", "Atom: Open On Github @ File"),
        "github [open] history":
            ACP("Open on GitHub: History", "Atom: Open On Github @ History"),
        "github [open] issues":
            ACP("Open on GitHub: Issues", "Atom: Open On Github @ Issues"),
        "github [open] repository":
            ACP("Open on GitHub: Repository", "Atom: Open On Github @ Repository"),
        #Open on GitHub
        "github close different":
            ACP("GitHub: Close All Diff Views", "Atom: GitHub Close All Diff Views"),
        "github empty different":
            ACP("GitHub: Close Empty Diff Views", "Atom: GitHub Close Empty Diff Views"),
        "github [show waterfall] diagnostics":
            ACP("GitHub:Okay Show Waterfall Diagnostics",
                "Atom: GitHub Show Waterfall Diagnostics"),
        "github [open] (issues | pull request)":
            ACP("GitHub: Open Issue or Pull Request",
                "Atom: GitHub Open Issue or Pull Request"),
        "github view staged changes [for current file]":
            ACP("GitHub: View Staged Changes for Current File",
                "Atom: GitHub View Staged Changes for Current File"),
        "github view unstaged changes [for current file]":
            ACP("GitHub: View Unstaged Changes for Current File",
                "Atom: GitHub View Unstaged Changes for Current File"),
        #Open on GitHub
        "github pull":
            ACK("a-g, s-f", "Atom: GitHub Pull"),
        "github push":
            ACK("a-g, p", "Atom: GitHub Push"),
        "github clone":
            ACK("a-g, equal", "Atom: GitHub Clone"),
        "github fetch":
            ACK("a-g, f", "Atom: GitHub Fetch"),
        "github logout":
            ACP("GitHub: Logout", "Atom: GitHub Logout"),
        "github force push":
            ACK("a-g, s-p", "Atom: GitHub Force Push"),
        "github tab [toggle]":
            ACK("c-8", "Atom: Github Toggle Github Tab"),
        "github focus [tab]":
            ACK("c-9", "Atom:Toggle Github Focus"),
        # Atom Development
        "dev (restart | reload) [atom]":
            ACP("Window: Reload", "Atom: Restart/Reload Atom"),

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
            ACP("Atom Beautify: Beautify Editor", "Atom : Beautify Editor"),
        "beautify migrate settings":
            ACP("Atom Beautify: Migrate Settings", "Atom: Beautify: Migrate Settings"),
        "beautify debug editor":
            ACP("Atom Beautify: Help Debug Editor", "Atom: Beautify: Debug Editor"),
        #Toggle Quotes
        "toggle quotes":
            ACK("cs-apostrophe", "Atom: Toggle Quotes: Single or Double"),
        #Script
        "script run":
            ACP("Script: Run", "Atom: Script: run"),
        "script [run] options":
            ACP("Script: Run Options", "Atom: Script: Run Options or Configure"),
        "script [run] profile":
            ACP("Script: Run With Profile", "Atom: Script: Run With Profile"),
        "script run [by] line":
            ACP("Script: Run By Line Number", "Atom: Script: Run Script by Line"),
        "script kill [process]":
            ACP("Script: Kill Process", "Atom: Script: Kill Process"),
        "script close view":
            ACP("Script: Close View", "Atom: Script: Close View"),
        "script copy [run] [results]":
            ACP("Script: Copy Run Results", "Atom: Script: Copy Run Results"),
        #"script close window and stop script":     ACP("Script: Close Window and Stop Script", "Atom: Script: Close Window and Stop Script"),
        #Delete Plus
        "delete words":
            ACP("Delete Plus: Delete", "Atom: Delete Plus"),
        #Last Edit
        "back edit":
            ACK("c-i", "Atom: Previous Edit"),
        "next edit":
            ACK("ca-i", "Atom: Next Last Edit"),
        #Looper
        #"cursor loud|capitalize [<n3>]":           ACK("a-down", "Atom: Looper Capitalize") * Repeat(extra="n"), # Not fully implemented
        #"cursor camel [<n4>]":                     ACK("a-down", "Atom: Looper Camelcase") * Repeat(extra="n"), # Not fully implemented
        #"cursor lowercase [<n5>]":                 ACK("a-down", "Atom: Looper Lowercase") * Repeat(extra="n"), # Not fully implemented
        "looping down cursor":
            ACK("a-down", "Atom: Looping Down at Cursor"),
        "looping up cursor":
            ACK("a-up", "Atom: Looping Up at Cursor"),
        "looping up":
            ACK("wa-up", "Atom: Looping Up"),
        #Git Plus
        "git (custom|run)":
            ACP("Git Plus: Run", "Atom: Git Run"),
        "git log":
            ACP("Git Plus: Log", "Atom: Git Log"),
        "git log current [file]":
            ACP("Git Plus: Log Current File", "Atom: Git Current File"),
        "git status":
            ACP("Git Plus: Status", "Atom: Git Status"),
        "git show":
            ACP("Git Plus: Show", "Atom: Git Show"),
        "git tags":
            ACP("Git Plus: Tags", "Atom: Git Tags"),
        "git open changed files":
            ACP("Git Plus: Git Open Changed Files", "Atom: Git Open Changed Files"),
        "git checkout [branch|tag]":
            ACP("Git Plus: Checkout", "Atom: Git Checkout Branch|Tag"),
        "git menu":
            ACP("Git Plus: Menu", "Atom: Git Menu"),
        "git pull":
            ACP("Git Plus: Pull", "Atom: Git Pull"),
        "git pull [using] rebase":
            ACP("Git Plus: Pull Using Rebase", "Atom: Git Pull Using Rebase"),
        "git push":
            ACP("Git Plus: Push", "Atom: Git Push"),
        "git commit":
            ACP("Git Plus: Commit", "Atom: Git Commit"),
        "git commit amend":
            ACP("Git Plus: Commit Amend", "Atom: Git Commit Amend"),
        "git merge":
            ACP("Git Plus: Merge", "Atom: Git Merge"),
        "git merge remote":
            ACP("Git Plus: Merge Remote", "Atom: Git Merge Remote"),
        "git diff":
            ACP("Git Plus: Diff", "Atom: Git Diff"),
        "git diff all":
            ACP("Git Plus: Diff All", "Atom: Git Diff All"),
        "git add":
            ACP("Git Plus: Add", "Atom: Git Add"),
        "git add all":
            ACP("Git plus: Add All", "Atom: Git Add All"),
        "git add [and] commit":
            ACP("Git Plus: Add And Commit", "Atom: Git Add And Commit"),
        "git add all [and] commit":
            ACP("Git Plus: Add All and Commit", "Atom: Git Add All and Commit"),
        "git add all commit [and] push":
            ACP("Git Plus: Add All Commit And Push", "Atom: Git Add All Commit Push"),
        "git new branch":
            ACP("Git Plus: New Branch", "Atom: Git New Branch"),
        "git (rm|remove)":
            ACP("Git Plus: Remove", "Atom: Git Remove"),
        #Project Manager
        "project manager [list]":
            ACP("Project Manager:List", "Atom: Project Manager: Toggle"),
        "project manager save":
            ACP("Project Manager:Save Project", "Atom: Project Manager: Save Project"),
        "project manager edit":
            ACP("Project Manager:Edit Project", "Atom: Project Manager: Edit Project"),
        #Menu Sidebar
        "[project manager] sidebar":
            ACP("Project Sidebar: Toggle", "Atom: Project Sidebar: Toggle"),
        #Expand Selection to Quotes
        "(expand|fill) quotes":
            ACK("c-apostrophe", "Atom: Expand Selection to Quotes"),
        #Auto Complete
        "auto [complete]":
            ACK("c-space", "Atom: Show Auto Complete Menu"),
        #Highlight Selected---- #Placeholder
        #Sublime Style Column Selection---- #Placeholder

        #Atom | Dragonfly Development--------------------------------------------------------------------------------------------------------------------------------------------------------
        # Template to create more commands. Documentation: https://dragonfly.readthedocs.org/en/latest/actions.html and http://caster.readthedocs.io/en/latest/caster/doc/Intro/
        # Used for basic key shortcuts
        #"text for voice command":               ACK("modifier-key", "program name: command name/description"),
        #"":                                     ACK("", "Atom: "),
        # Used for command that utilizes the "command palette" shortcut in the absence of assigned keyboard shortcut.
        #"text for voice command":               ACP("text as described in command palette", "command name/description"),
        #"":                                     ACP(""),
        #Atom Shortcut Snippets
        "dev keys [input] [<n>]":
            R(Text('#"": ACK("-", "Atom: "),') + Key("enter"),
              rdescript="Macro: Dev Keys #")*Repeat(extra="n"),
        "dev [command] palette [<n>]":
            R(Text('#"": ACP("", "Atom: "),') + Key("enter"),
              rdescript="Macro: Dev Command Palette #")*Repeat(extra="n"),
        #Repeatable Snippets
        "dev numb keys [input] [<n>]":
            R(Text('#" [<n>]": ACK("-", "Atom: ") * Repeat(extra="n"),') + Key("enter"),
              rdescript="Macro: Numb Dev Keys #")*Repeat(extra="n"),
        "dev numb [command] palette [<n>]":
            R(Text('#" [<n>]": ACP("", "Atom: ") * Repeat(extra="n"),') + Key("enter"),
              rdescript="Macro: Dev Numb Command Palette #")*Repeat(extra="n"),
        #Basic Dragonfly Snippets
        "dev key [<n>]":
            R(Text('"": Key(""),'), rdescript="Dragonfly: Print Dev Key #")*
            Repeat(extra="n"),
        "dev text [<n>]":
            R(Text('"": Text(""),'), rdescript="Dragonfly: Print Dev Text #")*
            Repeat(extra="n"),
        "send command [<n>]":
            R(Text('"": R(Function(SendJsonCommands, a_command=""), rdescript=""),'),
              rdescript="Macro: Print SendJsonCommands Template #")*Repeat(extra="n"),
    }

    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 50),
        IntegerRefST("line_number", 1, 50000),
        IntegerRefST("n2", 1, 10),
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
        "mim": "",
    }


#---------------------------------------------------------------------------

context = AppContext(executable="atom", title="Atom")
grammar = Grammar("Atom", context=context)
if settings.SETTINGS["apps"]["atom"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(AtomRule())
    else:
        rule = AtomRule()
        gfilter.run_on(rule)
        grammar.add_rule(AtomRule(name="atom"))
        grammar.load()
