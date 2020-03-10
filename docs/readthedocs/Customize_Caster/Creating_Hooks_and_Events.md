### Creating Hooks and Events

Hooks are a new concept to Caster 1.x.x. The basic idea is that Caster itself defines "events." Event objects contain immutable information about the stuff going on in the "guts" of Caster. Those objects are fed to "hooks", user-defined listeners, which can do whatever they want with that event data.

This should allow a decent amount of customization to happen without needing to make changes in the "guts" (Nexus, GrammarManager, CCRMerger, etc. of Caster.

Loosely coupled code leads to less bugs and more productivity, and so the use of hooks rather than "guts" modifications is encouraged whenever possible.

All new hooks are set to `false` by default unless they're defined as defaults in  `settings.toml`  under `default_hooks`

New event types can be added to  [Event types](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/event_types.py)

Example Hooks with Events:

- [printer_hook.py](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/examples/printer_hook.py) utilizes [activation event](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/activation_event.py)
- [format_hook.py](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/standard_hooks/format_hook.py) utilizes  [activation event](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/activation_event.py)
- [node_change_hook.py](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/node_change_event.py) utilizes [node change event](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/node_change_event.py)
- [show_window_on_error_hook.py](https://github.com/dictation-toolbox/Caster/blob/49b2e676fe98eca671c1184423dd656c347d281b/castervoice/lib/ctrl/mgr/grammar_manager.py#L302) utilizes [on error event](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/on_error_event.py)

Event placement in Caster source code:

-  `activation event` in [grammar_manager.py](https://github.com/dictation-toolbox/Caster/blob/3ff4f7d7c9c01fec2059ffa5c4ca708fdb7d09ad/castervoice/lib/ctrl/mgr/grammar_manager.py#L151)
-  `node change event` in [tree_rule.py](https://github.com/dictation-toolbox/Caster/blob/3ff4f7d7c9c01fec2059ffa5c4ca708fdb7d09ad/castervoice/lib/merge/selfmod/tree_rule/tree_rule.py#L57)
-  `on error event` in [grammar_manager.py](https://github.com/dictation-toolbox/Caster/blob/49b2e676fe98eca671c1184423dd656c347d281b/castervoice/lib/ctrl/mgr/grammar_manager.py#L302)



