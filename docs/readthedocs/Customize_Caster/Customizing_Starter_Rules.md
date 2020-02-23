## Starter Rules

Out-of-the-box, Caster gives the user new mouse navigation commands, text formatting and navigation commands, and programming-language specific rules. Reference Caster Commands documentation. The source code starter rules in `castervoice\rules `  are organized in the following broad categories.

- `apps` - Applications sorted by category

- `ccr` Contains programming languages and other domain specific use cases.

- `core` Caster features featuring grammars for letters, numbers and punctuation, manipulate windows, text manipulation/navigation and more.

## Modifying the Rules

If you want to modify the pre-made ruleset, there are a few ways to go about it. Of course, you could just edit the source, but then you'd have to deal with merge conflicts when updating to newer versions of Caster. There are two ways to get around this:

1. **Make a copy in Caster user directory.** 

1A. Copy the rule file or folder of interest from`castervoice\rules ` in the source code to user directory rules folder in `C:\Users\%USERNAME%\AppData\Local\caster\rules`. Any grammar copied into the user directory is not updated with Caster. It becomes the end-users responsibility to manage how and when the grammar's updates manually.

- Any directory `<SomeName>_rules` must be to be copied as a whole file to the user directory as they contain multiple grammar it's assigned to work together.
- Do not copy an entire category of rules so be selective.
- With the exception of folders`<SomeName>_rules` any other file can be copied and placed anywhere on the user directory.
- Note limitations with [support files](https://github.com/dictation-toolbox/Caster/issues/711)

2. **Use Simplified Transformers ** 

​	What Transformers do is expose pairs of rules to the user, allowing the user to change the rules's mapping as they see fit. This is recommended due to caster grammars updating where user directory grammars. Great for small changes across many grammars without editing grammar source code or copying premade rules.  Transformers are applied Caster first starts a.k.a boot time. Details are in the CCR section of the documentation.

​	Simplified transformers need to be enabled `Local\caster\settings\transformers.toml` Setting `TextReplacerTransformer ` to `true`. Create the file `Local\caster\transforms\words.txt` and it will be read at boot time, and a rule filter created from it and added to Caster's list of rule filters. The following is an example `words.txt`:

```
<<<SPEC>>>
shock -> earthquake
<<<NOT_SPECS>>>
sauce -> up
dunce -> down
lease -> left
ross -> right
```

​	This `words.txt` will create a rule filter which goes through **all** Caster rules at boot time and replaces the word "shock" in any spec with the word "earthquake". It will also replace "sauce", "dunce" , "lease" and "ross"  with "up", "down", "left" . and "right" in extras and defaults in any rule. The triple-angle-brackets indicate mode changes. Valid modes are `SPEC` (for specs only), `EXTRA`, `DEFAULT`, `NOT_SPECS` (for extras and defaults, but not specs), and `ANY` (for specs, extras, and defaults). The default mode is `ANY`.