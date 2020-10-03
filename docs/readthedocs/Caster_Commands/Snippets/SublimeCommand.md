# Sublime Command

<!-- MarkdownTOC  autolink="true" -->

- [Preliminary example](#preliminary-example)
- [Formatting for dynamically commands](#formatting-for-dynamically-commands)
- [Passing parameters](#passing-parameters)
- [Passing callable to parameters](#passing-callable-to-parameters)
- [Acknowledgments](#acknowledgments)

<!-- /MarkdownTOC -->

## Preliminary example

A useful resource for creating your own `SublimeCommand` rules can be [Package Resource Viewer](https://packagecontrol.io/packages/PackageResourceViewer) which allows you to quickly browse files of the packages you have installed.

## Formatting for dynamically commands

Let's look some further commands of the git package

```json
{
     "caption": "Git: Add...",
     "command": "git_add_choice"
 }
{
     "caption": "Git: Status",
     "command": "git_status"
 }
{
     "caption": "Git: Commit",
     "command": "git_commit"
 }
```

Based in our previous example one way to go about this is to create three separate specs

```python
mapping = {
	"git add":      R(SublimeCommand("git_add_choice")),
	"git status": R(SublimeCommand("git_status")),
	"git commit": R(SublimeCommand("git_commit")),
}
```

but this quickly becomes cumbersome and is unnecessarily verbose because we failed to take advantages of the pattern that appears in the sublime commands. In order to address this issue, we can employ formatting options like the ones used by Key/Text and reflector our code into something like

```python
mapping = {
	"git <action>":R(SublimeCommand("git_%(action)s")),
}

Choice("action",{
                "add":"add_choice",
                "commit" : "commit",
                "status" : "status",
            }
)
```

which of course requires less code to add new actions!



## Passing parameters

Let's continue with our Git example and try something different out:


```json
{
        "caption": "Git: Add Current File",
        "command": "git_raw", "args": { "command": "git add", "append_current_file": true }
}
```

Now that is interesting, unlike our previous examples here we do not only have a `caption`  and `command` but also a `args` entry!

How do we go about this?  `SublimeCommand` can also accept a parameters argument

```python
def SublimeCommand(self, command,parameters = {}):
```

where we can pass a dictionary of parameters to be passed to the command executed by sublime. 

```python
"git add current":R(SublimeCommand("git_raw",{ "command": "git add", "append_current_file": True })),
```

something important here is that this dictionary must be json serializable!

## Passing callable to parameters

but allowing us to pass parameters to the command create another issue that needs to be addressed. 

For example, in the get package we can find three variations of the same command `git_quick_commit`

```python
{
    "caption": "Git: Quick Commit (current file)",
    "command": "git_quick_commit"
}
,{
    "caption": "Git: Quick Commit (repo)",
    "command": "git_quick_commit", "args": { "target": "*" }
}
,{
    "caption": "Git: Quick Commit (repo, only already added files)",
    "command": "git_quick_commit", "args": { "target": false }
}
```

by using only a static dictionary as parameters, we would need three different specs, one for each variation which again involves a lot of unnecessary repetition. In order to overcome this limitation,`SublimeCommand` allows you to pass a callable instead, which would dynamically create dictionary of parameters based on the extras spoken during the utterance

```python
mapping = {
	"git quick commit <item>":R(SublimeCommand("git_quick_commit",
		lambda item: item)),
}

Choice("item",{
		"file":{},
		"repo":{"target":"*"},
		"already added":{"target":False}
	}
),
```


## Acknowledgments


This page contained parts from `Default.sublime-commands` of the Git package, which falls under the MIT license[](https://github.com/kemayo/sublime-text-git/blob/master/LICENSE).
