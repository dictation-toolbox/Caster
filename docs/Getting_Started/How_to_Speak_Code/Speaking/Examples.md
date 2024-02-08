# Voice Coding Examples

In the following examples, a comma separates commands that can be strung together into a single utterance, while a semicolon separates commands that must be said as separate utterances (because either the previous or next phrase is not a CCR command).

## Example 1

Dictate the following JavaScript function.

```python
function setStatusText(text) {
    var icon = $('.and-session-extender-connection-status > a.dropdown-toggle');
    icon.attr({ 'title': text });
}
```

**Function definition:**
_"set format gerrish gum bow; format function, ace, format set status text, prekris, format text, ross wally, ace, curly, shock"_

**Variable assignment:**
_"format var, ace, format icon, ace equals ace, dolly, prekris, thin quotes, dot, spine bow session extender connection status, ace greater than ace, arch, dot, format dropdown toggle, tau doc"_

**Setting the title attribute:**
_"laws gum bow icon dot, arch tango tango romeo, prekris, curly, ace two, lease, thin quotes, format title, ross, deckle, ace, format text, ross wally, semper, save"_

Alternately, one could use snippets/templates to make some of this easier/faster. For example, the following
would create the same function definition using a code snippet in Sublime Text.

_"set format gerrish gum bow; format fun, tabby, format set status text, tabby, format text, tabby"_

The rest of the dictation after the function definition would be the same. This is a savings of five words, or about 25%, for the function definition. Creating specific snippets for things like variable declarations and assignments, jQuery selectors, etc. could reduce this further.

## Example 2

Dictate a variable or identifier name that has a Caster CCR keyword embedded in it.

```python
var formatPattern = "some pattern";
```

If you tried saying "format var, ace, format format pattern", Dragon would output "var pattern". The reason for this is because the "format" command is itself a CCR command, and can therefore be repeated and mixed with other CCR commands. This is normally a good thing, but can make your life difficult if you need to dictate text or identifier names that have CCR keywords embedded in them.

To get around this, use the "terminal format" command. To dictate the above, I would say something similar to the following:

_"gerrish gum bow var, ace, terminal format format pattern; ace equals ace, quotes, laws bow some pattern, ross wally semper"_

This is something that I only run into occasionally in my day-to-day use of Caster. But because these examples consist almost entirely of Caster CCR commands, I've been making extensive use of the "terminal format" command while preparing them. :)

Note that this works with any of the formatting commands. For example, you can say "terminal gerrish gum bow", "terminal tie spine bow", or "terminal snake bow". However, I usually find it difficult, both cognitively and verbally, to string that many words together into a command without messing something up. To make it easier, I will usually explicitly set the format I want to work with by using the "set format" command, and then simply saying "terminal format". For example: "set format Gerrish gum bow; terminal format some stuff".

Sources [Chilimangoes's Examples Gist](https://gist.github.com/chilimangoes/f6ae51ca53d96a19a46c45ecd4b0d296)