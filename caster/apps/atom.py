"""
__author__ = 'Zone22'

Command-module for Atom
Official Site "https://atom.io/"
"""
from dragonfly import (Grammar, AppContext, MappingRule,
                       Dictation, IntegerRef,
                       Key, Text, Repeat, Pause)

from caster.lib.dfplus.state.short import R

class CommandRule(MappingRule):

    mapping = {

# Menu UI---Spoken Command/Action-----------------> Shortcut keys-------------> #Displayed Text
# Spoken commands that are commented out do not have assigned default shortcut keys or are incompatible.
# Legend: '#' For not assigned '##' for duplicates or '###' not supported by dragonfly.
	#File Menu
			"new window":							R(Key("cs-n"), rdescript="Atom: New Window"),
			"new file":								R(Key("c-n"), rdescript="Atom: New File"),
			"open file":							R(Key("c-o"), rdescript="Atom: Open File"),
			"open folder":							R(Key("cs-o"), rdescript="Atom: Open Folder"),
			"add project folder":					R(Key("ac-o"), rdescript="Atom: Add Project Folder"),
			"settings":								R(Key("cs-t"), rdescript="Atom: Settings"),
			"save":									R(Key("c-comma"), rdescript="Atom: Save"),
			#"Open your config":					R(Key(""), rdescript="Atom: Open Your Config"),
			#"Open your int script":				R(Key(""), rdescript="Atom: Open Your Int Script"),
			#"Open your key map":					R(Key(""), rdescript="Atom: Open Your Key Map"),
			#"Open your snippet":					R(Key(""), rdescript="Atom: Open Your Snippet"),
			#"Open your stylesheet":				R(Key(""), rdescript="Atom: Open Your Stylesheet")
			"save":									R(Key("c-s"), rdescript="Atom: Save"),
			"save as":								R(Key("cs-s"), rdescript="Atom: Save As"),
			#"save all":							R(Key(""), rdescript="Atom: Save All"),
			"close tab":							R(Key("c-w"), rdescript="Atom: Close Tab"),
			#"close pane":							R(Key(""), rdescript="Atom: Close Pane"),
			"close window":							R(Key("cs-w"), rdescript="Atom: Close Window"),
	#Edit Menu
			"undo":									R(Key("c-z"), rdescript="Atom: Undo"),
			"redo":									R(Key("c-y"), rdescript="Atom: Redo"),
			"cut":									R(Key("s-delete"), rdescript="Atom: Cut"),
			"copy":									R(Key("c-insert"), rdescript="Atom: Copy"),
			"copy path":							R(Key("cs-c"), rdescript="Atom: Copy Path"),
			"paste":								R(Key("s-insert"), rdescript="Atom: Paste"),
			"select all":							R(Key("c-a"), rdescript="Atom: Select All"),
			"toggle comments":						R(Key("c-slash"), rdescript="Atom: Toggle Comments"),
			"reflow section":						R(Key("ac-q"), rdescript="Atom: Reflow SECTION"),
			"select encoding":						R(Key("cs-u"), rdescript="Atom: Select Encoding"),
			"go to line [<n>]":						R(Key("c-g/20") + Repeat(extra="n2") + Key("enter"), rdescript="Atom: Go to Line #"),
			"select grammar":						R(Key("cs-l"), rdescript="Atom: Select Grammar"),
		#Lines Submenu
			"indent":								R(Key("c-lbrace"), rdescript="Atom: Indent"),
			"outdent":								R(Key("c-rightbrace"), rdescript="Atom: Outdent"),
		    #"auto indent":							R(Key(""), rdescript="Atom: Auto Indent"),
			"move line up":							R(Key("c-up"), rdescript="Atom: Move Line Up"),
            "move line down":						R(Key("c-down"), rdescript="Atom: Move Line Down"),
			"duplicate line":						R(Key("cs-d"), rdescript="Atom: Duplicate Line"),
			"delete line":							R(Key("cs-k"), rdescript="Atom: Delete Line"),
			"join line":							R(Key("c-j"), rdescript="Atom: Join Line"),
		#Text Submenu
			#"uppercase":							R(Key(""), rdescript="Atom: Convert Uppercase"),
			#"lowercase":							R(Key(""), rdescript="Atom: Convert lowercase"),
			"delete to end of word":				R(Key("c-delete"), rdescript="Atom: Delete to End oF Word"),
			#"delete to previous word boundary":	R(Key(""), rdescript="Atom: Delete to previous word boundary"),
			#"delete to next word boundary":		R(Key(""), rdescript="Atom: Delete to next word boundary"),
			"delete line":							R(Key("cs-k"), rdescript="Atom: Delete Line"),
			#"transpose":							R(Key(""), rdescript="Atom: Transpose"),
		#Folding Submenu
			"fold":									R(Key("ac-lbrace"), rdescript="Atom: Fold"),
			"unfold":								R(Key("ac-rightbrace"), rdescript="Atom: Unfold"),
			"unfold all":							R(Key("acs-rightbrace"), rdescript="Atom: Unfold All"),
			#"fold level 1":						R(Key(""), rdescript="Atom: Fold Level 1"),
			#"fold level 2":						R(Key(""), rdescript="Atom: Fold Level 2"),
			#"fold level 3":						R(Key(""), rdescript="Atom: Fold Level 3"),
			#"fold level 4":						R(Key(""), rdescript="Atom: Fold Level 4"),
			#"fold level 5":						R(Key(""), rdescript="Atom: Fold Level 5"),
			#"fold level 6":						R(Key(""), rdescript="Atom: Fold Level 6"),
			#"fold level 7":						R(Key(""), rdescript="Atom: Fold Level 7"),
			#"fold level 8":						R(Key(""), rdescript="Atom: Fold Level 8"),
			#"fold level 9":						R(Key(""), rdescript="Atom: Fold Level 9"),
		#Bookmarks Submenu
			"view all":								R(Key("c-f2"), rdescript="Atom: Reflow Section"),
			"toggle bookmark":						R(Key("ca-f2"), rdescript="Atom: Toggle Bookmark"),
			"next bookmark":						R(Key("f2"), rdescript="Atom: Jump to Next Bookmark"),
			"previous bookmark":					R(Key("s-f2"), rdescript="Atom: Jump to Previous Bookwork"),
	#View Menu
			"Reload File":							R(Key("ac-r"), rdescript="Atom: Reload"),
			"fullscreen":							R(Key("f11"), rdescript="Atom: Toggle Fullscreen"),
			#"toggle menubar":						R(Key(""), rdescript="Atom: Toggle Menubar"),
			"increase font size":					R(Key("cs-equals"), rdescript="Atom: Increase Font Size"),
			"decrease font size":					R(Key("cs-minus"), rdescript="Atom: Decrease Font size"),
			"reset font size":						R(Key("c-0"), rdescript="Atom: Reset Font Size"),
			#"toggle soft wrap":					R(Key(""), rdescript="Atom: Toggle Soft Wrap"),
			##"toggle command palette":				R(Key(""), rdescript="Atom: Toggle Command Palette"),
			"toggle treeview":						R(Key("c-backslash"), rdescript="Atom: Toggle Treeview"),
		#Panes Submenu
			#"split up":							R(Key(""), rdescript="Atom: Split Up"),
			#"split down":							R(Key(""), rdescript="Atom: Split Down"),
			#"split left":							R(Key(""), rdescript="Atom: Split Left"),
			#"split right":							R(Key(""), rdescript="Atom: Split Right"),
			#"focus next pane":						R(Key(""), rdescript="Atom: Focus Next Pane"),
			#"focus previous pane":					R(Key(""), rdescript="Atom: Focus Previous Pane"),
			#"focus pane above":					R(Key(""), rdescript="Atom: Focused Pane Above"),
			#"focus pane below":					R(Key(""), rdescript="Atom: Focus Pane Below"),
			#"focus pane on left":					R(Key(""), rdescript="Atom: Focus On left"),
			#"focus pane on right":					R(Key(""), rdescript="Atom: Focus Pane on Right"),
			#"close pane":							R(Key(""), rdescript="Atom: Close Pane "),
		#Developer Submenu
			#"open in development mode":			R(Key(""), rdescript="Open in Development Mode"),
			"run atom specs":						R(Key("ac-s"), rdescript="Atom: Run Atoms Specs"),
			"run package specs":					R(Key("ac-p"), rdescript="Atom: Run Package Specs "),
			"toggle developer tools":				R(Key("ac-i"), rdescript="Atom: Toggle Developer Tools"),
	#Selection Menu
			"add selection above":					R(Key("ac-up"), rdescript="Atom: Add Selection Above"),
			"add selection below":					R(Key("ac-down"), rdescript="Atom: Add Selection Below"),
			#"split into lines":					R(Key(""), rdescript="Atom: Split Into lines"),
			"single section":						R(Key("escape"), rdescript="Atom: Single Section"),
			"select to top":						R(Key("as-home"), rdescript="Atom: Select to Top"),
			"select to bottom":						R(Key("as-end"), rdescript="Atom: Select to Bottom"),
			"select line":							R(Key("c-l"), rdescript="Atom: Select Line"),
			#"select word":							R(Key(""), rdescript="Atom: Select Word"),
			"select to beginning of word":			R(Key("cs-left"), rdescript="Atom: Select to Beginning of Word"),
			#"select to beginning of line":			R(Key(""), rdescript="Atom: Select to Beginning of line"),
			"select to first character of line":	R(Key("s-home"), rdescript="Atom: Select to First character of Line"),
			"select to end of word":				R(Key("cs-right"), rdescript="Atom: Select to End of Word"),
			"select to end of line":				R(Key("s-end"), rdescript="Atom: Select to End of line"),
			"select inside brackets":				R(Key("ac-m"), rdescript="Atom: Select Inside Brackets"),
	#Find Menu
			"find in buffer":						R(Key("c-f"), rdescript="Atom: Find in Buffer"),
			"replacing in buffer":					R(Key("ac-f"), rdescript="Atom: Replacing in Buffer"),
			"select next":							R(Key("c-d"), rdescript="Atom: Select Next"),
			"select all":							R(Key("c-f3"), rdescript="Atom: Select All"),
			#"toggle find in buffer":				R(Key(""), rdescript="Atom: Toggle Find in Buffer"),
			"find in project":						R(Key("cs-f3"), rdescript="Atom: Find in Project"),
			#"toggle find in project":				R(Key(""), rdescript="Atom: Toggle Find in Project"),
			"find next":							R(Key("f3"), rdescript="Atom: Find Next"),
			"find previous":						R(Key("s-f3"), rdescript="Atom: Find Previous"),
			#"replace next":						R(Key(""), rdescript="Atom: Replace Next"),
			#"replace all":							R(Key(""), rdescript="Atom: Replace All"),
			"find buffer":							R(Key("c-b"), rdescript="Atom: Find Buffer"),
			"find file":							R(Key("c-p"), rdescript="Atom: Find File"),
			"find modified file":					R(Key("cs-b"), rdescript="Atom: Find Modified File"),
	#Packages Menu
		#Bracket Matcher Submenu
			"go to matching bracket":				R(Key("c-m"), rdescript="Atom: go to matching bracket"),
			##"select inside bracket":				R(Key("ac-m"), rdescript="Atom: Select inside bracket"),
			"remove bracket from selection":		R(Key("c-lbrace"), rdescript="Atom: Remove bracket from selection"), #Duplicate shortcut keys Line 52 Unresolved
		    ###"close current tag":					R(Key("ac-period"), rdescript="Atom: Close current tag"), #Dragonfly does not contain in key names 'period' or '.'
			"remove matching brackets":				R(Key("ac-backspace"), rdescript="Atom: Remove matching brackets"),
		#Command Palette Submenu
			"toggle command palette":				R(Key("cs-p"), rdescript="Atom: Toggle Command Palette"),
		#Dev Live Reload Submenu
			"reload all styles":					R(Key("acs-r"), rdescript="Atom: Reload All Styles"),
		#Git Diff Submenu
			#"move to next diff":					R(Key(""), rdescript="Atom: Move to Next Diff"),
			#"move to previous different":			R(Key(""), rdescript="Atom: Move to Previous Different"),
			#"toggle diff List":					R(Key(""), rdescript="Atom: Toggle Diff List"),
		#Keybinding Resolver Submenu
			###"toggle key binding resolver":		R(Key("c-period"), rdescript="Atom: Toggle Keybinding Resolver"), #Dragonfly does not contain in key names 'period' or '.'
		#Markdown Preview Submenu
			"markdown preview":						R(Key("cs-m"), rdescript="Atom: Toggle Preview"),
		#Open On Github Submenu
			#"blame":								R(Key(""), rdescript="Atom: Blame"),
			#"branch compare":						R(Key(""), rdescript="Atom: Branch Compare"),
			#"copy URL":							R(Key(""), rdescript="Atom: Copy URL"),
			#"file":								R(Key(""), rdescript="Atom: File"),
			#"history":								R(Key(""), rdescript="Atom: History"),
			#"issues":								R(Key(""), rdescript="Atom: Issues"),
			#"repository":							R(Key(""), rdescript="Atom: Repository"),
		#Package Generator Submenu
			#"generate atom package":				R(Key(""), rdescript="Atom: Generate Atom Package"),
			#"generate atom syntax theme":			R(Key(""), rdescript="Atom: Generate Atom Syntax Theme"),
		#Settings View Submenu
			"open setting":							R(Key("c-comma"), rdescript="Atom: Open Setting"),
			#"show key bindings":					R(Key(""), rdescript="Atom: Show Keybindings"),
			#"install packages | install themes":	R(Key(""), rdescript="Atom: install packages/themes"),
			#"update packages | install themes":	R(Key(""), rdescript="Atom: Update packages/themes"),
			#"manage packages":						R(Key(""), rdescript="Atom: Manage Packages"),
			#"manage themes":						R(Key(""), rdescript="Atom: Manage Themes"),
		#Snippets Submenu
			#"expand":								R(Key(""), rdescript="Atom: Expand"),
			"next snippet":							R(Key("tab"), rdescript="Atom: Next Stop|Snippet"),
			"previous snippet":						R(Key("as-tab"), rdescript="Atom: Previous Stop|Snippet"),
			"available snippet":					R(Key("as-tab"), rdescript="Atom: Available Snippets"),
		#Styleguide Submenu
			"show style guide":						R(Key(""), rdescript="Atom: Show Styleguide"),
			#Symbol
			"find symbol":							R(Key("c-r"), rdescript="Atom: Find Symbol"),
			"project symbol":						R(Key("cs-r"), rdescript="Atom: Project Symbol"),
		#Timecop Submenu
			#"Show":								R(Key(""), rdescript="Atom: Show"),
		#Tree View Submenu
			"focus":								R(Key("c-0"), rdescript="Atom: Focus"),
			"toggle":								R(Key("c-backslash"), rdescript="Atom: Toggle"),
			"reveal active file":					R(Key("cs-backslash"), rdescript="Atom: Reveal Active File"),
			#"toggle tree side":					R(Key(""), rdescript="Atom: Toggle Tree Side"),
		#Whitespaces Submenu
			#"remove trailing white spaces":		R(Key(""), rdescript="Atom: Remove Trailing White Spaces"),
			#"convert tabs to spaces":				R(Key(""), rdescript="Atom: Convert Tabs to Spaces"),
			#"convert spaces to tabs":				R(Key(""), rdescript="Atom: Convert Spaces to Tabs"),
		#Merge Conflicts Submenu
			#"Detect Merge Conflicts":				R(Key(""), rdescript="Atom: Detect"),
            }
    extras = [
            Dictation("text"),
            IntegerRef("n", 1, 10000),
			IntegerRef("n2", 1, 9),
             ]
    defaults ={"n": 1, "text":"nothing"}

#---------------------------------------------------------------------------

context = AppContext(executable="atom", title="Atom")
grammar = Grammar("Atom", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
	global grammar
	if grammar: grammar.unload()
	grammar = None
