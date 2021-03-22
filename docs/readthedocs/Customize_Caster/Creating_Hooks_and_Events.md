# Creating Hooks and Events

Hooks are a new concept to Caster 1.x.x. The basic idea is that Caster itself defines "events." Event objects contain immutable information about the stuff going on in the "guts" of Caster. Those objects are fed to "hooks", user-defined listeners, which can do whatever they want with that event data.  

Hooks and Events make use of dependency injection and class inheritance through base classes. This design pattern coupled with loosely coupled code leads to less bugs and more productivity, and so the use of hooks rather than "guts" modifications is encouraged whenever possible. This should allow a decent amount of customization to happen without needing to make changes in the "guts" (Nexus, GrammarManager, CCRMerger, etc. of Caster. 

All new hooks are set to `false` by default unless they' are defined as defaults in `settings.py`  under `default_hooks`. 

1. **Hook Runner Placement**

   First to figure out what data you want to monitor In the code and create a hook runner. For example Printer Hook monitors and prints enabled/disabled rules states. See [grammar_manager.py](https://github.com/dictation-toolbox/Caster/blob/3ff4f7d7c9c01fec2059ffa5c4ca708fdb7d09ad/castervoice/lib/ctrl/mgr/grammar_manager.py#L151). A hook runner runs every time an event occurs. Printer Hook runner example `self._hooks_runner.execute(RuleActivationEvent(class_name, enabled))` .

   The Anatomy of a Hook Runner:

   - `self._hooks_runner.execute`: executes the event as a hook runner

   - `RuleActivationEvent`: class name is the reference to the Event

   - `(class_name, enabled)`: event data are variables from source code captured by the Event

      **Note**: Hook Runners can be reused to capture data throughout the source code in multiple functions assuming the observed data uses the same variables.

2. **Create a Event**

   Create a Event and register [Event types](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/event_types.py). 

- Events can be reused in hooks.
- Don't forget to import the event at the location of your hook runner.

The Event needs a class name `RuleActivationEvent`,  registered event type `EventType.ACTIVATION` , and the variables (`class_name, enabled`). 

``` Python
from castervoice.lib.merge.ccrmerging2.hooks.events.base_event import BaseHookEvent
from castervoice.lib.merge.ccrmerging2.hooks.events.event_types import EventType

class RuleActivationEvent(BaseHookEvent):
    def __init__(self, rule_class_name, active):
        super(RuleActivationEvent, self).__init__(EventType.ACTIVATION)
        # Data from the hook runner
        self.rule_class_name = rule_class_name 
        self.active = active 
```

3.**Create a Hook**

   Hooks need class name `PrinterHook`, Event type `EventType.ACTIVATION` and a pronunciation`"printer"` 

- Hook can be enabled/disabled while Caster is running. The get_pronunciation Is returned as `printer` but the full pronunciation `enable/disable printer hook`.  The prefix/suffix is added automatically.

- The required `run` function is where you add your logic to process the event data.

- Advanced *optional* functionality with  `run_on_enable` and `run_on_disable`. These functions only run when a hook is enabled or disabled. Useful for when you want to process data differently on enabling or disabling a hook that is separate from  `run` function.

     **Note** `run_on_enable` should not be used If a hook is registered as a default hook in `settings.py.  The hook will already be enabled on Casters for starts.

- Hooks can be placed in the Caster User Directory `caster\hooks`.

```python
from castervoice.lib import printer
from castervoice.lib.merge.ccrmerging2.hooks.base_hook import BaseHook
from castervoice.lib.merge.ccrmerging2.hooks.events.event_types import EventType

class PrinterHook(BaseHook):

    def __init__(self):
        super(PrinterHook, self).__init__(EventType.ACTIVATION)

    def get_pronunciation(self):
        # Hook can be enabled/disabled while Caster is running
        return "printer" # enable/disable printer hook    
    
    # The `run` function Is executed by hook runner event occurs with new data.
    def run(self, event): # Notice both variables from the event data are stored in `event`
        state = "active" if event.active else "inactive" # Monitoring state
        # Printing To console rule class name and state
        printer.out("The rule {} was set to {}.".format(event.rule_class_name, state))

    def run_on_enable(self, event):
        # Logic for function to run when enabling a hook
        
    def run_on_disable(self, event):
       # Logic for function to run on when disabling a hook
        
def get_hook():
    return PrinterHook
```

Example Hooks with Events:

- [printer_hook.py](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/examples/printer_hook.py) utilizes [activation event](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/activation_event.py)
- [format_hook.py](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/standard_hooks/format_hook.py) utilizes  [activation event](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/activation_event.py)
- [node_change_hook.py](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/node_change_event.py) utilizes [node change event](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/node_change_event.py)
- [show_window_on_error_hook.py](https://github.com/dictation-toolbox/Caster/blob/5172a44d3cd58619f6228231e3aef2fddd1f1fb3/castervoice/lib/ctrl/mgr/grammar_manager.py#L302) utilizes [on error event](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/ccrmerging2/hooks/events/on_error_event.py)

Hook Runner Placement placement in Caster source code:

- `activation event` in [grammar_manager.py](https://github.com/dictation-toolbox/Caster/blob/3ff4f7d7c9c01fec2059ffa5c4ca708fdb7d09ad/castervoice/lib/ctrl/mgr/grammar_manager.py#L151)
- `node change event` in [tree_rule.py](https://github.com/dictation-toolbox/Caster/blob/5172a44d3cd58619f6228231e3aef2fddd1f1fb3/castervoice/lib/merge/selfmod/tree_rule/tree_rule.py#L57)
- `on error event` in [grammar_manager.py](https://github.com/dictation-toolbox/Caster/blob/5172a44d3cd58619f6228231e3aef2fddd1f1fb3/castervoice/lib/ctrl/mgr/grammar_manager.py#L302)
