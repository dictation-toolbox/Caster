# Companion Rules

​    The `companion_config.toml` allows you to set multiple rules as companions.  A child companion `MappingRules` grammar is linked to its parent `MergeRules` grammar Enabled/Disabled state. When the parent grammar state changes so does it's child companions.

- Enabling a parent rule with a companion enables them both
- Disabling the rule which enabled the companion disables the companion
- Disabling the companion does NOT disable the parent rule

Consider the following example `Python = ["PythonNon"]`

`Python` is the parent rule and `PythonNon` is its child. If you say  `Enable Python` then not only `Python` but also `PythonNon` rule would become enabled.

Guide to creating your own companions

- The names are the exact class names of the rule.

- The `parent` must be a MergeRules and the `child` MappingRules.

- Caution it is possible to have a companion rule circle, which  is to say, an infinite loop.

Default companions for Caster `1.x.x`

```toml
EclipseCCR = ["EclipseRule"]
Java = ["JavaNon"]
Matlab = ["MatlabNon"]
Navigation = ["NavigationNon"]
Prolog = ["PrologNon"]
Python = ["PythonNon"]
Rust = ["RustNon"]
VHDL = ["VHDLnon"]
VSCodeCcrRule = ["VSCodeNonCcrRule"]
```
