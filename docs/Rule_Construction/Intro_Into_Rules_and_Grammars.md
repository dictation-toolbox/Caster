# Intro to Grammars and Rules

This section is adapted from the Dragonfly documentation on rules and grammars ([Sources](https://dragonfly2.readthedocs.io/en/latest/object_model.html)). These terms are the building blocks for understanding how to customize or build your own grammars and rules. Most of the [Dragonfly documentation](https://dragonfly2.readthedocs.io/en/latest/index.html) directly applies to Caster. Starting with the Dragonfly documentation is not required to understand this documentation. The Caster documentation shows how to create your own rules and grammars by example. However there are differences which are mentioned throughout the documentation. 

## Rules

`Rules` represent voice commands or parts of voice commands. Each rule has a single root element e.g. MappingRule, MergeRule, SelfModifyingRule, etc. and are the basis of a tree structure of elements defining how the rule is built up out of speakable parts. The element tree determines what a user must say to cause this rule to be recognized.

## Grammars

In general a `grammar` is a collection of rules that are related to each other. It manages the rules, loading and unloading them, activating and deactivating them, and it takes care of all communications with the speech recognition engine. When a recognition occurs, the associated grammar receives the recognition event and dispatches it to the appropriate rule.

Common examples of different contexts:

- **Global**: the rules are available everywhere all the time on the computer. Collectively they are a global grammar.
- **Application**: specific rules are only available to a specific application or set of applications. For instance the Firefox application might have a rule that allows you to switch between tabs by voice. Through a Firefox extension you may have a separate rule that controls the extension. Collectively both rules are the Firefox grammar because they share the same context.

This seems very complex; by and large you'll be working with `rules` as Caster creates and manages the grammars for you.

## Rule Construction Overview

Rule construction documentation will walk you through the following:

- `Taxonomy of a Rule` gives a pictorial representation of the anatomy of a rule. The terms defined there are the basics for what you need to know to follow along with the rest of the documentation.

- `Your First Rule` - Guides you through experimenting with your own global rule without delving deep into details.

- `Basic Rules` - Expands on what you are introduced to during `Your First Rule`. 
  
  **Note** It is highly recommended that you skip `Advanced Rules` and `Loading Rules` until you're comfortable writing your own basic rules.

- `Advanced Rules` - Goes in-depth with Caster-specific features such as CCR

- `Loading Rules` - Which shows you how to load and define when and where rules are active such as `global` or `application` contexts.
