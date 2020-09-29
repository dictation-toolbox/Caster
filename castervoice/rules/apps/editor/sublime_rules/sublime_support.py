try : 
	from sublime_rules.snippet_utilities import placeholder,regular,regex
	from sublime_rules.sublime_snippets import SublimeCommand,Snippet,SnippetTransform
	from sublime_rules.sublime_communication_support import validate_subl,send_sublime,send_snippet,send_quick_panel
except :
	from castervoice.rules.apps.editor.sublime_rules.snippet_utilities import placeholder,regular,regex
	from castervoice.rules.apps.editor.sublime_rules.sublime_snippets import SublimeCommand,Snippet,SnippetTransform
	from castervoice.rules.apps.editor.sublime_rules.sublime_communication_support import validate_subl,send_sublime,send_snippet,send_quick_panel
	