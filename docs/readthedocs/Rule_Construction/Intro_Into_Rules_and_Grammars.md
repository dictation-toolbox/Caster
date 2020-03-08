# Intro Grammars and Rules 

This section is adapted from the Dragonfly documentation on rules and grammars ([Sources](https://dragonfly2.readthedocs.io/en/latest/object_model.html)). These terms are the building blocks for you to understand how to customize or build your own grammars and rules. Most of [Dragonfly documentation](https://dragonfly2.readthedocs.io/en/latest/index.html) directly applies to Caster. Starting off the Dragonfly documentation is not needed to understand this documentation. The Caster documentation shows how to create your own rules and grammars by example. However there are differences which are mentioned throughout the documentation. 

## Grammars

In general a `grammar` is a collection of rules that are related to each other. It manages the rules, loading and unloading them, activating and deactivating them, and it takes care of all communications with the speech recognition engine. When a recognition occurs, the associated grammar receives the recognition event and dispatches it to the appropriate rule.

Common Examples of different context:

- **Global** the rules are available everywhere all the time on the computer. Collectively they are a global grammars.
- **Application** specific rules are only available to a specific application or set of applications. For instance the Firefox application might have a rule that allows you to switch between tabs by voice. Through a Firefox extension you may have a separate rule that controls the extension. Collectively both rules are the Firefox grammar because they share the same context.

## Rules

`Rules` represent voice commands or parts of voice commands. By and large you'll be working with rules. Each rule has a single root element e.g. MappingRule,  MergeRule, SelfModifyingRule, etc. and are the basis of a tree structure of elements defining how the rule is built up out of speakable parts. The element tree determines what a user must say to cause this rule to be recognized. 

This seems very complex, but the next section `Taxonomy of a Rule`  gives a pictorial representation of the anatomy of a rule. The terms defined there are the basics for what you need to know to follow along with the rest of the documentation.



 