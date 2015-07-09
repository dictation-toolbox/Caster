"""
__author__ = 'Zone22'

Command-module for Atom
Official Site "https://atom.io/"
"""
from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)
from dragonfly.actions.action_mimic import Mimic

from caster.lib.dfplus.state.short import R

class CommandRule(MappingRule):

    mapping = {

# Spoken commands that are commented out do not have assigned default shortcut keys or are incompatible.
# The '#extra' subsection of commands that fit within the category but are not displayed by the menu or UI
# Legend: '#' for not assigned '##' for duplicates
# ----------Spoken Command/Action------------------> Shortcut keys----------> #Displayed Text
    #Basic Cursor Navigation
            "up [<n>]":                              R(Key("up"), rdescript="Atom: Move Cursor Up #") * Repeat(extra="n"),
            "down [<n>]":                            R(Key("down"), rdescript="Atom: Move Cursor Down #") * Repeat(extra="n"),
            "right [<n>]":                           R(Key("right"), rdescript="Atom: Move Cursor Right #") * Repeat(extra="n"),
            "left [<n>]":                            R(Key("left"), rdescript="Atom: Move Cursor Left #") * Repeat(extra="n"),
    #White Text Manipulation
            "tab|indent [<n>]":                      R(Key("tab"), rdescript="Atom: Press Tab Key #") * Repeat(extra="n"),
            "space [<n>]":                           R(Key("space"), rdescript="Atom: Press Tab Key #") * Repeat(extra="n"),
# Menu UI-------------------------------------------------------------------------------------------
    #File Menu
            "[open] new window":                     R(Key("cs-n"), rdescript="Atom: New Window"),
            "new file":                              R(Key("c-n"), rdescript="Atom: New File"),
            "open file":                             R(Key("c-o"), rdescript="Atom: Open File"),
            "open folder":                           R(Key("cs-o"), rdescript="Atom: Open Folder"),
            "add project folder":                    R(Key("ac-o"), rdescript="Atom: Add Project Folder"),
            "open settings":                         R(Key("c-comma"), rdescript="Atom: Open Settings"),
            "[open] last tab":                       R(Key("cs-t"), rdescript="Atom: Reopen last file or tab"),
            "open [your] config":                    R(Key("cs-p") + Text("Open your config") + Pause("4") + Key("enter"), rdescript="Atom: Open Your Config"),
            "open [your] int script":                R(Key("cs-p") + Text("Open your int script") + Pause("4") + Key("enter"), rdescript="Atom: Open Your Int Script"),
            "open [your] key map":                   R(Key("cs-p") + Text("Open your key map") + Pause("4") + Key("enter"), rdescript="Atom: Open Your Key Map"),
            "open [your] snippet":                   R(Key("cs-p") + Text("Open your snippet") + Pause("4") + Key("enter"), rdescript="Atom: Open Your Snippet"),
            "open [your] stylesheet":                R(Key("cs-p") + Text("Open your stylesheet") + Pause("4") + Key("enter"), rdescript="Atom: Open Your Stylesheet"),
            "save":                                  R(Key("c-s"), rdescript="Atom: Save"),
            "save as":                               R(Key("cs-s"), rdescript="Atom: Save As"),
            "save all":                              R(Key("cs-p") + Text("save all") + Pause("4") + Key("enter"), rdescript="Atom: Save All"),
            "close tab":                             R(Key("c-w"), rdescript="Atom: Close Tab"),
            "close pane":                            R(Key("cs-p") + Text("pane close") + Pause("4") + Key("enter"), rdescript="Atom: Close Pane"),
            "close window":                          R(Key("cs-w"), rdescript="Atom: Close Window"),
    #Edit Menu
            "undo":                                  R(Key("c-z"), rdescript="Atom: Undo"),
            "redo":                                  R(Key("c-y"), rdescript="Atom: Redo"),
            "cut":                                   R(Key("s-delete"), rdescript="Atom: Cut"),
            "copy":                                  R(Key("c-insert"), rdescript="Atom: Copy"),
            "paste":                                 R(Key("s-insert"), rdescript="Atom: Paste"),
            "copy path":                             R(Key("cs-c"), rdescript="Atom: Copy Path"),
            "select all":                            R(Key("c-a"), rdescript="Atom: Select All"),
            "[toggle] comments":                     R(Key("c-slash"), rdescript="Atom: Toggle Comments"),
            "reflow section":                        R(Key("ac-q"), rdescript="Atom: Reflow Section"),
            "select encoding":                       R(Key("cs-u"), rdescript="Atom: Select Encoding"),
            "[go to] line <n>":                      R(Key("c-g") + Pause("10") + Text("%(n)s") + Key("enter"), rdescript="Atom: Go to Line #"),
            "select grammar":                        R(Key("cs-l"), rdescript="Atom: Select Grammar"),
        #Lines Submenu
            ##"indent":                              R(Key("c-lbrace"), rdescript="Atom: Indent"), # Rework Dragonfly Keymapping
            "outdent":                               R(Key("c-rightbrace"), rdescript="Atom: Outdent"), # Rework Dragonfly Keymapping
            "auto indent":                           R(Key("cs-p") + Text("auto indent") + Pause("4") + Key("enter"), rdescript="Atom: Auto Indent"),
            "[move] line up [<n>]":                  R(Key("c-up"), rdescript="Atom: Move Line Up #") * Repeat(extra="n"),
            "[move] line down [<n>]":                R(Key("c-down"), rdescript="Atom: Move Line Down #") * Repeat(extra="n"),
            "duplicate line [<n>]":                  R(Key("cs-d"), rdescript="Atom: Duplicate Line") * Repeat(extra="n"), #Unless remapped the command triggers Dragon NaturallySpeaking dictation box
            "delete line [<n>]":                     R(Key("cs-k"), rdescript="Atom: Delete Line or # Lines Below") * Repeat(extra="n"),
            "join line":                             R(Key("c-j"), rdescript="Atom: Join Line"),
        #Text Submenu
            "uppercase":                             R(Key("cs-p") + Text("uppercase") + Pause("4") + Key("enter"), rdescript="Atom: Convert Uppercase"),
            "lowercase":                             R(Key("cs-p") + Text("lowercase") + Pause("4") + Key("enter"), rdescript="Atom: Convert lowercase"),
            "delete [to] end of word [<n>]":         R(Key("c-delete"), rdescript="Atom: Delete to End oF Word") * Repeat(extra="n"),
            "delete [to] previous word [<n>]":       R(Key("cs-p") + Text("delete to previous word boundary") + Pause("4") + Key("enter"), rdescript="Atom: Delete to previous word boundary") * Repeat(extra="n"),
            "delete [to] next word [<n>]":           R(Key("cs-p") + Text("delete to next word boundary") + Pause("4") + Key("enter"), rdescript="Atom: Delete to next word boundary") * Repeat(extra="n"),
            ##"delete line":                         R(Key("cs-k"), rdescript="Atom: Delete Line"),
            "transpose":                             R(Key("cs-p") + Text("transpose") +  Key("enter"), rdescript="Atom: Transpose"),
        #Folding Submenu
            "make fold":                             R(Key("acw-f"), rdescript="Atom: Make Fold"),
            "fold":                                  R(Key("ac-lbrace"), rdescript="Atom: Fold"),
            "unfold":                                R(Key("ac-rightbrace"), rdescript="Atom: Unfold"),
            "unfold all":                            R(Key("acs-rightbrace"), rdescript="Atom: Unfold All"),
            "fold [level] 1":                        R(Key("cs-p") + Text("fold at level 1") + Pause("4") + Key("enter"), rdescript="Atom: Fold Level 1"),
            "fold [level] 2":                        R(Key("cs-p") + Text("fold at level 2") + Pause("4") + Key("enter"), rdescript="Atom: Fold Level 2"),
            "fold [level] 3":                        R(Key("cs-p") + Text("fold at level 3") + Pause("4") + Key("enter"), rdescript="Atom: Fold Level 3"),
            "fold [level] 4":                        R(Key("cs-p") + Text("fold at level 4") + Pause("4") + Key("enter"), rdescript="Atom: Fold Level 4"),
            "fold [level] 5":                        R(Key("cs-p") + Text("fold at level 5") + Pause("4") + Key("enter"), rdescript="Atom: Fold Level 5"),
            "fold [level] 6":                        R(Key("cs-p") + Text("fold at level 7") + Pause("4") + Key("enter"), rdescript="Atom: Fold Level 7"),
            "fold [level] 8":                        R(Key("cs-p") + Text("fold at level 8") + Pause("4") + Key("enter"), rdescript="Atom: Fold Level 8"),
            "fold [level] 9":                        R(Key("cs-p") + Text("fold at level 9") + Pause("4") + Key("enter"), rdescript="Atom: Fold Level 9"),
        #Bookmarks Submenu
            "view all":                              R(Key("c-f2"), rdescript="Atom: Reflow Section"),
            "bookmark | book":                       R(Key("ca-f2"), rdescript="Atom: Toggle Bookmark"),
            "next bookmark | next book":             R(Key("f2"), rdescript="Atom: Jump to Next Bookmark"),
            "previous bookmark | previous book":     R(Key("s-f2"), rdescript="Atom: Jump to Previous Bookwork"),
    #View Menu
            "reload file":                           R(Key("ac-r"), rdescript="Atom: Reload"),
            "fullscreen":                            R(Key("f11"), rdescript="Atom: Toggle Fullscreen"),
            "toggle menubar":                        R(Key("cs-p") + Text("toggle menu bar") + Pause("4") + Key("enter"), rdescript="Atom: Toggle Menubar"),
            "increase font [size] [<n>]":            R(Key("cs-equals"), rdescript="Atom: Increase Font Size") * Repeat(extra="n"),
            "decrease font [size] [<n>]":            R(Key("cs-minus"), rdescript="Atom: Decrease Font size") * Repeat(extra="n"),
            "reset font [size]":                     R(Key("c-0"), rdescript="Atom: Reset Font Size"),
            "toggle soft wrap":                      R(Key("cs-p") + Text("toggle soft wrap") + Pause("4") + Key("enter"), rdescript="Atom: Toggle Soft Wrap"),
            ##"toggle command palette":              R(Key(""), rdescript="Atom: Toggle Command Palette"),
            "[toggle] treeview":                     R(Key("c-backslash"), rdescript="Atom: Toggle Treeview"),
        #Panes Submenu
            "split up":                              R(Key("cs-p") + Text("pane: split up") + Pause("4") + Pause("4") + Key("enter"), rdescript="Atom: Split Up"),
            "split down":                            R(Key("cs-p") + Text("pane: split down") + Pause("4") + Key("enter"), rdescript="Atom: Split Down"),
            "split left":                            R(Key("cs-p") + Text("pane: split left") + Pause("4") + Key("enter"), rdescript="Atom: Split Left"),
            "split right":                           R(Key("cs-p") + Text("pane: split right") + Pause("4") + Key("enter"), rdescript="Atom: Split Right"),
            "focus next pane":                       R(Key("cs-p") + Text("Window: focus next pane") + Pause("4") + Key("enter"), rdescript="Atom: Focus Next Pane"),
            "focus previous pane":                   R(Key("cs-p") + Text("Window: focus previous pane") + Pause("4") + Key("enter"), rdescript="Atom: Focus Previous Pane"),
            "focus pane above":                      R(Key("cs-p") + Text("Window: focus pane above") + Pause("4") + Key("enter"), rdescript="Atom: Focused Pane Above"),
            "focus pane below":                      R(Key("cs-p") + Text("Window: focus pane below") + Pause("4") + Key("enter"), rdescript="Atom: Focus Pane Below"),
            "focus pane on left":                    R(Key("cs-p") + Text("Window: focus pane on left") + Pause("4") + Key("enter"), rdescript="Atom: Focus On left"),
            "focus pane on right":                   R(Key("cs-p") + Text("Window: focus pane on right") + Pause("4") + Key("enter"), rdescript="Atom: Focus Pane on Right"),
            "close pane":                            R(Key("cs-p") + Text("Window: pane close") + Pause("4") + Key("enter"), rdescript="Atom: Close Pane"),
        #extras
            "pane 1":                                R(Key("a-1"), rdescript="Atom: Go to Pane 1"),
            "pane 2":                                R(Key("a-2"), rdescript="Atom: Go to Pane 2"),
            "pane 3":                                R(Key("a-3"), rdescript="Atom: Go to Pane 3"),
            "pane 4":                                R(Key("a-4"), rdescript="Atom: Go to Pane 4"),
            "pane 5":                                R(Key("a-5"), rdescript="Atom: Go to Pane 5"),
            "pane 6":                                R(Key("a-6"), rdescript="Atom: Go to Pane 6"),
            "pane 7":                                R(Key("a-7"), rdescript="Atom: Go to Pane 7"),
            "pane 8":                                R(Key("a-8"), rdescript="Atom: Go to Pane 8"),
            "pane 9":                                R(Key("a-9"), rdescript="Atom: Go to Pane 9"),
        #Developer Submenu
            #"open in development mode":             R(Key(""), rdescript="Open in Development Mode"),
            "run atom specs":                        R(Key("ac-s"), rdescript="Atom: Run Atoms Specs"),
            "run package specs":                     R(Key("ac-p"), rdescript="Atom: Run Package Specs "),
            "[toggle] developer tools":              R(Key("ac-i"), rdescript="Atom: Toggle Developer Tools"),
    #Selection Menu
            "[add] selection above [<n>]":           R(Key("ac-up"), rdescript="Atom: Add Selection Above #") * Repeat(extra="n"),
            "[add] selection below [<n>]":           R(Key("ac-down"), rdescript="Atom: Add Selection Below #") * Repeat(extra="n"),
            "split into lines":                      R(Key("cs-p") + Text("split into lines") + Pause("4") + Key("enter"), rdescript="Atom: Split Into lines"),
            "single section":                        R(Key("escape"), rdescript="Atom: Single Section"),
            "select [to] top":                       R(Key("cs-home"), rdescript="Atom: Select to Top"),
            "select [to] bottom":                    R(Key("cs-end"), rdescript="Atom: Select to Bottom"),
            "select line":                           R(Key("c-l"), rdescript="Atom: Select Line"),
            "select word":                           R(Key("cs-p") + Text("editor: word") + Pause("4") + Key("enter"), rdescript="Atom: Select Word"),
            "select [to] beginning [of] word [<n>]": R(Key("cs-left"), rdescript="Atom: Select to Beginning of Word #") * Repeat(extra="n"),
            "select [to] end of word [<n>]":         R(Key("cs-right"), rdescript="Atom: Select to End of Word #") * Repeat(extra="n"),
            "select [to] beginning [of] line":       R(Key("cs-p") + Text("editor: select to beginning of line") + Pause("4") + Key("enter"), rdescript="Atom: Select to Beginning of line"),
            "select [to] first character of line":   R(Key("s-home"), rdescript="Atom: Select to First character of Line"),
            "select [to] end of line":               R(Key("s-end"), rdescript="Atom: Select to End of line"),
            "[select] inside brackets":              R(Key("ac-m"), rdescript="Atom: Select Inside Brackets"),
    #Find Menu
            "find in buffer":                        R(Key("c-f"), rdescript="Atom: Find in Buffer"),
            "replacing in buffer":                   R(Key("ac-f"), rdescript="Atom: Replacing in Buffer"),
            "select next":                           R(Key("c-d"), rdescript="Atom: Select Next"),
            "select all":                            R(Key("c-f3"), rdescript="Atom: Select All"),
            "find [in] project":                     R(Key("cs-f3"), rdescript="Atom: Find in Project"),
            "toggle find in project":                R(Key("cs-f"), rdescript="Atom: Toggle Find in Project"),
            "find next":                             R(Key("f3"), rdescript="Atom: Find Next"),
            "find previous":                         R(Key("s-f3"), rdescript="Atom: Find Previous"),
            "find replace next":                     R(Key("cs-p") + Text("find and replace: replace next") + Pause("4") + Key("enter"), rdescript="Atom: Replace Next"),
            "find replace all":                      R(Key("cs-p") + Text("find and replace: replace all") + Pause("4") + Key("enter"), rdescript="Atom: Replace All"),
            "find buffer":                           R(Key("c-b"), rdescript="Atom: Find Buffer"),
            "find file":                             R(Key("c-p"), rdescript="Atom: Find File"),
            "find modified file":                    R(Key("cs-b"), rdescript="Atom: Find Modified File"),
    #Packages Menu
        #Bracket Matcher Submenu
            "[go to] matching bracket":              R(Key("c-m"), rdescript="Atom: go to matching bracket"),
            ##"select inside bracket":               R(Key("ac-m"), rdescript="Atom: Select inside bracket"),
            "remove bracket [from] selection":       R(Key("c-lbrace"), rdescript="Atom: Remove bracket from selection"), #Duplicate shortcut keys Line 52 Unresolved
            "close [current] tag":                   R(Key("cs-p") + Text("bracket matcher: close tag") + Pause("4") + Key("enter"), rdescript="Atom: Close current tag"), #Dragonfly does not contain in key names 'period' or '.'
            "remove matching brackets":              R(Key("ac-backspace"), rdescript="Atom: Remove matching brackets"),
        #Command Palette Submenu
            "[toggle] [command] palette":            R(Key("cs-p"), rdescript="Atom: Toggle Command Palette"),
        #Dev Live Reload Submenu
            "reload [all] styles":                   R(Key("acs-r"), rdescript="Atom: Reload All Styles"),
        #Git Diff Submenu
            "move to next diff [different]":         R(Key("cs-p") + Text("move to next diff") + Pause("4") + Key("enter"), rdescript="Atom: Move to Next Diff"),
            "move to previous diff [different]":     R(Key("cs-p") + Text("move to previous diff") + Pause("4") + Key("enter"), rdescript="Atom: Move to Previous Different"),
            "[toggle] diff List":                    R(Key("cs-p") + Text("toggle diff List") + Pause("4") + Key("enter"), rdescript="Atom: Toggle Diff List"),
        #Keybinding Resolver Submenu
            "toggle key binding resolver":           R(Key("cs-p") + Text("key binding resolver: toggle ") + Pause("4") + Key("enter"), rdescript="Atom: Toggle Keybinding Resolver"), #Dragonfly does not contain in key names 'period' or '.'
        #Markdown Preview Submenu
            "markdown preview":                      R(Key("cs-m"), rdescript="Atom: Toggle Preview"),
        #Package Generator Submenu
            "make|generate package":                 R(Key("cs-p") + Text("package generator: generate package") + Pause("4") + Key("enter"), rdescript="Atom: Generate Atom Package"),
            "make|generate syntax theme":            R(Key("cs-p") + Text("package generator: generate syntax theme") + Pause("4") + Key("enter"), rdescript="Atom: Generate Atom Syntax Theme"),
        #Settings View Submenu
            ##"open setting":                        R(Key("c-comma"), rdescript="Atom: Open Setting"),
            "show key bindings":                     R(Key("cs-p") + Text("settings view: show key bindings") + Pause("4") + Key("enter"), rdescript="Atom: Show Keybindings"),
            "installed themes":                      R(Key("cs-p") + Text("settings view: installed themes") + Pause("4") + Key("enter"), rdescript="Atom: Install Themes"),
            "uninstalled themes":                    R(Key("cs-p") + Text("settings view: uninstalled themes") + Pause("4") + Key("enter"), rdescript="Atom: Uninstall Themes"),
            "installed packages":                    R(Key("cs-p") + Text("settings view: installed packages") + Pause("4") + Key("enter"), rdescript="Atom: Install Packages"),
            "uninstalled packages":                  R(Key("cs-p") + Text("settings view: uninstalled packages") + Pause("4") + Key("enter"), rdescript="Atom: Uninstall packages/themes"),
            "manage packages":                       R(Key("cs-p") + Text("settings view: install packages and themes") + Pause("4") + Key("enter"), rdescript="Atom: Install Packages/Themes"),
            "update packages":                       R(Key("cs-p") + Text("settings view: check for package update") + Pause("4") + Key("enter"), rdescript="Atom: Check for Packages"),
        #Snippets Submenu
            "expand":                                R(Key("cs-p") + Text("snippets: expand") + Pause("4") + Key("enter"), rdescript="Atom: Expand"),
            "next snippet":                          R(Key("tab"), rdescript="Atom: Next Stop|Snippet"),
            "previous snippet":                      R(Key("as-tab"), rdescript="Atom: Previous Stop|Snippet"),
            "available snippet":                     R(Key("as-tab"), rdescript="Atom: Available Snippets"),
        #Styleguide Submenu
            "show style [guide]":                    R(Key("cs-g"), rdescript="Atom: Show Styleguide"),
            #Symbol
            "find symbol":                           R(Key("c-r"), rdescript="Atom: Find Symbol"),
            "project symbol":                        R(Key("cs-r"), rdescript="Atom: Project Symbol"),
        #Timecop Submenu
            "timecop":                               R(Key("cs-p") + Text("timecop:view") + Pause("4") + Key("enter"), rdescript="Atom: Show Timecop"),
        #Tree View Submenu
            "focus":                                 R(Key("c-0"), rdescript="Atom: Toggle Focus on TreeView"),
            "remove trailing white spaces":          R(Key("cs-p") + Text("remove trailing white spaces") + Pause("4") + Key("enter"), rdescript="Atom: Remove Trailing White Spaces"),
            "[toggle] tree view":                    R(Key("c-backslash"), rdescript="Atom: Toggle"),
            "[reveal] active file":                  R(Key("cs-backslash"), rdescript="Atom: Reveal Active File"),
            "[toggle] tree side":                    R(Key("cs-p") + Text("Tree View: show") + Pause("4") + Key("enter"), rdescript="Atom: Toggle Tree Side"),
        #Extras
            "tree show":                             R(Key("cs-p") + Text("Tree View: Show") + Pause("4") + Key("enter"), rdescript="Atom: Tree View: Show"),
            "tree rename":                           R(Key("cs-p") + Text("Tree View: Rename") + Pause("4") + Key("enter"), rdescript="Atom: Tree View: Rename"),
            "tree remove":                           R(Key("cs-p") + Text("Tree View: Remove") + Pause("4") + Key("enter"), rdescript="Atom: Tree View: Remove"),
            "tree add file":                         R(Key("cs-p") + Text("Tree View: Add File") + Pause("4") + Key("enter"), rdescript="Atom: Tree View: Add File"),
            "tree duplicate":                        R(Key("cs-p") + Text("Tree View: Duplicate") + Pause("4") + Key("enter"), rdescript="Atom: Tree View: Duplicate"),
            "tree add folder":                       R(Key("cs-p") + Text("Tree View: Add Folder") + Pause("4") + Key("enter"), rdescript="Atom: Tree View: Add Folder"),
        #Whitespaces Submenu
            "remove trailing white spaces":          R(Key("cs-p") + Text("remove trailing white spaces") + Pause("4") + Key("enter"), rdescript="Atom: Remove Trailing White Spaces"),
            "convert tabs to spaces":                R(Key("cs-p") + Text("convert tabs to spaces") + Pause("4") + Key("enter"), rdescript="Atom: Convert Tabs to Spaces"),
            "convert spaces to tabs":                R(Key("cs-p") + Text("convert spaces to tabs") + Pause("4") + Key("enter"), rdescript="Atom: Convert Spaces to Tabs"),
        #Merge Conflicts Submenu
            "[git] detect merge conflicts":          R(Key("cs-p") + Text("Merge Conflicts") + Pause("4") + Key("enter"),(""), rdescript="Atom: Detect"),

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

#Atom Third-Party Package Commands-------------------------------------------------------------------------------------------------
        #Adom Beautify
            "run beautify script":                   R(Key("ac-b"), rdescript="Atom: Run Beautify Package"),
        #Compare Files
            "compare files":                         R(Key("ac-c"), rdescript="Atom: Compare Files"),
        #Toggle Quotes
            "toggle quotes":                         R(Key("cs-apostrophe"), rdescript="Atom: Toggle Quotes: Single or Double"),
        #Script
            "script run by line":                    R(Key("cs-p") + Text("Script:run script by line") + Pause("4") + Key("enter"), rdescript="Atom: "),
            "script close view":                     R(Key("cs-p") + Text("Script:close view") + Pause("4") + Key("enter"), rdescript="Atom: "),
            "script run options":                    R(Key("cs-p") + Text("Script:run options") + Pause("4") + Key("enter"), rdescript="Atom: "),
            "script kill process":                   R(Key("cs-p") + Text("Script:kill process") + Pause("4") + Key("enter"), rdescript="Atom: "),
            "script save options":                   R(Key("cs-p") + Text("Script:save options") + Pause("4") + Key("enter"), rdescript="Atom: "),
            "script close options":                  R(Key("cs-p") + Text("Script:close options") + Pause("4") + Key("enter"), rdescript="Atom: "),
            "script run":                            R(Key("cs-p") + Text("Script:run") + Pause("4") + Key("enter"), rdescript="Atom: "),
            "script configure script":               R(Key("cs-p") + Text("Script:configure script") + Pause("4") + Key("enter"), rdescript="Atom: "),
            "script copy run results":               R(Key("cs-p") + Text("Script:copy run results") + Pause("4") + Key("enter"), rdescript="Atom: "),
        #Delete Plus
            "delete words":                          R(Key("cs-p") + Text("Delete Plus: delete") + Pause("4") + Key("enter"), rdescript="Atom: Delete Plus"),
        #Last Edit
            "last edit":                             R(Key("c-i"), rdescript="Atom: Last Edit"),
        #Looper
            "looping down cursor":                   R(Key("a-down"), rdescript="Atom: Looping Down at Cursor"),
            "looping up cursor":                     R(Key("a-up"), rdescript="Atom: Looping Up at Cursor"),
            "looping up":                            R(Key("wa-up"), rdescript="Atom: Looping Up"),
            "looping down":                          R(Key("wa-down"), rdescript="Atom: Looping Down"),
    #Open on GitHub
            "github [open] blame":                   R(Key("cs-p") + Text("Open on GitHub: blame") + Pause("4") + Key("enter"), rdescript="Atom: Open On Github @ Blame"),
            "github [open] branch compare":          R(Key("cs-p") + Text("Open on GitHub: branch compare") + Pause("4") + Key("enter"), rdescript="Atom: Open On Github @ Branch Compare"),
            "github [open] copy URL":                R(Key("cs-p") + Text("Open on GitHub: copy URL") + Pause("4") + Key("enter"), rdescript="Atom: Open On Github @ Copy URL"),
            "github [open] file":                    R(Key("cs-p") + Text("Open on GitHub: file") + Pause("4") + Key("enter"), rdescript="Atom: Open On Github @ File"),
            "github [open] history":                 R(Key("cs-p") + Text("Open on GitHub: history") + Pause("4") + Key("enter"), rdescript="Atom: Open On Github @ History"),
            "github [open] issues":                  R(Key("cs-p") + Text("Open on GitHub: issues") + Pause("4") + Key("enter"), rdescript="Atom: Open On Github @ Issues"),
            "github [open] repository":              R(Key("cs-p") + Text("Open on GitHub: repository") + Pause("4") + Key("enter"), rdescript="Atom: Open On Github @ Repository"),
    #Git Plus
            "git add":                               R(Key("cs-p") + Text("Git Plus: add") + Pause("4") + Key("enter"), rdescript="Atom: Git Add"),
            "git add all":                           R(Key("cs-p") + Text("Git plus: add all") + Pause("4") + Key("enter"), rdescript="Atom: Git Add All"),
            "git commit":                            R(Key("cs-p") + Text("Git Plus: git commit") + Pause("4") + Key("enter"), rdescript="Atom: Git Commit"),
            "git diff":                              R(Key("cs-p") + Text("Git Plus: diff") + Pause("4") + Key("enter"), rdescript="Atom: Git Diff"),
            "git diff all":                          R(Key("cs-p") + Text("Git Plus: diff all") + Pause("4") + Key("enter"), rdescript="Atom: Git Diff All"),
            "git add commit":                        R(Key("cs-p") + Text("Git Plus: add commit") + Pause("4") + Key("enter"), rdescript="Atom: Git Add Commit"),
            "git add all commit":                    R(Key("cs-p") + Text("Git Plus: add all commit") + Pause("4") + Key("enter"), rdescript="Atom: Git Add All Commit"),
            "git add all commit push":               R(Key("cs-p") + Text("Git Plus: add all commit push") + Pause("4") + Key("enter"), rdescript="Atom: Git Add All Commit Push"),
            "git log":                               R(Key("cs-p") + Text("Git Plus: log") + Pause("4") + Key("enter"), rdescript="Atom: Git Git Log"),
            "git merge":                             R(Key("cs-p") + Text("Git Plus: merge") + Pause("4") + Key("enter"), rdescript="Atom: Git Git Merge"),
            "git pull using rebase":                 R(Key("cs-p") + Text("Git Plus: pull using rebase") + Pause("4") + Key("enter"), rdescript="Atom: Git Git Pull Using Rebase"),
    #Project Manager
            "project manager":                       R(Key("cs-p") + Text("Project Manager:toggle") + Pause("4") + Key("enter"), rdescript="Atom: Project Manager: Toggle"),
            "save project":                          R(Key("cs-p") + Text("Project Manager:save project") + Pause("4") + Key("enter"), rdescript="Atom: Project Manager: Save Project"),
            "edit project":                          R(Key("cs-p") + Text("Project Manager:edit project") + Pause("4") + Key("enter"), rdescript="Atom: Project Manager: Edit Project"),
            "reload project setting":                R(Key("cs-p") + Text("Project Manager:project settings") + Pause("4") + Key("enter"), rdescript="Atom: Project Manager: Project Settings"),
    #Menu Sidebar
            "[project] sidebar":                     R(Key("cs-p") + Text("Project Sidebar: toggle") + Pause("4") + Key("enter"), rdescript="Atom:Project Sidebar: Toggle"),

#Atom Shortcut Development--------------------------------------------------------------------------------------------------------------------------------------------------------
    # Template to create more commands. Documentation: https://dragonfly.readthedocs.org/en/latest/actions.html
        # Used for basic key shortcuts
            #"text for voice command":               R(Key("modifier-key"), rdescript="program name: command name/description"),
            #"":                                     R(Key(""), rdescript="Atom: "),
        # Used for command that utilizes the "command palette" shortcut in the absence of assigned keyboard shortcut.
            #"text for voice command":               R(Key("cs-p") + Text("text as described in command palette") + Pause("4") + Key("enter"), rdescript="command name/description"),
            #"":                                     R(Key("cs-p") + Text("") + Pause("4") + Key("enter"),
    #Atom Shortcut Snippets
            "dev keys [input] [<n>]":                R(Text('#"":                                     R(Key("-"), rdescript="Atom: "),') + Key("enter"), rdescript="Macro: Dev Keys [Input] #") * Repeat(extra="n"),
            "dev [command] palette [<n>]":           R(Text('#"":                                     R(Key("cs-p") + Text("") + Pause("4") + Key("enter"), rdescript="Atom: "),') + Key("enter"), rdescript="Macro: Dev [Command] Palette #") * Repeat(extra="n"),
            "dev convert":                           Text('R(Key("cs-p") + Text("") + Pause("4") + Key("enter"),') + Key("delete"),

            }
    extras = [
            Dictation("text"),
            Dictation("mim"),
            IntegerRef("n", 1, 10000),
            IntegerRef("n2", 1, 9),
             ]
    defaults = {"n": 1, "mim":""}

#---------------------------------------------------------------------------

context = AppContext(executable="atom", title="Atom")
grammar = Grammar("Atom", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
