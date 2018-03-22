"""
__author__ = 'Zone22'
Command-module for Atom
Official Site "https://atom.io/"
"""
from dragonfly import (AppContext, Dictation, Grammar, IntegerRef, Key,
                       MappingRule, Pause, Repeat, Text)
from dragonfly.actions.action_mimic import Mimic

from caster.lib import control, settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

# How long to wait for the Atom palette to load before hitting the enter key
atom_palette_wait = "30"
if settings.SETTINGS["miscellaneous"]["atom_palette_wait"]:
    atom_palette_wait = settings.SETTINGS["miscellaneous"]["atom_palette_wait"]


# Utilizes the Palette UI to leverage commands.
def palletize(function_text):
    return Key("cs-p") + Text(function_text) + Pause(atom_palette_wait) + Key("enter")


class AtomRule(MergeRule):
    pronunciation = "atom"

    mapping = {

        # Spoken commands that are commented out do not have assigned default shortcut keys or are incompatible.
        # The '#extra' subsection of commands that fit within the category but are not displayed by the menu or UI
        # Legend: '#' for not assigned, '##' for shortcut or functional duplicate.
        # ----------Spoken Command/Action------------------> Shortcut keys----------> #Displayed Text

        #Basic Cursor Navigation
        "up [<n>]":
            R(Key("up"), rdescript="Atom: Move Cursor Up #") * Repeat(extra="n"),
        "down [<n>]":
            R(Key("down"), rdescript="Atom: Move Cursor Down #") * Repeat(extra="n"),
        "right [<n>]":
            R(Key("right"), rdescript="Atom: Move Cursor Right #") * Repeat(extra="n"),
        "left [<n>]":
            R(Key("left"), rdescript="Atom: Move Cursor Left #") * Repeat(extra="n"),
        #Basic White Text Manipulation
        "tab|indent [<n>]":
            R(Key("tab"), rdescript="Atom: Press Tab Key #") * Repeat(extra="n"),
        "space [<n>]":
            R(Key("space"), rdescript="Atom: Press Tab Key #") * Repeat(extra="n"),
        # Menu UI-------------------------------------------------------------------------------------------
        #File Menu
        "[open] new window":
            R(Key("cs-n"), rdescript="Atom: New Window"),
        "new file":
            R(Key("c-n"), rdescript="Atom: New File"),
        "open file":
            R(Key("c-o"), rdescript="Atom: Open File"),
        "open folder":
            R(Key("cs-o"), rdescript="Atom: Open Folder"),
        "add project folder":
            R(Key("ac-o"), rdescript="Atom: Add Project Folder"),
        "open settings":
            R(Key("c-comma"), rdescript="Atom: Open Settings"),
        "reopen closed item":
            R(palletize("Reopen Closed Item"), rdescript="Atom: Reopen Last File or Tab"),
        "open [your] config":
            R(palletize("Open Your Config"), rdescript="Atom: Open Your Config"),
        "open [your] int script":
            R(palletize("Open Your Int Script"), rdescript="Atom: Open Your Int Script"),
        "open [your] key map":
            R(palletize("Open Your Key Map"), rdescript="Atom: Open Your Key Map"),
        "open [your] snippet":
            R(palletize("Open Your Snippet"), rdescript="Atom: Open Your Snippet"),
        "open [your] stylesheet":
            R(palletize("Open your Stylesheet"), rdescript="Atom: Open Your Stylesheet"),
        #"save":                                    R(Key("c-s"), rdescript="Atom: Save"),
        "save as":
            R(Key("cs-s"), rdescript="Atom: Save As"),
        "save all":
            R(palletize("Save All"), rdescript="Atom: Save All"),
        "close pane":
            R(palletize("Pane Close"), rdescript="Atom: Close Pane"),
        "close pane others":
            R(Key("ca-w"), rdescript="Atom: Close Pane"),
        "close window":
            R(Key("cs-w"), rdescript="Atom: Close Window"),
        #Extra
        #Edit Menu
        #"cut":                                     R(Key("s-delete"), rdescript="Atom: Cut"),
        "copy ":
            R(Key("c-insert"), rdescript="Atom: Copy"),
        "paste [<n>]":
            R(Key("s-insert"), rdescript="Atom: Paste") * Repeat(extra="n"),
        "copy path":
            R(Key("cs-c"), rdescript="Atom: Copy Path"),
        "select all":
            R(Key("c-a"), rdescript="Atom: Select All"),
        "[toggle] comments":
            R(Key("c-slash"), rdescript="Atom: Toggle Comments"),
        "reflow section":
            R(Key("ac-q"), rdescript="Atom: Reflow Section"),
        "select encoding":
            R(Key("cs-u"), rdescript="Atom: Select Encoding"),
        "[go to] line <n>":
            R(Key("c-g") + Pause("10") + Text("%(n)s") + Key("enter"),
              rdescript="Atom: Go to Line #"),
        "select grammar":
            R(Key("cs-l"), rdescript="Atom: Select Grammar"),
        #Lines Submenu
        ##"indent":                                  R(Key("c-lbrace"), rdescript="Atom: Indent"), # Rework Dragonfly Keymapping
        "toggle outdent":
            R(Key("c-rightbrace"), rdescript="Atom: Toggle Auto Outdent"),
        "auto indent windows":
            R(palletize("Window Auto Indent"), rdescript="Atom: Auto Indent"),
        "[move] line up [<n>]":
            R(Key("c-up"), rdescript="Atom: Move Line Up #") * Repeat(extra="n"),
        "[move] line down [<n>]":
            R(Key("c-down"), rdescript="Atom: Move Line Down #") * Repeat(extra="n"),
        "duplicate line [<n>]":
            R(Key("cs-d"), rdescript="Atom: Duplicate Line") * Repeat(
                extra="n"
            ),  #Unless remapped the command triggers Dragon NaturallySpeaking dictation box
        "delete line [<n>]":
            R(Key("cs-k"), rdescript="Atom: Delete Line or # Lines Below") *
            Repeat(extra="n"),
        "join line":
            R(Key("c-j"), rdescript="Atom: Join Line"),
        "comment line":
            R(Key("c-slash"), rdescript="Atom: Toggle Comment Line"),
        #Text Submenu
        "uppercase":
            R(palletize("Editor Upper Case"), rdescript="Atom: Convert Uppercase"),
        "lowercase":
            R(palletize("Editor Lower Case"), rdescript="Atom: Convert lowercase"),
        "delete [to] end [of word] [<n>]":
            R(Key("c-delete"), rdescript="Atom: Delete to End oF Word") *
            Repeat(extra="n"),
        "delete sub [word] [<n>]":
            R(Key("a-backspace"), rdescript="Atom: Delete to End of Subword") *
            Repeat(extra="n"),
        "delete [to] previous [word] [<n>]":
            R(palletize("Delete to Previous Word boundary"),
              rdescript="Atom: Delete to previous word boundary") * Repeat(extra="n"),
        "delete [to] next [word] [<n>]":
            R(palletize("Delete to Next Word Boundary"),
              rdescript="Atom: Delete to next word boundary") * Repeat(extra="n"),
        ##"delete line":                           R(Key("cs-k"), rdescript="Atom: Delete Line"),
        "transpose":
            R(palletize("Transpose") + Key("enter"), rdescript="Atom: Transpose"),
        #Folding Submenu
        "make fold":
            R(Key("acw-f"), rdescript="Atom: Make Fold"),
        "fold":
            R(Key("ac-lbrace"), rdescript="Atom: Fold"),
        "unfold":
            R(Key("ac-rightbrace"), rdescript="Atom: Unfold"),
        "unfold all":
            R(Key("acs-rightbrace"), rdescript="Atom: Unfold All"),
        "fold [level] [<n2>]":
            R(Key("c-%(n)s"), rdescript="Atom: Fold Level 1-9"),
        #Bookmarks Submenu
        "view all":
            R(Key("c-f2"), rdescript="Atom: Reflow Section"),
        "bookmark | book":
            R(Key("ca-f2"), rdescript="Atom: Toggle Bookmark"),
        "next bookmark | next book":
            R(Key("f2"), rdescript="Atom: Jump to Next Bookmark"),
        "previous bookmark | previous book":
            R(Key("s-f2"), rdescript="Atom: Jump to Previous Bookwork"),
        #View Menu
        "reload file":
            R(Key("ac-r"), rdescript="Atom: Reload File"),
        "fullscreen":
            R(Key("f11"), rdescript="Atom: Toggle Fullscreen"),
        "toggle menubar":
            R(palletize("Toggle Menu Bar"), rdescript="Atom: Toggle Menubar"),
        "increase font [size] [<n>]":
            R(Key("cs-equals"), rdescript="Atom: Increase Font Size") * Repeat(extra="n"),
        "decrease font [size] [<n>]":
            R(Key("cs-minus"), rdescript="Atom: Decrease Font size") * Repeat(extra="n"),
        "reset font [size]":
            R(Key("c-0"), rdescript="Atom: Reset Font Size"),
        "toggle soft wrap":
            R(palletize("Toggle Soft Wrap"), rdescript="Atom: Toggle Soft Wrap"),
        ##"toggle command palette":                  R(Key(""), rdescript="Atom: Toggle Command Palette"),
        "[toggle] treeview":
            R(Key("c-backslash"), rdescript="Atom: Toggle Treeview"),
        #Panes Submenu
        "split above":
            R(palletize("Pane: Split Up"), rdescript="Atom: Split Up"),
        "split below":
            R(palletize("Pane: Split Down"), rdescript="Atom: Split Down"),
        "split left":
            R(palletize("Pane: Split Left"), rdescript="Atom: Split Left"),
        "split right":
            R(palletize("Pane: Split Right"), rdescript="Atom: Split Right"),
        "focus [on] next [pane]":
            R(palletize("Window: Focus Next Pane"), rdescript="Atom: Focus Next Pane"),
        "focus [on] previous [pane]":
            R(palletize("Window: Focus Previous Pane"),
              rdescript="Atom: Focus Previous Pane"),
        "focus [pane] [on] above":
            R(palletize("Window: Focus Pane Above"),
              rdescript="Atom: Focused Pane Above"),
        "focus [pane] [on] below":
            R(palletize("Window: Focus Pane Below"), rdescript="Atom: Focus Pane Below"),
        "focus [pane] [on] left":
            R(palletize("Window: Focus Pane on Left"), rdescript="Atom: Focus On left"),
        "focus [pane] [on] right":
            R(palletize("Window: Focus Pane on Right"),
              rdescript="Atom: Focus Pane on Right"),
        ##"close pane":                              R(palletize("Window: pane close"), rdescript="Atom: Close Pane"),
        #extras
        "[go to] pane [<n2>]":
            R(Key("a-%(n)s"), rdescript="Atom: Go to Pane 1-9"),
        "focus previous":
            R(palletize("Core: Focus Previous"), rdescript="Atom: Focus Previous"),
        "next pane":
            R(palletize("Window: Focus Previous Pane"), rdescript="Atom: Next Pane"),
        "previous pane":
            R(palletize("Window: Focus Next Pane"), rdescript="Atom: Previous Pane"),
        #Developer Submenu
        #"open in development mode":                R(Key(""), rdescript="Open in Development Mode"),
        "run atom [specs]":
            R(Key("ac-s"), rdescript="Atom: Run Atoms Specs"),
        "run package [specs]":
            R(Key("ac-p"), rdescript="Atom: Run Package Specs "),
        "[toggle] developer tools":
            R(Key("ac-i"), rdescript="Atom: Toggle Developer Tools"),
        #Selection Menu
        "[add] select above [<n>]":
            R(Key("ac-up"), rdescript="Atom: Add Selection Above #") * Repeat(extra="n"),
        "[add] select below [<n>]":
            R(Key("ac-down"), rdescript="Atom: Add Selection Below #") *
            Repeat(extra="n"),
        "split into lines":
            R(palletize("Split Into Lines"), rdescript="Atom: Split Into lines"),
        "single section":
            R(Key("escape"), rdescript="Atom: Single Section"),
        "select [to] top":
            R(Key("cs-home"), rdescript="Atom: Select to Top"),
        "select [to] bottom":
            R(Key("cs-end"), rdescript="Atom: Select to Bottom"),
        #"select line":                             R(Key("c-l"), rdescript="Atom: Select Line"),
        #"select word [<n>]":                       R(palletize("Editor: Word"), rdescript="Atom: Select Word") * Repeat(extra="n"),
        "[select] [to] begin [of] word [<n>]":
            R(Key("cs-left"), rdescript="Atom: Select to Beginning of Word #") *
            Repeat(extra="n"),
        "[select] [to] end word [<n>]":
            R(Key("cs-right"), rdescript="Atom: Select to End of Word #") *
            Repeat(extra="n"),
        "[select] [to] begin line":
            R(palletize("Editor: Select to Beginning of Line"),
              rdescript="Atom: Select to Beginning of line"),
        "[select] [to] first character":
            R(Key("s-home"), rdescript="Atom: Select to First Character of Line"),
        "[select] [to] end line":
            R(Key("s-end"), rdescript="Atom: Select to End of line"),
        "[select] inside brackets":
            R(Key("ac-m"), rdescript="Atom: Select Inside Brackets"),
        #Find Menu
        #"find in buffer":                          R(Key("c-f"), rdescript="Atom: Find in Buffer"),
        "replacing in buffer":
            R(Key("ac-f"), rdescript="Atom: Replacing in Buffer"),
        "select next":
            R(Key("a-f3"), rdescript="Atom: Select All"),
        "find replace next":
            R(palletize("Find and Replace: Replace Next"),
              rdescript="Atom: Replace Next"),
        "find replace all":
            R(palletize("Find and Replace: Replace All"), rdescript="Atom: Replace All"),
        "find buffer":
            R(Key("c-b"), rdescript="Atom: Find Buffer"),
        "find file":
            R(Key("c-p"), rdescript="Atom: Find File"),
        "find modified file":
            R(Key("cs-b"), rdescript="Atom: Find Modified File"),
        #Packages Menu
        #Bracket Matcher Submenu
        "bracket [go to] match":
            R(Key("c-m"), rdescript="Atom: Go To Matching Bracket"),
        ##"select inside bracket":                 R(Key("ac-m"), rdescript="Atom: Select inside bracket"),
        "bracket remove [from] selection":
            R(Key("c-lbrace"), rdescript="Atom: Remove Bracket from Selection"),
        "close [current] tag":
            R(palletize("Bracket Matcher: Close Tag"),
              rdescript="Atom: Close current tag"),
        "bracket remove matching":
            R(Key("ac-backspace"), rdescript="Atom: Remove matching brackets"),
        #Command Palette Submenu
        "[toggle] [command] palette":
            R(Key("cs-p"), rdescript="Atom: Toggle Command Palette"),
        #Dev Live Reload Submenu
        "reload [all] styles":
            R(Key("acs-r"), rdescript="Atom: Reload All Styles"),
        #Git Diff Submenu
        "move to next diff [different]":
            R(palletize("Move to Next Diff"), rdescript="Atom: Move to Next Diff"),
        "move to previous diff [different]":
            R(palletize("Move to Previous Diff"),
              rdescript="Atom: Move to Previous Different"),
        "[toggle] diff List":
            R(palletize("Toggle Diff List"), rdescript="Atom: Toggle Diff List"),
        #Keybinding Resolver Submenu
        "toggle key [binding] resolver":
            R(palletize("Key Binding Resolver: Toggle"),
              rdescript="Atom: Toggle Keybinding Resolver"),
        #Markdown Preview Submenu
        "markdown preview":
            R(Key("cs-m"), rdescript="Atom: Markdown Toggle Preview"),
        #Extras
        "markdown copy html":
            R(palletize("Markdown Preview: Copy HTML"),
              rdescript="Atom: Markdown Preview: Copy HTML"),
        "markdown toggle break on newline":
            R(palletize("Markdown Preview: Toggle Break On Single Newline"),
              rdescript="Atom: Markdown Preview: Toggle Break On Single Newline"),
        #Package Generator Submenu
        "make|generate package":
            R(palletize("Package Generator: Generate Package"),
              rdescript="Atom: Generate Atom Package"),
        "make|generate syntax theme":
            R(palletize("Package Generator: Generate Syntax Theme"),
              rdescript="Atom: Generate Atom Syntax Theme"),
        #Settings View Submenu
        ##"open setting":                             R(Key("c-comma"), rdescript="Atom: Open Setting"),
        "show key bindings":
            R(palletize("Settings View: Show Key Bindings"),
              rdescript="Atom: Show Keybindings"),
        "installed themes":
            R(palletize("Settings View: Installed Themes"),
              rdescript="Atom: Install Themes"),
        "uninstalled themes":
            R(palletize("Settings View: Uninstall Themes"),
              rdescript="Atom: Uninstall Themes"),
        "installed packages":
            R(palletize("Settings View: Installed Packages"),
              rdescript="Atom: Install Packages"),
        "uninstalled packages":
            R(palletize("Settings View: Uninstalled Packages"),
              rdescript="Atom: Uninstall packages/themes"),
        "search packages|themes":
            R(palletize("Settings View: Install Packages and Themes"),
              rdescript="Atom: Install Packages/Themes"),
        "update packages":
            R(palletize("Settings View: Check for Package Update"),
              rdescript="Atom: Check for Packages"),
        #Snippets Submenu
        "expand snippets":
            R(palletize("Snippets: Expand"), rdescript="Atom: Expand Snippets"),
        "next snippet":
            R(Key("tab"), rdescript="Atom: Next Stop|Snippet"),
        "previous snippet":
            R(Key("a-tab"), rdescript="Atom: Previous Stop|Snippet"),
        "available snippet":
            R(Key("as-tab"), rdescript="Atom: Available Snippets"),
        #Styleguide Submenu
        "show style [guide]":
            R(Key("cs-g"), rdescript="Atom: Show Styleguide"),
        #Symbol
        "find symbol":
            R(Key("c-r"), rdescript="Atom: Find Symbol"),
        "project symbol":
            R(Key("cs-r"), rdescript="Atom: Project Symbol"),
        #Timecop Submenu
        "timecop":
            R(palletize("Timecop: View"), rdescript="Atom: Show Timecop"),
        #Tree View Submenu
        "tree focus":
            R(Key("c-0"), rdescript="Atom: Toggle Focus on TreeView"),
        "tree [View] [toggle] view":
            R(Key("c-backslash"), rdescript="Atom: Toggle"),
        "tree [View] [reveal] active file":
            R(Key("cs-backslash"), rdescript="Atom: Reveal Active File"),
        "tree [View] [toggle] side":
            R(palletize("Tree View: show"), rdescript="Atom: Toggle Tree Side"),
        #Extras
        "tree show":
            R(palletize("Tree View: Show"), rdescript="Atom: Tree View: Show"),
        "tree rename":
            R(palletize("Tree View: Rename"), rdescript="Atom: Tree View: Rename"),
        "tree remove":
            R(palletize("Tree View: Remove"), rdescript="Atom: Tree View: Remove"),
        "tree add file":
            R(palletize("Tree View: Add File"), rdescript="Atom: Tree View: Add File"),
        "tree duplicate":
            R(palletize("Tree View: Duplicate"), rdescript="Atom: Tree View: Duplicate"),
        "tree add folder":
            R(palletize("Tree View: Add Folder"),
              rdescript="Atom: Tree View: Add Folder"),
        #Whitespaces Submenu
        "remove trailing [white] spaces":
            R(palletize("Whitespace: Remove Trailing Whitespace"),
              rdescript="Atom: Remove Trailing White Spaces"),
        "convert tabs [to] spaces":
            R(palletize("Whitespace: Convert Tabs to Spaces"),
              rdescript="Atom: Convert Tabs to Spaces"),
        "convert spaces [to] tabs":
            R(palletize("Whitespace: Convert Spaces to Tabs"),
              rdescript="Atom: Convert Spaces to Tabs"),
        #Open on GitHub
        "github [open] blame":
            R(palletize("Open on GitHub: Blame"),
              rdescript="Atom: Open On Github @ Blame"),
        "github [open] [branch] compare":
            R(palletize("Open on GitHub: Branch Compare"),
              rdescript="Atom: Open On Github @ Branch Compare"),
        "github [open] [copy] URL":
            R(palletize("Open on GitHub: Copy URL"),
              rdescript="Atom: Open On Github @ Copy URL"),
        "github [open] file":
            R(palletize("Open on GitHub: File"), rdescript="Atom: Open On Github @ File"),
        "github [open] history":
            R(palletize("Open on GitHub: History"),
              rdescript="Atom: Open On Github @ History"),
        "github [open] issues":
            R(palletize("Open on GitHub: Issues"),
              rdescript="Atom: Open On Github @ Issues"),
        "github [open] repository":
            R(palletize("Open on GitHub: Repository"),
              rdescript="Atom: Open On Github @ Repository"),
        #Open on GitHub
        "github close different":
            R(palletize("GitHub: Close All Diff Views"),
              rdescript="Atom: GitHub Close All Diff Views"),
        "github empty different":
            R(palletize("GitHub: Close Empty Diff Views"),
              rdescript="Atom: GitHub Close Empty Diff Views"),
        "github [show waterfall] diagnostics":
            R(palletize("GitHub:Okay Show Waterfall Diagnostics"),
              rdescript="Atom: GitHub Show Waterfall Diagnostics"),
        "github [open] issues | pull request":
            R(palletize("GitHub: Open Issue or Pull Request"),
              rdescript="Atom: GitHub Open Issue or Pull Request"),
        "github view staged changes [for current file]":
            R(palletize("GitHub: View Staged Changes for Current File"),
              rdescript="Atom: GitHub View Staged Changes for Current File"),
        "github view unstaged changes [for current file]":
            R(palletize("GitHub: View Unstaged Changes for Current File"),
              rdescript="Atom: GitHub View Unstaged Changes for Current File"),
        #Open on GitHub
        "github pull":
            R(Key("s-g"), rdescript="Atom: GitHub Pull"),
        "github push":
            R(Key("a-g") + Key("p"), rdescript="Atom: GitHub Push"),
        "github clone":
            R(Key("a-g") + Key("equal"), rdescript="Atom: GitHub Clone"),
        "github fetch":
            R(Key("a-g") + Key("f"), rdescript="Atom: GitHub Fetch"),
        "github logout":
            R(palletize("GitHub: Logout"), rdescript="Atom: GitHub Logout"),
        "github force push":
            R(Key("a-g"), rdescript="Atom: GitHub Force Push"),
        "github tab [toggle]":
            R(Key("c-8"), rdescript="Atom: Github Toggle Github Tab"),
        "github focus [tab]":
            R(Key("c-9") + Key("enter"), rdescript="Atom:Toggle Github Focus"),
        # Adom Development
        "dev restart | reload [atom]":
            R(palletize("Window: Reload"), rdescript="Atom: Restart/Reload Atom"),

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
            R(palletize("Atom Beautify: Beautify Editor"),
              rdescript="Atom : Beautify Editor"),
        "beautify migrate settings":
            R(palletize("Atom Beautify: Migrate Settings"),
              rdescript="Atom: Beautify: Migrate Settings"),
        "beautify debug editor":
            R(palletize("Atom Beautify: Help Debug Editor"),
              rdescript="Atom: Beautify: Debug Editor"),
        #Toggle Quotes
        "toggle quotes":
            R(Key("cs-apostrophe"), rdescript="Atom: Toggle Quotes: Single or Double"),
        #Script
        "script run":
            R(palletize("Script: Run"), rdescript="Atom: Script: run"),
        "script [run] options":
            R(palletize("Script: Run Options"),
              rdescript="Atom: Script: Run Options or Configure"),
        "script [run] profile":
            R(palletize("Script: Run With Profile"),
              rdescript="Atom: Script: Run With Profile"),
        "script run [by] line":
            R(palletize("Script: Run By Line Number"),
              rdescript="Atom: Script: Run Script by Line"),
        "script kill [process]":
            R(palletize("Script: Kill Process"), rdescript="Atom: Script: Kill Process"),
        "script close view":
            R(palletize("Script: Close View"), rdescript="Atom: Script: Close View"),
        "script copy [run] [results]":
            R(palletize("Script: Copy Run Results"),
              rdescript="Atom: Script: Copy Run Results"),
        #"script close window and stop script":     R(palletize("Script: Close Window and Stop Script"), rdescript="Atom: Script: Close Window and Stop Script"),
        #Delete Plus
        "delete words":
            R(palletize("Delete Plus: Delete"), rdescript="Atom: Delete Plus"),
        #Last Edit
        "back edit":
            R(Key("c-i"), rdescript="Atom: Previous Edit"),
        "next edit":
            R(Key("ca-i"), rdescript="Atom: Next Last Edit"),
        #Looper
        #"cursor loud|capitalize [<n3>]":           R(Key("a-down"), rdescript="Atom: Looper Capitalize") * Repeat(extra="n"), # Not fully implemented
        #"cursor camel [<n4>]":                     R(Key("a-down"), rdescript="Atom: Looper Camelcase") * Repeat(extra="n"), # Not fully implemented
        #"cursor lowercase [<n5>]":                 R(Key("a-down"), rdescript="Atom: Looper Lowercase") * Repeat(extra="n"), # Not fully implemented
        "looping down cursor":
            R(Key("a-down"), rdescript="Atom: Looping Down at Cursor"),
        "looping up cursor":
            R(Key("a-up"), rdescript="Atom: Looping Up at Cursor"),
        "looping up":
            R(Key("wa-up"), rdescript="Atom: Looping Up"),
        #Git Plus
        #"git custom|run":                          R(palletize("Git Plus: Run"), rdescript="Atom: Git Run"),
        #"git log":                                 R(palletize("Git Plus: Log"), rdescript="Atom: Git Log"),
        #"git log current [file]":                  R(palletize("Git Plus: Log Current File"), rdescript="Atom: Git Current File"),
        #"git status":                              R(palletize("Git Plus: Status"), rdescript="Atom: Git Status"),
        #"git show":                                R(palletize("Git Plus: Show"), rdescript="Atom: Git Show"),
        #"git tags":                                R(palletize("Git Plus: Tags"), rdescript="Atom: Git Tags"),
        #"git open changed files":                  R(palletize("Git Plus: Git Open Changed Files"), rdescript="Atom: Git Open Changed Files"),
        #"git checkout [branch|tag]":               R(palletize("Git Plus: Checkout"), rdescript="Atom: Git Checkout Branch|Tag"),
        #"git menu":                                R(palletize("Git Plus: Menu"), rdescript="Atom: Git Menu"),
        #"git pull":                                R(palletize("Git Plus: Pull"), rdescript="Atom: Git Pull"),
        #"git pull [using] rebase":                 R(palletize("Git Plus: Pull Using Rebase"), rdescript="Atom: Git Pull Using Rebase"),
        #"git push":                                R(palletize("Git Plus: Push"), rdescript="Atom: Git Push"),
        #"git commit":                              R(palletize("Git Plus: Commit"), rdescript="Atom: Git Commit"),
        #"git commit amend":                        R(palletize("Git Plus: Commit Amend"), rdescript="Atom: Git Commit Amend"),
        #"git merge":                               R(palletize("Git Plus: Merge"), rdescript="Atom: Git Merge"),
        #"git merge remote":                        R(palletize("Git Plus: Merge Remote"), rdescript="Atom: Git Merge Remote"),
        #"git diff":                                R(palletize("Git Plus: Diff"), rdescript="Atom: Git Diff"),
        #"git diff all":                            R(palletize("Git Plus: Diff All"), rdescript="Atom: Git Diff All"),
        #"git add":                                 R(palletize("Git Plus: Add"), rdescript="Atom: Git Add"),
        #"git add all":                             R(palletize("Git plus: Add All"), rdescript="Atom: Git Add All"),
        #"git add [and] commit":                    R(palletize("Git Plus: Add And Commit"), rdescript="Atom: Git Add And Commit"),
        #"git add all [and] commit":                R(palletize("Git Plus: Add All and Commit"), rdescript="Atom: Git Add All and Commit"),
        #"git add all commit [and] push":           R(palletize("Git Plus: Add All Commit And Push"), rdescript="Atom: Git Add All Commit Push"),
        #"git new branch":                          R(palletize("Git Plus: New Branch"), rdescript="Atom: Git New Branch"),
        #"git rm|remove":                           R(palletize("Git Plus: Remove"), rdescript="Atom: Git Remove"),
        #Project Manager
        "project manager [list]":
            R(palletize("Project Manager:List"),
              rdescript="Atom: Project Manager: Toggle"),
        "project manager save":
            R(palletize("Project Manager:Save Project"),
              rdescript="Atom: Project Manager: Save Project"),
        "project manager edit":
            R(palletize("Project Manager:Edit Project"),
              rdescript="Atom: Project Manager: Edit Project"),
        #Menu Sidebar
        "[project manager] sidebar":
            R(palletize("Project Sidebar: Toggle"),
              rdescript="Atom: Project Sidebar: Toggle"),
        #Expand Selection to Quotes
        "expand|fill quotes":
            R(Key("c-apostrophe"), rdescript="Atom: Expand Selection to Quotes"),
        #Auto Complete
        "auto [complete]":
            R(Key("c-space"), rdescript="Atom: Show Auto Complete Menu"),
        #Highlight Selected---- #Placeholder
        #Sublime Style Column Selection---- #Placeholder

        #Atom | Dragonfly Development--------------------------------------------------------------------------------------------------------------------------------------------------------
        # Template to create more commands. Documentation: https://dragonfly.readthedocs.org/en/latest/actions.html and http://caster.readthedocs.io/en/latest/caster/doc/Intro/
        # Used for basic key shortcuts
        #"text for voice command":               R(Key("modifier-key"), rdescript="program name: command name/description"),
        #"":                                     R(Key(""), rdescript="Atom: "),
        # Used for command that utilizes the "command palette" shortcut in the absence of assigned keyboard shortcut.
        #"text for voice command":               R(palletize("text as described in command palette"), rdescript="command name/description"),
        #"":                                     R(palletize(""),
        #Atom Shortcut Snippets
        "dev keys [input] [<n>]":
            R(Text(
                '       #"":                                     R(Key("-"), rdescript="Atom: "),'
            ) + Key("enter"),
              rdescript="Macro: Dev Keys #") * Repeat(extra="n"),
        "dev [command] palette [<n>]":
            R(Text(
                '       #"":                                     R(palletize(""), rdescript="Atom: "),'
            ) + Key("enter"),
              rdescript="Macro: Dev Command Palette #") * Repeat(extra="n"),
        #Repeatable Snippets
        "dev numb keys [input] [<n>]":
            R(Text(
                '#" [<n>]":                                R(Key("-"), rdescript="Atom: ") * Repeat(extra="n"),'
            ) + Key("enter"),
              rdescript="Macro: Numb Dev Keys #") * Repeat(extra="n"),
        "dev numb [command] palette [<n>]":
            R(Text(
                '#" [<n>]":                                R(palletize(""), rdescript="Atom: ") * Repeat(extra="n"),'
            ) + Key("enter"),
              rdescript="Macro: Dev Numb Command Palette #") * Repeat(extra="n"),
        #Basic Dragonfly Snippets
        "dev key [<n>]":
            R(Text('"":                                Key(""),'),
              rdescript="Dragonfly: Print Dev Key #") * Repeat(extra="n"),
        "dev text [<n>]":
            R(Text('"":                                Text(""),'),
              rdescript="Dragonfly: Print Dev Text #") * Repeat(extra="n"),
        "send command [<n>]":
            R(Text(
                '"":                                R(Function(SendJsonCommands, a_command=""), rdescript=""),'
            ),
              rdescript="Macro: Print SendJsonCommands template #") * Repeat(extra="n"),
    }

    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 10000),
        IntegerRefST("n2", 1, 9),
    ]
    defaults = {"n": 1, "mim": ""}


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
