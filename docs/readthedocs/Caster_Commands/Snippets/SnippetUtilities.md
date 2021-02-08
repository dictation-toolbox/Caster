# Snippet Utilities

In order to make development of grammars with snippets easier 

```python

```

## Utilities for generating special snippet constructs

### placeholder

First we start with utility to generate snippet code for placeholders fields at runtime

```python
def placeholder(field,default  = ""):	
```

where field  and default must be convertible to string
typically field is going to be an integer

```python
placeholder(1) = $1
placeholder(1,"data") = ${1:data}
placeholder(1,42)  = ${1:42}
```

but can also be anything else convertible to string because sublime allows you to define default values for environmental variables/snippet parameters

```python
placeholder("PARAMETER") = $PARAMETER
placeholder("PARAMETER","data") = ${PARAMETER:data}
placeholder("PARAMETER",2)  = ${PARAMETER:2}

```

Alternatively if you want you can also pass a tuple to the field argument if you want fields nested one within the other,for example

```python
placeholder((1,2),"data")  = ${1:${2:data}}  = placeholder(1,placeholder(2,"data"))
placeholder((1,"INTERESTING"),"data")  = ${1:${INTERESTING:data}} = placeholder(1,placeholder("INTERESTING","data"))
```

### Regular Expressions

Sublime support substitutions regular expressions using a syntax like

```
${var_name/regex/format_string/options} or
${var_name/regex/format_string}
```

You can find out more detailed information about regular expressions [here](https://sublime-text.readthedocs.io/en/stable/extensibility/snippets.html)

in a manner similar placeholder,a `regular` function is supplied in order to output this kind of text

```python
def regular(varname,regex,format_string,options  = "",*,
	ignore_case=False,replace_all=False,ignore_new_lines=True):
```

Please note that the arguments after `options` that is `ignore_case` and `replace_all` and `ignore_new_lines` are there for convenience to make setting options appropriately easier.

## Quickly loading snippets into grammars

In many cases it could be preferable to seemly be able to load snippets into grammars from a dictionary of the form

```python
"spoken rule":correspondence_snippet
```

This is possible via `load_snippets` ,which can be used as a decorator in the following manner:

```python
snippets = {
	"function main":[
	    "int main(){\n\t$0\n}\n",
	    "int main(int argc, char** argv){\n\t$0\n}\n",
	],
	"if end":"if($2 == ${1:v}.end()){\n\t$0\n}\n",
    "attribute assign":
        lambda n: "".join(["auto& " + placeholder(x) + " = $1."+placeholder(x)+";\n" for x in range(2,n + 2)]),
    "spec <dragonfly_action>": lambda dragonfly_action: '"$1":R({0}),'.format(dragonfly_action),
}

@load_snippets(snippets)
class SnippetGrammar(MappingRule):
	"""docstring for SnippetGrammar"""
	mapping = {}
	extras = [
		Choice("dragonfly_action",{
                "key":'Key("$0")',
                "text":'Text("$0")',
                "mimic":'Mimic("$0")',
                "focus":'FocusWindow("$0")',
                "wait window":'WaitWindow("$0")',
                "mouse":'Mouse("$0")',
                "function":'Function($0)',
                "sublime":'SublimeCommand("$0")',
            }
        )
	]
	default = {}	

```

Please notice we do not need to explicitly provide `IntegerRefST("n")` as it is handled by the decorator!
Furthermore because the for signature actually looks like

```python
def load_snippets(snippets,extras = [], defaults = {}):
	"""Utility in order to decorate grammars to quickly load snippets from a raw dictionary format
	
	Args:
	    snippets (TYPE): Description
	    extras (list, optional): Description
	    defaults (dict, optional): Description
	
	Returns:
	    TYPE: Description
	
	Raises:
	    TypeError: Description
```

We can also supply the `Choice` as `extras` argument to `load_snippets`

```python
snippets = {
	"function main":[
	    "int main(){\n\t$0\n}\n",
	    "int main(int argc, char** argv){\n\t$0\n}\n",
	],
	"if end":"if($2 == ${1:v}.end()){\n\t$0\n}\n",
    "attribute assign":
        lambda n: "".join(["auto& " + placeholder(x) + " = $1."+placeholder(x)+";\n" for x in range(2,n + 2)]),
    "spec <dragonfly_action>": lambda dragonfly_action: '"$1":R({0}),'.format(dragonfly_action),
}

extras  = [
		Choice("dragonfly_action",{
                "key":'Key("$0")',
                "text":'Text("$0")',
                "mimic":'Mimic("$0")',
                "focus":'FocusWindow("$0")',
                "wait window":'WaitWindow("$0")',
                "mouse":'Mouse("$0")',
                "function":'Function($0)',
                "sublime":'SublimeCommand("$0")',
            }
        )
]

@load_snippets(snippets,extras)
class SnippetGrammar(MappingRule):
	"""docstring for SnippetGrammar"""
	mapping = {}
	extras = []
	default = {}	
```

Ok, so far we have seen about our snippets dictionary can contain anything that we could put inside in `R(Snippet())` saving us a few keystrokes. However, with what we have seen so far we still need to to create dragonfly extras like the choice element separately, which can be a burden if we have a spec that only needs a single choice element. In order to address this issue and make your life easier the dictionary of snippets can also contain dictionaries as values like so

```python
snippets = {
	"function main":[
	    "int main(){\n\t$0\n}\n",
	    "int main(int argc, char** argv){\n\t$0\n}\n",
	],
	"if end":"if($2 == ${1:v}.end()){\n\t$0\n}\n",
    "attribute assign":
        lambda n: "".join(["auto& " + placeholder(x) + " = $1."+placeholder(x)+";\n" for x in range(2,n + 2)]),
    "spec <dragonfly_action>": {
        "key":'"$1":R(Key("$0"))',
        "text":'"$1":R(Text("$0"))',
        "mimic":'"$1":R(Mimic("$0"))',
        "focus":'"$1":R(FocusWindow("$0"))',
        "wait window":'"$1":R(WaitWindow("$0"))',
        "mouse":'"$1":R(Mouse("$0"))',
        "function":'"$1":R(Function($0))',
        "sublime":'"$1":R(SublimeCommand("$0"))',
    }
}


@load_snippets(snippets)
class SnippetGrammar(MappingRule):
	"""docstring for SnippetGrammar"""
	mapping = {}
	extras = []
	default = {}	
```

in which case a rule of the form 

```python
"spec <dragonfly_action>": R(Snippet("%(dragonfly_action)s"))
```

along with an appropriate `Choice("dragonfly_action",{...})` will be produced! Please note that this_option is only available if there is a single choice in the spoken rule/spec!



