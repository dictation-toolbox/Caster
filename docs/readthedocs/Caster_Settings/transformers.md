# Transformers

**Update**: The fate of Transformer feature has been decided, and it is now considered deprecated except for internal Caster use eg. `Simplified Transformers` view words.txt. See [Issue #43](https://github.com/synkarius/Caster/issues/43). No new transformers can be defined by the end user.

## Complex Transformers - Feature

In pre-1.0.0 Caster, there was a badly named feature called "filter  functions". The idea of these "filter functions" was that Caster would  define several times at which rules were being merged together, and  would give the user access to make changes to the merged rules at these  times. Due primarily to difficulty of use, "filter functions" did not  get used much.

What "filter functions" ultimately sought to provide was a way for  the user to change parts of Caster rules without needing to make changes to the source code, so that personal customizations wouldn't affect  everyone else.

Transformers are a simplified, safer, and more descriptively named  version of filter functions. Rather than providing the user with a pair  of rules and a metadata object, transformers simply provide the user  with a rule instance, with the intent that the user can then modify the  rule instance and expect their modifications to be applied to whichever  rules they've defined the transformer as being applicable to. See: `base_transformer.py` and `def_transformer.py`

See also section 4A, "The fate of transformers" for comments on transformer vs user directory usage/applicability.

Some time after filter functions were added to Caster, the Caster  user directory was added. This directory was a user-defined location  from which user rules and filter functions would be loaded.

## The fate of transformers

The creation of the Caster user directory largely denecessited filter functions. If users now had a place to put their custom rules, why  create functions to modify existing rules? After all, the process of  copying a file out of Caster, changing the pronunciation, and making  whatever other modifications were desired was much simpler than learning the filter function API, and just as effective in most cases.

There were potential edge cases for filter functions which both the  Caster user directory and the new transformers solution do not cover,  but since no one ever found those edge cases, nothing is lost by  simplifying the system, and in fact, much is gained.

The question remains though: if I have the user directory, and its  content overrides Caster "starter" content, why do I need transformers?  There are some prospective projects in the planning stages which might  make use of them, and also, it was the most natural way to preserve  words.txt functionality.
