# Taxonomy of a Rule

Throughout the Caster documentation, you will see references to `rule`, `command`, `spec`, `action`, `extra`, and `default`s. These all refer to parts of a Rule, typically a MappingRule or MergeRule. Both are structured the same way, as depicted below.

<img src="https://raw.githubusercontent.com/dictation-toolbox/Caster/master/docs/img/terminology.png">

- `spec` : This is what you say in order to invoke an `action`.
- `action` : This is what happens when you speak a `spec`. Examples include Dragonfly's [Key](http://dragonfly.readthedocs.io/en/latest/actions.html#key-action), Text, and Function actions, or Caster's [R](http://caster.readthedocs.io/en/latest/caster/doc/readthedocs/ContextStack/#registeredaction), [ContextSeeker](http://caster.readthedocs.io/en/latest/caster/doc/readthedocs/ContextStack/#contextseeker), or [AsynchronousAction](http://caster.readthedocs.io/en/latest/caster/doc/readthedocs/ContextStack/#asynchronousaction) actions.
- `command` : The combination of a `spec` and an `action`. In MappingRules or MergeRules, these are key/value pairs.
- `extra` : A sub-component of a `spec`. Examples include Dragonfly's Dictation, IntegerRef, and Choice, or Caster's IntegerRefST and Boolean.
- `default` : A default value for an `extra`. Optional `extra`s in a `spec` should have default values.
- `rule` : Any of the classes which extend Dragonfly's Rule class, but most commonly, MappingRule and MergeRule.
