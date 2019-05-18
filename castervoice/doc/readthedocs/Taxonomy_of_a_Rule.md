# Taxonomy of a Rule

Throughout the Caster documentation, you will see references to `rule`s, `command`s, `spec`s, `action`s, `extra`s, and `default`s. These all refer to parts of a Rule, typically a Dragonfly MappingRule or a Caster MergeRule. Both are structured the same way, as depicted below.

<img src="https://github.com/dictation-toolbox/Caster/blob/master/caster/doc/img/terminology.png">

- `spec` : This is what you say in order to invoke an `action`.
- `action` : This is what happens when you speak a `spec`. Examples include Dragonfly's [Key](http://dragonfly.readthedocs.io/en/latest/actions.html#key-action), Text, and Function actions, or Caster's [R](http://caster.readthedocs.io/en/latest/caster/doc/readthedocs/ContextStack/#registeredaction), [ContextSeeker](http://caster.readthedocs.io/en/latest/caster/doc/readthedocs/ContextStack/#contextseeker), or [AsynchronousAction](http://caster.readthedocs.io/en/latest/caster/doc/readthedocs/ContextStack/#asynchronousaction) actions.
- `extra` : A sub-component of a `spec`. Examples include Dragonfly's Dictation, IntegerRef, and Choice, or Caster's IntegerRefST and Boolean.
- `default` : A default value for an `extra`. Optional `extra`s in a `spec` should have default values.
- `command` : The combination of a `spec` and an `action`. In MappingRules or MergeRules, these are key/value pairs, but a Dragonfly [CompoundRule](http://dragonfly.readthedocs.io/en/latest/_modules/dragonfly/grammar/rule_compound.html) is also a `command`.
- `rule` : Any of the classes which extend Dragonfly's Rule class, but most commonly, MappingRule and MergeRule.
