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

# Menu UI---Spoken Command/Action-----------------> Shortcut keys-------> #Displayed Text
#Spoken commands that are commented out do not have assigned default shortcut keys.
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
			"Save":									R(Key("c-s"), rdescript="Atom: Save"),
			"save as":								R(Key("cs-s"), rdescript="Atom: Save As"),
			#"save all":							R(Key("Control shift S"), rdescript="Atom: Save All"),
			"close tab":							R(Key("c-w"), rdescript="Atom: Close Tab"),
			#"close pane":							R(Key(""), rdescript="Atom: Close Pane"),
			"close window":							R(Key("cs-w"), rdescript="Atom: Close Window"),
	#Edit Menu
			"undo":									R(Key(""), rdescript="Atom: Undo"),
			"redo":									R(Key(""), rdescript="Atom: Redo"),
			"cut":									R(Key(""), rdescript="Atom: Cut"),
			"copy":									R(Key(""), rdescript="Atom: Copy"),
			"copy path":							R(Key(""), rdescript="Atom: Copy Path"),
			"paste":								R(Key(""), rdescript="Atom: Paste"),
			"select all":							R(Key(""), rdescript="Atom: Select All"),
			"toggle comments":						R(Key(""), rdescript="Atom: Toggle Comments"),
			"reflow section":						R(Key(""), rdescript="Atom: Reflow SECTION"),
			"select encoding":						R(Key(""), rdescript="Atom: Select Encoding"),
			"go to line":							R(Key(""), rdescript="Atom: Go to Line"),
			"select grammar":						R(Key(""), rdescript="Atom: Select Grammar"),
		#Bookmarks Submenu
			"view all":								R(Key(""), rdescript="Atom: Reflow Section"),
			"toggle bookmark":						R(Key(""), rdescript="Atom: Toggle Bookmark"),
			"next bookmark":						R(Key(""), rdescript="Atom: Jump to Next Bookmark"),
			"previous bookmark":					R(Key(""), rdescript="Atom: Jump to Previous Bookwork"),
		#Lines Submenu
			"indent":								R(Key(""), rdescript="Atom: Indent"),
			"outdent":								R(Key(""), rdescript="Atom: Outdent"),
		#"auto indent":								R(Key(""), rdescript="Atom: Auto indent"),
			"move line up":							R(Key(""), rdescript="Atom: Move Line Up"),
			"move line down":						R(Key(""), rdescript="Atom: Move Line Down"),
			"delete line":							R(Key(""), rdescript="Atom: Delete Line"),
			"join line":							R(Key(""), rdescript="Atom: Join Line"),
		#Text Submenu
			#"uppercase":							R(Key(""), rdescript="Atom: Convert Uppercase"),
			#"lowercase":							R(Key(""), rdescript="Atom: Convert lowercase"),
			"delete to end of word":				R(Key(""), rdescript="Atom: Delete to End oF Word"),
			#"delete to previous word boundary":	R(Key(""), rdescript="Atom: Delete to previous word boundary"),
			#"delete to next word boundary":		R(Key(""), rdescript="Atom: Delete to next word boundary"),
			"delete line":							R(Key(""), rdescript="Atom: Delete Line"),
			#"transpose":							R(Key(""), rdescript="Atom: Transpose"),
		#Folding Submenu
			"fold":									R(Key(""), rdescript="Atom: Fold"),
			"unfold":								R(Key(""), rdescript="Atom: Unfold"),
			"unfold all":							R(Key(""), rdescript="Atom: Unfold All"),
			#"fold level 1":						R(Key(""), rdescript="Atom: Fold Level 1"),
			#"fold level 2":						R(Key(""), rdescript="Atom: Fold Level 2"),
			#"fold level 3":						R(Key(""), rdescript="Atom: Fold Level 3"),
			#"fold level 4":						R(Key(""), rdescript="Atom: Fold Level 4"),
			#"fold level 5":						R(Key(""), rdescript="Atom: Fold Level 5"),
			#"fold level 6":						R(Key(""), rdescript="Atom: Fold Level 6"),
			#"fold level 7":						R(Key(""), rdescript="Atom: Fold Level 7"),
			#"fold level 8":						R(Key(""), rdescript="Atom: Fold Level 8"),
			#"fold level 9":						R(Key(""), rdescript="Atom: Fold Level 9"),
	#View Menu
			"Reload File":							R(Key(""), rdescript="Atom: Reload"),
			"fullscreen":							R(Key(""), rdescript="Atom: Toggle Fullscreen"),
			"toggle menubar":						R(Key(""), rdescript="Atom: Toggle Menubar"),
			"increase font size":					R(Key(""), rdescript="Atom: Increase Font Size"),
			"decrease font size":					R(Key(""), rdescript="Atom: Decrease Font size"),
			"reset font size":						R(Key(""), rdescript="Atom: Reset Font Size"),
			"toggle soft wrap":						R(Key(""), rdescript="Atom: Toggle Soft Wrap"),
			#"toggle command palette":				R(Key(""), rdescript="Atom: Toggle Command Palette"),
			"toggle treeview":						R(Key(""), rdescript="Atom: Toggle Treeview"),
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
			"run atom specs":						R(Key(""), rdescript="Atom: Run Atoms Specs"),
			"run package specs":					R(Key(""), rdescript="Atom: Run Package Specs "),
			"toggle developer tools":				R(Key(""), rdescript="Atom: Toggle Developer Tools"),
	#Selection Menu
			"add selection above":					R(Key(""), rdescript="Atom: Add Selection Above"),
			"add selection below":					R(Key(""), rdescript="Atom: Add Selection Below"),
			#"split into lines":					R(Key(""), rdescript="Atom: Split Into lines"),
			"single section":						R(Key(""), rdescript="Atom: Single Section"),
			"select to top":						R(Key(""), rdescript="Atom: Select to Top"),
			"select to bottom":						R(Key(""), rdescript="Atom: Select to Bottom"),
			"select line":							R(Key(""), rdescript="Atom: Select Line"),
			#"select word":							R(Key(""), rdescript="Atom: Select Word"),
			"select to beginning of word":			R(Key(""), rdescript="Atom: Select to Beginning of Word"),
			#"select to beginning of line":			R(Key(""), rdescript="Atom: Select to Beginning of line"),
			"select to first character of line":	R(Key(""), rdescript="Atom: Select to First character of Line"),
			"select to end of word":				R(Key(""), rdescript="Atom: Select to End of Word"),
			"select to end of line":				R(Key(""), rdescript="Atom: Select to End of line"),
			"select inside brackets":				R(Key(""), rdescript="Atom: Select Inside Brackets"),
	#Find Menu
			"find in buffer":						R(Key(""), rdescript="Atom: Find in Buffer"),
			"replacing in buffer":					R(Key(""), rdescript="Atom: Replacing in Buffer"),
			"select next":							R(Key(""), rdescript="Atom: Select Next"),
			"select all":							R(Key(""), rdescript="Atom: Select All"),
			#"toggle find in buffer":				R(Key(""), rdescript="Atom: Toggle Find in Buffer"),
			"find in project":						R(Key(""), rdescript="Atom: Find in Project"),
			#"toggle find in project":				R(Key(""), rdescript="Atom: Toggle Find in Project"),
			"find next":							R(Key(""), rdescript="Atom: Find Next"),
			"find previous":						R(Key(""), rdescript="Atom: Find Previous"),
			#"replace next":						R(Key(""), rdescript="Atom: Replace Next"),
			#"replace all":							R(Key(""), rdescript="Atom: Replace All"),
			"find buffer":							R(Key(""), rdescript="Atom: Find Buffer"),
			"find file":							R(Key(""), rdescript="Atom: Find File"),
			"find modified file":					R(Key(""), rdescript="Atom: Find Modified File"),
	#Packages Menu
		#Bracket Matcher Submenu
			"go to matching bracket":				R(Key(""), rdescript="Atom: go to matching bracket"),
			"select inside bracket":				R(Key(""), rdescript="Atom: Select inside bracket"),
			"remove bracket from selection":		R(Key(""), rdescript="Atom: Remove bracket from selection"),
			"close current tag":					R(Key(""), rdescript="Atom: Close current tag"),
			"remove matching brackets":				R(Key(""), rdescript="Atom: Remove matching brackets"),
		#Command Palette Submenu
			"toggle command palette":				R(Key(""), rdescript="Atom: Toggle Command Palette"),
		#Dev Live Reload Submenu
			"reload all styles":					R(Key(""), rdescript="Atom: Reload All Styles"),
		#Git Diff Submenu
			#"move to next diff":					R(Key(""), rdescript="Atom: Move to Next Diff"),
			#"move to previous different":			R(Key(""), rdescript="Atom: Move to Previous Different"),
			#"toggle diff List":					R(Key(""), rdescript="Atom: Toggle Diff List"),
		#Keybinding Resolver Submenu
			"toggle key binding resolver":			R(Key(""), rdescript="Atom: Toggle Keybinding Resolver"),
		#Markdown Preview Submenu
			"Toggle preview":						R(Key(""), rdescript="Atom: Toggle Preview"),
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
			"open":									R(Key(""), rdescript="Atom: Open"),
			#"show key bindings":					R(Key(""), rdescript="Atom: Show Keybindings"),
			#"install packages | install themes":	R(Key(""), rdescript="Atom: install packages/themes"),
			#"update packages | install themes":	R(Key(""), rdescript="Atom: Update packages/themes"),
			#"manage packages":						R(Key(""), rdescript="Atom: Manage Packages"),
			#"manage themes":						R(Key(""), rdescript="Atom: Manage Themes"),
		#Snippets Submenu
			#"expand":								R(Key(""), rdescript="Atom: Expand"),
			"next stop":							R(Key(""), rdescript="Atom: Next Stop"),
			"previous stop":						R(Key(""), rdescript="Atom: Previous Stop"),
			"available":							R(Key(""), rdescript="Atom: Available"),
		#Styleguide Submenu
			"show":									R(Key(""), rdescript="Atom: Show"),
			#Symbol
			"find symbol":							R(Key(""), rdescript="Atom: Find Symbol"),
			"project symbol":						R(Key(""), rdescript="Atom: Project Symbol"),
		#Timecop Submenu
			#"Show":								R(Key(""), rdescript="Atom: Show"),
		#Tree View Submenu
			"focus":								R(Key(""), rdescript="Atom: Focus"),
			"toggle":								R(Key(""), rdescript="Atom: Toggle"),
			"reveal active file":					R(Key(""), rdescript="Atom: Reveal Active File"),
			#"toggle tree side":					R(Key(""), rdescript="Atom: Toggle Tree Side"),
		#Whitespaces Submenu
			"remove trailing white spaces":			R(Key(""), rdescript="Atom: Remove Trailing White Spaces"),
			"convert tabs to spaces":				R(Key(""), rdescript="Atom: Convert Tabs to Spaces"),
			"convert spaces to tabs":				R(Key(""), rdescript="Atom: Convert Spaces to Tabs"),
		#Merge Conflicts Submenu
			#"Detect Merge Conflicts":				R(Key(""), rdescript="Atom: Detect"),
            }
    extras = [
            Dictation("text"),
            IntegerRef("n", 1, 1000),
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
