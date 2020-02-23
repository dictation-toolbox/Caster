## Hooks and Events

​	Hooks are a new concept to Caster 1.0.0. The basic idea is that Caster itself defines "events", objects which contain immutable information about the stuff going on in the "guts" of Caster, and then those objects are fed to "hooks", user-defined listeners Called events which can do whatever they want with said information. This should allow a decent amount of customization to happen without needing to make changes in the "guts" (Nexus, GrammarManager, CCRMerger, etc. of Caster.

Loosely coupled code leads to less bugs and more productivity, and so the use of hooks rather than "guts" modifications is encouraged  whenever possible.

User made hooks can be placed in run from the Caster user directory `AppData\Local\caster\hooks`

New event type added to  [Event types](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/event_types.py)

Example hooks

- [printer_hook.py]([printer_hook.py](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/examples/printer_hook.py)) utilizes [activation event](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/activation_event.py)	

- [format_hook.py](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/standard_hooks/format_hook.py) utilizes  [activation event](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/activation_event.py)

- [node_change_event.py](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/node_change_event.py) utilizes [node change event](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/node_change_event.py)

Hooks placement in castor source code.

-  `activation event` in [grammar_manager.py](https://github.com/dictation-toolbox/Caster/blob/cb7adc4253d8d55089936e5b90ee57ce5784660e/castervoice/lib/ctrl/mgr/grammar_manager.py#L150)
- `node change event` in [tree_rule.py](https://github.com/dictation-toolbox/Caster/blob/30c022a7085be6c8dbfee1c839d50fc7c8cdaf82/castervoice/lib/merge/selfmod/tree_rule/tree_rule.py#L57)



