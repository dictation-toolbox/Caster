## Migrating between Dragonfly and Caster

Some users may be familiar with creating Dragonfly grammars.  New users who are unfamiliar with Dragonfly can skip to `Caster Loading Rules`. Caster differs primarily from Dragonfly on how it loads rules and creates rule contexts when creating grammars. The primary purpose for this difference is so that Caster can manage the CCR merger and make rules reloadable on save.

- Caster Supports Dragonfly functionality of AppContext and FunkContext but implemented differently and are not defined directly in the rules.
- Caster manages Logical Operations of grammars contexts and they are not defined within the grammar `get_rule`
- Caster grammars can be enabled and disabled by voice during runtime once loaded successfully by the speech recognition engine. 
- Caster Rules can only have one rule `class`  eg `Navigation(MappingRule)` pre file.
- Functions typically are not stored in the grammar file but in `support` files. e.g. `navigation.py` grammar has a support file `navigation_support.py`.

These are some basic examples of how Dragonfly vs Caster loads rules differently however they are functionally the same. 

**Dragonfly App Rule**

```python
context = AppContext(executable="devenv", title="microsoft visual studio")
grammar = Grammar("visual studio", context=context)
grammar.add_rule(MicrosoftVisualStudioRule())
grammar.load()
```

**Dragonfly Global Rule**

```python
grammar = Grammar("my new grammar")
grammar.add_rule(MyRule())
grammar.load()
```

Dragonfly rules can be converted to Caster equivalents by replacing the loading functions and with the proper Caster imports. See More details on how to load Caster rules in [Rule Construction](https://caster.readthedocs.io/en/latest/readthedocs/Rule_Construction/Rule_Construction/) including imports.

**Caster App Rule**

```python
def get_rule():
    details = RuleDetails(executable="devenv", 
                          title="microsoft visual studio")
    return MyRule, details
```

**Caster Global Rule**

```python
def get_rule():
    details = RuleDetails(name="my grammar")
    return MyRule, details
```

**Loading Dragonfly rules with Caster**

You can use Dragonfly Rules alongside alongside Caster Rules.  Dragonfly Rules will not utilize caster features like the ability to enable/disable a rule by voice, reload on edit and so on. Requirements to load dragonfly rules:

- The dragonfly rule file must be included in the top level of the Caster source code directory
- The dragonfly rule file must include  a `_` in the beginning of the file name e.g. `_MyDragonflyRule.py` 
- Caster needs to restarted to pick up new dragonfly rules

## Migrating from Caster Version `0.6.14`

 `1.0.0` has breaking changes with the previous versions of Caster. User made grammars and rules will need to be updated. High-level changes include but not limited to:

- User Rules and Caster settings are stored in a new location
- Rules and grammars are loaded differently via `get_rule` and some python imports have changed
- Rules can only have one rule `class` eg `Navigation(MappingRule)` pre file.
- Caster creates and manages grammars including Logical Operations of grammars contexts.
- Caster Currentlly supports AppContext and FunkContext but they are not defined directly within the grammar.
- Functions that used to be defined in grammars have been moved into what is called `support` files e.g. `navigation.py` grammar has a support file `navigation_support.py`.

Continue with the documentation to learn how to use the new grammar system. For a deeper understanding of between the changes in Caster `0.6.14` to `1.0.0`. read [Caster 1.0.0 Changes Summary](https://github.com/dictation-toolbox/Caster/issues/385#issuecomment-529165483).