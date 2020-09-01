## Starter Rules

Out-of-the-box, Caster gives the user new mouse navigation commands, text formatting and navigation commands, and programming-language specific rules. Reference Caster commands documentation for spec definitions. The source code starter rules are in `castervoice\rules `  and are organized in the following broad categories.

- `apps` - Applications sorted by application type

- `ccr` -  Programming languages and other domain specific use cases.

- `core` - Grammars for letters, numbers, punctuation, window manipulation, text manipulation, navigation and more.

## Modifying the Rules

If you want to modify Caster's starter rules, there are a few ways to go about it. Of course, you could just edit the source, but then you'd have to deal with merge conflicts when updating to newer versions of Caster. 

If you want to personalize existing command sets, you can use rule transformers. Rule transformers let you instruct Caster as to how it should modify command sets either at boot or at runtime when command sets change (for example, when you say `enable Python`).

There are two ways to get around this:

1. ### Use Simplified Transformers

   What simplified transformers do is expose specs of rules to the user, allowing the user to change the rules' specs as they see fit. Great for small changes across many grammars without editing source code or copying starter rules.  Transformers are applied to Caster when it first starts a.k.a boot time. Details are in the CCR section of the documentation.

   1. Simplified transformers need to be enabled `Local\caster\settings\transformers.toml`
   2. Set `TextReplacerTransformer ` to `true`.
   3. Create the file in `Local\caster\transforms\words.txt`

   User customizations are defined in words.txt and will be read at boot time, creating a rule transformers. The following is an example `words.txt`:

   ```
   <<<SPEC>>>
   shock -> earthquake
   <<<NOT_SPECS>>>
   sauce -> up
   dunce -> down
   lease -> left
   ross -> right
   ```
   ​	This `words.txt` will create a rule filter which goes through **all** Caster rules at boot time and replaces the word "shock" in any spec with the word "earthquake". It will also replace "sauce", "dunce" , "lease" and "ross"  with "up", "down", "left", and "right" in extras and defaults in any rule. The triple-angle-brackets indicate mode changes.  The default mode is `<<<ANY>>>`.

   Valid modes are: 

   - `<<<SPEC>>>` (for specs only)
   - `<<<EXTRA`>>>
   - `<<<DEFAULT`>>>
   - `<<<NOT_SPECS>>>` (for extras and defaults, but not specs)
   - `<<<ANY>>>` (for specs, extras, and defaults). 

   For pictorial representation of how these modes affect rules refer to [Taxonomy of a Rule](https://caster.readthedocs.io/en/latest/readthedocs/Rule_Construction/Taxonomy_of_a_Rule/).
   
   Note: Hyphens `-` are used in `->`

   

2. ### Override Caster starter rules using the User Directory.

   This allows you to copy starter rules and have them override the original ones in the core Caster code by placing them in the user directory. This allows you to make any edits such as adding, renaming, deleting specs and actions. Any rule copied into the user directory is not updated with Caster. It becomes the end-users responsibility to manage how and when the rules update manually. 
   
   To begin copy the rule file or folder of interest from `castervoice\rules ` in the source code to the [user directory](https://caster.readthedocs.io/en/latest/readthedocs/User_Dir/Caster_User_Dir/) rules folder. There are some important things to keep in mind:

- The rule class name e.g  `class ChromeRule` must stays the same for the override to work. 
- Any directory `<SomeName>_rules` must be copied as a whole file to the user directory as they contain a grammar with multiple rules that are designed to work together or require imports.
- Do not copy an entire category of rules so be selective.
- Files like `<SomeName>_rules.py` can be copied and placed anywhere on the user directory.
- Support files `<SomeName>_support`contain functions required for associated rules. Note limitations with [support files](https://github.com/dictation-toolbox/Caster/issues/711).
