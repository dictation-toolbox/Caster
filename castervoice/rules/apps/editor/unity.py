from dragonfly import Key,MappingRule, Dictation, Choice,Text
from castervoice.lib.merge.state.short import R
from castervoice.lib.merge.additions import IntegerRef
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

class UnityRule(MappingRule):
	mapping = {
		"show <window>" : R(Key("c-%(window)s")),
		"search <searchable> [<dictation>]" : R(Key("c-%(searchable)s,c-f") + Text("%(dictation)s")),
		"clear <searchable> [search]" : R(Key("c-%(searchable)s,c-f,backspace")),
		"show console" : R(Key("cs-c")),

		"max view" : R(Key("s-space")),

		"(play | stop) game" : R(Key("c-p")),
		"pause game" : R(Key("cs-p")),

		"build and run" : R(Key("c-b")),
		"build settings" : R(Key("cs-b")),

		"make empty [game object]" : R(Key("as-n")),
		"add component" : R(Key("cs-a")),

		"align with view" : R(Key("cs-f")),
		"move to view" : R(Key("ca-f")),

		"move [sibling] first" : R(Key("c-equals")),
		"move [sibling] last" : R(Key("c-hyphen")),
		"(set active | toggle )" : R(Key("as-a")),

		"[load] selection [<1to9>]" : R(Key("cs-%(1to9)s")),
		"store selection [<1to9>]" : R(Key("ca-%(1to9)s")),

		"rename":
			R(Key("f2")),
	}
	extras = [
		Dictation("dictation"),
        IntegerRef("1to9", 1, 10),
		Choice("searchable",
			{
			"scene" : "1",
			"(hierarchy | hire)" : "4",
			"project" : "5",
			}),
		Choice("window",
			{
			"scene" : "1",
			"game" : "2",
			"inspector" : "3",
			"(hierarchy | hire)" : "4",
			"project" : "5",
			"animation" : "6",
			"profiler" : "7",
			"audio mixer" : "8",
			"asset store" : "9",
			"services" : "0",
			}),
	]
	defaults = {
		"dictation":"",
		"1to9": "1"
	}
def get_rule():
    details = RuleDetails(name = "unity",executable="unity")
    return UnityRule, details
